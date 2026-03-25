"""
推荐引擎模块
智能搭配推荐核心逻辑
支持多人衣橱
"""

import json
import random
from typing import List, Dict, Optional, Any
from datetime import datetime
import re
import os


class OutfitRecommender:
    """搭配推荐引擎 - 多人衣橱版"""
    
    def __init__(self, database):
        self.db = database
        self.templates = self._load_templates()
        self.color_schemes = self._load_color_schemes()
    
    def _load_templates(self) -> List[Dict]:
        """加载搭配模板"""
        template_path = "./assets/data/templates.json"
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._get_default_templates()
    
    def _load_color_schemes(self) -> List[Dict]:
        """加载配色方案"""
        color_path = "./assets/data/color_schemes.json"
        if os.path.exists(color_path):
            with open(color_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._get_default_colors()
    
    def _get_default_templates(self) -> List[Dict]:
        """默认模板数据"""
        return [
            {
                "id": "t_casual_001",
                "name": "基础休闲搭配",
                "category": "休闲",
                "gender": "female",
                "occasions": ["日常", "逛街"],
                "items": {"outer": ["风衣"], "top": ["T恤"], "bottom": ["牛仔裤"], "shoes": ["小白鞋"]},
                "colors": {"primary": ["米色"], "accent": ["白色", "蓝色"]},
                "tips": "敞开穿更休闲，内搭塞进去显腿长"
            },
            {
                "id": "t_work_001",
                "name": "职场通勤搭配",
                "category": "职场",
                "gender": "female",
                "occasions": ["上班", "面试"],
                "items": {"outer": ["西装"], "top": ["衬衫"], "bottom": ["西裤"], "shoes": ["高跟鞋"]},
                "colors": {"primary": ["黑色", "白色"], "accent": ["藏青"]},
                "tips": "合身剪裁更显专业，配饰选择简约款"
            },
            {
                "id": "t_date_001",
                "name": "约会温柔搭配",
                "category": "约会",
                "gender": "female",
                "occasions": ["约会", "聚会"],
                "items": {"outer": ["针织开衫"], "top": ["连衣裙"], "bottom": [], "shoes": ["低跟鞋"]},
                "colors": {"primary": ["粉色", "米色"], "accent": ["白色"]},
                "tips": "柔和色调更有亲和力，适当露肤增加女人味"
            },
            {
                "id": "t_male_casual_001",
                "name": "男士休闲搭配",
                "category": "休闲",
                "gender": "male",
                "occasions": ["日常", "逛街"],
                "items": {"outer": ["夹克"], "top": ["T恤"], "bottom": ["牛仔裤"], "shoes": ["运动鞋"]},
                "colors": {"primary": ["黑色", "灰色"], "accent": ["白色"]},
                "tips": "简约百搭，适合日常各种场合"
            },
            {
                "id": "t_male_work_001",
                "name": "男士商务搭配",
                "category": "职场",
                "gender": "male",
                "occasions": ["上班", "商务"],
                "items": {"outer": ["西装"], "top": ["衬衫"], "bottom": ["西裤"], "shoes": ["皮鞋"]},
                "colors": {"primary": ["黑色", "深蓝"], "accent": ["白色"]},
                "tips": "合身是关键，衬衫袖口露出西装1-2cm"
            },
            {
                "id": "t_child_casual_001",
                "name": "儿童休闲搭配",
                "category": "休闲",
                "gender": "child",
                "occasions": ["日常", "上学"],
                "items": {"outer": [], "top": ["T恤"], "bottom": ["休闲裤"], "shoes": ["运动鞋"]},
                "colors": {"primary": ["蓝色", "粉色"], "accent": ["白色"]},
                "tips": "舒适为主，方便活动，选择透气面料"
            },
            {
                "id": "t_child_school_001",
                "name": "儿童上学搭配",
                "category": "上学",
                "gender": "child",
                "occasions": ["上学", "日常"],
                "items": {"outer": [], "top": ["衬衫"], "bottom": ["休闲裤"], "shoes": ["运动鞋"]},
                "colors": {"primary": ["白色", "蓝色"], "accent": []},
                "tips": "干净整洁，方便活动，备一件外套"
            }
        ]
    
    def _get_default_colors(self) -> List[Dict]:
        """默认配色方案"""
        return [
            {"name": "经典黑白", "colors": ["黑色", "白色"], "style": "简约", "occasions": ["职场", "日常"]},
            {"name": "大地色系", "colors": ["米色", "卡其色", "棕色", "驼色"], "style": "优雅", "occasions": ["通勤", "休闲"]},
            {"name": "莫兰迪色", "colors": ["雾霾蓝", "灰粉", "豆绿", "燕麦"], "style": "温柔", "occasions": ["约会", "日常"]},
            {"name": "海军蓝白", "colors": ["藏青", "白色", "条纹"], "style": "清爽", "occasions": ["休闲", "度假"]}
        ]
    
    def recommend(
        self, 
        occasion: str = "日常", 
        weather: Dict = None, 
        count: int = 3,
        member_id: str = None,
        member_profile: Dict = None
    ) -> List[Dict]:
        """生成搭配推荐
        
        Args:
            occasion: 场合
            weather: 天气信息
            count: 推荐数量
            member_id: 成员ID
            member_profile: 成员画像
        
        Returns:
            推荐方案列表
        """
        # 获取指定成员的衣橱
        items = self.db.get_all_items(member_id=member_id)
        
        if not items:
            # 没有单品，返回纯模板推荐
            return self._get_template_recommendations(occasion, count, member_profile)
        
        # 有单品，基于模板+实际单品生成
        return self._generate_personalized_recommendations(
            items, occasion, weather, count, member_profile
        )
    
    def _get_template_recommendations(
        self, 
        occasion: str, 
        count: int,
        member_profile: Dict = None
    ) -> List[Dict]:
        """纯模板推荐（无单品时）"""
        # 根据成员画像过滤模板
        gender = 'unisex'
        if member_profile:
            gender = member_profile.get('gender', 'unisex')
            if member_profile.get('relationship') == 'child':
                gender = 'child'
        
        # 过滤适合性别和场合的模板
        matching = [
            t for t in self.templates 
            if occasion in t.get('occasions', []) 
            and t.get('gender') in [gender, 'unisex']
        ]
        
        if not matching:
            matching = [t for t in self.templates if t.get('gender') in [gender, 'unisex']]
        
        if not matching:
            matching = self.templates
        
        # 随机选择
        selected = random.sample(matching, min(count, len(matching)))
        
        # 格式化输出
        return [self._format_template(t) for t in selected]
    
    def _generate_personalized_recommendations(
        self, 
        items: List[Dict], 
        occasion: str, 
        weather: Dict, 
        count: int,
        member_profile: Dict = None
    ) -> List[Dict]:
        """个性化推荐"""
        recommendations = []
        
        # 按类别分组
        by_category = {"outer": [], "top": [], "bottom": [], "shoes": [], "accessory": []}
        for item in items:
            cat = item.get('category', 'top')
            if cat in by_category:
                by_category[cat].append(item)
        
        # 根据天气调整
        temp = weather.get('temperature', 20) if weather else 20
        need_outer = temp < 20
        
        # 根据成员画像调整
        gender = 'unisex'
        preferred_colors = []
        preferred_styles = []
        
        if member_profile:
            gender = member_profile.get('gender', 'unisex')
            if member_profile.get('relationship') == 'child':
                gender = 'child'
            
            style_info = member_profile.get('style', {})
            preferred_colors = style_info.get('preferred_colors', [])
            preferred_styles = style_info.get('preferred_styles', [])
        
        # 筛选合适性别的模板
        matching_templates = [
            t for t in self.templates 
            if occasion in t.get('occasions', []) 
            and t.get('gender') in [gender, 'unisex']
        ]
        
        if not matching_templates:
            matching_templates = [
                t for t in self.templates 
                if t.get('gender') in [gender, 'unisex']
            ]
        
        if not matching_templates:
            matching_templates = self.templates
        
        selected_templates = random.sample(matching_templates, min(count * 2, len(matching_templates)))
        
        for template in selected_templates:
            outfit = self._match_items_to_template(
                template, by_category, need_outer, preferred_colors
            )
            if outfit:
                recommendations.append(outfit)
        
        # 如果匹配不够，补充纯模板
        while len(recommendations) < count:
            template = random.choice(matching_templates)
            recommendations.append(self._format_template(template))
        
        return recommendations[:count]
    
    def _match_items_to_template(
        self, 
        template: Dict, 
        by_category: Dict, 
        need_outer: bool,
        preferred_colors: List[str] = None
    ) -> Optional[Dict]:
        """将模板与用户单品匹配"""
        template_items = template.get('items', {})
        matched_items = []
        matched_details = []
        
        for cat, keywords in template_items.items():
            if not keywords:
                continue
            
            # 跳过外套如果不需要
            if cat == 'outer' and not need_outer:
                continue
            
            # 在用户单品中找匹配的
            user_items = by_category.get(cat, [])
            matched = self._find_matching_item(
                user_items, keywords, template.get('colors', {}), preferred_colors
            )
            
            if matched:
                color = matched.get('color', '') or ''
                name = matched.get('name', '')
                # 避免颜色重复
                if color and name.startswith(color):
                    matched_items.append(name)
                else:
                    matched_items.append(f"{color} {name}".strip())
                matched_details.append(matched)
            elif cat in ['top', 'bottom']:
                # 核心单品必须匹配到
                return None
        
        if len(matched_items) >= 2:
            # 获取友好的名称
            name = template.get('name', '')
            if not name or name.startswith('t_') or re.match(r't_.+_\d+$', name):
                category = template.get('category', '搭配')
                occasions = template.get('occasions', ['日常'])
                occasion = occasions[0]
                # 避免重复
                if category == occasion or category in occasion:
                    name = f"{occasion}搭配"
                else:
                    name = f"{occasion}{category}搭配"
            
            # 获取参考图
            image_path = self._get_outfit_image(template)
            
            return {
                "name": name,
                "items": matched_items,
                "item_details": matched_details,
                "style": template.get('category', '休闲'),
                "tips": template.get('tips', ''),
                "template_id": template.get('id'),
                "matched": True,
                "image_path": image_path
            }
        
        return None
    
    def _find_matching_item(
        self, 
        items: List[Dict], 
        keywords: List[str], 
        colors: Dict,
        preferred_colors: List[str] = None
    ) -> Optional[Dict]:
        """根据关键词和颜色找匹配单品"""
        target_colors = colors.get('primary', []) + colors.get('accent', [])
        
        # 如果有偏好颜色，优先搜索
        if preferred_colors:
            target_colors = preferred_colors + target_colors
        
        # 优先颜色匹配
        for item in items:
            item_color = item.get('color', '')
            if any(c in item_color for c in target_colors):
                return item
        
        # 其次关键词匹配
        for item in items:
            name = item.get('name', '')
            for kw in keywords:
                if kw in name:
                    return item
        
        # 随机选一个同品类
        return random.choice(items) if items else None
    
    def _format_template(self, template: Dict) -> Dict:
        """格式化模板输出"""
        items = []
        template_items = template.get('items', {})
        
        for cat, keywords in template_items.items():
            for kw in keywords:
                items.append(f"{kw}")
        
        return {
            "name": template.get('name', '推荐搭配'),
            "items": items,
            "style": template.get('category', '休闲'),
            "tips": template.get('tips', ''),
            "template_id": template.get('id'),
            "matched": False
        }
    
    def _get_outfit_image(self, template: Dict) -> Optional[str]:
        """获取搭配参考图"""
        # 返回模板对应的示例图片路径
        template_id = template.get('id', '')
        image_path = f"./assets/images/templates/{template_id}.jpg"
        if os.path.exists(image_path):
            return image_path
        return None
    
    def get_weather_adjustment(self, weather: Dict) -> Dict[str, Any]:
        """根据天气获取穿搭建议"""
        if not weather:
            return {"suggestion": "建议查看天气后获取更精准的搭配推荐"}
        
        temp = weather.get('temperature', 20)
        weather_code = weather.get('weather_code', 0)
        
        adjustments = {
            "need_outer": temp < 20,
            "need_coat": temp < 10,
            "need_umbrella": weather_code in [61, 63, 65, 80, 81, 82, 95, 96, 99],
            "suggestion": ""
        }
        
        if temp < 5:
            adjustments["suggestion"] = "天气寒冷，建议穿羽绒服或厚外套，注意保暖"
        elif temp < 15:
            adjustments["suggestion"] = "天气较凉，建议穿外套或针织开衫"
        elif temp < 25:
            adjustments["suggestion"] = "天气适宜，轻薄单品即可，可以叠穿增加层次感"
        else:
            adjustments["suggestion"] = "天气炎热，建议选择透气轻薄的面料"
        
        if adjustments["need_umbrella"]:
            adjustments["suggestion"] += "，今天可能下雨，记得带伞"
        
        return adjustments
    
    def analyze_wardrobe_coverage(self, member_id: str = None) -> Dict[str, Any]:
        """分析衣橱覆盖度"""
        items = self.db.get_all_items(member_id=member_id)
        
        # 按类别统计
        coverage = {
            "outer": {"count": 0, "status": "缺失"},
            "top": {"count": 0, "status": "缺失"},
            "bottom": {"count": 0, "status": "缺失"},
            "shoes": {"count": 0, "status": "缺失"},
            "accessory": {"count": 0, "status": "缺失"}
        }
        
        for item in items:
            cat = item.get('category', 'top')
            if cat in coverage:
                coverage[cat]["count"] += 1
        
        # 判断状态
        for cat, data in coverage.items():
            count = data["count"]
            if count >= 5:
                data["status"] = "充足"
            elif count >= 2:
                data["status"] = "基本"
            elif count >= 1:
                data["status"] = "不足"
            else:
                data["status"] = "缺失"
        
        # 计算整体覆盖度
        total = sum(d["count"] for d in coverage.values())
        categories_ok = sum(1 for d in coverage.values() if d["count"] >= 2)
        
        return {
            "coverage": coverage,
            "total_items": total,
            "categories_covered": categories_ok,
            "ready_for_outfit": categories_ok >= 3,
            "suggestions": self._get_coverage_suggestions(coverage)
        }
    
    def _get_coverage_suggestions(self, coverage: Dict) -> List[str]:
        """根据覆盖度给出建议"""
        suggestions = []
        
        # 按优先级排序
        priority = ['top', 'bottom', 'shoes', 'outer', 'accessory']
        
        for cat in priority:
            data = coverage.get(cat, {})
            if data.get("count", 0) < 2:
                cat_names = {
                    'outer': '外套',
                    'top': '上衣',
                    'bottom': '下装',
                    'shoes': '鞋子',
                    'accessory': '配饰'
                }
                suggestions.append(f"建议补充{cat_names.get(cat, cat)}")
        
        return suggestions[:3]