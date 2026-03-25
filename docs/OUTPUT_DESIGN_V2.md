# StyleBuddy 输出设计

> 图文并茂的结构化输出

---

## 一、设计原则

```
┌─────────────────────────────────────────────────────────────────┐
│                      输出设计原则                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 图文并茂 ─── 每个推荐都带商品图片                           │
│                                                                 │
│  2. 结构化输出 ─── 返回标准化的 JSON 数据                       │
│                                                                 │
│  3. 推送解耦 ─── 推送由接入方实现，Skill 只负责生成内容         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Skill 职责边界**：
- ✅ 业务逻辑处理
- ✅ 图片获取/缓存/处理
- ✅ 生成结构化的图文数据
- ❌ 推送到各渠道（由接入方实现）

---

## 二、输出数据结构

### 2.1 今日穿搭推荐

```python
@dataclass
class OutfitRecommendation:
    """穿搭推荐输出"""
    
    # 天气信息
    weather: Dict[str, Any]
    # {
    #   "city": "北京",
    #   "temp": 18,
    #   "condition": "多云",
    #   "humidity": 45,
    #   "wind": "东南风3级"
    # }
    
    # 用户画像摘要
    user_profile: Dict[str, Any]
    # {
    #   "body_type": "pear",
    #   "body_type_label": "梨形身材",
    #   "style_preference": ["极简通勤", "优雅知性"]
    # }
    
    # 推荐单品列表
    items: List[Dict[str, Any]]
    # [
    #   {
    #     "id": "item_001",
    #     "name": "白色衬衫",
    #     "category": "top",
    #     "category_label": "上衣",
    #     "color": "白色",
    #     "image": {
    #       "url": "https://...",        # 图片URL（优先）
    #       "path": "/path/to/image.jpg", # 本地路径
    #       "base64": "..."              # Base64编码（可选）
    #     },
    #     "source": "wardrobe",          # wardrobe/taobao_order/taobao_cart
    #     "taobao_url": "https://...",   # 淘宝链接（如有）
    #     "notes": "修身款"
    #   },
    #   ...
    # ]
    
    # 搭配说明
    tips: List[str]
    # [
    #   "高腰A字裙修饰臀部线条，适合梨形身材",
    #   "白衬衫+米色半裙=通勤经典组合"
    # ]
    
    # 元数据
    meta: Dict[str, Any]
    # {
    #   "generated_at": "2024-01-15T09:00:00",
    #   "template_id": "t_commuter_001",
    #   "match_score": 92
    # }
```

**输出示例**：

```json
{
  "weather": {
    "city": "北京",
    "temp": 18,
    "condition": "多云"
  },
  "user_profile": {
    "body_type_label": "梨形身材",
    "style_preference": ["极简通勤", "优雅知性"]
  },
  "items": [
    {
      "id": "item_001",
      "name": "白色衬衫",
      "category": "top",
      "category_label": "上衣",
      "color": "白色",
      "image": {
        "url": "https://img.alicdn.com/imgextra/xxx.jpg",
        "path": "/data/stylebuddy/images/wardrobe/item_001.jpg"
      },
      "source": "taobao_order",
      "taobao_url": "https://item.taobao.com/item.htm?id=123456"
    },
    {
      "id": "item_002",
      "name": "高腰A字裙",
      "category": "bottom",
      "category_label": "下装",
      "color": "米色",
      "image": {
        "path": "/data/stylebuddy/images/wardrobe/item_002.jpg"
      },
      "source": "wardrobe"
    },
    {
      "id": "item_003",
      "name": "乐福鞋",
      "category": "shoes",
      "category_label": "鞋子",
      "color": "黑色",
      "image": {
        "url": "https://img.alicdn.com/imgextra/yyy.jpg"
      },
      "source": "taobao_order"
    }
  ],
  "tips": [
    "高腰A字裙修饰臀部线条，适合梨形身材",
    "白衬衫+米色半裙=通勤经典组合",
    "同色系鞋包更显高级感"
  ],
  "meta": {
    "generated_at": "2024-01-15T09:00:00",
    "match_score": 92
  }
}
```

### 2.2 店铺上新推送

```python
@dataclass
class NewArrivalPush:
    """上新推送输出"""
    
    # 推送日期
    date: str                          # "2024-01-15"
    
    # 关注来源信息
    source: Dict[str, Any]
    # {
    #   "id": "shop_123456",
    #   "name": "ONLY官方旗舰店",
    #   "type": "taobao_shop",
    #   "url": "https://shop123.taobao.com/"
    # }
    
    # 新品列表
    items: List[Dict[str, Any]]
    # [
    #   {
    #     "id": "arrival_001",
    #     "item_id": "taobao_789",
    #     "title": "米色羊毛大衣",
    #     "price": 899,
    #     "image": {
    #       "url": "https://img.alicdn.com/xxx.jpg",
    #       "path": "/data/stylebuddy/images/taobao/shop_123456/item_789.jpg"
    #     },
    #     "url": "https://item.taobao.com/item.htm?id=789",
    #     "category": "outer",
    #     "category_label": "外套",
    #     "color": "米色",
    #     "style_tags": ["通勤", "优雅"],
    #     "selling_points": ["100%羊毛", "双面呢", "气质款"],
    #     "match_score": 95,
    #     "match_reason": "风格匹配、颜色适合、身材适配",
    #     "wardrobe_match": ["白色T恤", "牛仔裤"]
    #   },
    #   ...
    # ]
    
    # 今日推荐（匹配度最高）
    top_pick: Dict[str, Any]
    # {
    #   "item_id": "arrival_001",
    #   "title": "米色羊毛大衣",
    #   "reason": "匹配度最高，适合你的极简通勤风格"
    # }
    
    # 统计
    stats: Dict[str, Any]
    # {
    #   "total_new": 3,
    #   "high_match": 2,       # 匹配度>80的商品数
    #   "avg_match_score": 87
    # }
```

**输出示例**：

```json
{
  "date": "2024-01-15",
  "source": {
    "id": "shop_123456",
    "name": "ONLY官方旗舰店",
    "type": "taobao_shop"
  },
  "items": [
    {
      "id": "arrival_001",
      "title": "米色羊毛大衣",
      "price": 899,
      "image": {
        "url": "https://img.alicdn.com/imgextra/xxx.jpg",
        "path": "/data/stylebuddy/images/taobao/shop_123456/item_789.jpg"
      },
      "url": "https://item.taobao.com/item.htm?id=789",
      "category_label": "外套",
      "style_tags": ["通勤", "优雅"],
      "selling_points": ["100%羊毛", "双面呢"],
      "match_score": 95,
      "match_reason": "风格匹配、颜色适合",
      "wardrobe_match": ["白色T恤×3", "牛仔裤×2"]
    },
    {
      "id": "arrival_002",
      "title": "黑色针织连衣裙",
      "price": 399,
      "image": {
        "url": "https://img.alicdn.com/imgextra/yyy.jpg"
      },
      "url": "https://item.taobao.com/item.htm?id=790",
      "category_label": "连衣裙",
      "style_tags": ["优雅", "知性"],
      "match_score": 78,
      "match_reason": "风格匹配",
      "warning": "你衣橱有类似款，确认是否需要"
    }
  ],
  "top_pick": {
    "title": "米色羊毛大衣",
    "reason": "匹配度最高，适合你的极简通勤风格"
  },
  "stats": {
    "total_new": 3,
    "high_match": 2
  }
}
```

### 2.3 种草咨询结果

```python
@dataclass
class ConsultationResult:
    """种草咨询输出"""
    
    # 商品分析
    item: Dict[str, Any]
    # {
    #   "title": "米色针织开衫",
    #   "image": {
    #     "url": "https://...",
    #     "path": "/path/to/..."
    #   },
    #   "price": 259,
    #   "url": "https://item.taobao.com/...",
    #   "category": "outer",
    #   "category_label": "外套",
    #   "color": "米色",
    #   "style_tags": ["温柔", "通勤", "休闲"],
    #   "season": "春秋",
    #   "selling_points": ["针织", "开衫", "百搭"]
    # }
    
    # 可搭配单品
    wardrobe_matches: List[Dict[str, Any]]
    # [
    #   {
    #     "id": "item_001",
    #     "name": "白色T恤",
    #     "category_label": "上衣",
    #     "count": 3,              # 你有3件
    #     "image": {
    #       "url": "https://...",
    #       "path": "/path/to/..."
    #     }
    #   },
    #   ...
    # ]
    
    # 购买建议
    recommendation: str               # "推荐购买" / "谨慎购买" / "不推荐"
    
    # 理由
    reasons: List[str]
    # [
    #   "你衣橱里缺少针织开衫，补充后搭配更丰富",
    #   "米色与你现有衣服百搭，利用率高",
    #   "符合你的极简通勤风格"
    # ]
    
    # 注意事项/警告
    warnings: List[str]
    # [
    #   "你已有一件灰色针织衫，确认是否需要两件"
    # ]
    
    # 匹配度
    match_score: int                  # 0-100
```

**输出示例**：

```json
{
  "item": {
    "title": "米色针织开衫",
    "image": {
      "url": "https://img.alicdn.com/imgextra/zzz.jpg"
    },
    "price": 259,
    "url": "https://item.taobao.com/item.htm?id=999",
    "category_label": "外套",
    "style_tags": ["温柔", "通勤", "休闲"],
    "selling_points": ["针织", "开衫", "百搭"]
  },
  "wardrobe_matches": [
    {
      "name": "白色T恤",
      "category_label": "上衣",
      "count": 3,
      "image": {
        "path": "/data/stylebuddy/images/wardrobe/item_001.jpg"
      }
    },
    {
      "name": "牛仔裤",
      "category_label": "下装",
      "count": 2,
      "image": {
        "path": "/data/stylebuddy/images/wardrobe/item_002.jpg"
      }
    }
  ],
  "recommendation": "推荐购买",
  "reasons": [
    "你衣橱里缺少针织开衫，补充后搭配更丰富",
    "米色与你现有衣服百搭，利用率高"
  ],
  "warnings": [
    "你已有一件灰色针织衫，确认是否需要两件"
  ],
  "match_score": 85
}
```

### 2.4 衣橱分析报告

```python
@dataclass
class WardrobeReport:
    """衣橱分析报告输出"""
    
    # 统计概览
    overview: Dict[str, Any]
    # {
    #   "total_items": 89,
    #   "categories": 5,
    #   "colors": 12,
    #   "avg_price": 268
    # }
    
    # 品类分布（含图表）
    category_distribution: Dict[str, Any]
    # {
    #   "data": {"上衣": 35, "下装": 28, "外套": 12, "鞋子": 10, "配饰": 4},
    #   "chart": {
    #     "type": "pie",
    #     "image": {
    #       "path": "/data/stylebuddy/images/charts/category_pie.png"
    #     }
    #   }
    # }
    
    # 颜色分布
    color_distribution: Dict[str, Any]
    # {
    #   "data": {"黑": 30, "白": 25, "灰": 15, "米": 10, ...},
    #   "chart": {
    #     "type": "bar",
    #     "image": {
    #       "path": "/data/stylebuddy/images/charts/color_bar.png"
    #     }
    #   }
    # }
    
    # 季节分布
    season_distribution: Dict[str, Any]
    # {
    #   "data": {"春夏": 50, "秋冬": 30, "四季": 10}
    # }
    
    # 风格标签
    style_tags: List[str]
    # ["极简通勤", "优雅知性", "职场穿搭"]
    
    # 洞察建议
    insights: List[str]
    # [
    #   "上衣数量偏多，建议控制购买",
    #   "配饰较少，可适当补充提升搭配丰富度"
    # ]
    
    # 购物建议
    shopping_suggestions: List[Dict[str, Any]]
    # [
    #   {
    #     "item": "驼色大衣",
    #     "reason": "秋冬外套不足",
    #     "priority": "high"
    #   },
    #   ...
    # ]
```

---

## 三、图片服务

### 3.1 图片存储结构

```
data/stylebuddy/images/
├── wardrobe/              # 衣橱单品图片（用户拍照录入）
│   ├── item_001.jpg
│   ├── item_002.jpg
│   └── ...
│
├── taobao/               # 淘宝商品缓存图片
│   ├── shop_123456/      # 按店铺分目录
│   │   ├── item_789.jpg
│   │   └── ...
│   └── ...
│
├── arrivals/             # 上新商品图片
│   └── ...
│
└── charts/               # 统计图表
    ├── category_pie.png
    ├── color_bar.png
    └── ...
```

### 3.2 图片服务模块

```python
"""
图片服务模块
负责图片的获取、缓存、处理
"""

import os
import requests
import hashlib
from typing import Optional, Dict
from PIL import Image
import io

class ImageService:
    """图片服务"""
    
    def __init__(self, base_path: str = "./data/stylebuddy/images"):
        self.base_path = base_path
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """确保目录存在"""
        for subdir in ['wardrobe', 'taobao', 'arrivals', 'charts']:
            os.makedirs(os.path.join(self.base_path, subdir), exist_ok=True)
    
    def get_image(self, source: str, item_id: str) -> Optional[Dict]:
        """
        获取图片信息
        
        Args:
            source: 来源 - wardrobe/taobao/arrival
            item_id: 单品ID
        
        Returns:
            {
                "url": "https://...",      # 原始URL（如有）
                "path": "/path/to/...",    # 本地路径
                "exists": True/False
            }
        """
        # 查找本地图片
        dir_path = os.path.join(self.base_path, source)
        
        for ext in ['jpg', 'jpeg', 'png', 'webp']:
            path = os.path.join(dir_path, f"{item_id}.{ext}")
            if os.path.exists(path):
                return {
                    "path": path,
                    "exists": True
                }
        
        # 查询数据库获取原始URL
        # ...
        
        return None
    
    def download_and_cache(self, url: str, source: str, item_id: str) -> Optional[str]:
        """
        下载图片并缓存到本地
        
        Args:
            url: 图片URL
            source: 来源目录
            item_id: 单品ID
        
        Returns:
            本地路径
        """
        dir_path = os.path.join(self.base_path, source)
        
        # 确定文件扩展名
        ext = url.split('.')[-1].split('?')[0] or 'jpg'
        if ext not in ['jpg', 'jpeg', 'png', 'webp']:
            ext = 'jpg'
        
        save_path = os.path.join(dir_path, f"{item_id}.{ext}")
        
        # 已存在则跳过
        if os.path.exists(save_path):
            return save_path
        
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return save_path
        except Exception as e:
            print(f"下载图片失败: {e}")
        
        return None
    
    def create_outfit_collage(self, items: List[Dict], output_id: str) -> Optional[str]:
        """
        创建穿搭组合图（横向拼接）
        
        Args:
            items: 单品列表，每个包含 image.path 或 image.url
            output_id: 输出文件ID
        
        Returns:
            生成的图片路径
        """
        images = []
        
        for item in items:
            img_info = item.get('image', {})
            img_path = img_info.get('path')
            
            # 如果没有本地路径，尝试下载
            if not img_path and img_info.get('url'):
                img_path = self.download_and_cache(
                    img_info['url'],
                    'wardrobe',
                    item.get('id', hashlib.md5(img_info['url'].encode()).hexdigest())
                )
            
            if img_path and os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    images.append(img)
                except:
                    pass
        
        if not images:
            return None
        
        # 统一尺寸
        size = (200, 200)
        resized = [img.resize(size, Image.LANCZOS) for img in images]
        
        # 横向拼接
        total_width = size[0] * len(resized)
        combined = Image.new('RGB', (total_width, size[1]), (255, 255, 255))
        
        x = 0
        for img in resized:
            combined.paste(img, (x, 0))
            x += size[0]
        
        output_path = os.path.join(self.base_path, 'charts', f'outfit_{output_id}.jpg')
        combined.save(output_path, quality=85)
        
        return output_path
    
    def to_base64(self, image_path: str) -> Optional[str]:
        """图片转 Base64"""
        if not os.path.exists(image_path):
            return None
        
        with open(image_path, 'rb') as f:
            import base64
            return base64.b64encode(f.read()).decode()
```

---

## 四、消息构建服务

```python
"""
消息构建服务
构建标准化的输出数据结构
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import json

class MessageBuilder:
    """消息构建器"""
    
    def __init__(self, db, image_service: ImageService):
        self.db = db
        self.image_service = image_service
    
    def build_outfit_recommendation(
        self,
        weather: Dict,
        user_profile: Dict,
        items: List[Dict],
        tips: List[str],
        template_id: str = None
    ) -> Dict:
        """
        构建穿搭推荐输出
        """
        # 为每个单品添加图片信息
        items_with_image = []
        for item in items:
            item_copy = item.copy()
            
            # 获取图片
            image_info = self.image_service.get_image(
                item.get('source', 'wardrobe'),
                item['id']
            )
            
            if image_info:
                item_copy['image'] = image_info
            elif item.get('image_url'):
                # 下载并缓存
                path = self.image_service.download_and_cache(
                    item['image_url'],
                    'taobao',
                    item['id']
                )
                if path:
                    item_copy['image'] = {
                        'url': item['image_url'],
                        'path': path
                    }
            
            items_with_image.append(item_copy)
        
        result = {
            'weather': weather,
            'user_profile': {
                'body_type_label': self._body_type_label(user_profile.get('body_type')),
                'style_preference': user_profile.get('style_preferences', [])
            },
            'items': items_with_image,
            'tips': tips,
            'meta': {
                'generated_at': datetime.now().isoformat(),
                'template_id': template_id
            }
        }
        
        return result
    
    def build_new_arrival_push(
        self,
        source: Dict,
        items: List[Dict],
        user_profile: Dict
    ) -> Dict:
        """
        构建上新推送输出
        """
        # 为每个商品添加图片和匹配信息
        items_with_details = []
        
        for item in items:
            item_copy = item.copy()
            
            # 获取/下载图片
            if item.get('image_url'):
                path = self.image_service.download_and_cache(
                    item['image_url'],
                    'arrivals',
                    item['id']
                )
                item_copy['image'] = {
                    'url': item['image_url'],
                    'path': path
                } if path else {'url': item['image_url']}
            
            # 计算匹配度
            match_result = self._calculate_match(item, user_profile)
            item_copy.update(match_result)
            
            items_with_details.append(item_copy)
        
        # 按匹配度排序
        items_with_details.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        
        # 今日推荐
        top_pick = None
        if items_with_details:
            top = items_with_details[0]
            top_pick = {
                'title': top['title'],
                'reason': top.get('match_reason', '匹配度最高')
            }
        
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'source': source,
            'items': items_with_details,
            'top_pick': top_pick,
            'stats': {
                'total_new': len(items_with_details),
                'high_match': len([i for i in items_with_details if i.get('match_score', 0) >= 80])
            }
        }
    
    def build_consultation_result(
        self,
        item: Dict,
        user_profile: Dict
    ) -> Dict:
        """
        构建种草咨询输出
        """
        # 分析商品
        analysis = self._analyze_item(item)
        
        # 查找可搭配单品
        wardrobe_matches = self._find_wardrobe_matches(item, user_profile)
        
        # 为可搭配单品添加图片
        for match in wardrobe_matches:
            image_info = self.image_service.get_image('wardrobe', match['id'])
            if image_info:
                match['image'] = image_info
        
        # 生成建议
        recommendation, reasons, warnings = self._generate_advice(
            item, analysis, wardrobe_matches, user_profile
        )
        
        return {
            'item': {
                'title': item.get('title'),
                'image': {'url': item.get('image_url')} if item.get('image_url') else None,
                'price': item.get('price'),
                'url': item.get('url'),
                'category_label': analysis.get('category_label'),
                'style_tags': analysis.get('style_tags'),
                'selling_points': analysis.get('selling_points')
            },
            'wardrobe_matches': wardrobe_matches,
            'recommendation': recommendation,
            'reasons': reasons,
            'warnings': warnings,
            'match_score': analysis.get('match_score', 0)
        }
    
    def _body_type_label(self, body_type: str) -> str:
        """体型标签"""
        labels = {
            'standard': '标准体型',
            'pear': '梨形身材',
            'apple': '苹果形身材',
            'h': 'H形身材',
            'inverted_triangle': '倒三角身材'
        }
        return labels.get(body_type, '')
    
    def _calculate_match(self, item: Dict, user_profile: Dict) -> Dict:
        """计算匹配度"""
        # 实现匹配度计算逻辑
        pass
    
    def _analyze_item(self, item: Dict) -> Dict:
        """分析商品"""
        # 实现商品分析逻辑
        pass
    
    def _find_wardrobe_matches(self, item: Dict, user_profile: Dict) -> List[Dict]:
        """查找可搭配单品"""
        # 实现搭配查找逻辑
        pass
    
    def _generate_advice(self, item, analysis, matches, profile) -> tuple:
        """生成购买建议"""
        # 实现建议生成逻辑
        pass
```

---

## 五、对外接口

### 5.1 Skill 主入口

```python
"""
StyleBuddy 主入口
提供统一的对外接口
"""

class StyleBuddy:
    """StyleBuddy 主类"""
    
    def __init__(self):
        self.db = Database()
        self.image_service = ImageService()
        self.message_builder = MessageBuilder(self.db, self.image_service)
        self.recommender = OutfitRecommender(self.db)
        self.analyzer = WardrobeAnalyzer(self.db)
        # ...
    
    # ==================== 穿搭推荐 ====================
    
    def get_today_outfit(self, user_id: str = None) -> Dict:
        """
        获取今日穿搭推荐
        
        Returns:
            OutfitRecommendation 结构的字典
        """
        # 1. 获取用户画像
        user_profile = self.db.get_user_profile(user_id)
        
        # 2. 获取天气
        weather = self.weather_service.get_current()
        
        # 3. 获取推荐搭配
        outfit = self.recommender.recommend(
            user_profile=user_profile,
            weather=weather
        )
        
        # 4. 构建输出
        return self.message_builder.build_outfit_recommendation(
            weather=weather,
            user_profile=user_profile,
            items=outfit['items'],
            tips=outfit['tips'],
            template_id=outfit.get('template_id')
        )
    
    # ==================== 上新推送 ====================
    
    def check_new_arrivals(self, user_id: str = None) -> Dict:
        """
        检查关注店铺上新
        
        Returns:
            NewArrivalPush 结构的字典
        """
        user_profile = self.db.get_user_profile(user_id)
        sources = self.db.list_followed_sources()
        
        all_items = []
        for source in sources:
            items = self._fetch_shop_new_items(source)
            all_items.extend(items)
        
        return self.message_builder.build_new_arrival_push(
            source=sources[0] if sources else {},
            items=all_items,
            user_profile=user_profile
        )
    
    # ==================== 种草咨询 ====================
    
    def consult_item(self, item_url: str = None, item_image: str = None, 
                     user_id: str = None) -> Dict:
        """
        种草咨询
        
        Args:
            item_url: 商品链接
            item_image: 商品图片路径
        
        Returns:
            ConsultationResult 结构的字典
        """
        user_profile = self.db.get_user_profile(user_id)
        
        # 获取商品信息
        if item_url:
            item = self._fetch_item_info(item_url)
        elif item_image:
            item = self._analyze_item_image(item_image)
        else:
            return {'error': '请提供商品链接或图片'}
        
        return self.message_builder.build_consultation_result(
            item=item,
            user_profile=user_profile
        )
    
    # ==================== 衣橱分析 ====================
    
    def analyze_wardrobe(self, user_id: str = None) -> Dict:
        """
        分析衣橱
        
        Returns:
            WardrobeReport 结构的字典
        """
        # 实现分析逻辑
        pass
```

### 5.2 调用示例

```python
# 初始化
sb = StyleBuddy()

# 1. 获取今日穿搭
outfit = sb.get_today_outfit()
# 返回: {"weather": {...}, "items": [...], "tips": [...]}
# 接入方根据返回的数据渲染UI或推送

# 2. 检查上新
arrivals = sb.check_new_arrivals()
# 返回: {"date": "...", "items": [...], "top_pick": {...}}

# 3. 种草咨询
result = sb.consult_item(item_url="https://item.taobao.com/...")
# 返回: {"item": {...}, "wardrobe_matches": [...], "recommendation": "..."}
```

---

## 六、总结

### Skill 职责

| 职责 | 说明 |
|------|------|
| 业务逻辑 | 搭配推荐、上新检查、种草咨询、衣橱分析 |
| 图片处理 | 下载、缓存、拼接、转换 |
| 结构化输出 | 标准化的 JSON 数据，包含图片路径/URL |
| 数据存储 | 本地 SQLite 数据库 |

### 接入方职责

| 职责 | 说明 |
|------|------|
| 渠道推送 | 根据返回数据推送到钉钉/微信/飞书等 |
| UI渲染 | 根据返回数据渲染界面 |
| 用户交互 | 处理用户点击、输入等操作 |

### 输出格式

所有输出均为标准 JSON，包含：
- 结构化的文本内容
- 图片信息（URL + 本地路径）
- 元数据（时间、匹配度等）

接入方可根据自身渠道能力，选择合适的展示方式。