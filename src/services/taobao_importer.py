"""
淘宝导入模块
从淘宝订单、购物车、收藏夹导入商品到衣橱
"""

import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict

from ..storage.database import Database
from ..models.profile import MemberProfile
from .image_service import ImageService


@dataclass
class TaobaoItem:
    """淘宝商品"""
    item_id: str
    title: str
    price: float
    pic_url: str
    detail_url: str
    shop_name: str
    category: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    order_time: Optional[str] = None
    status: str = "unknown"  # ordered/in_cart/favorited
    
    def to_dict(self) -> Dict:
        return asdict(self)


class TaobaoImporter:
    """淘宝导入器
    
    功能：
    1. 解析淘宝订单数据
    2. 解析购物车/收藏夹数据
    3. AI 识别商品属性（品类、颜色、风格）
    4. 批量导入到成员衣橱
    """
    
    # 品类关键词映射
    CATEGORY_KEYWORDS = {
        'outer': ['外套', '大衣', '羽绒服', '风衣', '夹克', '西装', '皮衣', '棒球服', '棉服', '毛呢', '针织开衫'],
        'top': ['T恤', '衬衫', '毛衣', '针织衫', '卫衣', '吊带', '背心', '打底衫', '雪纺', 'blouse', 'POLO', 'polo', '羊绒衫', '羊毛衫'],
        'bottom': ['裤子', '裙', '牛仔裤', '休闲裤', '短裤', '半身裙', '连衣裙', '长裤', '西裤', '运动裤', '打底裤', '阔腿裤', '哈伦裤', '背带裤'],
        'shoes': ['鞋', '靴', '高跟鞋', '平底鞋', '运动鞋', '凉鞋', '拖鞋', '帆布鞋', '板鞋', '老爹鞋', '马丁靴', '切尔西', '豆豆鞋'],
        'accessory': ['包', '帽子', '围巾', '手套', '腰带', '项链', '耳环', '手表', '眼镜', '配饰', '包包', '手链', '丝巾', '发饰', '胸针'],
    }
    
    # 颜色关键词映射
    COLOR_KEYWORDS = {
        '黑色': ['黑色', '黑', '纯黑', '炭黑', '墨黑'],
        '白色': ['白色', '白', '纯白', '米白', '奶白', '象牙白'],
        '灰色': ['灰色', '灰', '浅灰', '深灰', '烟灰', '炭灰'],
        '米色': ['米色', '杏色', '奶茶色', '卡其色', '驼色', '燕麦色'],
        '蓝色': ['蓝色', '蓝', '天蓝', '深蓝', '藏蓝', '牛仔蓝', '雾霾蓝'],
        '粉色': ['粉色', '粉', '粉红', '浅粉', '玫粉', '樱花粉'],
        '红色': ['红色', '红', '大红', '酒红', '枣红', '砖红'],
        '绿色': ['绿色', '绿', '墨绿', '军绿', '薄荷绿', '牛油果绿'],
        '黄色': ['黄色', '黄', '姜黄', '鹅黄', '柠檬黄'],
        '紫色': ['紫色', '紫', '薰衣草紫', '香芋紫'],
        '棕色': ['棕色', '棕', '咖啡色', '褐色', '巧克力色'],
    }
    
    # 风格关键词映射
    STYLE_KEYWORDS = {
        'casual': ['休闲', '日常', '舒适', '宽松', '百搭'],
        'business': ['商务', '职业', '通勤', '正装', '西装'],
        'sweet': ['甜美', '可爱', '少女', '公主', '蓬蓬'],
        'cool': ['酷', '帅气', '街头', '个性', '朋克', '嘻哈'],
        'minimalist': ['简约', '基础', '纯色', '极简', '性冷淡'],
        'elegant': ['优雅', '气质', '淑女', '知性', '轻熟'],
        'vintage': ['复古', '文艺', '民族风', '国风', '古风'],
        'sporty': ['运动', '健身', '瑜伽', '跑步', '篮球', '足球'],
    }
    
    def __init__(self, db: Database, image_service: ImageService = None):
        """初始化淘宝导入器
        
        Args:
            db: Database 实例
            image_service: ImageService 实例（可选）
        """
        self.db = db
        self.image_service = image_service or ImageService()
    
    def parse_order_data(self, order_data: Dict) -> List[TaobaoItem]:
        """解析订单数据
        
        Args:
            order_data: 从淘宝 CLI 获取的订单数据
            
        Returns:
            商品列表
        """
        items = []
        
        # 解析订单列表
        orders = order_data.get('orders', [])
        if not orders and 'data' in order_data:
            orders = order_data.get('data', {}).get('orders', [])
        
        for order in orders:
            # 提取商品信息
            sub_orders = order.get('subOrders', [order])
            
            for sub in sub_orders:
                item_info = sub.get('itemInfo', sub)
                
                item = TaobaoItem(
                    item_id=str(item_info.get('itemId', uuid.uuid4().hex[:8])),
                    title=item_info.get('title', ''),
                    price=float(item_info.get('price', 0) or 0),
                    pic_url=item_info.get('pic', '') or item_info.get('picUrl', ''),
                    detail_url=item_info.get('detailUrl', ''),
                    shop_name=order.get('seller', {}).get('shopName', ''),
                    order_time=order.get('createTime', ''),
                    status='ordered'
                )
                
                # 尝试从标题提取颜色和尺码
                sku_info = sub.get('skuInfo', '')
                if sku_info:
                    item.color, item.size = self._parse_sku(sku_info)
                
                items.append(item)
        
        return items
    
    def parse_cart_data(self, cart_data: Dict) -> List[TaobaoItem]:
        """解析购物车数据"""
        items = []
        
        carts = cart_data.get('carts', [])
        if not carts and 'data' in cart_data:
            carts = cart_data.get('data', {}).get('carts', [])
        
        for cart_item in carts:
            item = TaobaoItem(
                item_id=str(cart_item.get('itemId', uuid.uuid4().hex[:8])),
                title=cart_item.get('title', ''),
                price=float(cart_item.get('price', 0) or 0),
                pic_url=cart_item.get('pic', '') or cart_item.get('picUrl', ''),
                detail_url=cart_item.get('detailUrl', ''),
                shop_name=cart_item.get('shopName', ''),
                status='in_cart'
            )
            
            sku_info = cart_item.get('skuInfo', '')
            if sku_info:
                item.color, item.size = self._parse_sku(sku_info)
            
            items.append(item)
        
        return items
    
    def parse_favorite_data(self, favorite_data: Dict) -> List[TaobaoItem]:
        """解析收藏夹数据"""
        items = []
        
        favorites = favorite_data.get('favorites', [])
        if not favorites and 'data' in favorite_data:
            favorites = favorite_data.get('data', {}).get('favorites', [])
        
        for fav in favorites:
            item = TaobaoItem(
                item_id=str(fav.get('itemId', uuid.uuid4().hex[:8])),
                title=fav.get('title', ''),
                price=float(fav.get('price', 0) or 0),
                pic_url=fav.get('pic', '') or fav.get('picUrl', ''),
                detail_url=fav.get('detailUrl', ''),
                shop_name=fav.get('shopName', ''),
                status='favorited'
            )
            
            items.append(item)
        
        return items
    
    def analyze_item(self, item: TaobaoItem) -> Dict[str, Any]:
        """分析商品属性
        
        Args:
            item: 淘宝商品
            
        Returns:
            分析结果：品类、颜色、风格、季节等
        """
        title = item.title.lower()
        
        # 识别品类
        category = self._detect_category(title)
        
        # 识别颜色
        color = item.color or self._detect_color(title)
        
        # 识别风格
        style = self._detect_style(title)
        
        # 识别季节
        season = self._detect_season(title)
        
        # 判断是否为服饰
        is_clothing = category is not None
        
        return {
            'category': category,
            'color': color,
            'style': style,
            'season': season,
            'is_clothing': is_clothing,
            'confidence': 0.8 if category else 0.3
        }
    
    def _detect_category(self, title: str) -> Optional[str]:
        """检测品类"""
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in title:
                    return category
        return None
    
    def _detect_color(self, title: str) -> Optional[str]:
        """检测颜色"""
        for color, keywords in self.COLOR_KEYWORDS.items():
            for keyword in keywords:
                if keyword in title:
                    return color
        return None
    
    def _detect_style(self, title: str) -> Optional[str]:
        """检测风格"""
        styles = []
        for style, keywords in self.STYLE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in title:
                    styles.append(style)
                    break
        return styles[0] if styles else None
    
    def _detect_season(self, title: str) -> str:
        """检测季节"""
        summer_keywords = ['夏季', '夏天', '短袖', '薄款', '透气', '冰丝', '防晒']
        winter_keywords = ['冬季', '冬天', '加绒', '保暖', '羽绒', '毛呢', '厚款']
        spring_autumn_keywords = ['春秋', '薄外套', '风衣']
        
        for kw in summer_keywords:
            if kw in title:
                return 'summer'
        for kw in winter_keywords:
            if kw in title:
                return 'winter'
        for kw in spring_autumn_keywords:
            if kw in title:
                return 'spring_autumn'
        
        return 'all_season'
    
    def _parse_sku(self, sku_info: str) -> Tuple[Optional[str], Optional[str]]:
        """解析 SKU 信息"""
        color = None
        size = None
        
        # 常见格式：颜色:白色;尺码:M 或 颜色分类:白色
        parts = sku_info.split(';')
        for part in parts:
            if ':' in part:
                key, value = part.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                if '颜色' in key or '色' in key:
                    color = value
                elif '尺码' in key or '码' in key or 'size' in key.lower():
                    size = value
        
        return color, size
    
    async def import_to_wardrobe(
        self,
        items: List[TaobaoItem],
        member_id: str,
        filter_clothing: bool = True,
        download_images: bool = True
    ) -> Dict[str, Any]:
        """导入商品到衣橱
        
        Args:
            items: 商品列表
            member_id: 目标成员 ID
            filter_clothing: 是否只导入服饰类
            download_images: 是否下载图片
            
        Returns:
            导入结果统计
        """
        result = {
            'total': len(items),
            'imported': 0,
            'skipped': 0,
            'failed': 0,
            'items': []
        }
        
        for item in items:
            # 分析商品
            analysis = self.analyze_item(item)
            
            # 过滤非服饰
            if filter_clothing and not analysis['is_clothing']:
                result['skipped'] += 1
                continue
            
            # 检查是否已存在
            existing = self.db.get_item_by_source_url(item.detail_url)
            if existing:
                result['skipped'] += 1
                continue
            
            # 下载图片
            local_image = None
            if download_images and item.pic_url:
                try:
                    local_image = await self.image_service.download_image(item.pic_url)
                except Exception as e:
                    print(f"下载图片失败: {e}")
            
            # 创建单品数据
            item_data = {
                'name': item.title,
                'category': analysis['category'],
                'color': analysis['color'] or item.color,
                'style': analysis['style'],
                'season': analysis['season'],
                'price': item.price,
                'source': 'taobao',
                'source_url': item.detail_url,
                'image_path': local_image,
                'tags': [item.shop_name] if item.shop_name else []
            }
            
            # 保存到数据库
            try:
                item_id = self.db.add_item(item_data, member_id)
                result['imported'] += 1
                result['items'].append({
                    'id': item_id,
                    'name': item.title,
                    'category': analysis['category']
                })
            except Exception as e:
                result['failed'] += 1
                print(f"导入失败: {e}")
        
        return result
    
    def get_import_preview(self, items: List[TaobaoItem]) -> Dict[str, Any]:
        """获取导入预览
        
        Args:
            items: 商品列表
            
        Returns:
            预览数据（分类统计、将导入的商品）
        """
        preview = {
            'total': len(items),
            'categories': {},
            'clothing_items': [],
            'non_clothing_items': []
        }
        
        for item in items:
            analysis = self.analyze_item(item)
            
            if analysis['is_clothing']:
                preview['clothing_items'].append({
                    'title': item.title,
                    'category': analysis['category'],
                    'color': analysis['color'],
                    'price': item.price,
                    'pic_url': item.pic_url
                })
                
                cat = analysis['category'] or 'other'
                preview['categories'][cat] = preview['categories'].get(cat, 0) + 1
            else:
                preview['non_clothing_items'].append({
                    'title': item.title,
                    'price': item.price
                })
        
        return preview


class TaobaoImportSession:
    """淘宝导入会话
    
    管理导入流程状态
    """
    
    def __init__(self, importer: TaobaoImporter):
        self.importer = importer
        self._pending_items: List[TaobaoItem] = []
        self._preview: Optional[Dict] = None
        self._member_id: Optional[str] = None
    
    def start_session(self, data: Dict, data_type: str, member_id: str) -> Dict:
        """开始导入会话
        
        Args:
            data: 原始数据
            data_type: 数据类型 (order/cart/favorite)
            member_id: 目标成员
            
        Returns:
            预览结果
        """
        self._member_id = member_id
        
        # 解析数据
        if data_type == 'order':
            self._pending_items = self.importer.parse_order_data(data)
        elif data_type == 'cart':
            self._pending_items = self.importer.parse_cart_data(data)
        elif data_type == 'favorite':
            self._pending_items = self.importer.parse_favorite_data(data)
        else:
            return {'error': '未知数据类型'}
        
        # 生成预览
        self._preview = self.importer.get_import_preview(self._pending_items)
        
        return {
            'status': 'preview',
            'preview': self._preview,
            'message': self._format_preview_message()
        }
    
    def _format_preview_message(self) -> str:
        """格式化预览消息"""
        if not self._preview:
            return ""
        
        lines = [f"## 📦 导入预览\n"]
        lines.append(f"**共 {self._preview['total']} 件商品**\n")
        
        if self._preview['clothing_items']:
            lines.append(f"**服饰类：{len(self._preview['clothing_items'])} 件**（将导入）")
            for cat, count in self._preview['categories'].items():
                cat_name = {'outer': '外套', 'top': '上装', 'bottom': '下装', 'shoes': '鞋子', 'accessory': '配饰'}.get(cat, cat)
                lines.append(f"- {cat_name}：{count}件")
        
        if self._preview['non_clothing_items']:
            lines.append(f"\n**非服饰类：{len(self._preview['non_clothing_items'])} 件**（将跳过）")
        
        lines.append("\n---\n")
        lines.append("回复「确认导入」开始导入，或「取消」放弃")
        
        return "\n".join(lines)
    
    async def confirm_import(self) -> Dict:
        """确认导入"""
        if not self._pending_items or not self._member_id:
            return {'error': '没有待导入的商品'}
        
        result = await self.importer.import_to_wardrobe(
            self._pending_items,
            self._member_id
        )
        
        # 清理会话
        self._pending_items = []
        self._preview = None
        
        return {
            'status': 'completed',
            'result': result,
            'message': f"## ✅ 导入完成\n\n成功导入 **{result['imported']}** 件单品\n\n跳过 {result['skipped']} 件（非服饰/重复）"
        }
    
    def cancel(self):
        """取消导入"""
        self._pending_items = []
        self._preview = None
        self._member_id = None
    
    def is_active(self) -> bool:
        """是否有活跃会话"""
        return len(self._pending_items) > 0