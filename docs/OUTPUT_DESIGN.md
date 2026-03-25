# StyleBuddy 输出与推送设计

> 图文并茂 + 多渠道推送

---

## 一、输出设计原则

### 1.1 核心原则

```
┌─────────────────────────────────────────────────────────────────┐
│                      输出设计原则                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 图文并茂 ─── 每个推荐都带商品图片                           │
│                                                                 │
│  2. 渠道无关 ─── 支持钉钉/微信/飞书/短信等多渠道                 │
│                                                                 │
│  3. 格式适配 ─── 根据渠道能力选择最佳展示格式                   │
│                                                                 │
│  4. 交互友好 ─── 支持按钮操作、链接跳转                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 图文输出场景

| 场景 | 图片内容 | 展示方式 |
|------|---------|---------|
| 今日穿搭推荐 | 衣橱单品图片/淘宝商品图 | 多图拼接 + 文字说明 |
| 店铺上新推送 | 商品主图 | 卡片式展示 |
| 种草咨询 | 商品图片 + 可搭配单品图 | 对比展示 |
| 衣橱分析 | 统计图表 | 可视化图表 |

---

## 二、消息格式设计

### 2.1 今日穿搭推荐（核心场景）

```
┌─────────────────────────────────────────────────────────────────┐
│                    今日穿搭推荐                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  🌤️ 北京 18°C 多云                                      │   │
│  │  👤 梨形身材 · 极简通勤风格                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
│  │         │  │         │  │         │  │         │          │
│  │  👔     │  │  👖     │  │  👟     │  │  💍     │          │
│  │ 白衬衫  │  │ A字裙   │  │ 乐福鞋  │  │ 项链    │          │
│  │         │  │         │  │         │  │         │          │
│  │ [图片]  │  │ [图片]  │  │ [图片]  │  │ [图片]  │          │
│  │         │  │         │  │         │  │         │          │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘          │
│                                                                 │
│  💡 搭配说明：                                                  │
│  • 高腰A字裙修饰臀部线条，适合梨形身材                          │
│  • 白衬衫+米色半裙=通勤经典组合                                 │
│  • 同色系鞋包更显高级感                                        │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  [换一套]  [调整风格]  [记录今天穿了]  [分享搭配]        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**图片来源**：
- 衣橱单品：用户拍照录入时的图片
- 淘宝导入：商品主图 URL
- 本地图片：存储在 `assets/images/wardrobe/`

### 2.2 店铺上新推送

```
┌─────────────────────────────────────────────────────────────────┐
│                    店铺上新推送                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🌅 早安！你关注的店铺有上新啦                                   │
│  📅 2024-01-15                                                 │
│                                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                 │
│  🏪 ONLY官方旗舰店                                              │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ┌────────┐                                              │  │
│  │  │        │  米色羊毛大衣                                │  │
│  │  │ [商品图]│  ¥899                                       │  │
│  │  │        │  风格：通勤优雅                              │  │
│  │  └────────┘  匹配度：⭐⭐⭐⭐⭐                           │  │
│  │                                                          │  │
│  │  💬 "这款大衣很适合你的极简通勤风格，米色与你衣橱百搭"    │  │
│  │                                                          │  │
│  │  [查看详情]  [加入种草清单]                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ┌────────┐                                              │  │
│  │  │        │  黑色针织连衣裙                              │  │
│  │  │ [商品图]│  ¥399                                       │  │
│  │  │        │  风格：优雅知性                              │  │
│  │  └────────┘  匹配度：⭐⭐⭐⭐                             │  │
│  │                                                          │  │
│  │  💬 "你衣橱有类似款，确认是否需要"                        │  │
│  │                                                          │  │
│  │  [查看详情]  [加入种草清单]                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                 │
│  💡 今日推荐：米色羊毛大衣匹配度最高！                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 种草咨询结果

```
┌─────────────────────────────────────────────────────────────────┐
│                    种草咨询结果                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  👗 商品分析                                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ┌────────────┐                                          │  │
│  │  │            │  米色针织开衫                            │  │
│  │  │  [商品图]  │  类型：外套                              │  │
│  │  │            │  风格：温柔/通勤/休闲                    │  │
│  │  └────────────┘  季节：春秋                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  🔍 与你衣橱的匹配度                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  可搭配单品：                                                   │
│                                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                        │
│  │         │  │         │  │         │                        │
│  │ [图片]  │  │ [图片]  │  │ [图片]  │                        │
│  │         │  │         │  │         │                        │
│  │ 白T恤×3 │  │ 牛仔裤×2│  │ 米色半裙│                        │
│  └─────────┘  └─────────┘  └─────────┘                        │
│                                                                 │
│  💡 购买建议：推荐购买！                                        │
│  • 你衣橱里缺少针织开衫，补充后搭配更丰富                       │
│  • 米色与你现有衣服百搭，利用率高                               │
│  • 符合你的极简通勤风格                                        │
│                                                                 │
│  ⚠️ 注意：你已有一件灰色针织衫，确认是否需要两件？              │
│                                                                 │
│  [加入种草清单]  [跳转淘宝购买]  [不感兴趣]                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 三、多渠道推送架构

### 3.1 架构设计

```
┌─────────────────────────────────────────────────────────────────┐
│                      消息输出架构                                │
└─────────────────────────────────────────────────────────────────┘

                        ┌─────────────┐
                        │  消息内容   │
                        │  (结构化)   │
                        └──────┬──────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Channel Router    │
                    │   (渠道路由器)      │
                    └──────────┬──────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   钉钉      │       │   微信      │       │   飞书      │
│  Adapter    │       │  Adapter    │       │  Adapter    │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ ActionCard  │       │ 图文消息    │       │ 富文本卡片  │
│ FeedCard    │       │ 小程序卡片  │       │ 交互卡片    │
│ Markdown    │       │ 客服消息    │       │ Markdown    │
└─────────────┘       └─────────────┘       └─────────────┘
         │                     │                     │
         ▼                     ▼                     ▼
    钉钉用户              微信用户               飞书用户
```

### 3.2 渠道适配器设计

```python
"""
渠道适配器基类
定义统一的消息输出接口
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class ImageContent:
    """图片内容"""
    url: Optional[str] = None       # 图片URL
    path: Optional[str] = None      # 本地路径
    base64: Optional[str] = None    # Base64编码
    caption: str = ""               # 图片说明

@dataclass
class OutfitRecommendation:
    """穿搭推荐消息"""
    weather: Dict                   # 天气信息
    user_profile: Dict              # 用户画像摘要
    
    items: List[Dict]               # 单品列表（含图片）
    # 每个item: {name, category, image, notes}
    
    tips: List[str]                 # 搭配说明
    actions: List[Dict]             # 操作按钮

@dataclass
class NewArrivalMessage:
    """上新推送消息"""
    date: str
    source_name: str
    
    items: List[Dict]               # 商品列表（含图片）
    # 每个item: {title, image, price, style, match_score, match_reason, selling_points}
    
    top_pick: Dict                  # 今日推荐

@dataclass
class ConsultationResult:
    """种草咨询结果"""
    item_analysis: Dict             # 商品分析
    item_image: ImageContent        # 商品图片
    
    wardrobe_matches: List[Dict]    # 可搭配单品（含图片）
    
    recommendation: str             # 购买建议
    reasons: List[str]              # 理由
    warnings: List[str]             # 注意事项
    
    actions: List[Dict]             # 操作按钮


class ChannelAdapter(ABC):
    """渠道适配器基类"""
    
    @property
    @abstractmethod
    def channel_name(self) -> str:
        """渠道名称"""
        pass
    
    @property
    @abstractmethod
    def capabilities(self) -> Dict[str, bool]:
        """
        渠道能力
        - image: 支持图片
        - markdown: 支持 Markdown
        - buttons: 支持按钮
        - carousel: 支持轮播
        - rich_card: 支持富文本卡片
        """
        pass
    
    @abstractmethod
    def send_outfit_recommendation(self, message: OutfitRecommendation) -> bool:
        """发送穿搭推荐"""
        pass
    
    @abstractmethod
    def send_new_arrivals(self, message: NewArrivalMessage) -> bool:
        """发送上新推送"""
        pass
    
    @abstractmethod
    def send_consultation(self, message: ConsultationResult) -> bool:
        """发送种草咨询结果"""
        pass
    
    @abstractmethod
    def send_text(self, text: str) -> bool:
        """发送纯文本"""
        pass
    
    def upload_image(self, image: ImageContent) -> Optional[str]:
        """
        上传图片，返回图片URL或媒体ID
        
        不同渠道的图片处理方式：
        - 钉钉：上传到钉钉服务器获取 mediaId
        - 微信：上传到微信服务器获取 media_id
        - 飞书：上传到飞书服务器获取 file_key
        """
        # 默认实现：返回原图URL或路径
        if image.url:
            return image.url
        elif image.path:
            # 子类可重写此方法上传图片
            return f"file://{image.path}"
        return None
```

### 3.3 钉钉适配器实现

```python
"""
钉钉渠道适配器
"""

import requests
from typing import Dict, List, Optional
import json

class DingTalkAdapter(ChannelAdapter):
    """钉钉适配器"""
    
    def __init__(self, webhook: str, access_token: str = None):
        self.webhook = webhook
        self.access_token = access_token
    
    @property
    def channel_name(self) -> str:
        return "dingtalk"
    
    @property
    def capabilities(self) -> Dict[str, bool]:
        return {
            "image": True,
            "markdown": True,
            "buttons": True,
            "carousel": False,
            "rich_card": True  # ActionCard
        }
    
    def send_outfit_recommendation(self, message: OutfitRecommendation) -> bool:
        """发送穿搭推荐 - 使用 ActionCard"""
        
        # 构建图文内容
        text_parts = [
            f"### 🌤️ {message.weather.get('city', '')} {message.weather.get('temp', '')}°C {message.weather.get('condition', '')}\n\n",
            f"👤 {message.user_profile.get('body_type_label', '')} · {message.user_profile.get('style_label', '')}\n\n",
            "---\n\n",
            "### 👗 今日穿搭\n\n"
        ]
        
        # 添加单品图片（使用 Markdown 图片语法）
        for item in message.items:
            image_url = item.get('image_url') or item.get('image_path')
            if image_url:
                text_parts.append(f"![{item['name']}]({image_url})\n\n")
            text_parts.append(f"**{item['name']}** ({item['category_label']})\n\n")
        
        # 添加搭配说明
        text_parts.append("---\n\n")
        text_parts.append("### 💡 搭配说明\n\n")
        for tip in message.tips:
            text_parts.append(f"• {tip}\n\n")
        
        # 构建 ActionCard
        payload = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": f"今日穿搭推荐 - {message.weather.get('temp', '')}°C",
                "text": "".join(text_parts),
                "btnOrientation": "1",
                "btns": [
                    {"title": "换一套", "actionURL": "stylebuddy://refresh_outfit"},
                    {"title": "记录今天穿了", "actionURL": "stylebuddy://log_outfit"}
                ]
            }
        }
        
        return self._send(payload)
    
    def send_new_arrivals(self, message: NewArrivalMessage) -> bool:
        """发送上新推送 - 使用 FeedCard"""
        
        links = []
        for item in message.items[:5]:  # 最多5个
            links.append({
                "title": f"{item['title']} ¥{item['price']} - 匹配度 {item['match_score']}%",
                "messageURL": item.get('url', ''),
                "picURL": item.get('image', '')
            })
        
        payload = {
            "msgtype": "feedCard",
            "feedCard": {
                "links": links
            }
        }
        
        return self._send(payload)
    
    def send_consultation(self, message: ConsultationResult) -> bool:
        """发送种草咨询结果 - 使用 Markdown"""
        
        text_parts = [
            "### 👗 商品分析\n\n",
            f"![商品图]({message.item_image.url})\n\n" if message.item_image.url else "",
            f"**{message.item_analysis.get('title', '')}**\n\n",
            f"类型：{message.item_analysis.get('category_label', '')}\n\n",
            f"风格：{', '.join(message.item_analysis.get('style_tags', []))}\n\n",
            "---\n\n",
            "### 🔍 可搭配单品\n\n"
        ]
        
        # 添加可搭配单品图片
        for match in message.wardrobe_matches:
            if match.get('image'):
                text_parts.append(f"![{match['name']}]({match['image']})\n\n")
            text_parts.append(f"• {match['name']}\n\n")
        
        # 添加建议
        text_parts.append("---\n\n")
        text_parts.append(f"### 💡 {message.recommendation}\n\n")
        for reason in message.reasons:
            text_parts.append(f"• {reason}\n\n")
        
        for warning in message.warnings:
            text_parts.append(f"⚠️ {warning}\n\n")
        
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "种草咨询结果",
                "text": "".join(text_parts)
            }
        }
        
        return self._send(payload)
    
    def send_text(self, text: str) -> bool:
        """发送纯文本"""
        payload = {
            "msgtype": "text",
            "text": {
                "content": text
            }
        }
        return self._send(payload)
    
    def upload_image(self, image: ImageContent) -> Optional[str]:
        """上传图片到钉钉"""
        if not self.access_token:
            return image.url
        
        # 调用钉钉媒体上传接口
        url = f"https://oapi.dingtalk.com/media/upload?access_token={self.access_token}&type=image"
        
        if image.path:
            with open(image.path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, files=files)
        elif image.base64:
            import base64
            import io
            image_data = base64.b64decode(image.base64)
            files = {'media': ('image.jpg', io.BytesIO(image_data))}
            response = requests.post(url, files=files)
        else:
            return image.url
        
        if response.status_code == 200:
            result = response.json()
            if result.get('errcode') == 0:
                return result.get('media_id')
        
        return None
    
    def _send(self, payload: Dict) -> bool:
        """发送消息"""
        response = requests.post(self.webhook, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result.get('errcode') == 0
        return False
```

### 3.4 微信适配器实现（示意）

```python
"""
微信渠道适配器
通过微信客服消息或模板消息发送
"""

class WeChatAdapter(ChannelAdapter):
    """微信适配器"""
    
    def __init__(self, appid: str, secret: str):
        self.appid = appid
        self.secret = secret
        self._access_token = None
    
    @property
    def channel_name(self) -> str:
        return "wechat"
    
    @property
    def capabilities(self) -> Dict[str, bool]:
        return {
            "image": True,
            "markdown": False,
            "buttons": False,
            "carousel": False,
            "rich_card": True  # 图文消息
        }
    
    def send_outfit_recommendation(self, message: OutfitRecommendation) -> bool:
        """发送穿搭推荐 - 使用图文消息"""
        
        # 上传图片获取 media_id
        media_ids = []
        for item in message.items:
            if item.get('image_path'):
                media_id = self._upload_media(item['image_path'], 'image')
                if media_id:
                    media_ids.append(media_id)
        
        if media_ids:
            # 发送图片消息
            for media_id in media_ids:
                self._send_image(media_id)
        
        # 发送文字说明
        text = self._format_outfit_text(message)
        return self._send_text(text)
    
    def send_new_arrivals(self, message: NewArrivalMessage) -> bool:
        """发送上新推送 - 使用图文消息"""
        
        articles = []
        for item in message.items[:8]:  # 最多8个
            articles.append({
                "title": f"{item['title']} ¥{item['price']}",
                "description": f"匹配度 {item['match_score']}% | {', '.join(item.get('style_tags', []))}",
                "url": item.get('url', ''),
                "picurl": item.get('image', '')
            })
        
        return self._send_news(articles)
    
    # ... 其他方法实现
```

### 3.5 飞书适配器实现（示意）

```python
"""
飞书渠道适配器
使用飞书机器人 Webhook
"""

class FeishuAdapter(ChannelAdapter):
    """飞书适配器"""
    
    def __init__(self, webhook: str, app_id: str = None, app_secret: str = None):
        self.webhook = webhook
        self.app_id = app_id
        self.app_secret = app_secret
    
    @property
    def channel_name(self) -> str:
        return "feishu"
    
    @property
    def capabilities(self) -> Dict[str, bool]:
        return {
            "image": True,
            "markdown": True,
            "buttons": True,
            "carousel": False,
            "rich_card": True  # 交互式卡片
        }
    
    def send_outfit_recommendation(self, message: OutfitRecommendation) -> bool:
        """发送穿搭推荐 - 使用交互式卡片"""
        
        # 构建卡片 JSON
        card = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"今日穿搭推荐 - {message.weather.get('temp', '')}°C"
                },
                "template": "blue"
            },
            "elements": []
        }
        
        # 添加单品图片和文字
        for item in message.items:
            if item.get('image_url'):
                card["elements"].append({
                    "tag": "img",
                    "img_key": self._upload_image(item['image_url']),
                    "alt": {
                        "tag": "plain_text",
                        "content": item['name']
                    }
                })
            
            card["elements"].append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**{item['name']}**\n{item['category_label']}"
                }
            })
        
        # 添加搭配说明
        tips_text = "\n".join([f"• {tip}" for tip in message.tips])
        card["elements"].append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**💡 搭配说明**\n{tips_text}"
            }
        })
        
        # 添加按钮
        card["elements"].append({
            "tag": "action",
            "actions": [
                {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "换一套"},
                    "type": "default",
                    "value": {"action": "refresh"}
                },
                {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "记录今天穿了"},
                    "type": "primary",
                    "value": {"action": "log"}
                }
            ]
        })
        
        payload = {
            "msg_type": "interactive",
            "card": card
        }
        
        return self._send(payload)
    
    # ... 其他方法实现
```

---

## 四、图片管理模块

### 4.1 图片存储设计

```
assets/images/
├── wardrobe/              # 衣橱单品图片
│   ├── item_001.jpg
│   ├── item_002.jpg
│   └── ...
├── taobao/               # 淘宝商品缓存图片
│   ├── shop_123456/
│   │   ├── item_789.jpg
│   │   └── ...
│   └── ...
├── outfits/              # 搭配组合图片（生成）
│   ├── outfit_20240115.jpg
│   └── ...
└── charts/               # 统计图表图片
    ├── category_dist.png
    └── color_dist.png
```

### 4.2 图片服务模块

```python
"""
图片服务模块
管理图片的上传、缓存、处理
"""

import os
import requests
import hashlib
from typing import Optional, Dict, List
from PIL import Image
import io
import base64

class ImageService:
    """图片服务"""
    
    def __init__(self, base_path: str = "./assets/images"):
        self.base_path = base_path
        self.cache_dir = os.path.join(base_path, "cache")
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_item_image(self, item_id: str, source: str = "wardrobe") -> Optional[str]:
        """
        获取单品图片
        
        Args:
            item_id: 单品ID
            source: 来源 - wardrobe/taobao
        
        Returns:
            图片路径或URL
        """
        # 1. 检查本地是否有图片
        local_path = self._find_local_image(item_id, source)
        if local_path:
            return local_path
        
        # 2. 如果是淘宝商品，尝试从数据库获取图片URL
        # ...
        
        return None
    
    def download_image(self, url: str, save_path: str = None) -> Optional[str]:
        """
        下载图片到本地
        
        Args:
            url: 图片URL
            save_path: 保存路径（可选）
        
        Returns:
            本地路径
        """
        if not save_path:
            # 使用 URL hash 作为文件名
            ext = url.split('.')[-1].split('?')[0] or 'jpg'
            filename = hashlib.md5(url.encode()).hexdigest() + '.' + ext
            save_path = os.path.join(self.cache_dir, filename)
        
        if os.path.exists(save_path):
            return save_path
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return save_path
        except Exception as e:
            print(f"下载图片失败: {e}")
        
        return None
    
    def create_outfit_image(self, items: List[Dict], output_path: str) -> Optional[str]:
        """
        创建搭配组合图片（拼接多张单品图）
        
        Args:
            items: 单品列表，每个单品包含 image_path 或 image_url
            output_path: 输出路径
        
        Returns:
            生成的图片路径
        """
        images = []
        for item in items:
            img_path = item.get('image_path') or self.download_image(item.get('image_url', ''))
            if img_path and os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    images.append(img)
                except:
                    pass
        
        if not images:
            return None
        
        # 统一尺寸
        size = (200, 200)
        resized_images = []
        for img in images:
            resized = img.resize(size, Image.LANCZOS)
            resized_images.append(resized)
        
        # 横向拼接
        total_width = size[0] * len(resized_images)
        combined = Image.new('RGB', (total_width, size[1]), (255, 255, 255))
        
        x_offset = 0
        for img in resized_images:
            combined.paste(img, (x_offset, 0))
            x_offset += size[0]
        
        combined.save(output_path)
        return output_path
    
    def image_to_base64(self, image_path: str) -> Optional[str]:
        """图片转 Base64"""
        if not os.path.exists(image_path):
            return None
        
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    
    def image_to_url(self, image_path: str) -> Optional[str]:
        """
        将本地图片转换为可访问的URL
        
        方案：
        1. 如果有图床配置，上传到图床
        2. 如果有内网服务，返回内网URL
        3. 返回 data URI (base64)
        """
        if not os.path.exists(image_path):
            return None
        
        # 方案1: 上传到图床（如果有配置）
        # ...
        
        # 方案3: 返回 data URI
        base64_data = self.image_to_base64(image_path)
        if base64_data:
            ext = image_path.split('.')[-1]
            return f"data:image/{ext};base64,{base64_data}"
        
        return None
    
    def _find_local_image(self, item_id: str, source: str) -> Optional[str]:
        """查找本地图片"""
        if source == "wardrobe":
            dir_path = os.path.join(self.base_path, "wardrobe")
        elif source == "taobao":
            dir_path = os.path.join(self.base_path, "taobao")
        else:
            return None
        
        # 查找匹配的图片文件
        for ext in ['jpg', 'jpeg', 'png', 'webp']:
            path = os.path.join(dir_path, f"{item_id}.{ext}")
            if os.path.exists(path):
                return path
        
        return None
```

### 4.3 图片上传到渠道

```python
"""
图片上传服务
将图片上传到各渠道服务器
"""

class ImageUploader:
    """图片上传器"""
    
    def __init__(self, config: Dict):
        self.config = config
    
    def upload_to_dingtalk(self, image_path: str, access_token: str) -> Optional[str]:
        """上传到钉钉，返回 media_id"""
        url = f"https://oapi.dingtalk.com/media/upload?access_token={access_token}&type=image"
        
        with open(image_path, 'rb') as f:
            response = requests.post(url, files={'media': f})
        
        if response.status_code == 200:
            result = response.json()
            if result.get('errcode') == 0:
                return result.get('media_id')
        
        return None
    
    def upload_to_wechat(self, image_path: str, access_token: str) -> Optional[str]:
        """上传到微信，返回 media_id"""
        url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image"
        
        with open(image_path, 'rb') as f:
            response = requests.post(url, files={'media': f})
        
        if response.status_code == 200:
            result = response.json()
            return result.get('media_id')
        
        return None
    
    def upload_to_feishu(self, image_path: str, app_id: str, app_secret: str) -> Optional[str]:
        """上传到飞书，返回 image_key"""
        # 先获取 tenant_access_token
        token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        token_resp = requests.post(token_url, json={
            "app_id": app_id,
            "app_secret": app_secret
        })
        tenant_token = token_resp.json().get('tenant_access_token')
        
        # 上传图片
        upload_url = "https://open.feishu.cn/open-apis/im/v1/images"
        headers = {"Authorization": f"Bearer {tenant_token}"}
        
        with open(image_path, 'rb') as f:
            form = {'image_type': 'message', 'image': f}
            response = requests.post(upload_url, headers=headers, files=form)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                return result['data'].get('image_key')
        
        return None
```

---

## 五、渠道路由器

### 5.1 路由器实现

```python
"""
渠道路由器
根据用户配置选择合适的渠道发送消息
"""

from typing import Dict, List, Optional, Any
from enum import Enum

class ChannelType(Enum):
    DINGTALK = "dingtalk"
    WECHAT = "wechat"
    FEISHU = "feishu"
    SMS = "sms"
    EMAIL = "email"

class ChannelRouter:
    """渠道路由器"""
    
    def __init__(self, db, config: Dict = None):
        self.db = db
        self.config = config or {}
        self.adapters: Dict[str, ChannelAdapter] = {}
        
        self._init_adapters()
    
    def _init_adapters(self):
        """初始化所有已配置的渠道适配器"""
        channels = self.db.get_user_channels()
        
        for channel in channels:
            channel_type = channel['type']
            channel_config = channel['config']
            
            if channel_type == ChannelType.DINGTALK.value:
                self.adapters[channel_type] = DingTalkAdapter(
                    webhook=channel_config.get('webhook'),
                    access_token=channel_config.get('access_token')
                )
            elif channel_type == ChannelType.WECHAT.value:
                self.adapters[channel_type] = WeChatAdapter(
                    appid=channel_config.get('appid'),
                    secret=channel_config.get('secret')
                )
            elif channel_type == ChannelType.FEISHU.value:
                self.adapters[channel_type] = FeishuAdapter(
                    webhook=channel_config.get('webhook'),
                    app_id=channel_config.get('app_id'),
                    app_secret=channel_config.get('app_secret')
                )
    
    def get_adapter(self, channel_type: str = None) -> Optional[ChannelAdapter]:
        """获取渠道适配器"""
        if channel_type:
            return self.adapters.get(channel_type)
        
        # 返回默认渠道（第一个已配置的）
        if self.adapters:
            return list(self.adapters.values())[0]
        
        return None
    
    def send_outfit_recommendation(self, message: OutfitRecommendation, 
                                    channel_type: str = None) -> Dict:
        """发送穿搭推荐"""
        adapter = self.get_adapter(channel_type)
        if not adapter:
            return {"success": False, "error": "未配置推送渠道"}
        
        # 根据渠道能力调整消息格式
        if not adapter.capabilities.get('image'):
            # 渠道不支持图片，只发送文字
            return self._send_text_outfit(message, adapter)
        
        success = adapter.send_outfit_recommendation(message)
        return {"success": success, "channel": adapter.channel_name}
    
    def send_new_arrivals(self, message: NewArrivalMessage,
                          channel_type: str = None) -> Dict:
        """发送上新推送"""
        adapter = self.get_adapter(channel_type)
        if not adapter:
            return {"success": False, "error": "未配置推送渠道"}
        
        success = adapter.send_new_arrivals(message)
        return {"success": success, "channel": adapter.channel_name}
    
    def send_consultation(self, message: ConsultationResult,
                          channel_type: str = None) -> Dict:
        """发送种草咨询结果"""
        adapter = self.get_adapter(channel_type)
        if not adapter:
            return {"success": False, "error": "未配置推送渠道"}
        
        success = adapter.send_consultation(message)
        return {"success": success, "channel": adapter.channel_name}
    
    def _send_text_outfit(self, message: OutfitRecommendation, 
                          adapter: ChannelAdapter) -> Dict:
        """发送纯文字版穿搭推荐"""
        text = f"""🌤️ 今日穿搭推荐

天气：{message.weather.get('city', '')} {message.weather.get('temp', '')}°C

👗 推荐搭配：
"""
        for item in message.items:
            text += f"• {item['name']} ({item['category_label']})\n"
        
        text += "\n💡 搭配说明：\n"
        for tip in message.tips:
            text += f"• {tip}\n"
        
        success = adapter.send_text(text)
        return {"success": success, "channel": adapter.channel_name}
```

---

## 六、数据库扩展

### 6.1 用户渠道配置表

```sql
-- 用户渠道配置表
CREATE TABLE user_channels (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    
    -- 渠道信息
    channel_type TEXT NOT NULL,      -- dingtalk/wechat/feishu/sms/email
    channel_name TEXT,               -- 自定义名称
    
    -- 渠道配置（JSON）
    config TEXT,                     -- 渠道特定配置
    /*
     * 钉钉: {"webhook": "...", "access_token": "..."}
     * 微信: {"appid": "...", "secret": "..."}
     * 飞书: {"webhook": "...", "app_id": "...", "app_secret": "..."}
     */
    
    -- 状态
    is_default INTEGER DEFAULT 0,    -- 是否默认渠道
    is_active INTEGER DEFAULT 1,     -- 是否启用
    
    -- 推送设置
    push_time TEXT DEFAULT '09:00',  -- 推送时间
    push_types TEXT,                 -- 推送类型 JSON: ["outfit", "new_arrivals"]
    
    created_at TEXT,
    updated_at TEXT
);
```

### 6.2 图片缓存表

```sql
-- 图片缓存表
CREATE TABLE image_cache (
    id TEXT PRIMARY KEY,
    
    -- 关联信息
    source_type TEXT,                -- item/new_arrival/outfit
    source_id TEXT,                  -- 关联ID
    
    -- 图片信息
    original_url TEXT,               -- 原始URL
    local_path TEXT,                 -- 本地路径
    
    -- 渠道媒体ID
    dingtalk_media_id TEXT,          -- 钉钉 media_id
    wechat_media_id TEXT,            -- 微信 media_id
    feishu_image_key TEXT,           -- 飞书 image_key
    
    -- 状态
    status TEXT DEFAULT 'pending',   -- pending/downloaded/uploaded/failed
    
    created_at TEXT,
    updated_at TEXT
);
```

---

## 七、使用示例

### 7.1 发送今日穿搭

```python
# 构建穿搭推荐消息
outfit_message = OutfitRecommendation(
    weather={
        "city": "北京",
        "temp": 18,
        "condition": "多云"
    },
    user_profile={
        "body_type_label": "梨形身材",
        "style_label": "极简通勤"
    },
    items=[
        {
            "name": "白色衬衫",
            "category": "top",
            "category_label": "上衣",
            "image_path": "./assets/images/wardrobe/item_001.jpg",
            "notes": "修身款"
        },
        {
            "name": "高腰A字裙",
            "category": "bottom",
            "category_label": "下装",
            "image_path": "./assets/images/wardrobe/item_002.jpg",
            "notes": "米色"
        },
        {
            "name": "乐福鞋",
            "category": "shoes",
            "category_label": "鞋子",
            "image_url": "https://img.alicdn.com/xxx.jpg",
            "notes": "黑色"
        }
    ],
    tips=[
        "高腰A字裙修饰臀部线条，适合梨形身材",
        "白衬衫+米色半裙=通勤经典组合"
    ],
    actions=[
        {"text": "换一套", "action": "refresh"},
        {"text": "记录今天穿了", "action": "log"}
    ]
)

# 发送
router = ChannelRouter(db)
result = router.send_outfit_recommendation(outfit_message)
```

### 7.2 发送上新推送

```python
# 构建上新消息
arrival_message = NewArrivalMessage(
    date="2024-01-15",
    source_name="ONLY官方旗舰店",
    items=[
        {
            "title": "米色羊毛大衣",
            "image": "https://img.alicdn.com/xxx.jpg",
            "price": 899,
            "url": "https://item.taobao.com/xxx",
            "style_tags": ["通勤", "优雅"],
            "match_score": 95,
            "match_reason": "风格匹配、颜色适合",
            "selling_points": ["100%羊毛", "双面呢"]
        }
    ],
    top_pick={
        "title": "米色羊毛大衣",
        "reason": "匹配度最高！"
    }
)

# 发送
result = router.send_new_arrivals(arrival_message)
```

---

## 八、总结

### 核心设计

1. **图文并茂**
   - 每个推荐都带商品图片
   - 支持单品图、组合图、统计图
   - 图片自动下载、缓存、上传

2. **渠道无关**
   - 抽象 ChannelAdapter 接口
   - 支持钉钉/微信/飞书等多渠道
   - 根据渠道能力自动适配格式

3. **消息结构化**
   - OutfitRecommendation - 穿搭推荐
   - NewArrivalMessage - 上新推送
   - ConsultationResult - 种草咨询

### 新增模块

| 模块 | 功能 |
|------|------|
| `channel_adapter.py` | 渠道适配器基类 |
| `dingtalk_adapter.py` | 钉钉适配器 |
| `wechat_adapter.py` | 微信适配器 |
| `feishu_adapter.py` | 飞书适配器 |
| `channel_router.py` | 渠道路由器 |
| `image_service.py` | 图片服务 |

### 新增数据表

| 表名 | 用途 |
|------|------|
| `user_channels` | 用户渠道配置 |
| `image_cache` | 图片缓存 |

---

**这个设计方案是否符合预期？有需要调整的地方吗？**