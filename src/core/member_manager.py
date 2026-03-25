"""
家庭成员管理模块
管理多人衣橱的核心模块
"""

import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict

from ..models.profile import MemberProfile, BodyMeasurements, StyleProfile, ChildProfile, BodyType


@dataclass
class FamilyMember:
    """家庭成员"""
    id: str
    family_id: str
    name: str
    relationship: str  # self/spouse/child/parent/other
    avatar: str        # emoji avatar
    gender: Optional[str] = None
    is_initialized: bool = False
    created_at: str = ""
    updated_at: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'FamilyMember':
        return cls(
            id=data['id'],
            family_id=data['family_id'],
            name=data['name'],
            relationship=data['relationship'],
            avatar=data.get('avatar', '👤'),
            gender=data.get('gender'),
            is_initialized=data.get('is_initialized', False),
            created_at=data.get('created_at', ''),
            updated_at=data.get('updated_at', '')
        )


class MemberManager:
    """家庭成员管理器"""
    
    # 关系类型到头像的映射
    RELATIONSHIP_AVATARS = {
        "self": "👩",
        "spouse": "👨", 
        "child": "👧",
        "parent": "👴",
        "other": "👤"
    }
    
    # 关系类型到称呼的映射（用于识别用户输入）
    RELATIONSHIP_KEYWORDS = {
        "self": ["我", "自己", "本人的", "我的"],
        "spouse": ["老公", "老婆", "丈夫", "妻子", "配偶", "先生", "太太"],
        "child": ["小孩", "孩子", "儿子", "女儿", "宝宝", "宝贝", "娃", "小朋友"],
        "parent": ["爸爸", "妈妈", "父亲", "母亲", "父母", "老爸", "老妈"]
    }
    
    def __init__(self, db):
        """初始化成员管理器
        
        Args:
            db: Database 实例
        """
        self.db = db
    
    def get_family_id(self) -> str:
        """获取或创建家庭ID"""
        family = self.db.get_family()
        if family:
            return family['id']
        return self.db.create_family()
    
    def get_all_members(self) -> List[FamilyMember]:
        """获取所有家庭成员"""
        members_data = self.db.get_all_members()
        return [FamilyMember.from_dict(m) for m in members_data]
    
    def get_member(self, member_id: str) -> Optional[FamilyMember]:
        """获取指定成员"""
        data = self.db.get_member(member_id)
        if data:
            return FamilyMember.from_dict(data)
        return None
    
    def get_member_by_name(self, name: str) -> Optional[FamilyMember]:
        """通过名称获取成员"""
        members = self.get_all_members()
        for m in members:
            if m.name == name:
                return m
        return None
    
    def add_member(
        self, 
        name: str, 
        relationship: str,
        gender: Optional[str] = None
    ) -> FamilyMember:
        """添加家庭成员
        
        Args:
            name: 成员名称（如"老公"、"小明"）
            relationship: 关系类型
            gender: 性别（male/female）
            
        Returns:
            新创建的成员
        """
        family_id = self.get_family_id()
        member_id = f"member_{uuid.uuid4().hex[:8]}"
        
        # 获取对应头像
        avatar = self.RELATIONSHIP_AVATARS.get(relationship, "👤")
        if gender == "male":
            if relationship == "child":
                avatar = "👦"
        elif gender == "female":
            if relationship == "self":
                avatar = "👩"
            elif relationship == "spouse":
                avatar = "👩"
        
        now = datetime.now().isoformat()
        member = FamilyMember(
            id=member_id,
            family_id=family_id,
            name=name,
            relationship=relationship,
            avatar=avatar,
            gender=gender,
            is_initialized=False,
            created_at=now,
            updated_at=now
        )
        
        self.db.add_member(member.to_dict())
        
        # 为成员创建空的画像
        self.db.create_profile(member_id, {
            'member_id': member_id,
            'name': name,
            'gender': gender,
            'relationship': relationship
        })
        
        return member
    
    def update_member(self, member_id: str, updates: Dict[str, Any]) -> bool:
        """更新成员信息"""
        updates['updated_at'] = datetime.now().isoformat()
        return self.db.update_member(member_id, updates)
    
    def delete_member(self, member_id: str) -> bool:
        """删除成员（及其衣橱数据）"""
        # 检查是否为主用户
        member = self.get_member(member_id)
        if member and member.relationship == "self":
            return False  # 不能删除主用户
        
        # 删除成员的所有数据
        self.db.delete_member_items(member_id)
        self.db.delete_member_profile(member_id)
        return self.db.delete_member(member_id)
    
    def set_member_initialized(self, member_id: str):
        """标记成员已完成初始化"""
        self.update_member(member_id, {'is_initialized': True})
    
    # ============ 画像管理 ============
    
    def get_profile(self, member_id: str) -> Optional[MemberProfile]:
        """获取成员画像"""
        data = self.db.get_profile(member_id)
        if data:
            return MemberProfile.from_dict(data)
        return None
    
    def update_profile(self, member_id: str, profile_data: Dict[str, Any]) -> bool:
        """更新成员画像"""
        profile_data['updated_at'] = datetime.now().isoformat()
        
        # 如果更新了身材数据，重新计算身材类型
        if 'body' in profile_data:
            body = BodyMeasurements.from_dict(profile_data['body'])
            body_type = body.calculate_body_type()
            if body_type:
                profile_data['body_type'] = body_type.value
        
        return self.db.update_profile(member_id, profile_data)
    
    def update_body_measurements(
        self, 
        member_id: str, 
        measurements: Dict[str, int]
    ) -> bool:
        """更新身材数据"""
        profile = self.get_profile(member_id)
        if not profile:
            return False
        
        # 更新身材数据
        for key, value in measurements.items():
            if hasattr(profile.body, key):
                setattr(profile.body, key, value)
        
        # 计算身材类型
        profile.body_type = profile.body.calculate_body_type()
        profile.updated_at = datetime.now()
        
        return self.db.update_profile(member_id, profile.to_dict())
    
    def update_style_preferences(
        self,
        member_id: str,
        preferred_styles: Optional[List[str]] = None,
        avoided_styles: Optional[List[str]] = None,
        preferred_colors: Optional[List[str]] = None,
        avoided_colors: Optional[List[str]] = None
    ) -> bool:
        """更新风格偏好"""
        profile = self.get_profile(member_id)
        if not profile:
            return False
        
        if preferred_styles:
            profile.style.preferred_styles = preferred_styles
        if avoided_styles:
            profile.style.avoided_styles = avoided_styles
        if preferred_colors:
            profile.style.preferred_colors = preferred_colors
        if avoided_colors:
            profile.style.avoided_colors = avoided_colors
        
        profile.updated_at = datetime.now()
        return self.db.update_profile(member_id, profile.to_dict())
    
    def update_child_profile(
        self,
        member_id: str,
        birth_date: Optional[str] = None,
        school: Optional[str] = None,
        grade: Optional[str] = None,
        favorite_characters: Optional[List[str]] = None,
        activities: Optional[List[str]] = None
    ) -> bool:
        """更新儿童画像"""
        profile = self.get_profile(member_id)
        if not profile or not profile.is_child():
            return False
        
        if not profile.child:
            profile.child = ChildProfile()
        
        if birth_date:
            from datetime import date
            try:
                profile.child.birth_date = date.fromisoformat(birth_date)
            except:
                pass
        if school:
            profile.child.school = school
        if grade:
            profile.child.grade = grade
        if favorite_characters:
            profile.child.favorite_characters = favorite_characters
        if activities:
            profile.child.activities = activities
        
        profile.updated_at = datetime.now()
        return self.db.update_profile(member_id, profile.to_dict())
    
    # ============ 成员识别 ============
    
    def recognize_member_from_text(self, text: str) -> Optional[FamilyMember]:
        """从文本中识别目标成员
        
        Examples:
            "今天我穿什么？" -> self
            "给老公挑件衣服" -> spouse
            "小孩的校服" -> child
        
        Args:
            text: 用户输入的文本
            
        Returns:
            识别到的成员，如果未识别返回None
        """
        members = self.get_all_members()
        
        # 先尝试精确匹配成员名称
        for member in members:
            if member.name in text:
                return member
        
        # 再尝试关系关键词匹配
        for relationship, keywords in self.RELATIONSHIP_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    # 找到对应关系的成员
                    for member in members:
                        if member.relationship == relationship:
                            return member
        
        return None
    
    def get_member_summary(self, member_id: str) -> Dict[str, Any]:
        """获取成员概要信息"""
        member = self.get_member(member_id)
        profile = self.get_profile(member_id)
        item_count = self.db.count_items(member_id)
        
        summary = {
            'id': member_id,
            'name': member.name if member else '未知',
            'avatar': member.avatar if member else '👤',
            'relationship': member.relationship if member else 'unknown',
            'is_initialized': member.is_initialized if member else False,
            'item_count': item_count,
            'has_body_data': False,
            'has_style_prefs': False,
            'body_type': None
        }
        
        if profile:
            summary['has_body_data'] = bool(profile.body.height)
            summary['has_style_prefs'] = bool(profile.style.preferred_styles)
            summary['body_type'] = profile.body_type.value if profile.body_type else None
            
            if profile.is_child() and profile.child:
                summary['age'] = profile.get_age()
                summary['school'] = profile.child.school
        
        return summary
    
    def list_members_for_display(self) -> List[Dict[str, Any]]:
        """获取成员列表用于显示"""
        members = self.get_all_members()
        result = []
        
        for member in members:
            summary = self.get_member_summary(member.id)
            result.append({
                'id': member.id,
                'name': member.name,
                'avatar': member.avatar,
                'relationship': member.relationship,
                'is_initialized': member.is_initialized,
                'item_count': summary['item_count']
            })
        
        return result