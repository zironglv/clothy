"""
初始化引导模块
引导新用户完成信息收集
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import json

from ..models.profile import (
    MemberProfile, BodyMeasurements, StyleProfile, ChildProfile,
    BodyType, SkinTone, StylePreference, BODY_TEMPLATES
)
from .member_manager import MemberManager


@dataclass
class InitStep:
    """初始化步骤"""
    key: str
    question: str
    description: str = ""
    options: List[Dict] = field(default_factory=list)
    input_type: str = "text"  # text/number/select/multi
    required: bool = False
    skip_keyword: str = "跳过"
    
    def to_dict(self) -> Dict:
        return {
            'key': self.key,
            'question': self.question,
            'description': self.description,
            'options': self.options,
            'input_type': self.input_type,
            'required': self.required,
            'skip_keyword': self.skip_keyword
        }


class Initializer:
    """初始化引导器
    
    引导用户完成：
    1. 基本信息（性别）
    2. 身材信息（身高、体重、三围等）
    3. 风格偏好（喜欢的风格、颜色）
    4. 儿童专属信息（如果是儿童）
    """
    
    # 基本信息步骤
    BASIC_STEPS = [
        InitStep(
            key="gender",
            question="请选择您的性别",
            input_type="select",
            options=[
                {"label": "👩 女生", "value": "female"},
                {"label": "👨 男生", "value": "male"}
            ],
            required=True
        ),
        InitStep(
            key="height",
            question="您的身高是多少？(cm)",
            description="例如：165",
            input_type="number",
            required=False
        ),
        InitStep(
            key="weight",
            question="您的体重是多少？(kg)",
            description="例如：52",
            input_type="number",
            required=False
        ),
    ]
    
    # 身材信息步骤
    BODY_STEPS = [
        InitStep(
            key="shoulder_width",
            question="肩宽是多少？(cm)",
            description="不填也没关系，可以之后补充",
            input_type="number"
        ),
        InitStep(
            key="bust",
            question="胸围是多少？(cm)",
            description="帮助我推荐更合身的上衣",
            input_type="number"
        ),
        InitStep(
            key="waist",
            question="腰围是多少？(cm)",
            description="帮助我推荐更合适的裤子/裙子",
            input_type="number"
        ),
        InitStep(
            key="hip",
            question="臀围是多少？(cm)",
            description="帮助我推荐更合身的下装",
            input_type="number"
        ),
    ]
    
    # 风格偏好步骤
    STYLE_STEPS = [
        InitStep(
            key="preferred_styles",
            question="您平时喜欢穿什么风格？",
            description="可以多选",
            input_type="multi",
            options=[
                {"label": "休闲日常", "value": "casual"},
                {"label": "商务通勤", "value": "business"},
                {"label": "甜美可爱", "value": "sweet"},
                {"label": "酷飒帅气", "value": "cool"},
                {"label": "简约基础", "value": "minimalist"},
                {"label": "优雅气质", "value": "elegant"},
                {"label": "复古文艺", "value": "vintage"},
                {"label": "运动活力", "value": "sporty"},
            ]
        ),
        InitStep(
            key="preferred_colors",
            question="喜欢的颜色有哪些？",
            description="如：黑色、白色、粉色...",
            input_type="text"
        ),
        InitStep(
            key="avoided_colors",
            question="有什么颜色不太穿吗？",
            description="我会尽量避免推荐这些颜色",
            input_type="text"
        ),
    ]
    
    # 儿童专属步骤
    CHILD_STEPS = [
        InitStep(
            key="birth_date",
            question="宝贝的出生日期是？",
            description="格式：2020-01-01",
            input_type="text"
        ),
        InitStep(
            key="school",
            question="宝贝在哪个学校/幼儿园？",
            description="了解学校是否有着装要求",
            input_type="text"
        ),
        InitStep(
            key="favorite_characters",
            question="宝贝喜欢的卡通形象？",
            description="如：艾莎、小猪佩奇、奥特曼...",
            input_type="text"
        ),
    ]
    
    def __init__(self, member_manager: MemberManager, db):
        """初始化引导器
        
        Args:
            member_manager: MemberManager 实例
            db: Database 实例
        """
        self.member_manager = member_manager
        self.db = db
        
        # 初始化状态存储
        self._init_states: Dict[str, Dict] = {}
    
    def get_init_state(self, member_id: str) -> Dict:
        """获取成员的初始化状态"""
        if member_id not in self._init_states:
            self._init_states[member_id] = {
                'current_phase': 'basic',
                'current_step': 0,
                'data': {},
                'started_at': datetime.now().isoformat()
            }
        return self._init_states[member_id]
    
    def start_init(self, member_id: str) -> Dict[str, Any]:
        """开始初始化流程
        
        Returns:
            包含第一个问题的字典
        """
        state = self.get_init_state(member_id)
        member = self.member_manager.get_member(member_id)
        
        # 根据成员类型选择步骤
        if member and member.relationship == "child":
            steps = self.BASIC_STEPS + self.CHILD_STEPS
        else:
            steps = self.BASIC_STEPS + self.BODY_STEPS + self.STYLE_STEPS
        
        state['steps'] = [s.to_dict() for s in steps]
        state['current_step'] = 0
        state['data'] = {'member_id': member_id}
        
        return self._get_current_question(state)
    
    def process_answer(self, member_id: str, answer: Any) -> Dict[str, Any]:
        """处理用户回答
        
        Args:
            member_id: 成员 ID
            answer: 用户回答
            
        Returns:
            包含下一个问题或完成状态
        """
        state = self.get_init_state(member_id)
        steps = state.get('steps', [])
        current_step = state.get('current_step', 0)
        
        if current_step >= len(steps):
            return self._complete_init(member_id, state)
        
        current = steps[current_step]
        
        # 检查是否跳过
        if answer == current.get('skip_keyword', '跳过') or answer in ['跳过', '不需要', '没有', '无']:
            # 不是必填，可以跳过
            if not current.get('required'):
                state['current_step'] += 1
                return self._get_next(state)
            else:
                return {
                    'status': 'error',
                    'message': '这个问题需要回答哦',
                    'step': current
                }
        
        # 验证并保存答案
        validated = self._validate_answer(current, answer)
        if validated.get('error'):
            return {
                'status': 'error',
                'message': validated['error'],
                'step': current
            }
        
        # 保存数据
        state['data'][current['key']] = validated['value']
        state['current_step'] += 1
        
        # 检查是否完成
        if state['current_step'] >= len(steps):
            return self._complete_init(member_id, state)
        
        return self._get_next(state)
    
    def _validate_answer(self, step: Dict, answer: Any) -> Dict:
        """验证答案"""
        input_type = step.get('input_type', 'text')
        
        if input_type == 'number':
            try:
                value = int(answer)
                return {'value': value}
            except (ValueError, TypeError):
                return {'error': '请输入一个数字'}
        
        elif input_type == 'select':
            options = [o['value'] for o in step.get('options', [])]
            if answer in options:
                return {'value': answer}
            return {'error': '请从选项中选择'}
        
        elif input_type == 'multi':
            # 多选，可以是列表或逗号分隔的字符串
            if isinstance(answer, list):
                return {'value': answer}
            elif isinstance(answer, str):
                values = [a.strip() for a in answer.split(',')]
                return {'value': values}
            return {'error': '格式错误'}
        
        else:  # text
            return {'value': str(answer)}
    
    def _get_current_question(self, state: Dict) -> Dict[str, Any]:
        """获取当前问题"""
        steps = state.get('steps', [])
        current_step = state.get('current_step', 0)
        
        if current_step >= len(steps):
            return {
                'status': 'complete',
                'message': '初始化已完成！'
            }
        
        step = steps[current_step]
        total = len(steps)
        
        return {
            'status': 'in_progress',
            'phase': state.get('current_phase', 'basic'),
            'step_number': current_step + 1,
            'total_steps': total,
            'progress': f"[{'■' * (current_step + 1)}{'□' * (total - current_step - 1)}]",
            'question': step['question'],
            'description': step.get('description', ''),
            'options': step.get('options', []),
            'input_type': step.get('input_type', 'text'),
            'skip_keyword': step.get('skip_keyword', '跳过')
        }
    
    def _get_next(self, state: Dict) -> Dict[str, Any]:
        """获取下一个问题"""
        return self._get_current_question(state)
    
    def _complete_init(self, member_id: str, state: Dict) -> Dict[str, Any]:
        """完成初始化"""
        data = state.get('data', {})
        
        # 构建画像
        profile_data = self._build_profile_data(data)
        
        # 更新数据库
        self.member_manager.update_profile(member_id, profile_data)
        self.member_manager.set_member_initialized(member_id)
        
        # 清理状态
        if member_id in self._init_states:
            del self._init_states[member_id]
        
        # 获取成员信息
        member = self.member_manager.get_member(member_id)
        
        return {
            'status': 'complete',
            'message': '初始化完成！让我来了解一下您的衣橱吧～',
            'profile': profile_data,
            'member': member.to_dict() if member else None,
            'next_actions': [
                '拍照添加第一件衣服',
                '从淘宝导入已购商品',
                '查看搭配建议'
            ]
        }
    
    def _build_profile_data(self, data: Dict) -> Dict:
        """构建画像数据"""
        profile = {
            'gender': data.get('gender'),
            'body': {
                'height': data.get('height'),
                'weight': data.get('weight'),
                'shoulder_width': data.get('shoulder_width'),
                'bust': data.get('bust'),
                'waist': data.get('waist'),
                'hip': data.get('hip'),
            },
            'style': {
                'preferred_styles': data.get('preferred_styles', []),
                'preferred_colors': self._parse_colors(data.get('preferred_colors', '')),
                'avoided_colors': self._parse_colors(data.get('avoided_colors', '')),
            }
        }
        
        # 儿童专属信息
        if data.get('birth_date'):
            profile['child'] = {
                'birth_date': data.get('birth_date'),
                'school': data.get('school'),
                'favorite_characters': self._parse_list(data.get('favorite_characters', ''))
            }
        
        return profile
    
    def _parse_colors(self, text: str) -> List[str]:
        """解析颜色列表"""
        if not text:
            return []
        
        # 常见颜色映射
        color_map = {
            '黑': 'black', '黑色': 'black',
            '白': 'white', '白色': 'white',
            '灰': 'gray', '灰色': 'gray',
            '米': 'beige', '米色': 'beige', '杏色': 'beige',
            '蓝': 'blue', '蓝色': 'blue',
            '粉': 'pink', '粉色': 'pink', '粉红': 'pink',
            '红': 'red', '红色': 'red',
            '绿': 'green', '绿色': 'green',
            '黄': 'yellow', '黄色': 'yellow',
            '紫': 'purple', '紫色': 'purple',
            '棕': 'brown', '棕色': 'brown', '咖啡色': 'brown',
        }
        
        colors = []
        for key, value in color_map.items():
            if key in text:
                colors.append(value)
        
        return colors
    
    def _parse_list(self, text: str) -> List[str]:
        """解析列表"""
        if not text:
            return []
        
        # 支持逗号、顿号、空格分隔
        import re
        items = re.split(r'[,，、\s]+', text)
        return [item.strip() for item in items if item.strip()]
    
    def cancel_init(self, member_id: str):
        """取消初始化"""
        if member_id in self._init_states:
            del self._init_states[member_id]
    
    def is_in_init(self, member_id: str) -> bool:
        """检查是否在初始化中"""
        return member_id in self._init_states


# 风格报告生成器
class StyleReportGenerator:
    """风格报告生成器
    
    根据用户画像生成个性化风格报告
    """
    
    @classmethod
    def generate_report(cls, profile: MemberProfile) -> Dict[str, Any]:
        """生成风格报告"""
        report = {
            'body_type_analysis': cls._analyze_body_type(profile),
            'color_analysis': cls._analyze_colors(profile),
            'style_analysis': cls._analyze_style(profile),
            'recommendations': cls._get_recommendations(profile),
            'shopping_tips': cls._get_shopping_tips(profile)
        }
        
        return report
    
    @classmethod
    def _analyze_body_type(cls, profile: MemberProfile) -> Dict:
        """分析身材类型"""
        body_type = profile.body_type
        
        descriptions = {
            BodyType.HOURGLASS: {
                'name': 'X型/沙漏型',
                'description': '肩臀相近，腰部纤细，是理想的身材类型',
                'tips': '几乎适合所有款式，可以大胆尝试各种风格'
            },
            BodyType.PEAR: {
                'name': 'A型/梨型',
                'description': '臀围大于肩围，下半身较丰满',
                'tips': '适合上身亮色、下身深色的搭配，避免紧身裤'
            },
            BodyType.APPLE: {
                'name': 'O型/苹果型',
                'description': '腰围较宽，上半身较丰满',
                'tips': '适合V领、A字裙，避免紧身和过于宽松的款式'
            },
            BodyType.RECTANGLE: {
                'name': 'H型/矩型',
                'description': '肩腰臀差距不大，身材匀称',
                'tips': '适合用腰带、层次搭配来制造曲线感'
            },
            BodyType.INVERTED_TRIANGLE: {
                'name': 'Y型/倒三角',
                'description': '肩宽大于臀围，上半身较壮',
                'tips': '适合下身穿亮色或有图案的款式，避免垫肩'
            }
        }
        
        if body_type:
            return descriptions.get(body_type, {
                'name': '未知',
                'description': '数据不足，无法判断',
                'tips': '建议补充更多身材数据'
            })
        
        return {
            'name': '待分析',
            'description': '缺少身材数据',
            'tips': '完善身材信息后可以获取更精准的建议'
        }
    
    @classmethod
    def _analyze_colors(cls, profile: MemberProfile) -> Dict:
        """分析颜色偏好"""
        preferred = profile.style.preferred_colors
        avoided = profile.style.avoided_colors
        skin_tone = profile.skin_tone
        
        # 根据肤色推荐
        skin_recommendations = {
            SkinTone.COOL: ['白色', '灰色', '蓝色', '紫色', '粉色'],
            SkinTone.WARM: ['米色', '橙色', '黄色', '棕色', '绿色'],
            SkinTone.NEUTRAL: ['黑白灰', '蓝色', '绿色', '米色']
        }
        
        return {
            'preferred': preferred,
            'avoided': avoided,
            'skin_tone_recommendations': skin_recommendations.get(skin_tone, [])
        }
    
    @classmethod
    def _analyze_style(cls, profile: MemberProfile) -> Dict:
        """分析风格偏好"""
        styles = profile.style.preferred_styles
        
        style_descriptions = {
            StylePreference.CASUAL: '休闲日常风 - 舒适自在，适合日常',
            StylePreference.BUSINESS: '商务通勤风 - 干练利落，适合职场',
            StylePreference.SWEET: '甜美可爱风 - 温柔俏皮，少女感',
            StylePreference.COOL: '酷飒帅气风 - 个性张扬，街头感',
            StylePreference.MINIMALIST: '极简风 - 简约大方，经典百搭',
            StylePreference.ELEGANT: '优雅气质风 - 知性大方，高级感',
            StylePreference.VINTAGE: '复古文艺风 - 怀旧经典，独特魅力',
            StylePreference.SPORTY: '运动活力风 - 青春阳光，活力满满'
        }
        
        return {
            'styles': [style_descriptions.get(s, s.value) for s in styles],
            'primary_style': styles[0].value if styles else 'casual'
        }
    
    @classmethod
    def _get_recommendations(cls, profile: MemberProfile) -> List[str]:
        """获取穿搭建议"""
        recommendations = []
        
        body_type = profile.body_type
        if body_type == BodyType.PEAR:
            recommendations.append("上身选择亮色或带图案的款式，下身选择深色")
            recommendations.append("A字裙是你的好朋友，可以平衡身材比例")
        elif body_type == BodyType.APPLE:
            recommendations.append("V领可以拉长颈部线条，显瘦显高")
            recommendations.append("避免腰部有装饰的衣服，选择高腰线款式")
        elif body_type == BodyType.HOURGLASS:
            recommendations.append("可以大胆尝试各种风格，你的身材很完美")
            recommendations.append("腰带是点睛之笔，可以突出腰线")
        
        return recommendations
    
    @classmethod
    def _get_shopping_tips(cls, profile: MemberProfile) -> List[str]:
        """获取购物建议"""
        tips = []
        
        # 根据衣橱缺失推荐
        # 这里可以接入实际衣橱数据
        
        tips.append("建议补充基础款单品，如白衬衫、黑裤子")
        tips.append("可以尝试添加一件亮色单品作为点缀")
        
        if profile.style.preferred_colors:
            tips.append(f"您喜欢{','.join(profile.style.preferred_colors[:3])}色，可以多关注这些颜色的单品")
        
        return tips