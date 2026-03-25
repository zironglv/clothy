"""
主路由模块
处理用户输入，路由到相应处理模块
集成所有核心功能
"""

from typing import Dict, Any, Optional, Tuple
import json
from datetime import datetime

from .member_manager import MemberManager
from .session_manager import SessionManager
from .command_parser import CommandParser, Intent, ParsedCommand
from .initializer import Initializer
from .recommender import OutfitRecommender
from ..storage.database import Database
from ..services.message_builder import MessageBuilder
from ..services.image_service import ImageService
from ..services.taobao_importer import TaobaoImporter, TaobaoImportSession
from ..services.source_monitor import SourceManager, SourceMonitor
from ..services.clothing_recognizer import ClothingRecognizer


class MainRouter:
    """主路由器 - 集成所有功能"""
    
    def __init__(self, db_path: str = "./assets/data/wardrobe.db"):
        """初始化主路由"""
        # 核心组件
        self.db = Database(db_path)
        self.member_manager = MemberManager(self.db)
        self.session_manager = SessionManager(self.db, self.member_manager)
        self.command_parser = CommandParser(self.member_manager)
        self.initializer = Initializer(self.member_manager, self.db)
        self.recommender = OutfitRecommender(self.db)
        
        # 服务组件
        self.image_service = ImageService()
        self.taobao_importer = TaobaoImporter(self.db, self.image_service)
        self.taobao_session = TaobaoImportSession(self.taobao_importer)
        self.source_manager = SourceManager(self.db)
        self.source_monitor = SourceMonitor(self.db, self.source_manager)
        self.clothing_recognizer = ClothingRecognizer()
        
        # 确保主用户存在
        self._ensure_main_user()
    
    def _ensure_main_user(self):
        """确保主用户存在"""
        members = self.member_manager.get_all_members()
        has_self = any(m.relationship == "self" for m in members)
        
        if not has_self:
            # 创建主用户
            self.member_manager.add_member(
                name="我",
                relationship="self",
                gender=None
            )
    
    async def process_input(
        self, 
        text: str, 
        image_url: Optional[str] = None,
        image_data: Optional[bytes] = None
    ) -> Dict[str, Any]:
        """处理用户输入
        
        Args:
            text: 用户文本
            image_url: 图片 URL（可选）
            image_data: 图片二进制数据（可选）
            
        Returns:
            响应消息
        """
        # 1. 如果有图片，优先处理图片
        if image_url or image_data:
            return await self._handle_image(text, image_url, image_data)
        
        # 2. 解析命令
        command = self.command_parser.parse(text)
        
        # 3. 处理初始化流程（如果正在进行中）
        current_member_id = self.session_manager.get_current_member_id()
        if current_member_id and self.initializer.is_in_init(current_member_id):
            return self._handle_init_answer(command)
        
        # 4. 根据意图路由
        return await self._route_by_intent(command)
    
    async def _route_by_intent(self, command: ParsedCommand) -> Dict[str, Any]:
        """根据意图路由"""
        intent = command.intent
        
        # 成员管理
        if intent == Intent.ADD_MEMBER:
            return self._handle_add_member(command)
        
        if intent == Intent.SWITCH_MEMBER:
            return self._handle_switch_member(command)
        
        if intent == Intent.LIST_MEMBERS:
            return self._handle_list_members()
        
        # 初始化
        if intent == Intent.INIT_PROFILE:
            return self._handle_start_init()
        
        # 淘宝导入
        if intent == Intent.IMPORT_ORDER:
            return await self._handle_taobao_import(command)
        
        # 关注店铺
        if intent == Intent.FOLLOW_SHOP:
            return self._handle_follow_shop(command)
        
        if intent == Intent.CHECK_NEW:
            return await self._handle_check_new()
        
        # 衣橱管理
        if intent == Intent.ADD_ITEM:
            return await self._handle_add_item(command)
        
        if intent == Intent.LIST_ITEMS:
            return self._handle_list_items(command)
        
        # 搭配推荐
        if intent == Intent.GET_RECOMMENDATION:
            return await self._handle_recommendation(command)
        
        # 衣橱分析
        if intent == Intent.ANALYZE_WARDROBE:
            return self._handle_analysis()
        
        # 种草
        if intent == Intent.ADD_WISHLIST:
            return await self._handle_add_wishlist(command)
        
        if intent == Intent.CHECK_WISHLIST:
            return self._handle_check_wishlist()
        
        # 帮助
        if intent == Intent.HELP:
            return self._handle_help()
        
        # 未知
        return self._handle_unknown(command)
    
    # ============ 成员管理处理 ============
    
    def _handle_add_member(self, command: ParsedCommand) -> Dict[str, Any]:
        """处理添加成员"""
        # 引导用户输入成员信息
        content = """## 👨‍👩‍👧‍👦 添加家庭成员

请告诉我新成员的信息：

**格式示例：**
- 「给老公建个衣橱」
- 「添加小孩」
- 「添加我妈妈」

**支持的成员类型：**
- 👨 老公/配偶
- 👧 小孩/孩子
- 👴 父母

---
💡 *每个成员可以独立管理自己的衣橱*
"""
        return MessageBuilder.build_markdown("添加成员", content)
    
    def _handle_switch_member(self, command: ParsedCommand) -> Dict[str, Any]:
        """处理切换成员"""
        member_name = command.member_name
        member_id = command.member_id
        
        if not member_id and member_name:
            # 尝试通过名称切换
            member = self.session_manager.switch_member_by_name(member_name)
            if member:
                current_member = self.member_manager.get_member(
                    self.session_manager.get_current_member_id()
                )
                return MessageBuilder.build_member_switch_message(
                    {'name': current_member.name, 'avatar': current_member.avatar},
                    {'name': member.name, 'avatar': member.avatar}
                )
        
        if member_id:
            self.session_manager.switch_member(member_id)
            member = self.member_manager.get_member(member_id)
            return MessageBuilder.build_markdown(
                "切换成功",
                f"## ✅ 已切换\n\n当前正在查看 **{member.avatar} {member.name}** 的衣橱"
            )
        
        # 未找到成员
        members = self.member_manager.list_members_for_display()
        lines = ["## ⚠️ 未找到该成员\n", "当前家庭成员："]
        for m in members:
            lines.append(f"- {m['avatar']} {m['name']}")
        
        return MessageBuilder.build_markdown("未找到成员", "\n".join(lines))
    
    def _handle_list_members(self) -> Dict[str, Any]:
        """处理列出成员"""
        members = self.member_manager.list_members_for_display()
        return MessageBuilder.build_member_list_message(members)
    
    # ============ 初始化处理 ============
    
    def _handle_start_init(self) -> Dict[str, Any]:
        """处理开始初始化"""
        member_id = self.session_manager.get_current_member_id()
        if not member_id:
            return MessageBuilder.build_text("请先选择一个成员")
        
        result = self.initializer.start_init(member_id)
        return self._format_init_response(result)
    
    def _handle_init_answer(self, command: ParsedCommand) -> Dict[str, Any]:
        """处理初始化回答"""
        member_id = self.session_manager.get_current_member_id()
        
        # 从文本中提取回答
        answer = command.raw_text
        
        result = self.initializer.process_answer(member_id, answer)
        return self._format_init_response(result)
    
    def _format_init_response(self, result: Dict) -> Dict[str, Any]:
        """格式化初始化响应"""
        if result.get('status') == 'complete':
            profile = result.get('profile', {})
            return MessageBuilder.build_markdown(
                "初始化完成",
                f"""## ✅ 信息已保存

**感谢您完成信息填写！**

现在我可以：
- 根据您的身材推荐更合身的搭配
- 了解您的风格偏好
- 给出更个性化的建议

---
**下一步：**
- 拍照添加第一件衣服 📸
- 说「今天穿什么」试试看 ✨
"""
            )
        
        if result.get('status') == 'error':
            return MessageBuilder.build_markdown("⚠️ 提示", result.get('message', '请重新输入'))
        
        # 进行中
        step = result
        content = f"""## 📝 完善个人信息

**进度：** {step.get('progress', '')} {step.get('step_number', 1)}/{step.get('total_steps', 1)}

### {step.get('question', '')}

"""
        if step.get('description'):
            content += f"*{step.get('description')}*\n\n"
        
        if step.get('options'):
            content += "**选项：**\n"
            for opt in step['options']:
                content += f"- {opt['label']}\n"
            content += "\n"
        
        content += f"💡 *输入「{step.get('skip_keyword', '跳过')}」可以跳过此问题*"
        
        return MessageBuilder.build_markdown("初始化", content)
    
    # ============ 衣橱管理处理 ============
    
    async def _handle_add_item(
        self, 
        command: ParsedCommand,
        image_url: Optional[str] = None,
        image_data: Optional[bytes] = None
    ) -> Dict[str, Any]:
        """处理添加单品"""
        # 这里需要调用 AI 识别模块
        # 暂时返回引导消息
        content = """## 📸 添加单品

**请拍照或发送图片给我，我来帮您录入！**

我会自动识别：
- 🏷️ 品类（外套、上衣、裤子等）
- 🎨 颜色
- ✨ 风格

---
💡 *也可以说「录入一件白衬衫」手动添加*
"""
        return MessageBuilder.build_markdown("添加单品", content)
    
    async def _handle_image(
        self, 
        text: str, 
        image_url: Optional[str],
        image_data: Optional[bytes]
    ) -> Dict[str, Any]:
        """处理图片输入"""
        member_id = self.session_manager.get_current_member_id()
        member = self.member_manager.get_member(member_id) if member_id else None
        
        # 下载或保存图片
        local_path = None
        if image_url:
            local_path = await self.image_service.download_image(image_url)
        elif image_data:
            import uuid
            item_id = f"item_{uuid.uuid4().hex[:8]}"
            local_path = self.image_service.save_item_image(image_data, item_id)
        
        if not local_path:
            return MessageBuilder.build_markdown(
                "处理失败",
                "图片处理失败，请重试"
            )
        
        # 使用 AI 识别服装属性
        attributes = await self.clothing_recognizer.recognize_from_image(local_path)
        
        if attributes.category == 'unknown':
            # 识别失败，请求用户帮助
            return MessageBuilder.build_markdown(
                "需要帮助",
                f"""## 📸 图片已收到

我没能完全识别这件单品，能告诉我吗？

**请回复：**
- 品类（外套/上衣/裤子/裙子/鞋子/配饰）
- 颜色
- 风格（可选）

**示例：** 「这是一件白色T恤」

---
📷 *图片已保存*
"""
            )
        
        # 识别成功，自动添加
        item_data = {
            'name': f"{attributes.color}{attributes.subcategory}" if attributes.subcategory else f"{attributes.color}{attributes.category}",
            'category': attributes.category,
            'color': attributes.color,
            'style': attributes.style,
            'season': attributes.season,
            'material': attributes.material,
            'source': 'photo',
            'image_path': local_path
        }
        
        item_id = self.db.add_item(item_data, member_id)
        
        return MessageBuilder.build_item_added_message(
            item_data,
            {'name': member.name, 'avatar': member.avatar} if member else None
        )
    
    def _handle_list_items(self, command: ParsedCommand) -> Dict[str, Any]:
        """处理查看衣橱"""
        member_id = self.session_manager.get_current_member_id()
        member = self.member_manager.get_member(member_id) if member_id else None
        
        category = command.category
        items = self.db.get_all_items(category=category, member_id=member_id)
        
        return MessageBuilder.build_wardrobe_overview(items, member)
    
    # ============ 搭配推荐处理 ============
    
    async def _handle_recommendation(self, command: ParsedCommand) -> Dict[str, Any]:
        """处理搭配推荐"""
        # 识别目标成员
        member, switched = self.session_manager.recognize_and_switch(command.raw_text)
        
        member_id = self.session_manager.get_current_member_id()
        member = self.member_manager.get_member(member_id) if member_id else None
        profile = self.member_manager.get_profile(member_id) if member_id else None
        
        # 获取天气
        weather = await self._get_weather()
        
        # 获取衣橱单品
        items = self.db.get_all_items(member_id=member_id)
        
        if not items:
            return MessageBuilder.build_markdown(
                "衣橱是空的",
                f"""## 👗 衣橱空空如也

{member.name if member else '您'}的衣橱还没有衣服呢！

**添加方式：**
1. 拍照发给我
2. 说「从淘宝导入」导入已购商品

---
💡 *添加几件衣服后我就能推荐搭配啦*
"""
            )
        
        # 使用推荐器生成推荐
        outfits = self.recommender.recommend(
            occasion="日常",
            weather=weather,
            count=3,
            member_id=member_id,
            member_profile=profile.to_dict() if profile else None
        )
        
        # 构建消息
        return MessageBuilder.build_recommendation_message(outfits, weather, member)
    
    async def _get_weather(self, lat: float = 39.9, lon: float = 116.4) -> Optional[Dict]:
        """获取天气信息"""
        try:
            import httpx
            async with httpx.AsyncClient(timeout=5) as client:
                url = "https://api.open-meteo.com/v1/forecast"
                params = {
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,weather_code",
                    "timezone": "auto"
                }
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    current = data.get('current', {})
                    weather_codes = {
                        0: "晴", 1: "晴", 2: "多云", 3: "阴",
                        45: "雾", 48: "雾", 51: "小雨", 53: "小雨", 55: "中雨",
                        61: "小雨", 63: "中雨", 65: "大雨", 71: "小雪", 73: "中雪", 75: "大雪",
                        80: "阵雨", 81: "阵雨", 82: "暴雨", 95: "雷阵雨"
                    }
                    code = current.get('weather_code', 0)
                    return {
                        'temperature': current.get('temperature_2m'),
                        'weather': weather_codes.get(code, "未知"),
                        'weather_code': code
                    }
        except:
            pass
        return None
    
    # ============ 分析处理 ============
    
    def _handle_analysis(self) -> Dict[str, Any]:
        """处理衣橱分析"""
        member_id = self.session_manager.get_current_member_id()
        items = self.db.get_all_items(member_id=member_id)
        
        # 统计
        categories = {}
        colors = {}
        seasons = {}
        
        for item in items:
            cat = item.get('category', 'other')
            categories[cat] = categories.get(cat, 0) + 1
            
            color = item.get('color', '未知')
            colors[color] = colors.get(color, 0) + 1
            
            season = item.get('season', '四季')
            seasons[season] = seasons.get(season, 0) + 1
        
        analysis = {
            'categories': categories,
            'colors': colors,
            'seasons': seasons,
            'tips': [
                f"您的衣橱共有 {len(items)} 件单品",
                f"最常见品类：{max(categories, key=categories.get) if categories else '无'}",
                f"最常见颜色：{max(colors, key=colors.get) if colors else '无'}",
            ]
        }
        
        return MessageBuilder.build_analysis_message(analysis)
    
    # ============ 淘宝导入处理 ============
    
    async def _handle_taobao_import(self, command: ParsedCommand) -> Dict[str, Any]:
        """处理淘宝导入"""
        member_id = self.session_manager.get_current_member_id()
        
        content = """## 📦 淘宝导入

**支持导入：**
- 🛒 已购订单
- ❤️ 收藏夹
- 🛍️ 购物车

**使用方法：**
1. 在淘宝APP中复制商品链接
2. 发给我，我会自动识别

**或者使用淘宝CLI：**
```
taobao orders --recent
```

---
💡 *导入后我会自动识别商品品类、颜色等信息*
"""
        return MessageBuilder.build_markdown("淘宝导入", content)
    
    async def import_from_taobao_data(
        self, 
        data: Dict, 
        data_type: str = 'order'
    ) -> Dict[str, Any]:
        """从淘宝数据导入
        
        Args:
            data: 淘宝数据（订单/购物车/收藏夹）
            data_type: 数据类型
            
        Returns:
            导入结果
        """
        member_id = self.session_manager.get_current_member_id()
        
        # 开始导入会话
        result = self.taobao_session.start_session(data, data_type, member_id)
        
        if result.get('error'):
            return MessageBuilder.build_markdown("导入失败", result['error'])
        
        return MessageBuilder.build_markdown("导入预览", result['message'])
    
    async def confirm_taobao_import(self) -> Dict[str, Any]:
        """确认淘宝导入"""
        result = await self.taobao_session.confirm_import()
        
        if result.get('error'):
            return MessageBuilder.build_markdown("导入失败", result['error'])
        
        return MessageBuilder.build_markdown("导入完成", result['message'])
    
    # ============ 关注店铺处理 ============
    
    def _handle_follow_shop(self, command: ParsedCommand) -> Dict[str, Any]:
        """处理关注店铺"""
        member_id = self.session_manager.get_current_member_id()
        sources = self.source_manager.get_sources(member_id)
        
        if sources:
            lines = ["## 🏪 我的关注\n"]
            for s in sources:
                type_name = self.source_manager.SOURCE_TYPE_NAMES.get(s['source_type'], s['source_type'])
                lines.append(f"**{s['name']}** ({type_name})")
                if s.get('last_checked'):
                    lines.append(f"  上次检查：{s['last_checked'][:10]}")
                lines.append("")
            
            lines.append("---\n")
            lines.append("**管理操作：**\n")
            lines.append("- 「检查上新」- 查看关注店铺的新品")
            lines.append("- 发送店铺链接 - 添加新关注")
        else:
            lines = ["## 🏪 关注店铺\n"]
            lines.append("您还没有关注任何店铺。\n\n")
            lines.append("**添加方式：**\n")
            lines.append("- 发送淘宝店铺链接给我\n")
            lines.append("- 说「关注XX店」")
        
        return MessageBuilder.build_markdown("关注店铺", "\n".join(lines))
    
    async def _handle_check_new(self) -> Dict[str, Any]:
        """处理检查上新"""
        member_id = self.session_manager.get_current_member_id()
        
        # 获取新品
        new_items = self.source_monitor.get_new_items(member_id)
        
        if not new_items:
            return MessageBuilder.build_markdown(
                "检查上新",
                """## 🔍 检查上新

暂无新品上架。

---
💡 *我会定期检查您关注的店铺，有新品会第一时间通知您*
"""
            )
        
        lines = [f"## ✨ 发现 {len(new_items)} 件新品\n"]
        
        for item in new_items[:10]:
            lines.append(f"**{item['name']}**")
            lines.append(f"  店铺：{item.get('source_name', '未知')}")
            if item.get('price'):
                lines.append(f"  价格：¥{item['price']}")
            lines.append("")
        
        if len(new_items) > 10:
            lines.append(f"... 还有 {len(new_items) - 10} 件新品")
        
        return MessageBuilder.build_markdown("新品上架", "\n".join(lines))
    
    async def add_followed_source(
        self,
        source_type: str,
        name: str,
        url: str = None,
        external_id: str = None
    ) -> Dict[str, Any]:
        """添加关注来源"""
        member_id = self.session_manager.get_current_member_id()
        
        source_id = self.source_manager.add_source(
            source_type=source_type,
            name=name,
            url=url,
            external_id=external_id,
            member_id=member_id
        )
        
        return MessageBuilder.build_markdown(
            "关注成功",
            f"""## ✅ 已关注

**{name}**

我会定期检查上新，有适合您的商品会通知您！

---
💡 *说「检查上新」查看最新上架*
"""
        )
    
    # ============ 种草处理 ============
    
    async def _handle_add_wishlist(self, command: ParsedCommand) -> Dict[str, Any]:
        """处理添加种草"""
        return MessageBuilder.build_markdown(
            "种草功能",
            "🚧 种草功能开发中，敬请期待！"
        )
    
    def _handle_check_wishlist(self) -> Dict[str, Any]:
        """处理查看种草"""
        return MessageBuilder.build_markdown(
            "种草清单",
            "🚧 种草功能开发中，敬请期待！"
        )
    
    # ============ 其他处理 ============
    
    def _handle_help(self) -> Dict[str, Any]:
        """处理帮助"""
        content = """## 👗 Clothy 功能指南

### 📸 衣橱管理
- 拍照添加单品
- 「录入一件白衬衫」
- 「看看我的衣橱」
- 「查看外套」

### ✨ 搭配推荐
- 「今天我穿什么？」
- 「给我推荐一套搭配」
- 「老公今天穿什么？」

### 📊 分析统计
- 「衣橱分析」
- 「我的衣服分布」

### 👨‍👩‍👧‍👦 多人衣橱
- 「添加家庭成员」
- 「切换到老公的衣橱」
- 「家庭成员」

### 🛒 种草逛街
- 「种草这件」
- 「看看种草清单」

### ⚙️ 其他
- 「初始化」- 完善个人信息
- 「帮助」- 查看功能列表

---
💡 *随时拍照发给我，我来帮你录入！*
"""
        return MessageBuilder.build_markdown("帮助", content)
    
    def _handle_unknown(self, command: ParsedCommand) -> Dict[str, Any]:
        """处理未知命令"""
        suggestion = self.command_parser.get_suggested_response(command)
        return MessageBuilder.build_markdown("提示", suggestion)
    
    # ============ 状态查询 ============
    
    def get_context(self) -> Dict[str, Any]:
        """获取当前上下文"""
        return self.session_manager.get_session_context()