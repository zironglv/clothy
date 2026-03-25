"""
命令解析模块
解析用户输入，识别意图和目标成员
"""

import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum


class Intent(str, Enum):
    """用户意图"""
    # 成员管理
    ADD_MEMBER = "add_member"           # 添加家庭成员
    SWITCH_MEMBER = "switch_member"     # 切换成员
    LIST_MEMBERS = "list_members"       # 列出成员
    
    # 衣橱管理
    ADD_ITEM = "add_item"               # 添加单品
    LIST_ITEMS = "list_items"           # 查看衣橱
    DELETE_ITEM = "delete_item"         # 删除单品
    
    # 搭配推荐
    GET_RECOMMENDATION = "get_recommendation"  # 今日搭配
    
    # 种草
    ADD_WISHLIST = "add_wishlist"       # 添加种草
    CHECK_WISHLIST = "check_wishlist"   # 查看种草
    
    # 分析
    ANALYZE_WARDROBE = "analyze_wardrobe"  # 衣橱分析
    
    # 初始化
    INIT_PROFILE = "init_profile"       # 初始化画像
    
    # 关注店铺
    FOLLOW_SHOP = "follow_shop"         # 关注店铺
    CHECK_NEW = "check_new"             # 查看上新
    
    # 淘宝导入
    IMPORT_ORDER = "import_order"       # 导入订单
    
    # 其他
    UNKNOWN = "unknown"
    HELP = "help"


@dataclass
class ParsedCommand:
    """解析后的命令"""
    intent: Intent
    member_id: Optional[str] = None
    member_name: Optional[str] = None   # 用户提到的成员名称
    category: Optional[str] = None
    item_name: Optional[str] = None
    item_data: Optional[Dict] = None
    raw_text: str = ""
    confidence: float = 0.0


class CommandParser:
    """命令解析器"""
    
    # 意图识别关键词
    INTENT_PATTERNS = {
        Intent.ADD_MEMBER: [
            r"添加(家庭)?成员",
            r"给(.{1,3})建(个)?衣橱",
            r"新建(家庭)?成员",
            r"增加(家庭)?成员",
            r"帮我(家人)?添加",
        ],
        Intent.SWITCH_MEMBER: [
            r"切换到(.{1,5})的?衣橱",
            r"看看(.{1,5})的?衣橱",
            r"查(.{1,5})的?衣橱",
            r"切换(回)?(我|老公|老婆|小孩|孩子|宝宝)",
        ],
        Intent.LIST_MEMBERS: [
            r"(查看|列出|显示)?家庭成员",
            r"有哪些成员",
            r"家里有谁",
        ],
        Intent.ADD_ITEM: [
            r"(录入|添加|添加一件|加一件)(新)?(.+)",
            r"(这件|这个)(衣服|裤子|裙子|外套|鞋子)",
            r"拍(了)?(一张)?照片?",
            r"我有(一件|一条|一双)",
        ],
        Intent.LIST_ITEMS: [
            r"(查看|看看|显示)?我的?衣橱",
            r"我有什么衣服",
            r"(查看|看看)?(.+)(类|种|类型)",
            r"看看(.+)有什么",
        ],
        Intent.DELETE_ITEM: [
            r"删除(.+)",
            r"移除(.+)",
            r"不要(.+)了",
        ],
        Intent.GET_RECOMMENDATION: [
            r"今天(我|.{1,3})?(穿|搭配|穿什么|怎么穿)",
            r"(给我|给.{1,3})推荐(搭配|穿搭)",
            r"(帮|给)(我|.{1,3})配(一套|衣服)",
            r"(看看|有没有)适合今天的",
        ],
        Intent.ADD_WISHLIST: [
            r"种草(.+)",
            r"(看中|喜欢|想要)(这件|这个|这件衣服)",
            r"加入(购物车|种草|心愿单)",
        ],
        Intent.CHECK_WISHLIST: [
            r"(查看|看看)?种草(清单|列表)?",
            r"(我)?想要什么",
            r"心愿单",
        ],
        Intent.ANALYZE_WARDROBE: [
            r"衣橱分析",
            r"(分析|看看)?我的?(衣服|衣橱)(分布|统计|情况)",
            r"(我)?有哪些类型",
        ],
        Intent.INIT_PROFILE: [
            r"初始化(画像|身材|偏好)?",
            r"(开始)?(设置|填写)(身材|画像|偏好)",
            r"完善(我的)?信息",
        ],
        Intent.FOLLOW_SHOP: [
            r"关注(店铺|商店)",
            r"(订阅|追踪)(.{2,10})店",
        ],
        Intent.CHECK_NEW: [
            r"(查看|看看)?上新",
            r"(有|有没有)?新(款|品|商品)",
            r"(最近|最新)?(店铺|关注)(更新)?",
        ],
        Intent.IMPORT_ORDER: [
            r"导入(淘宝)?订单",
            r"(从)?淘宝导入",
            r"导入(我)?买(过)?的",
        ],
        Intent.HELP: [
            r"帮助",
            r"(怎么|如何)用",
            r"能做什么",
            r"(功能|能力)(列表)?",
        ],
    }
    
    # 成员关系关键词映射
    MEMBER_KEYWORDS = {
        "self": ["我", "自己", "本人"],
        "spouse": ["老公", "丈夫", "先生", "老婆", "妻子", "太太", "配偶"],
        "child": ["小孩", "孩子", "儿子", "女儿", "宝宝", "宝贝", "娃", "小朋友"],
        "parent": ["爸爸", "妈妈", "父亲", "母亲", "父母", "老爸", "老妈"],
    }
    
    # 品类关键词
    CATEGORY_KEYWORDS = {
        "outer": ["外套", "大衣", "羽绒服", "风衣", "夹克", "西装", "皮衣", "棒球服", "卫衣外套"],
        "top": ["上衣", "T恤", "衬衫", "毛衣", "针织衫", "卫衣", "吊带", "背心", "打底衫", "雪纺", " blouse"],
        "bottom": ["裤子", "裙", "牛仔裤", "休闲裤", "短裤", "半身裙", "连衣裙", "长裤", "西裤", "运动裤"],
        "shoes": ["鞋", "靴", "高跟鞋", "平底鞋", "运动鞋", "凉鞋", "拖鞋", "帆布鞋", "板鞋"],
        "accessory": ["包", "帽子", "围巾", "手套", "腰带", "项链", "耳环", "手表", "眼镜", "配饰", "包包"],
    }
    
    def __init__(self, member_manager=None):
        """初始化命令解析器
        
        Args:
            member_manager: MemberManager 实例（用于识别成员名称）
        """
        self.member_manager = member_manager
    
    def parse(self, text: str) -> ParsedCommand:
        """解析用户输入
        
        Args:
            text: 用户输入文本
            
        Returns:
            解析后的命令对象
        """
        text = text.strip()
        
        # 1. 识别意图
        intent, confidence = self._detect_intent(text)
        
        # 2. 识别目标成员
        member_id, member_name = self._detect_member(text)
        
        # 3. 提取品类
        category = self._detect_category(text)
        
        # 4. 提取单品信息（如果需要）
        item_name = self._extract_item_name(text, intent)
        
        return ParsedCommand(
            intent=intent,
            member_id=member_id,
            member_name=member_name,
            category=category,
            item_name=item_name,
            raw_text=text,
            confidence=confidence
        )
    
    def _detect_intent(self, text: str) -> Tuple[Intent, float]:
        """检测用户意图"""
        # 按优先级匹配
        priority_order = [
            Intent.ADD_MEMBER,
            Intent.SWITCH_MEMBER,
            Intent.LIST_MEMBERS,
            Intent.INIT_PROFILE,
            Intent.IMPORT_ORDER,
            Intent.FOLLOW_SHOP,
            Intent.CHECK_NEW,
            Intent.ANALYZE_WARDROBE,
            Intent.CHECK_WISHLIST,
            Intent.ADD_WISHLIST,
            Intent.GET_RECOMMENDATION,
            Intent.LIST_ITEMS,
            Intent.DELETE_ITEM,
            Intent.ADD_ITEM,
            Intent.HELP,
        ]
        
        for intent in priority_order:
            patterns = self.INTENT_PATTERNS.get(intent, [])
            for pattern in patterns:
                if re.search(pattern, text):
                    return intent, 0.9
        
        return Intent.UNKNOWN, 0.3
    
    def _detect_member(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """检测目标成员
        
        Returns:
            (member_id, member_name) - 如果只识别到名称但未找到成员，返回 (None, name)
        """
        # 如果没有 member_manager，只能识别关键词
        if not self.member_manager:
            return None, None
        
        # 先尝试精确匹配成员名称
        members = self.member_manager.get_all_members()
        for member in members:
            if member.name in text:
                return member.id, member.name
        
        # 再尝试关系关键词匹配
        for relationship, keywords in self.MEMBER_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    # 找到对应关系的成员
                    for member in members:
                        if member.relationship == relationship:
                            return member.id, member.name
        
        return None, None
    
    def _detect_category(self, text: str) -> Optional[str]:
        """检测品类"""
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return category
        return None
    
    def _extract_item_name(self, text: str, intent: Intent) -> Optional[str]:
        """提取单品名称"""
        if intent != Intent.ADD_ITEM:
            return None
        
        # 尝试提取"录入xxx"或"添加xxx"中的xxx
        patterns = [
            (r"录入(新)?(.+)", 2),      # 第2组是单品名
            (r"添加(一件)?(.+)", 2),    # 第2组是单品名
            (r"我有(一件|一条|一双)?(.+)", 2),  # 第2组是单品名
            (r"买了(一件|一条|一双)?(.+)", 2),  # 第2组是单品名
        ]
        
        for pattern, group_idx in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(group_idx).strip()
        
        return None
    
    def get_suggested_response(self, command: ParsedCommand) -> str:
        """获取建议响应（用于未知意图）"""
        if command.intent == Intent.UNKNOWN:
            return "抱歉，我不太理解您的意思。您可以试试：\n\n" \
                   "• 「今天我穿什么」- 获取搭配推荐\n" \
                   "• 「录入一件白衬衫」- 添加单品\n" \
                   "• 「看看我的衣橱」- 查看衣橱\n" \
                   "• 「添加家庭成员」- 添加成员\n\n" \
                   "或者直接拍照/发图片给我，我来帮您录入！"
        
        return None


def extract_body_info_from_text(text: str) -> Dict[str, Any]:
    """从文本中提取身材信息
    
    Examples:
        "我身高165，体重52kg" -> {"height": 165, "weight": 52}
        "腰围66cm" -> {"waist": 66}
    """
    result = {}
    
    # 身高
    height_match = re.search(r"身高\s*(\d{2,3})\s*(cm|厘米)?", text)
    if not height_match:
        height_match = re.search(r"(\d{2,3})\s*(cm|厘米)?(高|的身高)", text)
    if height_match:
        result['height'] = int(height_match.group(1))
    
    # 体重
    weight_match = re.search(r"体重\s*(\d{2,3})\s*(kg|公斤|斤)?", text)
    if not weight_match:
        weight_match = re.search(r"(\d{2,3})\s*(kg|公斤)(?!.*腰)", text)
    if weight_match:
        result['weight'] = int(weight_match.group(1))
    
    # 肩宽
    shoulder_match = re.search(r"肩宽\s*(\d{1,3})\s*(cm)?", text)
    if shoulder_match:
        result['shoulder_width'] = int(shoulder_match.group(1))
    
    # 胸围
    bust_match = re.search(r"胸围\s*(\d{2,3})\s*(cm)?", text)
    if bust_match:
        result['bust'] = int(bust_match.group(1))
    
    # 腰围
    waist_match = re.search(r"腰围\s*(\d{2,3})\s*(cm)?", text)
    if waist_match:
        result['waist'] = int(waist_match.group(1))
    
    # 臀围
    hip_match = re.search(r"臀围\s*(\d{2,3})\s*(cm)?", text)
    if hip_match:
        result['hip'] = int(hip_match.group(1))
    
    return result


def extract_style_preference_from_text(text: str) -> Dict[str, List[str]]:
    """从文本中提取风格偏好"""
    result = {
        'preferred_styles': [],
        'avoided_styles': [],
        'preferred_colors': [],
        'avoided_colors': []
    }
    
    # 风格关键词
    style_keywords = {
        'casual': ['休闲', '日常', '舒适', '随便'],
        'business': ['商务', '职业', '正式', '通勤'],
        'sweet': ['甜美', '可爱', '少女', '温柔'],
        'cool': ['酷', '帅气', '街头', '个性'],
        'minimalist': ['简约', '极简', '基础', '干净'],
        'elegant': ['优雅', '气质', '淑女', '大方'],
    }
    
    # 颜色关键词
    color_keywords = {
        'black': ['黑色', '黑色系'],
        'white': ['白色', '白色系'],
        'gray': ['灰色', '灰色系'],
        'beige': ['米色', '杏色', '奶茶色'],
        'blue': ['蓝色', '蓝色系'],
        'pink': ['粉色', '粉色系', '粉红'],
        'green': ['绿色', '绿色系'],
        'red': ['红色', '红色系'],
    }
    
    # 喜欢/不喜欢的表达
    like_patterns = ['喜欢', '偏好', '爱穿', '经常穿', '适合']
    dislike_patterns = ['不喜欢', '讨厌', '不穿', '不适合', '避免']
    
    for style, keywords in style_keywords.items():
        for keyword in keywords:
            for pattern in like_patterns:
                if pattern + keyword in text or keyword + pattern in text:
                    result['preferred_styles'].append(style)
            for pattern in dislike_patterns:
                if pattern + keyword in text or keyword + pattern in text:
                    result['avoided_styles'].append(style)
    
    for color, keywords in color_keywords.items():
        for keyword in keywords:
            for pattern in like_patterns:
                if pattern + keyword in text or keyword + pattern in text:
                    result['preferred_colors'].append(color)
            for pattern in dislike_patterns:
                if pattern + keyword in text or keyword + pattern in text:
                    result['avoided_colors'].append(color)
    
    # 去重
    for key in result:
        result[key] = list(set(result[key]))
    
    return result