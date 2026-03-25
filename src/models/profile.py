"""
用户画像模型
管理身材信息、风格偏好等
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime, date


class BodyType(str, Enum):
    """身材类型"""
    HOURGLASS = "hourglass"  # X型/沙漏型
    PEAR = "pear"           # A型/梨型
    APPLE = "apple"         # O型/苹果型
    RECTANGLE = "rectangle"  # H型/矩型
    INVERTED_TRIANGLE = "inverted_triangle"  # Y型/倒三角


class SkinTone(str, Enum):
    """肤色"""
    COOL = "cool"      # 冷色调
    WARM = "warm"      # 暖色调
    NEUTRAL = "neutral"  # 中性


class StylePreference(str, Enum):
    """风格偏好"""
    CASUAL = "casual"        # 休闲
    BUSINESS = "business"    # 商务
    SWEET = "sweet"          # 甜美
    COOL = "cool"            # 酷飒
    MINIMALIST = "minimalist"  # 极简
    VINTAGE = "vintage"      # 复古
    SPORTY = "sporty"        # 运动
    ELEGANT = "elegant"      # 优雅


@dataclass
class BodyMeasurements:
    """身材数据"""
    height: Optional[int] = None      # 身高 cm
    weight: Optional[int] = None      # 体重 kg
    shoulder_width: Optional[int] = None  # 肩宽 cm
    bust: Optional[int] = None        # 胸围 cm
    waist: Optional[int] = None       # 腰围 cm
    hip: Optional[int] = None         # 臀围 cm
    inseam: Optional[int] = None      # 腿长/内长 cm
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BodyMeasurements':
        return cls(
            height=data.get('height'),
            weight=data.get('weight'),
            shoulder_width=data.get('shoulder_width'),
            bust=data.get('bust'),
            waist=data.get('waist'),
            hip=data.get('hip'),
            inseam=data.get('inseam')
        )
    
    def calculate_body_type(self) -> Optional[BodyType]:
        """根据三围计算身材类型"""
        if not all([self.bust, self.waist, self.hip]):
            return None
        
        bust_waist_diff = self.bust - self.waist
        hip_waist_diff = self.hip - self.waist
        bust_hip_diff = abs(self.bust - self.hip)
        
        # X型：胸腰差>15，臀腰差>15，胸臀差<5
        if bust_waist_diff > 15 and hip_waist_diff > 15 and bust_hip_diff < 5:
            return BodyType.HOURGLASS
        
        # A型：臀围明显大于胸围（>5cm）
        if self.hip - self.bust > 5:
            return BodyType.PEAR
        
        # O型：腰围大于等于胸围或臀围的80%
        if self.waist >= self.bust * 0.8 or self.waist >= self.hip * 0.8:
            return BodyType.APPLE
        
        # Y型：肩宽/胸围明显大于臀围
        if self.bust - self.hip > 5:
            return BodyType.INVERTED_TRIANGLE
        
        # H型：三围差距不大
        return BodyType.RECTANGLE


@dataclass
class StyleProfile:
    """风格画像"""
    preferred_styles: List[StylePreference] = field(default_factory=list)
    avoided_styles: List[StylePreference] = field(default_factory=list)
    preferred_colors: List[str] = field(default_factory=list)
    avoided_colors: List[str] = field(default_factory=list)
    preferred_patterns: List[str] = field(default_factory=list)  # 纯色、条纹、格子、印花
    preferred_brands: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'preferred_styles': [s.value for s in self.preferred_styles],
            'avoided_styles': [s.value for s in self.avoided_styles],
            'preferred_colors': self.preferred_colors,
            'avoided_colors': self.avoided_colors,
            'preferred_patterns': self.preferred_patterns,
            'preferred_brands': self.preferred_brands
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'StyleProfile':
        return cls(
            preferred_styles=[StylePreference(s) for s in data.get('preferred_styles', [])],
            avoided_styles=[StylePreference(s) for s in data.get('avoided_styles', [])],
            preferred_colors=data.get('preferred_colors', []),
            avoided_colors=data.get('avoided_colors', []),
            preferred_patterns=data.get('preferred_patterns', []),
            preferred_brands=data.get('preferred_brands', [])
        )


@dataclass
class ChildProfile:
    """儿童专属画像"""
    birth_date: Optional[date] = None     # 出生日期
    school: Optional[str] = None           # 学校
    grade: Optional[str] = None           # 年级
    uniform_info: Optional[Dict] = None    # 校服信息
    size_preference: Optional[str] = None  # 尺码偏好（如"买大一号"）
    favorite_characters: List[str] = field(default_factory=list)  # 喜欢的卡通形象
    activities: List[str] = field(default_factory=list)  # 课外活动（舞蹈、画画等）
    special_needs: Optional[str] = None    # 特殊需求（过敏、敏感等）
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'school': self.school,
            'grade': self.grade,
            'uniform_info': self.uniform_info,
            'size_preference': self.size_preference,
            'favorite_characters': self.favorite_characters,
            'activities': self.activities,
            'special_needs': self.special_needs
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ChildProfile':
        birth_date = None
        if data.get('birth_date'):
            try:
                birth_date = date.fromisoformat(data['birth_date'])
            except:
                pass
        
        return cls(
            birth_date=birth_date,
            school=data.get('school'),
            grade=data.get('grade'),
            uniform_info=data.get('uniform_info'),
            size_preference=data.get('size_preference'),
            favorite_characters=data.get('favorite_characters', []),
            activities=data.get('activities', []),
            special_needs=data.get('special_needs')
        )
    
    @property
    def age(self) -> Optional[int]:
        """计算年龄"""
        if not self.birth_date:
            return None
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )


@dataclass
class MemberProfile:
    """完整成员画像"""
    member_id: str
    
    # 基本信息
    name: str
    gender: Optional[str] = None  # male/female
    relationship: str = "self"    # self/spouse/child/parent/other
    
    # 身材画像
    body: BodyMeasurements = field(default_factory=BodyMeasurements)
    body_type: Optional[BodyType] = None
    skin_tone: Optional[SkinTone] = None
    
    # 风格画像
    style: StyleProfile = field(default_factory=StyleProfile)
    
    # 儿童画像（仅儿童使用）
    child: Optional[ChildProfile] = None
    
    # 其他信息
    occupation: Optional[str] = None  # 职业
    lifestyle: Optional[str] = None   # 生活方式（通勤、居家、运动等）
    
    # 时间戳
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'member_id': self.member_id,
            'name': self.name,
            'gender': self.gender,
            'relationship': self.relationship,
            'body': self.body.to_dict(),
            'body_type': self.body_type.value if self.body_type else None,
            'skin_tone': self.skin_tone.value if self.skin_tone else None,
            'style': self.style.to_dict(),
            'child': self.child.to_dict() if self.child else None,
            'occupation': self.occupation,
            'lifestyle': self.lifestyle,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemberProfile':
        profile = cls(
            member_id=data['member_id'],
            name=data['name'],
            gender=data.get('gender'),
            relationship=data.get('relationship', 'self'),
            body=BodyMeasurements.from_dict(data.get('body', {})),
            body_type=BodyType(data['body_type']) if data.get('body_type') else None,
            skin_tone=SkinTone(data['skin_tone']) if data.get('skin_tone') else None,
            style=StyleProfile.from_dict(data.get('style', {})),
            occupation=data.get('occupation'),
            lifestyle=data.get('lifestyle'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else datetime.now()
        )
        
        if data.get('child'):
            profile.child = ChildProfile.from_dict(data['child'])
        
        return profile
    
    def update_body_type(self):
        """更新身材类型"""
        self.body_type = self.body.calculate_body_type()
    
    def is_child(self) -> bool:
        """是否为儿童"""
        return self.relationship == "child"
    
    def get_age(self) -> Optional[int]:
        """获取年龄（儿童返回实际年龄，成人返回None）"""
        if self.child:
            return self.child.age
        return None


# 预设身材模板
BODY_TEMPLATES = {
    "female_petite": {
        "description": "女生 - 娇小",
        "body": BodyMeasurements(
            height=155, weight=45, shoulder_width=36,
            bust=80, waist=62, hip=84
        )
    },
    "female_average": {
        "description": "女生 - 标准",
        "body": BodyMeasurements(
            height=163, weight=52, shoulder_width=38,
            bust=84, waist=66, hip=90
        )
    },
    "female_tall": {
        "description": "女生 - 高挑",
        "body": BodyMeasurements(
            height=170, weight=58, shoulder_width=40,
            bust=86, waist=68, hip=94
        )
    },
    "male_average": {
        "description": "男生 - 标准",
        "body": BodyMeasurements(
            height=175, weight=70, shoulder_width=44,
            bust=90, waist=80, hip=92
        )
    },
    "child_boy_5": {
        "description": "男童 - 5岁",
        "body": BodyMeasurements(
            height=110, weight=20, shoulder_width=28,
            bust=56, waist=52, hip=58
        )
    },
    "child_girl_5": {
        "description": "女童 - 5岁",
        "body": BodyMeasurements(
            height=108, weight=18, shoulder_width=26,
            bust=54, waist=50, hip=56
        )
    }
}