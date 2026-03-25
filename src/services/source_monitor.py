"""
关注来源管理模块
管理用户关注的店铺、博主等来源
"""

import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

from ..storage.database import Database


@dataclass
class FollowedSource:
    """关注来源"""
    id: str
    source_type: str       # taobao_shop/douyin_blogger/wechat_account
    name: str
    external_id: str       # 外部平台ID
    url: str
    avatar: str
    description: str
    follower_count: int
    member_id: str         # 所属成员
    last_checked: str      # 最后检查时间
    created_at: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


class SourceManager:
    """关注来源管理器
    
    功能：
    1. 添加/删除关注来源
    2. 获取关注列表
    3. 更新检查状态
    """
    
    SOURCE_TYPE_NAMES = {
        'taobao_shop': '淘宝店铺',
        'douyin_blogger': '抖音博主',
        'wechat_account': '公众号',
        'xiaohongshu_blogger': '小红书博主',
        'weibo_account': '微博账号',
    }
    
    def __init__(self, db: Database):
        """初始化来源管理器
        
        Args:
            db: Database 实例
        """
        self.db = db
    
    def add_source(
        self,
        source_type: str,
        name: str,
        external_id: str = None,
        url: str = None,
        avatar: str = None,
        description: str = None,
        follower_count: int = 0,
        member_id: str = None
    ) -> str:
        """添加关注来源
        
        Args:
            source_type: 来源类型
            name: 名称
            external_id: 外部ID
            url: 链接
            avatar: 头像
            description: 描述
            follower_count: 粉丝数
            member_id: 所属成员
            
        Returns:
            来源ID
        """
        source_data = {
            'source_type': source_type,
            'source_id': external_id,
            'name': name,
            'url': url,
            'avatar': avatar,
            'description': description,
            'follower_count': follower_count,
            'member_id': member_id
        }
        
        return self.db.add_followed_source(source_data)
    
    def get_sources(self, member_id: str = None, source_type: str = None) -> List[Dict]:
        """获取关注来源列表
        
        Args:
            member_id: 成员ID（可选）
            source_type: 来源类型（可选）
            
        Returns:
            来源列表
        """
        sources = self.db.get_followed_sources(member_id)
        
        if source_type:
            sources = [s for s in sources if s.get('source_type') == source_type]
        
        return sources
    
    def get_source(self, source_id: str) -> Optional[Dict]:
        """获取单个来源"""
        sources = self.db.get_followed_sources()
        for s in sources:
            if s['id'] == source_id:
                return s
        return None
    
    def update_last_checked(self, source_id: str):
        """更新最后检查时间"""
        self.db.update_source_last_checked(source_id)
    
    def delete_source(self, source_id: str) -> bool:
        """删除关注来源"""
        return self.db.delete_followed_source(source_id)
    
    def get_sources_for_check(self, hours: int = 24) -> List[Dict]:
        """获取需要检查的来源
        
        Args:
            hours: 距上次检查超过多少小时
            
        Returns:
            需要检查的来源列表
        """
        sources = self.db.get_followed_sources()
        
        result = []
        for s in sources:
            last_checked = s.get('last_checked')
            if not last_checked:
                result.append(s)
                continue
            
            # 检查时间间隔
            try:
                last_time = datetime.fromisoformat(last_checked)
                now = datetime.now()
                diff_hours = (now - last_time).total_seconds() / 3600
                
                if diff_hours >= hours:
                    result.append(s)
            except:
                result.append(s)
        
        return result
    
    def get_source_stats(self, member_id: str = None) -> Dict[str, Any]:
        """获取来源统计"""
        sources = self.get_sources(member_id)
        
        stats = {
            'total': len(sources),
            'by_type': {},
            'new_items_count': 0
        }
        
        for s in sources:
            st = s.get('source_type', 'unknown')
            stats['by_type'][st] = stats['by_type'].get(st, 0) + 1
        
        return stats


class SourceMonitor:
    """来源监控器
    
    功能：
    1. 定期检查关注的店铺/博主上新
    2. 发现新品时通知用户
    3. 分析新品是否适合用户
    """
    
    def __init__(self, db: Database, source_manager: SourceManager):
        """初始化监控器
        
        Args:
            db: Database 实例
            source_manager: SourceManager 实例
        """
        self.db = db
        self.source_manager = source_manager
    
    async def check_source(self, source_id: str) -> Dict[str, Any]:
        """检查单个来源的新品
        
        Args:
            source_id: 来源ID
            
        Returns:
            检查结果
        """
        source = self.source_manager.get_source(source_id)
        if not source:
            return {'error': '来源不存在'}
        
        source_type = source.get('source_type')
        
        # 根据类型调用不同的检查方法
        if source_type == 'taobao_shop':
            new_items = await self._check_taobao_shop(source)
        elif source_type == 'douyin_blogger':
            new_items = await self._check_douyin_blogger(source)
        else:
            new_items = []
        
        # 更新检查时间
        self.source_manager.update_last_checked(source_id)
        
        # 保存新品到数据库
        for item in new_items:
            item['source_id'] = source_id
            self.db.add_source_item(item)
        
        return {
            'source': source,
            'new_items': new_items,
            'count': len(new_items)
        }
    
    async def _check_taobao_shop(self, source: Dict) -> List[Dict]:
        """检查淘宝店铺上新
        
        Args:
            source: 来源信息
            
        Returns:
            新品列表
        """
        # TODO: 集成淘宝 CLI 获取店铺商品
        # 这里返回模拟数据
        return []
    
    async def _check_douyin_blogger(self, source: Dict) -> List[Dict]:
        """检查抖音博主上新"""
        # TODO: 实现抖音检查
        return []
    
    async def check_all(self, hours: int = 24) -> Dict[str, Any]:
        """检查所有需要更新的来源
        
        Args:
            hours: 距上次检查超过多少小时
            
        Returns:
            检查结果汇总
        """
        sources = self.source_manager.get_sources_for_check(hours)
        
        results = {
            'checked': 0,
            'total_new_items': 0,
            'details': []
        }
        
        for source in sources:
            result = await self.check_source(source['id'])
            results['checked'] += 1
            results['total_new_items'] += result.get('count', 0)
            results['details'].append({
                'source_name': source['name'],
                'new_count': result.get('count', 0)
            })
        
        return results
    
    def get_new_items(self, member_id: str = None) -> List[Dict]:
        """获取新品列表
        
        Args:
            member_id: 成员ID
            
        Returns:
            新品列表
        """
        sources = self.source_manager.get_sources(member_id)
        
        all_items = []
        for source in sources:
            items = self.db.get_source_items(source['id'], is_new=True)
            for item in items:
                item['source_name'] = source['name']
            all_items.extend(items)
        
        return all_items
    
    def mark_items_as_seen(self, item_ids: List[str]):
        """标记商品为已查看"""
        for item_id in item_ids:
            self.db.mark_item_analyzed(item_id, {'seen': True})


class ShopAnalyzer:
    """店铺/博主分析器
    
    分析关注的店铺/博主：
    1. 风格定位
    2. 价格区间
    3. 是否适合用户
    """
    
    def __init__(self, db: Database):
        self.db = db
    
    def analyze_source(self, source_id: str) -> Dict[str, Any]:
        """分析来源
        
        Args:
            source_id: 来源ID
            
        Returns:
            分析结果
        """
        items = self.db.get_source_items(source_id)
        
        if not items:
            return {
                'status': 'no_data',
                'message': '暂无数据'
            }
        
        # 统计品类分布
        categories = {}
        colors = {}
        prices = []
        
        for item in items:
            cat = item.get('category')
            if cat:
                categories[cat] = categories.get(cat, 0) + 1
            
            color = item.get('color')
            if color:
                colors[color] = colors.get(color, 0) + 1
            
            price = item.get('price')
            if price:
                prices.append(float(price))
        
        # 计算价格区间
        price_range = None
        if prices:
            price_range = {
                'min': min(prices),
                'max': max(prices),
                'avg': sum(prices) / len(prices)
            }
        
        # 判断风格
        style = self._detect_style(items)
        
        return {
            'status': 'analyzed',
            'item_count': len(items),
            'categories': categories,
            'colors': colors,
            'price_range': price_range,
            'style': style
        }
    
    def _detect_style(self, items: List[Dict]) -> Optional[str]:
        """检测店铺风格"""
        # 简单风格检测
        style_keywords = {
            'casual': ['休闲', '日常', '舒适'],
            'business': ['商务', '通勤', '职业'],
            'sweet': ['甜美', '可爱', '少女'],
            'cool': ['酷', '街头', '个性'],
            'minimalist': ['简约', '基础', '纯色'],
            'elegant': ['优雅', '气质', '轻熟'],
        }
        
        style_count = {s: 0 for s in style_keywords}
        
        for item in items:
            name = item.get('name', '').lower()
            desc = item.get('description', '').lower()
            text = name + ' ' + desc
            
            for style, keywords in style_keywords.items():
                for kw in keywords:
                    if kw in text:
                        style_count[style] += 1
        
        if max(style_count.values()) > 0:
            return max(style_count, key=style_count.get)
        
        return None
    
    def check_fit_for_member(self, source_id: str, member_profile: Dict) -> Dict[str, Any]:
        """检查来源是否适合成员
        
        Args:
            source_id: 来源ID
            member_profile: 成员画像
            
        Returns:
            适合度分析
        """
        source_analysis = self.analyze_source(source_id)
        
        if source_analysis['status'] != 'analyzed':
            return {'fit': False, 'reason': '数据不足'}
        
        fit_score = 0
        reasons = []
        
        # 检查风格匹配
        source_style = source_analysis.get('style')
        member_styles = member_profile.get('style', {}).get('preferred_styles', [])
        
        if source_style and source_style in member_styles:
            fit_score += 40
            reasons.append(f"风格匹配：{source_style}")
        
        # 检查颜色匹配
        member_colors = member_profile.get('style', {}).get('preferred_colors', [])
        source_colors = list(source_analysis.get('colors', {}).keys())
        
        color_match = set(member_colors) & set(source_colors)
        if color_match:
            fit_score += 30
            reasons.append(f"颜色匹配：{', '.join(color_match)}")
        
        # 检查价格区间
        price_range = source_analysis.get('price_range')
        # 可以根据用户消费习惯判断
        
        return {
            'fit_score': fit_score,
            'fit': fit_score >= 50,
            'reasons': reasons,
            'source_analysis': source_analysis
        }