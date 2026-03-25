"""
会话管理模块
管理当前操作的成员上下文
"""

import json
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

from .member_manager import MemberManager, FamilyMember


class SessionManager:
    """会话管理器
    
    负责管理当前用户正在操作哪个成员的衣橱。
    会话状态持久化存储，重启后恢复。
    """
    
    SESSION_FILE = "session_state.json"
    
    def __init__(self, db, member_manager: MemberManager, data_dir: str = "./assets/data"):
        """初始化会话管理器
        
        Args:
            db: Database 实例
            member_manager: MemberManager 实例
            data_dir: 数据目录
        """
        self.db = db
        self.member_manager = member_manager
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self._current_member_id: Optional[str] = None
        self._load_session()
    
    def _get_session_file(self) -> Path:
        """获取会话文件路径"""
        return self.data_dir / self.SESSION_FILE
    
    def _load_session(self):
        """加载会话状态"""
        session_file = self._get_session_file()
        
        if session_file.exists():
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._current_member_id = data.get('current_member_id')
            except:
                self._current_member_id = None
        
        # 验证成员是否还存在
        if self._current_member_id:
            member = self.member_manager.get_member(self._current_member_id)
            if not member:
                self._current_member_id = None
    
    def _save_session(self):
        """保存会话状态"""
        session_file = self._get_session_file()
        
        data = {
            'current_member_id': self._current_member_id,
            'updated_at': datetime.now().isoformat()
        }
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_current_member(self) -> Optional[FamilyMember]:
        """获取当前成员
        
        Returns:
            当前成员，如果未设置则返回主用户
        """
        # 如果有当前成员，返回它
        if self._current_member_id:
            member = self.member_manager.get_member(self._current_member_id)
            if member:
                return member
        
        # 否则返回主用户（self）
        members = self.member_manager.get_all_members()
        for m in members:
            if m.relationship == "self":
                self._current_member_id = m.id
                self._save_session()
                return m
        
        return None
    
    def get_current_member_id(self) -> Optional[str]:
        """获取当前成员ID"""
        member = self.get_current_member()
        return member.id if member else None
    
    def switch_member(self, member_id: str) -> bool:
        """切换当前成员
        
        Args:
            member_id: 目标成员ID
            
        Returns:
            是否切换成功
        """
        member = self.member_manager.get_member(member_id)
        if not member:
            return False
        
        self._current_member_id = member_id
        self._save_session()
        return True
    
    def switch_member_by_name(self, name: str) -> Optional[FamilyMember]:
        """通过名称切换成员
        
        Args:
            name: 成员名称
            
        Returns:
            切换后的成员，如果未找到返回None
        """
        member = self.member_manager.get_member_by_name(name)
        if member:
            self.switch_member(member.id)
            return member
        return None
    
    def switch_member_by_relationship(self, relationship: str) -> Optional[FamilyMember]:
        """通过关系类型切换成员
        
        Args:
            relationship: 关系类型（self/spouse/child/parent）
            
        Returns:
            切换后的成员，如果未找到返回None
        """
        members = self.member_manager.get_all_members()
        for m in members:
            if m.relationship == relationship:
                self.switch_member(m.id)
                return m
        return None
    
    def switch_to_self(self) -> Optional[FamilyMember]:
        """切换回主用户"""
        return self.switch_member_by_relationship("self")
    
    def recognize_and_switch(self, text: str) -> tuple[Optional[FamilyMember], bool]:
        """识别文本中的成员并切换
        
        Args:
            text: 用户输入文本
            
        Returns:
            (识别到的成员, 是否进行了切换)
        """
        member = self.member_manager.recognize_member_from_text(text)
        
        if member and member.id != self._current_member_id:
            self.switch_member(member.id)
            return member, True
        
        return member, False
    
    def get_session_context(self) -> Dict[str, Any]:
        """获取当前会话上下文"""
        member = self.get_current_member()
        
        if not member:
            return {
                'member': None,
                'profile': None,
                'is_initialized': False
            }
        
        profile = self.member_manager.get_profile(member.id)
        
        return {
            'member': {
                'id': member.id,
                'name': member.name,
                'avatar': member.avatar,
                'relationship': member.relationship
            },
            'profile': profile.to_dict() if profile else None,
            'is_initialized': member.is_initialized
        }
    
    def reset_session(self):
        """重置会话（切换回主用户）"""
        self._current_member_id = None
        self._save_session()
        self._load_session()
    
    def get_switch_prompt(self, from_member: FamilyMember, to_member: FamilyMember) -> str:
        """生成切换提示语"""
        messages = {
            ('self', 'spouse'): f"好的，已切换到{to_member.name}的衣橱 👨",
            ('self', 'child'): f"好的，已切换到{to_member.name}的衣橱 👧",
            ('spouse', 'self'): "好的，已切换回您的衣橱 👩",
            ('spouse', 'child'): f"好的，已切换到{to_member.name}的衣橱 👧",
            ('child', 'self'): "好的，已切换回您的衣橱 👩",
            ('child', 'spouse'): f"好的，已切换到{to_member.name}的衣橱 👨",
        }
        
        key = (from_member.relationship, to_member.relationship)
        return messages.get(key, f"好的，已切换到{to_member.name}的衣橱 {to_member.avatar}")