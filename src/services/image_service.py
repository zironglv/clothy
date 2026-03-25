"""
图片服务模块
处理图片下载、缓存、拼接等
"""

import os
import hashlib
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
import json

import httpx
from PIL import Image


class ImageService:
    """图片服务
    
    功能：
    - 下载网络图片到本地
    - 图片缓存（避免重复下载）
    - 图片拼接（用于消息展示）
    - 缩略图生成
    """
    
    def __init__(self, cache_dir: str = "./assets/images/cache", 
                 items_dir: str = "./assets/images/items",
                 sources_dir: str = "./assets/images/sources"):
        """初始化图片服务
        
        Args:
            cache_dir: 缓存目录
            items_dir: 单品图片目录
            sources_dir: 关注来源图片目录
        """
        self.cache_dir = Path(cache_dir)
        self.items_dir = Path(items_dir)
        self.sources_dir = Path(sources_dir)
        
        # 确保目录存在
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.items_dir.mkdir(parents=True, exist_ok=True)
        self.sources_dir.mkdir(parents=True, exist_ok=True)
        
        # 缓存索引
        self.cache_index_file = self.cache_dir / "index.json"
        self.cache_index = self._load_cache_index()
    
    def _load_cache_index(self) -> Dict:
        """加载缓存索引"""
        if self.cache_index_file.exists():
            try:
                with open(self.cache_index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache_index(self):
        """保存缓存索引"""
        with open(self.cache_index_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache_index, f, ensure_ascii=False, indent=2)
    
    def _get_url_hash(self, url: str) -> str:
        """计算 URL 的哈希值"""
        return hashlib.md5(url.encode()).hexdigest()
    
    async def download_image(self, url: str, use_cache: bool = True) -> Optional[str]:
        """下载图片
        
        Args:
            url: 图片 URL
            use_cache: 是否使用缓存
            
        Returns:
            本地文件路径，失败返回 None
        """
        if not url:
            return None
        
        # 检查缓存
        url_hash = self._get_url_hash(url)
        if use_cache and url_hash in self.cache_index:
            cached_path = self.cache_dir / self.cache_index[url_hash]['filename']
            if cached_path.exists():
                return str(cached_path)
        
        # 下载图片
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()
                
                # 确定文件扩展名
                content_type = response.headers.get('content-type', '')
                ext = '.jpg'
                if 'png' in content_type:
                    ext = '.png'
                elif 'gif' in content_type:
                    ext = '.gif'
                elif 'webp' in content_type:
                    ext = '.webp'
                
                # 保存文件
                filename = f"{url_hash}{ext}"
                filepath = self.cache_dir / filename
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                # 更新缓存索引
                self.cache_index[url_hash] = {
                    'url': url,
                    'filename': filename,
                    'downloaded_at': datetime.now().isoformat()
                }
                self._save_cache_index()
                
                return str(filepath)
                
        except Exception as e:
            print(f"下载图片失败: {url}, 错误: {e}")
            return None
    
    def save_item_image(self, image_data: bytes, item_id: str, ext: str = '.jpg') -> str:
        """保存单品图片
        
        Args:
            image_data: 图片二进制数据
            item_id: 单品 ID
            ext: 文件扩展名
            
        Returns:
            保存的文件路径
        """
        filename = f"{item_id}{ext}"
        filepath = self.items_dir / filename
        
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        return str(filepath)
    
    def get_item_image_path(self, item_id: str) -> Optional[str]:
        """获取单品图片路径"""
        for ext in ['.jpg', '.png', '.jpeg', '.webp']:
            path = self.items_dir / f"{item_id}{ext}"
            if path.exists():
                return str(path)
        return None
    
    def create_collage(self, image_paths: List[str], 
                       columns: int = 3,
                       thumb_size: int = 200,
                       padding: int = 10,
                       background_color: str = '#FFFFFF') -> Optional[str]:
        """创建图片拼接
        
        Args:
            image_paths: 图片路径列表
            columns: 列数
            thumb_size: 缩略图大小
            padding: 间距
            background_color: 背景色
            
        Returns:
            拼接后的图片路径
        """
        if not image_paths:
            return None
        
        # 过滤存在的图片
        valid_paths = [p for p in image_paths if os.path.exists(p)]
        if not valid_paths:
            return None
        
        # 限制数量
        max_images = min(len(valid_paths), columns * 3)  # 最多3行
        valid_paths = valid_paths[:max_images]
        
        # 计算布局
        rows = (len(valid_paths) + columns - 1) // columns
        
        # 创建画布
        canvas_width = columns * thumb_size + (columns + 1) * padding
        canvas_height = rows * thumb_size + (rows + 1) * padding
        
        try:
            canvas = Image.new('RGB', (canvas_width, canvas_height), background_color)
        except Exception as e:
            print(f"创建画布失败: {e}")
            return None
        
        # 放置图片
        for i, path in enumerate(valid_paths):
            try:
                img = Image.open(path)
                
                # 转换模式
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # 创建缩略图（居中裁剪）
                img.thumbnail((thumb_size, thumb_size), Image.Resampling.LANCZOS)
                
                # 计算位置
                row = i // columns
                col = i % columns
                x = padding + col * (thumb_size + padding)
                y = padding + row * (thumb_size + padding)
                
                # 居中放置
                img_width, img_height = img.size
                offset_x = (thumb_size - img_width) // 2
                offset_y = (thumb_size - img_height) // 2
                
                canvas.paste(img, (x + offset_x, y + offset_y))
                
            except Exception as e:
                print(f"处理图片失败 {path}: {e}")
                continue
        
        # 保存
        collage_id = uuid.uuid4().hex[:8]
        output_path = self.cache_dir / f"collage_{collage_id}.jpg"
        canvas.save(output_path, 'JPEG', quality=85)
        
        return str(output_path)
    
    def create_thumbnail(self, image_path: str, size: int = 200) -> Optional[str]:
        """创建缩略图
        
        Args:
            image_path: 原图路径
            size: 缩略图大小
            
        Returns:
            缩略图路径
        """
        if not os.path.exists(image_path):
            return None
        
        try:
            img = Image.open(image_path)
            
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            img.thumbnail((size, size), Image.Resampling.LANCZOS)
            
            # 生成缩略图路径
            path = Path(image_path)
            thumb_path = self.cache_dir / f"thumb_{path.stem}.jpg"
            
            img.save(thumb_path, 'JPEG', quality=85)
            return str(thumb_path)
            
        except Exception as e:
            print(f"创建缩略图失败: {e}")
            return None
    
    def clear_cache(self, days: int = 30):
        """清理过期缓存
        
        Args:
            days: 保留天数
        """
        import time
        
        cutoff = time.time() - days * 24 * 60 * 60
        
        for url_hash, info in list(self.cache_index.items()):
            downloaded_at = info.get('downloaded_at', '')
            if downloaded_at:
                try:
                    dt = datetime.fromisoformat(downloaded_at)
                    if dt.timestamp() < cutoff:
                        # 删除文件
                        filepath = self.cache_dir / info['filename']
                        if filepath.exists():
                            filepath.unlink()
                        # 删除索引
                        del self.cache_index[url_hash]
                except:
                    pass
        
        self._save_cache_index()
    
    def get_image_stats(self) -> Dict[str, Any]:
        """获取图片统计信息"""
        stats = {
            'cache_count': len(self.cache_index),
            'items_count': len(list(self.items_dir.glob('*.jpg'))) + 
                          len(list(self.items_dir.glob('*.png'))),
            'sources_count': len(list(self.sources_dir.glob('*.jpg'))),
            'cache_size': sum(f.stat().st_size for f in self.cache_dir.glob('*') if f.is_file()),
            'items_size': sum(f.stat().st_size for f in self.items_dir.glob('*') if f.is_file()),
        }
        
        # 转换为 MB
        stats['cache_size_mb'] = round(stats['cache_size'] / 1024 / 1024, 2)
        stats['items_size_mb'] = round(stats['items_size'] / 1024 / 1024, 2)
        
        return stats