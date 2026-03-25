# StyleBuddy 多人衣橱设计

> 支持管理家庭成员的衣橱

---

## 一、需求场景

```
┌─────────────────────────────────────────────────────────────────┐
│                     多人衣橱场景                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  👩 妈妈（主用户）                                               │
│     └─ 管理自己的衣橱                                           │
│     └─ 帮老公搭配                                               │
│     └─ 给孩子买衣服                                             │
│     └─ 给爸妈挑衣服                                             │
│                                                                 │
│  👨 丈夫                                                         │
│     └─ 有自己的身材信息、风格偏好                               │
│     └─ 有自己的衣橱                                             │
│                                                                 │
│  👧 小孩                                                         │
│     └─ 需要记录身高体重（长得快）                               │
│     └─ 有自己的衣橱                                             │
│                                                                 │
│  👴 老人                                                         │
│     └─ 有自己的穿衣偏好                                         │
│     └─ 有自己的衣橱                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**核心价值**：
- 一个 Skill 管理全家人的衣橱
- 每个成员独立画像、独立衣橱
- 主用户可切换管理不同成员
- 可为家人推荐穿搭、购买建议

---

## 二、数据模型设计

### 2.1 家庭与成员

```
┌─────────────┐       ┌─────────────┐
│   Family    │──1:N──│   Member    │
│   (家庭)    │       │   (成员)    │
└─────────────┘       └──────┬──────┘
                             │
                             │ 1:N
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   Profile   │       │   Items     │       │  Wishlist   │
│  (画像)     │       │  (衣橱)     │       │  (种草)     │
└─────────────┘       └─────────────┘       └─────────────┘
```

### 2.2 数据库表设计

```sql
-- 家庭表
CREATE TABLE families (
    id TEXT PRIMARY KEY,
    
    -- 家庭信息
    name TEXT,                        -- 家庭名称，如"青枫的家"
    
    -- 创建者（主用户）
    creator_id TEXT,
    
    -- 时间戳
    created_at TEXT,
    updated_at TEXT
);

-- 成员表
CREATE TABLE members (
    id TEXT PRIMARY KEY,
    family_id TEXT NOT NULL,          -- 所属家庭
    
    -- 基本信息
    name TEXT NOT NULL,               -- 成员名称，如"老公"、"小明"
    nickname TEXT,                    -- 昵称
    avatar TEXT,                      -- 头像
    
    -- 关系
    relationship TEXT,                -- 关系：self/spouse/child/parent/other
    /*
     * self: 本人（主用户）
     * spouse: 配偶
     * child: 子女
     * parent: 父母
     * other: 其他
     */
    
    -- 角色权限
    role TEXT DEFAULT 'member',       -- owner/admin/member
    
    -- 顺序（用于排序显示）
    display_order INTEGER DEFAULT 0,
    
    -- 状态
    is_active INTEGER DEFAULT 1,
    
    created_at TEXT,
    updated_at TEXT,
    
    FOREIGN KEY (family_id) REFERENCES families(id)
);

-- 用户画像表（扩展）
CREATE TABLE profiles (
    id TEXT PRIMARY KEY,
    member_id TEXT NOT NULL,          -- 关联成员（原来是 user_id）
    
    -- 基本信息
    gender TEXT,                      -- male/female
    
    -- 身材信息
    height INTEGER,
    weight REAL,
    body_type TEXT,
    age_range TEXT,
    
    -- 详细尺寸
    shoulder_width REAL,
    bust REAL,
    waist REAL,
    hip REAL,
    leg_length REAL,
    
    -- 风格偏好
    style_preferences TEXT,
    avoid_elements TEXT,
    favorite_colors TEXT,
    avoid_colors TEXT,
    
    -- 特殊标签（新增）
    special_tags TEXT,                -- JSON: ["孕妇", "运动达人", "商务人士"]
    
    -- 儿童专用（新增）
    is_child INTEGER DEFAULT 0,
    birth_date TEXT,                  -- 出生年月（用于计算年龄、身高增长）
    school TEXT,                      -- 学校（用于校服等场景）
    
    -- 初始化状态
    init_status TEXT DEFAULT 'pending',
    init_step INTEGER DEFAULT 0,
    
    created_at TEXT,
    updated_at TEXT,
    
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- 衣橱单品表（扩展）
CREATE TABLE items (
    id TEXT PRIMARY KEY,
    member_id TEXT NOT NULL,          -- 关联成员（原来是 user_id）
    
    -- 单品信息
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    color TEXT,
    season TEXT,
    style TEXT,
    
    -- 图片
    image_path TEXT,
    
    -- 淘宝来源
    source TEXT DEFAULT 'manual',
    taobao_item_id TEXT,
    taobao_order_id TEXT,
    taobao_price REAL,
    taobao_shop TEXT,
    taobao_buy_time TEXT,
    taobao_image_url TEXT,
    taobao_product_url TEXT,
    
    -- 共享标记（新增）
    is_shared INTEGER DEFAULT 0,      -- 是否共享给其他家庭成员
    shared_with TEXT,                 -- JSON: 共享给哪些成员
    
    created_at TEXT,
    updated_at TEXT,
    
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- 搭配记录表（扩展）
CREATE TABLE outfits (
    id TEXT PRIMARY KEY,
    member_id TEXT NOT NULL,          -- 关联成员
    
    date TEXT NOT NULL,
    occasion TEXT,
    weather TEXT,
    items TEXT,
    rating INTEGER,
    notes TEXT,
    
    created_at TEXT,
    
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- 种草清单表（扩展）
CREATE TABLE wishlist (
    id TEXT PRIMARY KEY,
    member_id TEXT NOT NULL,          -- 关联成员（为谁买的）
    
    name TEXT NOT NULL,
    category TEXT,
    color TEXT,
    source TEXT,
    taobao_item_id TEXT,
    taobao_product_url TEXT,
    taobao_image_url TEXT,
    taobao_price REAL,
    status TEXT DEFAULT 'pending',
    notes TEXT,
    
    -- 购买记录（新增）
    bought_for TEXT,                  -- 为谁买的（成员ID）
    bought_at TEXT,                   -- 购买时间
    
    created_at TEXT,
    updated_at TEXT,
    
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- 风格画像表（扩展）
CREATE TABLE style_profiles (
    id TEXT PRIMARY KEY,
    member_id TEXT NOT NULL,          -- 关联成员
    
    style_tags TEXT,
    color_distribution TEXT,
    season_distribution TEXT,
    category_distribution TEXT,
    insights TEXT,
    shopping_suggestions TEXT,
    body_suggestions TEXT,
    
    user_feedback TEXT,
    feedback_time TEXT,
    
    created_at TEXT,
    updated_at TEXT,
    
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- 关注来源表（扩展）
CREATE TABLE followed_sources (
    id TEXT PRIMARY KEY,
    member_id TEXT NOT NULL,          -- 关联成员（谁关注的）
    
    source_type TEXT NOT NULL,
    source_url TEXT NOT NULL,
    source_id TEXT,
    source_name TEXT,
    source_avatar TEXT,
    
    style_tags TEXT,
    target_audience TEXT,
    
    last_check_time TEXT,
    last_new_count INTEGER DEFAULT 0,
    check_status TEXT DEFAULT 'pending',
    error_message TEXT,
    
    push_enabled INTEGER DEFAULT 1,
    push_time TEXT DEFAULT '09:00',
    
    user_notes TEXT,
    
    created_at TEXT,
    updated_at TEXT,
    
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- 上新商品表（扩展）
CREATE TABLE new_arrivals (
    id TEXT PRIMARY KEY,
    member_id TEXT NOT NULL,          -- 关联成员
    source_id TEXT NOT NULL,
    
    item_id TEXT NOT NULL,
    item_url TEXT,
    item_title TEXT,
    item_image TEXT,
    item_price REAL,
    
    category TEXT,
    color TEXT,
    style_tags TEXT,
    season TEXT,
    selling_points TEXT,
    target_match TEXT,
    
    match_score REAL,
    match_reason TEXT,
    wardrobe_match TEXT,
    
    status TEXT DEFAULT 'new',
    pushed_at TEXT,
    user_feedback TEXT,
    
    publish_time TEXT,
    created_at TEXT,
    updated_at TEXT,
    
    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (source_id) REFERENCES followed_sources(id)
);

-- 当前会话状态表（新增）
CREATE TABLE session_state (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,         -- 会话ID
    
    -- 当前选中的成员
    current_member_id TEXT,           -- 当前操作的成员
    current_family_id TEXT,           -- 当前家庭
    
    -- 最后活动时间
    last_active_at TEXT,
    
    created_at TEXT,
    updated_at TEXT,
    
    FOREIGN KEY (current_member_id) REFERENCES members(id),
    FOREIGN KEY (current_family_id) REFERENCES families(id)
);
```

---

## 三、成员管理模块

### 3.1 成员管理器

```python
"""
成员管理模块
管理家庭成员
"""

from typing import Dict, List, Optional
from datetime import datetime
import uuid

class MemberManager:
    """成员管理器"""
    
    # 关系类型
    RELATIONSHIP_TYPES = {
        'self': '本人',
        'spouse': '配偶',
        'child': '子女',
        'parent': '父母',
        'other': '其他'
    }
    
    # 默认头像（按关系类型）
    DEFAULT_AVATARS = {
        'self': '👤',
        'spouse_male': '👨',
        'spouse_female': '👩',
        'child_male': '👦',
        'child_female': '👧',
        'parent_male': '👴',
        'parent_female': '👵',
        'other': '👤'
    }
    
    def __init__(self, db):
        self.db = db
    
    def create_family(self, name: str, creator_id: str = None) -> Dict:
        """
        创建家庭
        
        Args:
            name: 家庭名称
            creator_id: 创建者ID
        
        Returns:
            家庭信息
        """
        family_id = f"family_{uuid.uuid4().hex[:8]}"
        
        # 创建家庭
        self.db.insert('families', {
            'id': family_id,
            'name': name,
            'creator_id': creator_id,
            'created_at': datetime.now().isoformat()
        })
        
        # 自动创建"本人"成员
        member = self.add_member(
            family_id=family_id,
            name='我',
            relationship='self',
            role='owner'
        )
        
        return {
            'family_id': family_id,
            'name': name,
            'self_member': member
        }
    
    def add_member(self, family_id: str, name: str, relationship: str = 'other',
                   nickname: str = None, gender: str = None, 
                   role: str = 'member') -> Dict:
        """
        添加家庭成员
        
        Args:
            family_id: 家庭ID
            name: 成员名称
            relationship: 关系类型
            nickname: 昵称
            gender: 性别
            role: 角色
        
        Returns:
            成员信息
        """
        member_id = f"member_{uuid.uuid4().hex[:8]}"
        
        # 确定默认头像
        if relationship == 'spouse':
            avatar_key = f"spouse_{gender}" if gender else 'spouse_male'
        elif relationship == 'child':
            avatar_key = f"child_{gender}" if gender else 'child_male'
        elif relationship == 'parent':
            avatar_key = f"parent_{gender}" if gender else 'parent_male'
        else:
            avatar_key = relationship
        
        # 获取排序号
        order = self.db.count('members', {'family_id': family_id})
        
        member = {
            'id': member_id,
            'family_id': family_id,
            'name': name,
            'nickname': nickname,
            'avatar': self.DEFAULT_AVATARS.get(avatar_key, '👤'),
            'relationship': relationship,
            'role': role,
            'display_order': order,
            'created_at': datetime.now().isoformat()
        }
        
        self.db.insert('members', member)
        
        # 同时创建空的画像记录
        self.db.insert('profiles', {
            'id': f"profile_{member_id}",
            'member_id': member_id,
            'gender': gender,
            'init_status': 'pending',
            'created_at': datetime.now().isoformat()
        })
        
        return member
    
    def get_member(self, member_id: str) -> Optional[Dict]:
        """获取成员信息"""
        return self.db.get('members', {'id': member_id})
    
    def get_member_with_profile(self, member_id: str) -> Optional[Dict]:
        """获取成员信息（含画像）"""
        member = self.get_member(member_id)
        if not member:
            return None
        
        profile = self.db.get('profiles', {'member_id': member_id})
        member['profile'] = profile
        
        return member
    
    def list_members(self, family_id: str) -> List[Dict]:
        """
        获取家庭成员列表
        
        Returns:
            成员列表，按 display_order 排序
        """
        members = self.db.query('members', {'family_id': family_id, 'is_active': 1})
        
        # 按顺序排序，self 在最前
        def sort_key(m):
            if m['relationship'] == 'self':
                return (0, m['display_order'])
            return (1, m['display_order'])
        
        members.sort(key=sort_key)
        
        # 附带画像状态
        for member in members:
            profile = self.db.get('profiles', {'member_id': member['id']})
            member['profile_status'] = profile.get('init_status') if profile else 'pending'
            member['item_count'] = self.db.count('items', {'member_id': member['id']})
        
        return members
    
    def update_member(self, member_id: str, updates: Dict) -> bool:
        """更新成员信息"""
        updates['updated_at'] = datetime.now().isoformat()
        return self.db.update('members', {'id': member_id}, updates)
    
    def remove_member(self, member_id: str) -> bool:
        """
        移除家庭成员（软删除）
        
        注意：不能移除 self 成员
        """
        member = self.get_member(member_id)
        if not member:
            return False
        
        if member['relationship'] == 'self':
            return False  # 不能移除本人
        
        return self.db.update('members', {'id': member_id}, {
            'is_active': 0,
            'updated_at': datetime.now().isoformat()
        })
    
    def get_family_info(self, family_id: str) -> Dict:
        """获取家庭信息"""
        family = self.db.get('families', {'id': family_id})
        if not family:
            return None
        
        family['members'] = self.list_members(family_id)
        return family
```

### 3.2 会话状态管理

```python
"""
会话状态管理
管理当前操作的成员
"""

class SessionManager:
    """会话管理器"""
    
    def __init__(self, db):
        self.db = db
    
    def get_current_member(self, session_id: str) -> Optional[Dict]:
        """
        获取当前会话选中的成员
        
        Returns:
            当前成员信息，如果未设置则返回默认成员（self）
        """
        state = self.db.get('session_state', {'session_id': session_id})
        
        if state and state.get('current_member_id'):
            return self.db.get('members', {'id': state['current_member_id']})
        
        # 未设置，返回默认成员（家庭中的 self）
        # 先找到或创建默认家庭
        family = self._get_or_create_default_family()
        self_member = self.db.get('members', {'family_id': family['id'], 'relationship': 'self'})
        
        return self_member
    
    def set_current_member(self, session_id: str, member_id: str) -> bool:
        """设置当前成员"""
        state = self.db.get('session_state', {'session_id': session_id})
        
        now = datetime.now().isoformat()
        
        if state:
            return self.db.update('session_state', {'session_id': session_id}, {
                'current_member_id': member_id,
                'last_active_at': now
            })
        else:
            return self.db.insert('session_state', {
                'id': f"session_{uuid.uuid4().hex[:8]}",
                'session_id': session_id,
                'current_member_id': member_id,
                'last_active_at': now,
                'created_at': now
            })
    
    def _get_or_create_default_family(self) -> Dict:
        """获取或创建默认家庭"""
        # 查找第一个家庭
        families = self.db.query('families', {})
        if families:
            return families[0]
        
        # 创建默认家庭
        return MemberManager(self.db).create_family('我的家')
```

---

## 四、交互设计

### 4.1 用户命令

```
# 成员管理
"添加家庭成员"              → 引导添加
"添加我老公"                → 快速添加
"给孩子建个衣橱"            → 添加子女成员
"家庭成员列表"              → 显示所有成员

# 切换成员
"切换到老公的衣橱"          → 切换当前操作成员
"看看小孩的衣服"            → 切换并查看
"回到我的衣橱"              → 切换回自己

# 查看状态
"现在在管理谁的衣橱？"       → 显示当前成员
"我家里有哪些人？"          → 显示家庭成员

# 穿搭推荐
"今天我穿什么？"             → 当前成员的推荐
"今天老公穿什么？"           → 指定成员推荐
"给小孩配一套穿搭"           → 指定成员推荐

# 衣橱操作
"录入一件衬衫"              → 录入到当前成员衣橱
"给老公录入一件衬衫"        → 录入到指定成员衣橱
"我有哪些黑衣服？"          → 查询当前成员
"小孩有多少衣服？"          → 查询指定成员统计
```

### 4.2 交互流程示例

#### 添加家庭成员

```
用户："添加家庭成员"

StyleBuddy：
┌─────────────────────────────────────────────────────────────────┐
│                    添加家庭成员                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  请问要添加谁？                                                  │
│                                                                 │
│  [👨 老公]  [👩 老婆]  [👦 儿子]  [👧 女儿]                    │
│  [👴 爸爸]  [👵 妈妈]  [👤 其他...]                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

用户：点击 "👨 老公"

StyleBuddy：
┌─────────────────────────────────────────────────────────────────┐
│                    添加老公                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📝 名称：[老公        ]                                        │
│  📝 昵称：[           ]（可选）                                 │
│                                                                 │
│  [确认添加]                                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

用户：确认添加

StyleBuddy：
┌─────────────────────────────────────────────────────────────────┐
│ ✅ 已添加成员                                                    │
│                                                                 │
│  👨 老公                                                        │
│                                                                 │
│  接下来需要完善他的信息吗？                                      │
│  • 身材信息（身高、体重、体型）                                  │
│  • 风格偏好（喜欢的穿衣风格）                                    │
│  • 淘宝导入（从淘宝订单导入他的衣服）                            │
│                                                                 │
│  [现在设置]  [稍后再说]                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 切换成员

```
用户："家庭成员列表"

StyleBuddy：
┌─────────────────────────────────────────────────────────────────┐
│                    我的家                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  👤 我 ★ 当前                      45件衣服                     │
│     极简通勤风格                                                │
│                                                                 │
│  👨 老公                           23件衣服                     │
│     商务休闲风格                                                │
│                                                                 │
│  👦 小明（儿子）                    18件衣服                     │
│     还未设置画像                                                │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  [➕ 添加成员]                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

用户：点击 "👨 老公"

StyleBuddy：
┌─────────────────────────────────────────────────────────────────┐
│ ✅ 已切换到老公的衣橱                                            │
│                                                                 │
│  👨 老公                                                        │
│  • 身高：178cm  体重：75kg                                      │
│  • 风格：商务休闲                                               │
│  • 衣橱：23件单品                                               │
│                                                                 │
│  你现在可以为老公：                                              │
│  • 推荐："今天穿什么？"                                         │
│  • 录入："录入一件蓝色衬衫"                                     │
│  • 分析："分析衣橱"                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 混合操作

```
用户："今天我穿什么？"

StyleBuddy：（根据当前成员推荐）
┌─────────────────────────────────────────────────────────────────┐
│ 👤 你的今日穿搭                                                 │
│                                                                 │
│  🌤️ 北京 18°C 多云                                              │
│                                                                 │
│  [图片] [图片] [图片]                                           │
│  白衬衫  牛仔裤  乐福鞋                                         │
│                                                                 │
│  💡 搭配建议：...                                               │
└─────────────────────────────────────────────────────────────────┘

用户："今天老公穿什么？"

StyleBuddy：（切换到老公并推荐）
┌─────────────────────────────────────────────────────────────────┐
│ 👨 老公的今日穿搭                                               │
│                                                                 │
│  🌤️ 北京 18°C 多云                                              │
│                                                                 │
│  [图片] [图片] [图片]                                           │
│  蓝色衬衫  西裤  皮鞋                                           │
│                                                                 │
│  💡 搭配建议：商务休闲风格，适合通勤...                          │
└─────────────────────────────────────────────────────────────────┘

用户："给老公录入一件新买的夹克"

StyleBuddy：
┌─────────────────────────────────────────────────────────────────┐
│ 👨 录入到老公的衣橱                                              │
│                                                                 │
│  请发送夹克的照片，或描述一下：                                  │
│  • "黑色夹克"                                                   │
│  • "灰色牛仔夹克"                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 五、语义解析增强

### 5.1 成员识别

```python
"""
成员识别模块
从用户输入中识别目标成员
"""

import re
from typing import Optional, Dict, List

class MemberRecognizer:
    """成员识别器"""
    
    # 成员关键词映射
    MEMBER_KEYWORDS = {
        # 自己
        'self': ['我', '我的', '自己'],
        
        # 配偶
        'spouse_male': ['老公', '丈夫', '先生', '孩子他爸', '孩儿他爸'],
        'spouse_female': ['老婆', '妻子', '夫人', '孩子他妈', '孩儿他妈'],
        
        # 子女
        'child': ['孩子', '小孩', '儿子', '女儿', '宝贝', '宝宝', '小朋友'],
        'child_male': ['儿子', '男宝', '男孩'],
        'child_female': ['女儿', '女宝', '女孩'],
        
        # 父母
        'parent_male': ['爸爸', '父亲', '老爸', '公公', '岳父'],
        'parent_female': ['妈妈', '母亲', '老妈', '婆婆', '岳母'],
        
        # 其他
        'other': ['家人', '家里']
    }
    
    def __init__(self, db):
        self.db = db
    
    def recognize(self, text: str, family_id: str) -> Optional[Dict]:
        """
        从文本中识别目标成员
        
        Args:
            text: 用户输入文本
            family_id: 家庭ID
        
        Returns:
            识别到的成员信息，如果没有则返回 None
        """
        # 获取家庭成员
        members = self.db.query('members', {'family_id': family_id, 'is_active': 1})
        
        # 1. 尝试匹配成员名称
        for member in members:
            if member['name'] in text or (member.get('nickname') and member['nickname'] in text):
                return member
        
        # 2. 尝试匹配关系关键词
        for relationship, keywords in self.MEMBER_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    # 找到匹配的成员
                    matched = self._find_member_by_relationship(members, relationship, keyword)
                    if matched:
                        return matched
        
        return None
    
    def _find_member_by_relationship(self, members: List[Dict], 
                                      relationship: str, 
                                      keyword: str) -> Optional[Dict]:
        """根据关系类型查找成员"""
        if relationship == 'self':
            return next((m for m in members if m['relationship'] == 'self'), None)
        
        if relationship in ['spouse_male', 'spouse_female']:
            gender = 'male' if 'male' in relationship else 'female'
            return next((m for m in members 
                        if m['relationship'] == 'spouse' 
                        and self._get_member_gender(m) == gender), None)
        
        if relationship in ['child_male', 'child_female']:
            gender = 'male' if 'male' in relationship else 'female'
            return next((m for m in members 
                        if m['relationship'] == 'child'
                        and self._get_member_gender(m) == gender), None)
        
        if relationship == 'child':
            return next((m for m in members if m['relationship'] == 'child'), None)
        
        if relationship in ['parent_male', 'parent_female']:
            gender = 'male' if 'male' in relationship else 'female'
            return next((m for m in members 
                        if m['relationship'] == 'parent'
                        and self._get_member_gender(m) == gender), None)
        
        return None
    
    def _get_member_gender(self, member: Dict) -> str:
        """获取成员性别"""
        profile = self.db.get('profiles', {'member_id': member['id']})
        return profile.get('gender') if profile else None
    
    def extract_member_context(self, text: str, family_id: str) -> Dict:
        """
        提取成员上下文
        
        Returns:
            {
                'target_member': 成员信息或 None,
                'action': 操作内容,
                'is_explicit': 是否明确指定了成员
            }
        """
        target = self.recognize(text, family_id)
        
        if target:
            # 移除成员称呼，提取操作
            action = text
            for keyword in [target['name']] + self.MEMBER_KEYWORDS.get(
                self._get_relationship_key(target), []
            ):
                action = action.replace(keyword, '').strip()
            
            return {
                'target_member': target,
                'action': action,
                'is_explicit': True
            }
        
        return {
            'target_member': None,
            'action': text,
            'is_explicit': False
        }
    
    def _get_relationship_key(self, member: Dict) -> str:
        """获取成员的关系关键词键"""
        return member.get('relationship', 'other')
```

### 5.2 命令解析

```python
"""
命令解析器
解析用户命令并路由到正确的处理逻辑
"""

class CommandParser:
    """命令解析器"""
    
    def __init__(self, db, session_manager, member_recognizer):
        self.db = db
        self.session_manager = session_manager
        self.member_recognizer = member_recognizer
    
    def parse(self, text: str, session_id: str) -> Dict:
        """
        解析用户命令
        
        Returns:
            {
                'intent': 意图,
                'target_member_id': 目标成员ID,
                'current_member_id': 当前成员ID,
                'params': 参数,
                'original_text': 原始文本
            }
        """
        # 获取当前状态
        family_id = self.session_manager.get_family_id(session_id)
        current_member = self.session_manager.get_current_member(session_id)
        
        # 提取成员上下文
        context = self.member_recognizer.extract_member_context(text, family_id)
        
        # 确定目标成员
        if context['is_explicit']:
            target_member_id = context['target_member']['id']
        else:
            target_member_id = current_member['id']
        
        # 解析意图
        intent = self._detect_intent(context['action'])
        
        return {
            'intent': intent,
            'target_member_id': target_member_id,
            'current_member_id': current_member['id'],
            'params': self._extract_params(context['action'], intent),
            'original_text': text,
            'is_explicit_member': context['is_explicit']
        }
    
    def _detect_intent(self, text: str) -> str:
        """检测意图"""
        text_lower = text.lower()
        
        # 成员管理
        if any(kw in text for kw in ['添加成员', '添加家人', '新建成员']):
            return 'add_member'
        if any(kw in text for kw in ['家庭成员', '成员列表', '家里有哪些人']):
            return 'list_members'
        if any(kw in text for kw in ['切换', '切换到']):
            return 'switch_member'
        
        # 穿搭推荐
        if any(kw in text for kw in ['今天穿什么', '穿什么', '搭配', '推荐穿搭']):
            return 'outfit_recommend'
        
        # 衣橱管理
        if any(kw in text for kw in ['录入', '添加', '新买']):
            return 'add_item'
        if any(kw in text for kw in ['我有哪些', '有什么', '查看衣橱']):
            return 'list_items'
        if any(kw in text for kw in ['删除', '移除']):
            return 'remove_item'
        
        # 衣橱分析
        if any(kw in text for kw in ['分析衣橱', '衣橱分析', '衣橱报告']):
            return 'analyze_wardrobe'
        
        # 种草咨询
        if any(kw in text for kw in ['适合我吗', '买不买', '要不要买', '这件怎么样']):
            return 'consult_item'
        
        # 关注店铺
        if any(kw in text for kw in ['关注店铺', '关注这个店']):
            return 'follow_shop'
        
        return 'unknown'
    
    def _extract_params(self, text: str, intent: str) -> Dict:
        """提取参数"""
        params = {}
        
        if intent == 'add_item':
            # 尝试提取服装信息
            params['item_text'] = text
        
        elif intent == 'outfit_recommend':
            # 尝试提取场合
            occasion_keywords = {
                '约会': 'date',
                '面试': 'interview',
                '上班': 'work',
                '通勤': 'work',
                '运动': 'sport',
                '休闲': 'casual',
                '聚会': 'party'
            }
            for kw, occasion in occasion_keywords.items():
                if kw in text:
                    params['occasion'] = occasion
                    break
        
        return params
```

---

## 六、输出格式扩展

### 6.1 输出增加成员信息

```python
@dataclass
class OutfitRecommendation:
    """穿搭推荐输出（扩展）"""
    
    # 成员信息（新增）
    member: Dict[str, Any]
    # {
    #   "id": "member_xxx",
    #   "name": "老公",
    #   "relationship": "spouse",
    #   "avatar": "👨"
    # }
    
    # 天气信息
    weather: Dict[str, Any]
    
    # 用户画像摘要
    user_profile: Dict[str, Any]
    
    # 推荐单品列表
    items: List[Dict[str, Any]]
    
    # 搭配说明
    tips: List[str]
    
    # 元数据
    meta: Dict[str, Any]
```

**输出示例**：

```json
{
  "member": {
    "id": "member_abc123",
    "name": "老公",
    "relationship": "spouse",
    "avatar": "👨"
  },
  "weather": {
    "city": "北京",
    "temp": 18,
    "condition": "多云"
  },
  "user_profile": {
    "body_type_label": "标准体型",
    "style_preference": ["商务休闲"]
  },
  "items": [
    {
      "id": "item_001",
      "name": "蓝色衬衫",
      "category_label": "上衣",
      "image": {"url": "https://...", "path": "/path/to/..."}
    }
  ],
  "tips": ["商务休闲风格，适合通勤场合"]
}
```

---

## 七、儿童特殊处理

### 7.1 儿童画像字段

```python
# 儿童专属字段
CHILD_FIELDS = {
    'birth_date': '出生日期',          # 用于计算年龄
    'height_growth': '身高增长记录',    # JSON: [{"date": "2024-01", "height": 120}]
    'weight_growth': '体重增长记录',    # JSON
    'school': '学校',                  # 学校名称
    'uniform_info': '校服信息',        # JSON: 校服款式、尺码等
    'size_preference': '尺码偏好',     # 如 "买大一号"
    'favorite_characters': '喜欢的卡通形象',  # 如 "奥特曼"、"艾莎"
    'activity_preference': '活动偏好'   # 如 "运动"、"绘画"
}
```

### 7.2 儿童穿搭建议

```python
def get_child_outfit_tips(member: Dict, weather: Dict) -> List[str]:
    """获取儿童穿搭特别建议"""
    tips = []
    
    profile = member.get('profile', {})
    
    # 根据年龄给建议
    age = calculate_age(profile.get('birth_date'))
    if age and age < 3:
        tips.append("建议选择方便换尿布的款式")
        tips.append("面料要柔软透气，避免皮肤过敏")
    elif age and age < 6:
        tips.append("选择方便活动的款式，适合跑跳")
        tips.append("避免细小的装饰物，防止误吞")
    elif age and age < 12:
        tips.append("选择耐脏易清洗的面料")
    
    # 根据天气给建议
    if weather.get('temp', 20) > 25:
        tips.append("孩子好动易出汗，选择透气面料")
    if weather.get('condition') in ['雨', '小雨']:
        tips.append("准备雨衣雨鞋，孩子喜欢踩水")
    
    # 根据活动给建议
    activity = profile.get('activity_preference')
    if activity == '运动':
        tips.append("选择运动服，方便活动")
    if activity == '绘画':
        tips.append("可以穿耐脏的罩衣或围裙")
    
    return tips
```

---

## 八、总结

### 新增模块

| 模块 | 文件 | 功能 |
|------|------|------|
| 成员管理 | `member_manager.py` | 添加/删除/查询家庭成员 |
| 会话管理 | `session_manager.py` | 管理当前操作成员 |
| 成员识别 | `member_recognizer.py` | 从文本识别目标成员 |
| 命令解析 | `command_parser.py` | 解析命令并路由 |

### 数据库新增表

| 表名 | 用途 |
|------|------|
| `families` | 家庭信息 |
| `members` | 家庭成员 |
| `session_state` | 会话状态 |

### 扩展字段

- 所有业务表增加 `member_id` 字段（替代原来的 `user_id`）
- `profiles` 表增加儿童专属字段
- 输出格式增加 `member` 信息

### 交互特性

- 自动识别命令中的目标成员
- 支持切换当前操作成员
- 儿童成员有特殊的穿搭建议