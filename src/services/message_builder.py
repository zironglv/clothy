"""
消息构建服务
构建钉钉消息格式
"""

from typing import List, Dict, Any, Optional
from datetime import datetime


class MessageBuilder:
    """消息构建器
    
    构建各种类型的钉钉消息：
    - Markdown 消息
    - Link 卡片
    - ActionCard 按钮
    - FeedCard 图文列表
    """
    
    @staticmethod
    def build_text(text: str) -> Dict[str, Any]:
        """构建纯文本消息"""
        return {
            "msgtype": "text",
            "text": {
                "content": text
            }
        }
    
    @staticmethod
    def build_markdown(title: str, content: str) -> Dict[str, Any]:
        """构建 Markdown 消息
        
        Args:
            title: 消息标题
            content: Markdown 内容
        """
        return {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": content
            }
        }
    
    @staticmethod
    def build_link(title: str, text: str, url: str, pic_url: str = None) -> Dict[str, Any]:
        """构建 Link 卡片消息"""
        msg = {
            "msgtype": "link",
            "link": {
                "title": title,
                "text": text,
                "messageUrl": url
            }
        }
        if pic_url:
            msg["link"]["picUrl"] = pic_url
        return msg
    
    @staticmethod
    def build_action_card(title: str, text: str, buttons: List[Dict[str, str]]) -> Dict[str, Any]:
        """构建 ActionCard 按钮消息
        
        Args:
            title: 标题
            text: 内容
            buttons: 按钮列表，每个按钮格式：{"title": "按钮文字", "actionURL": "链接"}
        """
        return {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": text,
                "btns": buttons
            }
        }
    
    @staticmethod
    def build_feed_card(items: List[Dict[str, str]]) -> Dict[str, Any]:
        """构建 FeedCard 图文列表消息
        
        Args:
            items: 图文列表，每项格式：{"title": "标题", "messageURL": "链接", "picURL": "图片"}
        """
        return {
            "msgtype": "feedCard",
            "feedCard": {
                "links": items
            }
        }
    
    # ============ 业务消息构建 ============
    
    @classmethod
    def build_welcome_message(cls, member_name: str = None, has_items: bool = False) -> Dict[str, Any]:
        """构建欢迎消息"""
        name = f"{member_name}的" if member_name else ""
        
        if has_items:
            content = f"""## 👗 Clothy - 你的AI穿搭闺蜜

欢迎回来！{name}衣橱已准备就绪。

**你可以这样问我：**
- 「今天{member_name or '我'}穿什么？」- 获取今日搭配
- 「看看{member_name or '我'}的衣橱」- 查看单品
- 「给{member_name or '我'}推荐一套衣服」- 搭配建议

**衣橱管理：**
- 直接拍照发给我，帮你录入
- 「录入一件白衬衫」- 手动添加
- 「我的衣橱分析」- 查看衣橱统计

---

💡 *需要帮助？发送「帮助」查看完整功能列表*
"""
        else:
            content = f"""## 👗 Clothy - 你的AI穿搭闺蜜

你好！我是你的穿搭助手，帮你管理{name or '衣橱'}、推荐搭配。

**开始使用：**
1. 拍一张衣服照片发给我
2. 或者说「初始化」让我了解你的身材和偏好

**我能做什么：**
- 📸 拍照录入衣橱
- 👔 智能搭配推荐
- 📊 衣橱分析统计
- 🛒 种草清单管理
- 👨‍👩‍👧‍👦 多人衣橱管理

---

💡 *发送「帮助」查看更多功能*
"""
        
        return cls.build_markdown("Clothy 欢迎你", content)
    
    @classmethod
    def build_member_switch_message(cls, from_member: Dict, to_member: Dict) -> Dict[str, Any]:
        """构建成员切换消息"""
        content = f"""## 👋 已切换衣橱

**{from_member['avatar']} {from_member['name']}** → **{to_member['avatar']} {to_member['name']}**

当前正在查看 **{to_member['name']}** 的衣橱。

---

💡 *说「回到我的衣橱」可以切换回来*
"""
        return cls.build_markdown("衣橱切换", content)
    
    @classmethod
    def build_member_list_message(cls, members: List[Dict]) -> Dict[str, Any]:
        """构建成员列表消息"""
        lines = ["## 👨‍👩‍👧‍👦 家庭成员\n"]
        
        for m in members:
            status = "✅ 已初始化" if m.get('is_initialized') else "⏳ 待完善"
            items = f"（{m.get('item_count', 0)}件单品）" if m.get('item_count') else ""
            lines.append(f"**{m['avatar']} {m['name']}** {status} {items}")
        
        lines.append("\n---\n")
        lines.append("**管理操作：**")
        lines.append("- 「添加家庭成员」- 添加新成员")
        lines.append("- 「切换到XX的衣橱」- 查看其他成员衣橱")
        
        return cls.build_markdown("家庭成员", "\n".join(lines))
    
    @classmethod
    def build_item_added_message(cls, item: Dict, member: Dict = None) -> Dict[str, Any]:
        """构建单品添加成功消息"""
        member_name = member.get('name', '') if member else ''
        
        content = f"""## ✅ 单品已录入

**{item['name']}**

- 品类：{item.get('category', '未分类')}
- 颜色：{item.get('color', '未设置')}
- 风格：{item.get('style', '未设置')}
- 季节：{item.get('season', '四季')}

"""
        if member_name:
            content += f"已添加到 {member['avatar']} {member_name} 的衣橱\n\n"
        
        content += "---\n**下一步：**\n- 继续拍照添加更多单品\n- 说「今天穿什么」获取搭配推荐"
        
        return cls.build_markdown("录入成功", content)
    
    @classmethod
    def build_wardrobe_overview(cls, items: List[Dict], member: Dict = None) -> Dict[str, Any]:
        """构建衣橱概览消息"""
        member_name = member.get('name', '') if member else ''
        
        # 按品类统计
        categories = {}
        for item in items:
            cat = item.get('category', 'other')
            categories[cat] = categories.get(cat, 0) + 1
        
        cat_names = {
            'outer': '外套',
            'top': '上装',
            'bottom': '下装',
            'shoes': '鞋子',
            'accessory': '配饰',
            'other': '其他'
        }
        
        lines = [f"## 👗 {member_name or '我'}的衣橱\n"]
        lines.append(f"**共 {len(items)} 件单品**\n")
        
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            lines.append(f"- {cat_names.get(cat, cat)}：{count}件")
        
        lines.append("\n---\n")
        lines.append("**操作：**")
        lines.append("- 「查看外套」- 按品类筛选")
        lines.append("- 「今天穿什么」- 搭配推荐")
        lines.append("- 「衣橱分析」- 详细统计")
        
        return cls.build_markdown("衣橱概览", "\n".join(lines))
    
    @classmethod
    def build_recommendation_message(
        cls, 
        outfits: List[Dict], 
        weather: Optional[Dict],
        member: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """构建搭配推荐消息"""
        lines = ["## ✨ 今日搭配建议\n"]
        
        # 天气信息
        if weather:
            temp = weather.get('temperature', '')
            weather_desc = weather.get('weather', '')
            lines.append(f"**今日天气：** {temp}°C {weather_desc}\n")
        
        # 成员信息
        if member:
            lines.append(f"**{member.get('avatar', '👤')} {member.get('name', '')}的衣橱**\n")
        
        lines.append("---\n")
        
        if not outfits:
            lines.append("暂时没有合适的搭配推荐。\n")
            lines.append("\n**建议：**\n")
            lines.append("- 多添加一些不同类型的单品\n")
            lines.append("- 完善风格偏好信息")
        else:
            for i, outfit in enumerate(outfits[:3], 1):
                lines.append(f"### 方案 {i}")
                
                style = outfit.get('style', '日常风格')
                lines.append(f"*{style}风格*\n")
                
                items = outfit.get('items', [])
                if items:
                    for item in items:
                        # 判断品类添加表情
                        emoji = '👔'
                        item_lower = item.lower() if isinstance(item, str) else str(item).lower()
                        if any(kw in item_lower for kw in ['外套', '大衣', '西装', '夹克']):
                            emoji = '🧥'
                        elif any(kw in item_lower for kw in ['t恤', '衬衫', '毛衣', '卫衣', '上衣']):
                            emoji = '👕'
                        elif any(kw in item_lower for kw in ['裤', '裙', '牛仔']):
                            emoji = '👖'
                        elif any(kw in item_lower for kw in ['鞋', '靴']):
                            emoji = '👟'
                        elif any(kw in item_lower for kw in ['包', '帽', '围巾', '配饰']):
                            emoji = '👜'
                        
                        lines.append(f"{emoji} **{item}**")
                
                tips = outfit.get('tips', '')
                if tips:
                    lines.append(f"\n💡 {tips}")
                
                lines.append("\n")
        
        lines.append("---")
        lines.append("\n*说「换一套」获取更多推荐*")
        
        return cls.build_markdown("搭配推荐", "\n".join(lines))
    
    @classmethod
    def build_weather_alert(cls, weather: Dict, tips: List[str]) -> Dict[str, Any]:
        """构建天气提醒消息"""
        lines = [f"## 🌤️ 天气提醒\n"]
        
        lines.append(f"**今日天气：** {weather.get('temperature', '')}°C")
        lines.append(f"**天气状况：** {weather.get('weather', '')}")
        
        if weather.get('rain_probability'):
            lines.append(f"**降雨概率：** {weather.get('rain_probability')}%")
        
        lines.append("\n**穿搭建议：**")
        for tip in tips:
            lines.append(f"- {tip}")
        
        return cls.build_markdown("天气提醒", "\n".join(lines))
    
    @classmethod
    def build_profile_init_message(cls, step: int, total: int, question: str) -> Dict[str, Any]:
        """构建画像初始化消息"""
        progress = "■" * step + "□" * (total - step)
        
        content = f"""## 📝 完善个人信息

**进度：** [{progress}] {step}/{total}

{question}

---

💡 *随时可以跳过，后续再说「完善信息」继续*
"""
        return cls.build_markdown("初始化", content)
    
    @classmethod
    def build_analysis_message(cls, analysis: Dict) -> Dict[str, Any]:
        """构建衣橱分析消息"""
        lines = ["## 📊 衣橱分析报告\n"]
        
        # 品类分布
        lines.append("### 品类分布")
        for cat, count in analysis.get('categories', {}).items():
            lines.append(f"- {cat}：{count}件")
        
        # 颜色分布
        lines.append("\n### 颜色分布")
        for color, count in analysis.get('colors', {}).items():
            lines.append(f"- {color}：{count}件")
        
        # 季节分布
        lines.append("\n### 季节分布")
        for season, count in analysis.get('seasons', {}).items():
            lines.append(f"- {season}：{count}件")
        
        # 建议
        lines.append("\n### 💡 搭配建议")
        for tip in analysis.get('tips', []):
            lines.append(f"- {tip}")
        
        return cls.build_markdown("衣橱分析", "\n".join(lines))
    
    @classmethod
    def build_child_tip(cls, child_age: int, weather: Dict = None) -> List[str]:
        """构建儿童穿搭建议"""
        tips = []
        
        if child_age < 3:
            tips = [
                "👶 宝宝还小，选择方便换尿布的衣服",
                "面料要柔软透气，避免粗糙材质",
                "选择包脚款式或准备小袜子，避免着凉"
            ]
        elif child_age < 6:
            tips = [
                "🧒 孩子好动，选择方便活动的款式",
                "避免有小装饰的衣服，防止误吞",
                "准备一套备用衣物，应对意外弄脏"
            ]
        else:
            tips = [
                "👧 可以让孩子参与选择衣服",
                "注意学校是否有着装要求",
                "选择耐脏、好清洗的面料"
            ]
        
        if weather:
            if weather.get('temperature', 30) > 30:
                tips.append("☀️ 天气热，孩子好动易出汗，选择透气面料")
            elif weather.get('temperature', 15) < 15:
                tips.append("🧥 天气转凉，准备薄外套备用")
            
            if '雨' in weather.get('weather', ''):
                tips.append("🌧️ 下雨天，准备雨衣雨靴，孩子喜欢踩水")
        
        return tips


def format_item_list(items: List[Dict], max_display: int = 10) -> str:
    """格式化单品列表"""
    lines = []
    
    for i, item in enumerate(items[:max_display], 1):
        cat_emoji = {
            'outer': '🧥', 'top': '👕', 'bottom': '👖', 
            'shoes': '👟', 'accessory': '👜'
        }.get(item.get('category'), '👔')
        
        color = item.get('color', '')
        style = item.get('style', '')
        info = f"{color} {style}".strip()
        
        lines.append(f"{i}. {cat_emoji} **{item.get('name', '')}** {'- ' + info if info else ''}")
    
    if len(items) > max_display:
        lines.append(f"\n... 还有 {len(items) - max_display} 件单品")
    
    return "\n".join(lines)