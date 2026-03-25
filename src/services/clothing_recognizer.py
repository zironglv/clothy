"""
AI 识别模块
使用多模态模型识别服装属性
"""

import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import os


@dataclass
class ClothingAttributes:
    """服装属性"""
    category: str          # outer/top/bottom/shoes/accessory
    subcategory: str       # 子品类（如 T恤、衬衫、牛仔裤等）
    color: str             # 主颜色
    secondary_color: str   # 次颜色
    pattern: str           # 图案（纯色、条纹、格子、印花等）
    style: str             # 风格（casual/business/sweet等）
    season: str            # 季节（spring/summer/autumn/winter/all_season）
    material: str          # 材质
    fit: str               # 版型（修身/宽松/常规）
    length: str            # 长度（短款/常规/长款）
    sleeve_length: str     # 袖长（无袖/短袖/中袖/长袖）
    neckline: str          # 领型
    gender: str            # 性别（male/female/unisex）
    age_group: str         # 年龄段（adult/child/teen）
    
    # 置信度
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'category': self.category,
            'subcategory': self.subcategory,
            'color': self.color,
            'secondary_color': self.secondary_color,
            'pattern': self.pattern,
            'style': self.style,
            'season': self.season,
            'material': self.material,
            'fit': self.fit,
            'length': self.length,
            'sleeve_length': self.sleeve_length,
            'neckline': self.neckline,
            'gender': self.gender,
            'age_group': self.age_group,
            'confidence': self.confidence
        }


class ClothingRecognizer:
    """服装识别器
    
    使用多模态模型识别服装图片的属性
    支持降级策略：
    1. 多模态模型识别（qwen-vl-plus 等）
    2. 本地图像分析（PIL）
    3. 标题关键词分析
    """
    
    # 品类定义
    CATEGORIES = {
        'outer': {
            'name': '外套',
            'subcategories': ['羽绒服', '大衣', '风衣', '夹克', '西装', '皮衣', '棉服', '棒球服', '毛呢外套', '针织开衫']
        },
        'top': {
            'name': '上装',
            'subcategories': ['T恤', '衬衫', '毛衣', '针织衫', '卫衣', '吊带', '背心', '打底衫', '雪纺衫', 'POLO衫']
        },
        'bottom': {
            'name': '下装',
            'subcategories': ['牛仔裤', '休闲裤', '短裤', '半身裙', '连衣裙', '西裤', '运动裤', '打底裤', '阔腿裤', '半裙']
        },
        'shoes': {
            'name': '鞋子',
            'subcategories': ['高跟鞋', '平底鞋', '运动鞋', '凉鞋', '拖鞋', '帆布鞋', '板鞋', '老爹鞋', '马丁靴', '短靴']
        },
        'accessory': {
            'name': '配饰',
            'subcategories': ['手提包', '单肩包', '双肩包', '帽子', '围巾', '手套', '腰带', '项链', '耳环', '手表']
        }
    }
    
    # 颜色映射
    COLORS = {
        'black': '黑色',
        'white': '白色',
        'gray': '灰色',
        'beige': '米色',
        'blue': '蓝色',
        'pink': '粉色',
        'red': '红色',
        'green': '绿色',
        'yellow': '黄色',
        'purple': '紫色',
        'brown': '棕色',
        'orange': '橙色',
        'navy': '藏青色',
        'khaki': '卡其色',
        'cream': '奶油色',
        'multicolor': '多色/拼色'
    }
    
    # 风格映射
    STYLES = {
        'casual': '休闲日常',
        'business': '商务通勤',
        'sweet': '甜美可爱',
        'cool': '酷飒帅气',
        'minimalist': '简约基础',
        'elegant': '优雅气质',
        'vintage': '复古文艺',
        'sporty': '运动活力',
        'chinese': '国风汉服',
        'korean': '韩系清新'
    }
    
    def __init__(self, model_client=None):
        """初始化识别器
        
        Args:
            model_client: 多模态模型客户端（可选）
        """
        self.model_client = model_client
    
    async def recognize_from_image(self, image_path: str) -> ClothingAttributes:
        """从图片识别服装属性
        
        Args:
            image_path: 图片路径
            
        Returns:
            服装属性
        """
        # 策略1：使用多模态模型
        if self.model_client:
            try:
                result = await self._recognize_with_vision_model(image_path)
                if result and result.confidence > 0.7:
                    return result
            except Exception as e:
                print(f"多模态识别失败: {e}")
        
        # 策略2：本地图像分析
        try:
            result = self._recognize_with_local_analysis(image_path)
            if result:
                return result
        except Exception as e:
            print(f"本地分析失败: {e}")
        
        # 策略3：返回默认值
        return ClothingAttributes(
            category='unknown',
            subcategory='',
            color='未知',
            secondary_color='',
            pattern='未知',
            style='casual',
            season='all_season',
            material='',
            fit='',
            length='',
            sleeve_length='',
            neckline='',
            gender='unisex',
            age_group='adult',
            confidence=0.0
        )
    
    async def recognize_from_url(self, image_url: str) -> ClothingAttributes:
        """从URL识别服装属性"""
        # 先下载图片，再识别
        # 这里简化处理，实际应该下载到本地
        return await self.recognize_from_image(image_url)
    
    def recognize_from_title(self, title: str) -> ClothingAttributes:
        """从商品标题识别服装属性
        
        Args:
            title: 商品标题
            
        Returns:
            服装属性
        """
        title_lower = title.lower()
        
        # 识别品类
        category, subcategory = self._detect_category_from_text(title_lower)
        
        # 识别颜色
        color = self._detect_color_from_text(title)
        
        # 识别风格
        style = self._detect_style_from_text(title)
        
        # 识别季节
        season = self._detect_season_from_text(title)
        
        return ClothingAttributes(
            category=category,
            subcategory=subcategory,
            color=color,
            secondary_color='',
            pattern=self._detect_pattern_from_text(title),
            style=style,
            season=season,
            material=self._detect_material_from_text(title),
            fit=self._detect_fit_from_text(title),
            length='',
            sleeve_length=self._detect_sleeve_from_text(title),
            neckline=self._detect_neckline_from_text(title),
            gender=self._detect_gender_from_text(title),
            age_group='adult',
            confidence=0.6
        )
    
    async def _recognize_with_vision_model(self, image_path: str) -> Optional[ClothingAttributes]:
        """使用视觉模型识别"""
        if not self.model_client:
            return None
        
        # 构建提示词
        prompt = """请分析这张服装图片，返回以下属性的JSON格式：

{
  "category": "品类（outer/top/bottom/shoes/accessory）",
  "subcategory": "子品类",
  "color": "主颜色",
  "secondary_color": "次颜色",
  "pattern": "图案（纯色/条纹/格子/印花/碎花等）",
  "style": "风格（casual/business/sweet/cool/minimalist/elegant等）",
  "season": "适合季节（spring/summer/autumn/winter/all_season）",
  "material": "材质",
  "fit": "版型（修身/宽松/常规）",
  "length": "长度（短款/常规/长款）",
  "sleeve_length": "袖长（无袖/短袖/中袖/长袖）",
  "neckline": "领型",
  "gender": "适合性别（male/female/unisex）"
}

只返回JSON，不要其他内容。"""
        
        try:
            # 调用模型
            # 这里是伪代码，实际需要根据具体的模型客户端实现
            # response = await self.model_client.chat_with_image(image_path, prompt)
            # result = json.loads(response)
            
            # 模拟返回
            result = {
                'category': 'top',
                'subcategory': 'T恤',
                'color': '白色',
                'style': 'casual',
                'season': 'all_season'
            }
            
            return ClothingAttributes(
                category=result.get('category', 'unknown'),
                subcategory=result.get('subcategory', ''),
                color=result.get('color', '未知'),
                secondary_color=result.get('secondary_color', ''),
                pattern=result.get('pattern', ''),
                style=result.get('style', 'casual'),
                season=result.get('season', 'all_season'),
                material=result.get('material', ''),
                fit=result.get('fit', ''),
                length=result.get('length', ''),
                sleeve_length=result.get('sleeve_length', ''),
                neckline=result.get('neckline', ''),
                gender=result.get('gender', 'unisex'),
                age_group='adult',
                confidence=0.9
            )
            
        except Exception as e:
            print(f"视觉模型调用失败: {e}")
            return None
    
    def _recognize_with_local_analysis(self, image_path: str) -> Optional[ClothingAttributes]:
        """使用本地图像分析"""
        try:
            from PIL import Image
            import numpy as np
            
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # 分析主颜色
            color = self._extract_dominant_color(img_array)
            
            return ClothingAttributes(
                category='unknown',
                subcategory='',
                color=color,
                secondary_color='',
                pattern='',
                style='casual',
                season='all_season',
                material='',
                fit='',
                length='',
                sleeve_length='',
                neckline='',
                gender='unisex',
                age_group='adult',
                confidence=0.4
            )
            
        except Exception as e:
            print(f"本地分析失败: {e}")
            return None
    
    def _extract_dominant_color(self, img_array) -> str:
        """提取主颜色"""
        # 简化实现，实际可以用更复杂的颜色聚类
        try:
            import numpy as np
            
            # 重塑为像素列表
            pixels = img_array.reshape(-1, img_array.shape[-1])
            
            # 计算平均颜色
            avg_color = np.mean(pixels, axis=0)
            
            # 映射到颜色名称
            r, g, b = avg_color[:3]
            
            if r < 30 and g < 30 and b < 30:
                return '黑色'
            elif r > 225 and g > 225 and b > 225:
                return '白色'
            elif r > 200 and g < 100 and b < 100:
                return '红色'
            elif r < 100 and g < 100 and b > 200:
                return '蓝色'
            elif r < 100 and g > 200 and b < 100:
                return '绿色'
            elif r > 200 and g > 200 and b < 100:
                return '黄色'
            elif r > 200 and g < 200 and b > 100:
                return '粉色'
            elif abs(r - g) < 30 and abs(g - b) < 30:
                if r < 128:
                    return '灰色'
                else:
                    return '米色'
            
            return '未知'
            
        except:
            return '未知'
    
    # ============ 文本分析辅助方法 ============
    
    def _detect_category_from_text(self, text: str) -> tuple:
        """从文本检测品类"""
        # 外套
        outer_keywords = ['羽绒服', '大衣', '风衣', '夹克', '西装', '皮衣', '棉服', '棒球服', '外套']
        for kw in outer_keywords:
            if kw in text:
                return 'outer', kw
        
        # 上装
        top_keywords = ['t恤', 't-shirt', '衬衫', '毛衣', '针织', '卫衣', '吊带', '背心', '打底', '雪纺', 'polo']
        for kw in top_keywords:
            if kw in text:
                if '衫' in text:
                    return 'top', '衬衫'
                elif '毛衣' in text or '针织' in text:
                    return 'top', '毛衣'
                elif '卫衣' in text:
                    return 'top', '卫衣'
                return 'top', kw
        
        # 下装
        bottom_keywords = ['裤', '裙', '牛仔', '短裤', '半身裙', '连衣裙', '阔腿', '运动裤']
        for kw in bottom_keywords:
            if kw in text:
                if '裙' in text:
                    return 'bottom', '连衣裙' if '连衣' in text else '半身裙'
                return 'bottom', '裤子'
        
        # 鞋子
        shoes_keywords = ['鞋', '靴', '高跟鞋', '运动鞋', '凉鞋', '帆布', '板鞋', '老爹', '马丁']
        for kw in shoes_keywords:
            if kw in text:
                return 'shoes', kw
        
        # 配饰
        acc_keywords = ['包', '帽子', '围巾', '手套', '腰带', '项链', '耳环', '手表']
        for kw in acc_keywords:
            if kw in text:
                return 'accessory', kw
        
        return 'top', ''
    
    def _detect_color_from_text(self, text: str) -> str:
        """从文本检测颜色"""
        color_keywords = {
            '黑色': ['黑色', '黑', '纯黑', '炭黑'],
            '白色': ['白色', '白', '纯白', '米白', '奶白'],
            '灰色': ['灰色', '灰', '浅灰', '深灰'],
            '米色': ['米色', '杏色', '奶茶', '卡其', '驼色'],
            '蓝色': ['蓝色', '蓝', '天蓝', '深蓝', '藏蓝', '牛仔'],
            '粉色': ['粉色', '粉', '粉红', '浅粉'],
            '红色': ['红色', '红', '大红', '酒红'],
            '绿色': ['绿色', '绿', '墨绿', '军绿'],
            '黄色': ['黄色', '黄', '姜黄', '鹅黄'],
        }
        
        for color, keywords in color_keywords.items():
            for kw in keywords:
                if kw in text:
                    return color
        
        return '未知'
    
    def _detect_style_from_text(self, text: str) -> str:
        """从文本检测风格"""
        style_keywords = {
            'casual': ['休闲', '日常', '舒适', '宽松', '百搭'],
            'business': ['商务', '职业', '通勤', '正装', '西装'],
            'sweet': ['甜美', '可爱', '少女', '公主'],
            'cool': ['酷', '帅气', '街头', '个性', '朋克'],
            'minimalist': ['简约', '基础', '纯色', '极简'],
            'elegant': ['优雅', '气质', '淑女', '知性'],
            'sporty': ['运动', '健身', '瑜伽'],
            'vintage': ['复古', '文艺', '民族'],
        }
        
        for style, keywords in style_keywords.items():
            for kw in keywords:
                if kw in text:
                    return style
        
        return 'casual'
    
    def _detect_season_from_text(self, text: str) -> str:
        """从文本检测季节"""
        if any(kw in text for kw in ['夏季', '夏天', '短袖', '薄款', '透气', '冰丝']):
            return 'summer'
        if any(kw in text for kw in ['冬季', '冬天', '加绒', '保暖', '羽绒', '毛呢']):
            return 'winter'
        if any(kw in text for kw in ['春秋', '薄外套']):
            return 'spring_autumn'
        return 'all_season'
    
    def _detect_pattern_from_text(self, text: str) -> str:
        """检测图案"""
        if '条纹' in text:
            return '条纹'
        if '格子' in text or '格纹' in text:
            return '格子'
        if '印花' in text or '碎花' in text:
            return '印花'
        if '纯色' in text:
            return '纯色'
        return ''
    
    def _detect_material_from_text(self, text: str) -> str:
        """检测材质"""
        materials = ['棉', '麻', '丝', '羊毛', '羊绒', '涤纶', '雪纺', '牛仔', '皮革', '人造革']
        for m in materials:
            if m in text:
                return m
        return ''
    
    def _detect_fit_from_text(self, text: str) -> str:
        """检测版型"""
        if '修身' in text or '紧身' in text:
            return '修身'
        if '宽松' in text or 'oversize' in text.lower():
            return '宽松'
        return '常规'
    
    def _detect_sleeve_from_text(self, text: str) -> str:
        """检测袖长"""
        if '无袖' in text or '吊带' in text or '背心' in text:
            return '无袖'
        if '短袖' in text:
            return '短袖'
        if '中袖' in text or '七分袖' in text:
            return '中袖'
        if '长袖' in text:
            return '长袖'
        return ''
    
    def _detect_neckline_from_text(self, text: str) -> str:
        """检测领型"""
        necklines = {
            '圆领': ['圆领', '圆领'],
            'V领': ['v领', 'V领'],
            '翻领': ['翻领', '衬衫领'],
            '高领': ['高领', '立领'],
            '一字领': ['一字领', '一字肩'],
            '方领': ['方领'],
        }
        for name, keywords in necklines.items():
            for kw in keywords:
                if kw in text:
                    return name
        return ''
    
    def _detect_gender_from_text(self, text: str) -> str:
        """检测适合性别"""
        if any(kw in text for kw in ['男款', '男士', '男装', 'men']):
            return 'male'
        if any(kw in text for kw in ['女款', '女士', '女装', 'women', '女']):
            return 'female'
        if any(kw in text for kw in ['童装', '儿童', '小孩', '宝宝']):
            return 'child'
        return 'unisex'