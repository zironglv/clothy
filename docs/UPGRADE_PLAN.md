# StyleBuddy 升级方案：淘宝联动版

> 让 StyleBuddy 与淘宝桌面版深度联动，打造完整的个人穿搭管理系统

---

## 一、升级目标

### 当前痛点
1. 衣橱数据需要手动拍照录入，冷启动成本高
2. 缺乏用户身材信息，推荐不够精准
3. 淘宝购物数据未能利用，数据孤岛

### 升级价值
1. **一键初始化** - 导入淘宝历史订单，快速建立线上衣橱
2. **精准推荐** - 结合身材数据和风格偏好，推荐更合身
3. **消费洞察** - 分析购物习惯，避免重复购买
4. **智能种草** - 结合现有衣橱，给出购买建议

---

## 二、核心流程设计

### 2.1 初始化流程（首次使用）

```
┌─────────────────────────────────────────────────────────────────┐
│                      StyleBuddy 初始化流程                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: 欢迎与介绍                                             │
│  ───────────────────────────────────────────────────────────── │
│  "你好呀！我是 StyleBuddy，你的 AI 穿搭闺蜜 🌸                    │
│   我可以帮你管理衣橱、每日搭配、逛街参谋~                         │
│   为了更好地为你服务，我们需要先认识一下彼此！"                   │
│                                                                 │
│  [开始设置] [稍后再说]                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: 身材信息收集                                           │
│  ───────────────────────────────────────────────────────────── │
│  "先告诉我一些你的基本信息，这样推荐会更准哦~"                     │
│                                                                 │
│  📏 身高：[    ] cm                                             │
│  ⚖️ 体重：[    ] kg                                             │
│  👤 身形：○ 标准体型  ○ 梨形  ○ 苹果形  ○ H形  ○ 倒三角         │
│  🎂 年龄段：○ 18-25  ○ 25-35  ○ 35-45  ○ 45+                   │
│                                                                 │
│  [可选] 填写更详细身体数据...                                   │
│  ────────────────────────────────────────────────────────────── │
│  └── 肩宽：[    ] cm                                            │
│  └── 胸围：[    ] cm                                            │
│  └── 腰围：[    ] cm                                            │
│  └── 臀围：[    ] cm                                            │
│  └── 腿长：[    ] cm                                            │
│                                                                 │
│  [下一步]                                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: 风格偏好收集                                           │
│  ───────────────────────────────────────────────────────────── │
│  "你平时喜欢什么样的风格呢？（可多选）"                          │
│                                                                 │
│  □ 极简通勤 ─── 干练利落，职场首选                              │
│  □ 休闲舒适 ─── 舒适为主，日常百搭                              │
│  □ 甜美可爱 ─── 软萌少女，温柔气质                              │
│  □ 酷帅街头 ─── 潮流个性，不拘一格                              │
│  □ 优雅知性 ─── 气质优雅，知性大方                              │
│  □ 复古文艺 ─── 复古文艺，有品味                                │
│  □ 运动活力 ─── 运动休闲，活力满满                              │
│  □ 法式浪漫 ─── 法式优雅，浪漫随性                              │
│                                                                 │
│  "有什么不想穿的元素吗？"                                       │
│  □ 露肩/一字肩   □ 超短裙/裤   □ 紧身款   □ 荧光色             │
│  □ 蕾丝        □ 荷叶边      □ 豹纹     □ 其他...              │
│                                                                 │
│  [下一步]                                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: 淘宝数据导入（核心！）                                  │
│  ───────────────────────────────────────────────────────────── │
│  "太棒了！现在让我们来建立你的线上衣橱吧~                        │
│   我可以从你的淘宝历史订单和购物车中导入服装商品，                │
│   这样你就不用一件件手动录入了！"                                │
│                                                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  🛒 导入数据来源（可多选）                                  │ │
│  │                                                            │ │
│  │  ☑️ 历史订单 ─── 已买过的服装单品                           │ │
│  │     └─ 可选择导入时间范围：○ 全部 ○ 近1年 ○ 近6个月 ○ 近3个月│ │
│  │                                                            │ │
│  │  ☐ 购物车 ─── 加购但未买的商品（种草清单）                  │ │
│  │     └─ 会自动识别服装类商品                                │ │
│  │                                                            │ │
│  │  ☐ 收藏夹 ─── 收藏的宝贝                                   │ │
│  │     └─ 可能包含非服装商品                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  [开始导入] [跳过，稍后再说]                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: 导入进度与商品分类                                      │
│  ───────────────────────────────────────────────────────────── │
│  正在从淘宝导入你的服装数据...                                   │
│                                                                 │
│  📦 已发现 127 件服装类商品                                      │
│  ✅ 已分类 89 件                                                 │
│  ────────────────────────────────────────────────────────────── │
│  │ 外套: 12件  上衣: 35件  下装: 28件  鞋子: 10件  配饰: 4件   │ │
│  └───────────────────────────────────────────────────────────── │
│                                                                 │
│  🤖 AI 正在识别商品信息...                                      │
│  ── 白色雪纺衬衫 ── 上衣 ── 白色 ── 春夏                        │
│  ── 黑色阔腿裤 ── 下装 ── 黑色 ── 四季                          │
│  ── 卡其色风衣 ── 外套 ── 卡其 ── 秋冬                          │
│  ── ...                                                        │
│                                                                 │
│  [继续]                                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 6: 风格理解报告                                           │
│  ───────────────────────────────────────────────────────────── │
│  "太好了！我已经了解了你的衣橱，来看看我的理解对不对吧~           │
│                                                                 │
│  ╔════════════════════════════════════════════════════════════╗ │
│  ║              🎨 你的穿衣风格画像                            ║ │
│  ╠════════════════════════════════════════════════════════════╣ │
│  ║                                                            ║ │
│  ║  👤 体型特征                                               ║ │
│  ║  ──────────────────────────────────────────────────────── ║ │
│  ║  你是标准体型，身高 165cm，适合大多数版型。                 ║ │
│  ║  建议：突出腰线，选择合身剪裁更显身材比例。                 ║ │
│  ║                                                            ║ │
│  ║  🌈 颜色偏好                                               ║ │
│  ║  ──────────────────────────────────────────────────────── ║ │
│  ║  你偏爱中性色调，黑白灰占比 60%，适合极简风格。             ║ │
│  ║  亮点：偶尔尝试卡其、驼色等温暖色调增加层次感。            ║ │
│  ║                                                            ║ │
│  ║  👗 风格标签                                               ║ │
│  ║  ──────────────────────────────────────────────────────── ║ │
│  ║  #极简通勤 #优雅知性 #职场穿搭                             ║ │
│  ║                                                            ║ │
│  ║  📊 衣橱构成分析                                           ║ │
│  ║  ──────────────────────────────────────────────────────── ║ │
│  ║  上衣 ████████████████ 35件 (39%)                         ║ │
│  ║  下装 ████████████ 28件 (31%)                             ║ │
│  ║  外套 █████ 12件 (13%)                                     ║ │
│  ║  鞋子 ████ 10件 (11%)                                      ║ │
│  ║  配饰 ██ 4件 (4%)                                          ║ │
│  ║                                                            ║ │
│  ║  ⚠️ 衣橱洞察                                               ║ │
│  ║  ──────────────────────────────────────────────────────── ║ │
│  ║  • 上衣数量偏多，建议控制购买                               ║ │
│  ║  • 配饰较少，可适当补充提升搭配丰富度                       ║ │
│  ║  • 春夏单品占 70%，秋冬单品偏少                            ║ │
│  ║                                                            ║ │
│  ║  💡 购物建议                                               ║ │
│  ║  ──────────────────────────────────────────────────────── ║ │
│  ║  建议补充：                                                ║ │
│  ║  ✓ 一件经典驼色大衣（秋冬外套不足）                        ║ │
│  ║  ✓ 一双黑色短靴（秋冬鞋履缺乏）                            ║ │
│  ║  ✓ 几条丝巾/腰带（配饰太少）                               ║ │
│  ║                                                            ║ │
│  ╚════════════════════════════════════════════════════════════╝ │
│                                                                 │
│  "这份理解准确吗？有什么想调整的地方吗？"                         │
│  [很准确！] [有些地方不太对...]                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 7: 初始化完成                                             │
│  ───────────────────────────────────────────────────────────── │
│  "太好了！我们已经完成了初始化设置 🎉                            │
│                                                                 │
│   现在你可以：                                                  │
│   • 🌤️ 每天问我「今天穿什么」                                   │
│   • 📸 拍照录入新衣服                                          │
│   • 🛍️ 逛街时问我「这件适合我吗」                               │
│   • 📊 随时查看衣橱分析                                        │
│                                                                 │
│   我会根据你的身材和风格偏好，给你最合适的建议！                  │
│   有任何问题随时问我~"                                          │
│                                                                 │
│  [开始使用 StyleBuddy]                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 三、数据库模型扩展

### 3.1 新增表：用户画像表 (user_profile)

```sql
CREATE TABLE IF NOT EXISTS user_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 基本信息
    nickname TEXT,                    -- 昵称
    gender TEXT,                      -- 性别：male/female/other
    
    -- 身材信息
    height INTEGER,                   -- 身高 cm
    weight REAL,                      -- 体重 kg
    body_type TEXT,                   -- 体型：standard/pear/apple/h/inverted_triangle
    age_range TEXT,                   -- 年龄段：18-25/25-35/35-45/45+
    
    -- 详细尺寸（可选）
    shoulder_width REAL,              -- 肩宽 cm
    bust REAL,                        -- 胸围 cm
    waist REAL,                       -- 腰围 cm
    hip REAL,                         -- 臀围 cm
    leg_length REAL,                  -- 腿长 cm
    
    -- 风格偏好（JSON 数组）
    style_preferences TEXT,           -- ["极简通勤", "优雅知性"]
    avoid_elements TEXT,              -- ["露肩", "超短裙", "紧身款"]
    
    -- 颜色偏好
    favorite_colors TEXT,             -- ["黑", "白", "灰", "卡其"]
    avoid_colors TEXT,                -- ["荧光色", "大红色"]
    
    -- 初始化状态
    init_status TEXT DEFAULT 'pending',  -- pending/body_info/style_info/taobao_import/completed
    init_step INTEGER DEFAULT 0,      -- 当前步骤 0-6
    
    -- 时间戳
    created_at TEXT,
    updated_at TEXT
);
```

### 3.2 扩展单品表：items 表增加淘宝关联字段

```sql
-- 在 items 表中新增字段
ALTER TABLE items ADD COLUMN source TEXT DEFAULT 'manual';  -- 来源：manual/taobao_order/taobao_cart/taobao_favorite
ALTER TABLE items ADD COLUMN taobao_item_id TEXT;            -- 淘宝商品 ID
ALTER TABLE items ADD COLUMN taobao_order_id TEXT;           -- 淘宝订单 ID（如果来自订单）
ALTER TABLE items ADD COLUMN taobao_price REAL;              -- 购买价格
ALTER TABLE items ADD COLUMN taobao_shop TEXT;               -- 店铺名称
ALTER TABLE items ADD COLUMN taobao_buy_time TEXT;           -- 购买时间
ALTER TABLE items ADD COLUMN taobao_image_url TEXT;          -- 淘宝商品图 URL
ALTER TABLE items ADD COLUMN taobao_product_url TEXT;        -- 商品链接
```

### 3.3 新增表：风格画像表 (style_profile)

```sql
CREATE TABLE IF NOT EXISTS style_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 风格标签（AI 生成）
    style_tags TEXT,              -- JSON: ["极简通勤", "优雅知性"]
    
    -- 颜色分析
    color_distribution TEXT,      -- JSON: {"黑": 30, "白": 25, "灰": 15, ...}
    
    -- 季节分布
    season_distribution TEXT,     -- JSON: {"春": 20, "夏": 50, "秋": 20, "冬": 10}
    
    -- 品类分布
    category_distribution TEXT,   -- JSON: {"上衣": 39, "下装": 31, ...}
    
    -- 洞察建议
    insights TEXT,                -- JSON: ["上衣数量偏多", "配饰较少"]
    shopping_suggestions TEXT,    -- JSON: ["建议补充驼色大衣", "秋冬鞋履缺乏"]
    
    -- 用户反馈
    user_feedback TEXT,           -- 用户对风格画像的反馈
    feedback_time TEXT,            -- 反馈时间
    
    -- 时间戳
    created_at TEXT,
    updated_at TEXT
);
```

---

## 四、模块设计

### 4.1 初始化模块 (src/core/initializer.py)

```python
"""
初始化模块
管理用户首次使用时的引导流程
"""

class StyleBuddyInitializer:
    """初始化引导器"""
    
    STEPS = [
        "welcome",        # Step 0: 欢迎介绍
        "body_info",      # Step 1: 身材信息
        "style_info",     # Step 2: 风格偏好
        "taobao_import",  # Step 3: 淘宝数据导入
        "import_progress", # Step 4: 导入进度
        "style_report",   # Step 5: 风格报告
        "completed"       # Step 6: 完成
    ]
    
    def __init__(self, db, taobao_client=None):
        self.db = db
        self.taobao_client = taobao_client
        self.current_step = self._load_progress()
    
    def is_initialized(self) -> bool:
        """检查是否已完成初始化"""
        profile = self.db.get_user_profile()
        return profile and profile.get('init_status') == 'completed'
    
    def get_welcome_message(self) -> str:
        """获取欢迎消息"""
        return """你好呀！我是 StyleBuddy，你的 AI 穿搭闺蜜 🌸

我可以帮你管理衣橱、每日搭配、逛街参谋~
为了更好地为你服务，我们需要先认识一下彼此！

[开始设置] [稍后再说]"""
    
    def collect_body_info(self, info: dict) -> dict:
        """收集身材信息"""
        # 验证并保存身材信息
        return self.db.update_user_profile(info)
    
    def collect_style_preferences(self, preferences: dict) -> dict:
        """收集风格偏好"""
        return self.db.update_user_profile(preferences)
    
    def start_taobao_import(self, sources: list, time_range: str = "all") -> dict:
        """开始淘宝数据导入"""
        # 调用 taobao-native CLI 获取订单/购物车数据
        pass
    
    def generate_style_profile(self) -> dict:
        """生成风格画像报告"""
        # 分析已导入的衣橱数据
        pass
    
    def complete_initialization(self) -> bool:
        """完成初始化"""
        return self.db.update_user_profile({
            'init_status': 'completed',
            'init_step': 6
        })
```

### 4.2 淘宝数据导入模块 (src/services/taobao_importer.py)

```python
"""
淘宝数据导入模块
从淘宝桌面版获取订单、购物车、收藏数据
"""

import json
import subprocess
from typing import List, Dict, Optional

class TaobaoImporter:
    """淘宝数据导入器"""
    
    # 服装类目关键词（用于识别服装商品）
    CLOTHING_KEYWORDS = [
        "T恤", "衬衫", "毛衣", "针织衫", "卫衣", "外套", "夹克", "大衣", "风衣",
        "羽绒服", "棉服", "西装", "马甲", "背心", "连衣裙", "半身裙", "裤子",
        "牛仔裤", "休闲裤", "西裤", "短裤", "打底裤", "内衣", "睡衣", "泳衣",
        "运动服", "汉服", "旗袍", "婚纱", "礼服", "鞋子", "靴子", "高跟鞋",
        "平底鞋", "运动鞋", "凉鞋", "拖鞋", "包包", "围巾", "帽子", "手套",
        "袜子", "腰带", "领带", "领结", "胸针", "发饰", "耳饰", "项链", "手链"
    ]
    
    def __init__(self, db, taobao_cli_path: str = "taobao-native"):
        self.db = db
        self.taobao_cli = taobao_cli_path
    
    def import_orders(self, time_range: str = "all") -> Dict:
        """
        导入历史订单中的服装商品
        
        流程：
        1. 调用 taobao-native navigate --args '{"page":"order"}' 进入订单页
        2. 调用 taobao-native read_page_content 读取订单列表
        3. 解析订单中的服装商品
        4. 识别商品类型、颜色、季节等信息
        5. 存入数据库
        """
        results = {
            "total": 0,
            "clothing_items": 0,
            "imported": 0,
            "failed": 0,
            "items": []
        }
        
        # Step 1: 进入订单页面
        self._navigate_to_orders()
        
        # Step 2: 读取订单数据
        orders = self._read_orders()
        
        # Step 3: 筛选服装商品
        for order in orders:
            results["total"] += 1
            for item in order.get("items", []):
                if self._is_clothing(item.get("title", "")):
                    results["clothing_items"] += 1
                    # 解析并保存
                    clothing_item = self._parse_clothing_item(item, order)
                    if self._save_item(clothing_item):
                        results["imported"] += 1
                        results["items"].append(clothing_item)
                    else:
                        results["failed"] += 1
        
        return results
    
    def import_cart(self) -> Dict:
        """
        导入购物车中的服装商品（作为种草清单）
        """
        results = {
            "total": 0,
            "clothing_items": 0,
            "imported": 0,
            "items": []
        }
        
        # 进入购物车页面
        self._navigate_to_cart()
        
        # 读取购物车数据
        cart_items = self._read_cart()
        
        for item in cart_items:
            results["total"] += 1
            if self._is_clothing(item.get("title", "")):
                results["clothing_items"] += 1
                clothing_item = self._parse_cart_item(item)
                clothing_item["source"] = "taobao_cart"
                self._save_to_wishlist(clothing_item)
                results["imported"] += 1
                results["items"].append(clothing_item)
        
        return results
    
    def import_favorites(self) -> Dict:
        """导入收藏夹"""
        pass
    
    def _is_clothing(self, title: str) -> bool:
        """判断商品是否为服装"""
        title_lower = title.lower()
        return any(kw in title for kw in self.CLOTHING_KEYWORDS)
    
    def _parse_clothing_item(self, item: dict, order: dict) -> dict:
        """
        解析服装商品信息
        使用 LLM 或规则提取：
        - category: 上衣/下装/外套/鞋子/配饰
        - color: 颜色
        - season: 春夏/秋冬/四季
        - style: 风格标签
        """
        return {
            "name": item.get("title"),
            "category": self._guess_category(item.get("title", "")),
            "color": self._extract_color(item.get("title", "")),
            "season": self._guess_season(item.get("title", "")),
            "source": "taobao_order",
            "taobao_item_id": item.get("itemId"),
            "taobao_order_id": order.get("orderId"),
            "taobao_price": item.get("price"),
            "taobao_shop": order.get("shopName"),
            "taobao_buy_time": order.get("createTime"),
            "taobao_image_url": item.get("image"),
            "taobao_product_url": f"https://item.taobao.com/item.htm?id={item.get('itemId')}"
        }
    
    def _navigate_to_orders(self):
        """导航到订单页面"""
        subprocess.run([
            self.taobao_cli, "navigate", 
            "--args", '{"page":"order","sourceApp":"StyleBuddy"}'
        ], check=True)
    
    def _navigate_to_cart(self):
        """导航到购物车页面"""
        subprocess.run([
            self.taobao_cli, "navigate",
            "--args", '{"page":"cart","sourceApp":"StyleBuddy"}'
        ], check=True)
    
    def _read_orders(self) -> List[Dict]:
        """读取订单列表"""
        # 使用 taobao-native read_page_content 读取
        result = subprocess.run([
            self.taobao_cli, "read_page_content",
            "--args", '{}',
            "-o", "/tmp/taobao_orders.json"
        ], capture_output=True, text=True)
        
        with open("/tmp/taobao_orders.json") as f:
            data = json.load(f)
        
        return self._parse_orders_from_content(data)
    
    def _read_cart(self) -> List[Dict]:
        """读取购物车列表"""
        result = subprocess.run([
            self.taobao_cli, "read_page_content",
            "--args", '{}',
            "-o", "/tmp/taobao_cart.json"
        ], capture_output=True, text=True)
        
        with open("/tmp/taobao_cart.json") as f:
            data = json.load(f)
        
        return self._parse_cart_from_content(data)
```

### 4.3 风格画像生成模块 (src/services/style_analyzer.py)

```python
"""
风格画像生成模块
分析用户衣橱数据，生成个人风格画像
"""

from typing import Dict, List
from collections import Counter

class StyleAnalyzer:
    """风格分析器"""
    
    # 风格关键词映射
    STYLE_KEYWORDS = {
        "极简通勤": ["衬衫", "西装", "西裤", "风衣", "基础款", "纯色", "黑", "白", "灰"],
        "休闲舒适": ["卫衣", "T恤", "牛仔裤", "休闲裤", "运动鞋", "宽松"],
        "甜美可爱": ["连衣裙", "蕾丝", "粉色", "蝴蝶结", "碎花", "荷叶边"],
        "酷帅街头": ["夹克", "工装", "马丁靴", "黑色", "铆钉", "破洞"],
        "优雅知性": ["针织衫", "半身裙", "高跟鞋", "驼色", "卡其", "气质"],
        "复古文艺": ["格子", "波点", "复古", "文艺", "棉麻", "绣花"],
        "运动活力": ["运动服", "运动鞋", "瑜伽", "跑步", "健身"],
        "法式浪漫": ["法式", "浪漫", "V领", "碎花裙", "茶歇裙"]
    }
    
    # 季节关键词
    SEASON_KEYWORDS = {
        "春夏": ["短袖", "薄", "雪纺", "纱", "凉鞋", "短裙", "短裤", "连衣裙", "防晒"],
        "秋冬": ["厚", "毛", "针织", "羽绒服", "大衣", "靴子", "围巾", "毛衣"],
        "四季": ["基础款", "百搭", "休闲", "牛仔裤", "白衬衫"]
    }
    
    def __init__(self, db):
        self.db = db
    
    def analyze(self) -> Dict:
        """
        分析用户衣橱，生成风格画像
        """
        # 获取所有单品
        items = self.db.get_all_items()
        user_profile = self.db.get_user_profile()
        
        if not items:
            return {"error": "衣橱为空，请先导入服装数据"}
        
        # 1. 品类分布
        category_dist = self._analyze_category(items)
        
        # 2. 颜色分布
        color_dist = self._analyze_color(items)
        
        # 3. 季节分布
        season_dist = self._analyze_season(items)
        
        # 4. 风格标签
        style_tags = self._analyze_style(items)
        
        # 5. 结合身材信息的建议
        body_suggestions = self._body_based_suggestions(user_profile)
        
        # 6. 衣橱洞察
        insights = self._generate_insights(category_dist, color_dist, season_dist)
        
        # 7. 购物建议
        shopping_suggestions = self._generate_shopping_suggestions(
            category_dist, color_dist, season_dist, style_tags
        )
        
        return {
            "style_tags": style_tags,
            "color_distribution": color_dist,
            "season_distribution": season_dist,
            "category_distribution": category_dist,
            "body_suggestions": body_suggestions,
            "insights": insights,
            "shopping_suggestions": shopping_suggestions
        }
    
    def _analyze_category(self, items: List) -> Dict:
        """分析品类分布"""
        categories = [item.get("category", "unknown") for item in items]
        counter = Counter(categories)
        total = len(categories)
        
        return {
            cat: {"count": count, "percent": round(count/total*100, 1)}
            for cat, count in counter.most_common()
        }
    
    def _analyze_color(self, items: List) -> Dict:
        """分析颜色分布"""
        colors = [item.get("color", "未知") for item in items if item.get("color")]
        counter = Counter(colors)
        total = len(colors)
        
        return {
            color: {"count": count, "percent": round(count/total*100, 1)}
            for color, count in counter.most_common(10)
        }
    
    def _analyze_season(self, items: List) -> Dict:
        """分析季节分布"""
        seasons = {"春夏": 0, "秋冬": 0, "四季": 0}
        
        for item in items:
            season = item.get("season", "四季")
            seasons[season] = seasons.get(season, 0) + 1
        
        total = sum(seasons.values())
        return {s: {"count": c, "percent": round(c/total*100, 1)} for s, c in seasons.items()}
    
    def _analyze_style(self, items: List) -> List[str]:
        """分析风格标签"""
        style_scores = {style: 0 for style in self.STYLE_KEYWORDS}
        
        for item in items:
            name = item.get("name", "") + item.get("color", "")
            for style, keywords in self.STYLE_KEYWORDS.items():
                for kw in keywords:
                    if kw in name:
                        style_scores[style] += 1
        
        # 取前3个风格标签
        sorted_styles = sorted(style_scores.items(), key=lambda x: x[1], reverse=True)
        return [s[0] for s in sorted_styles[:3] if s[1] > 0]
    
    def _body_based_suggestions(self, profile: Dict) -> List[str]:
        """基于身材信息的建议"""
        suggestions = []
        
        if not profile:
            return suggestions
        
        body_type = profile.get("body_type")
        height = profile.get("height")
        
        if body_type == "pear":
            suggestions.append("梨形身材建议选择A字裙或阔腿裤，修饰臀部线条")
        elif body_type == "apple":
            suggestions.append("苹果形身材建议选择V领或深色上衣，拉长身形")
        elif body_type == "h":
            suggestions.append("H形身材可以通过腰带或收腰设计打造曲线感")
        
        if height and height < 160:
            suggestions.append("娇小身材建议选择高腰款式，显高显瘦")
        elif height and height > 170:
            suggestions.append("高挑身材可以尝试长款大衣，气质出众")
        
        return suggestions
    
    def _generate_insights(self, cat_dist, color_dist, season_dist) -> List[str]:
        """生成衣橱洞察"""
        insights = []
        
        # 品类洞察
        if cat_dist.get("上衣", {}).get("percent", 0) > 40:
            insights.append("上衣数量偏多，建议控制购买")
        
        if cat_dist.get("配饰", {}).get("percent", 0) < 5:
            insights.append("配饰较少，可适当补充提升搭配丰富度")
        
        # 季节洞察
        if season_dist.get("秋冬", {}).get("percent", 0) < 20:
            insights.append("秋冬单品偏少，建议补充")
        
        # 颜色洞察
        neutral_colors = sum([
            color_dist.get(c, {}).get("percent", 0) 
            for c in ["黑", "白", "灰", "米", "卡其"]
        ])
        if neutral_colors > 70:
            insights.append("中性色占比高，可尝试亮色点缀")
        
        return insights
    
    def _generate_shopping_suggestions(self, cat_dist, color_dist, season_dist, style_tags) -> List[str]:
        """生成购物建议"""
        suggestions = []
        
        # 基于品类缺失
        if cat_dist.get("外套", {}).get("percent", 0) < 10:
            suggestions.append("建议补充一件经典款外套")
        
        if cat_dist.get("鞋子", {}).get("percent", 0) < 10:
            suggestions.append("鞋子款式较少，可补充百搭鞋款")
        
        # 基于季节
        if season_dist.get("秋冬", {}).get("percent", 0) < 25:
            suggestions.append("秋冬单品不足，建议补充大衣或靴子")
        
        # 基于风格
        if "极简通勤" in style_tags:
            suggestions.append("可考虑补充一件驼色风衣，百搭显气质")
        
        return suggestions
```

### 4.4 路由更新 (src/core/router.py)

```python
"""
能力检测与路由模块（更新版）
增加初始化检测和淘宝导入路由
"""

class CapabilityRouter:
    """能力路由器"""
    
    def __init__(self, config_path: str = "./config.yaml"):
        self.config = self._load_config(config_path)
        self._capabilities = None
        self.initializer = None
        self.taobao_importer = None
    
    def detect(self, force: bool = False) -> Dict[str, Any]:
        """检测系统能力"""
        if self._capabilities is not None and not force:
            return self._capabilities
        
        self._capabilities = {
            "model_tier": self._detect_model(),
            "weather_api": self._test_weather_api(),
            "image_search": self._test_image_search(),
            "image_gen": self._test_image_gen(),
            "calendar": False,
            "taobao_native": self._test_taobao_native(),  # 新增
            "initialized": self._check_initialization()   # 新增
        }
        
        return self._capabilities
    
    def _test_taobao_native(self) -> bool:
        """检测淘宝桌面版 CLI 是否可用"""
        try:
            result = subprocess.run(
                ["taobao-native", "--version"],
                capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _check_initialization(self) -> bool:
        """检查用户是否已完成初始化"""
        from .storage.database import Database
        db = Database()
        profile = db.get_user_profile()
        return profile and profile.get("init_status") == "completed"
    
    def get_initialization_step(self) -> int:
        """获取当前初始化步骤"""
        from .storage.database import Database
        db = Database()
        profile = db.get_user_profile()
        if not profile:
            return 0
        return profile.get("init_step", 0)
```

---

## 五、SKILL.md 更新

```markdown
---
name: stylebuddy
version: 0.5.0
description: "OpenClaw首个生活场景Skill - 你的AI穿搭闺蜜。拍照录入衣橱、智能推荐搭配、逛街种草咨询，还有衣橱分析帮你科学购物。支持淘宝订单导入，一键初始化线上衣橱。支持多模态识别，无需关键词，像跟闺蜜聊天一样自然。"
---

# StyleBuddy - AI穿搭闺蜜 🌸

> OpenClaw 生态首个生活场景 Skill

你的专属 AI 穿搭顾问，像闺蜜一样懂你的风格。无论是日常穿搭、衣橱管理还是逛街种草，一句话搞定。

## 🆕 v0.5.0 新特性

### 淘宝联动初始化
- **一键导入** - 从淘宝历史订单快速建立线上衣橱
- **购物车同步** - 购物车商品自动识别为种草清单
- **收藏夹导入** - 收藏的宝贝也能导入管理

### 身材信息管理
- **精准推荐** - 结合身高、体重、体型推荐合身穿搭
- **风格偏好** - 记录你的风格偏好，推荐更对味

### 风格画像报告
- **衣橱分析** - 了解你的衣橱构成和风格倾向
- **购物建议** - 基于现有衣橱给出补充建议
- **避免重复** - 帮你理性消费

## ✨ 核心能力

### 0. 初始化流程（首次使用必经）

```
新用户 → 身材信息 → 风格偏好 → 淘宝导入 → 风格报告 → 开始使用
```

**触发条件**：检测到用户未完成初始化时自动引导

**淘宝数据导入**：
- 历史订单：自动识别服装类商品，提取品类、颜色等信息
- 购物车：未购买的商品进入种草清单
- 时间范围：支持全部/近1年/近6个月/近3个月

### 1. 衣橱智能管理
📸 **拍照录入** — 拍下衣服自动识别类型、颜色、季节  
📂 **自动分类** — 上衣/下装/外套/鞋子/配饰智能归档  
🛒 **淘宝导入** — 一键导入淘宝订单，快速建立衣橱

### 2. 每日穿搭推荐
🌤️ **场景感知** — "今天约会穿什么？""明天有雨怎么搭？"  
🎨 **风格匹配** — 根据你的用户画像（身材/风格/偏好）智能推荐  
👗 **成套搭配** — 上衣+下装+鞋子+配饰一键生成

### 3. 逛街种草咨询
📱 **实时参谋** — 看中一件衣服？拍照发给 StyleBuddy  
💡 **搭配建议** — "这件和我衣橱里的米色风衣能搭吗？"  
🛍️ **购买决策** — 基于现有衣橱，给出买或不买的建议

### 4. 衣橱分析洞察
📊 **配置分析** — 了解你的衣橱构成（颜色分布、季节占比、风格偏向）  
🎯 **购物指南** — "缺一件黑色基础款打底衫""夏季单品太多，建议补充秋季"  
💰 **理性消费** — 避免重复购买，优化衣橱性价比

## 🚀 使用示例

### 初始化相关
```
开始设置        → 启动初始化流程
导入淘宝订单    → 从淘宝导入服装数据
更新身材信息    → 修改身高体重等
重新生成风格报告 → 更新风格画像
```

### 日常使用
```
今天穿什么？                    → 根据天气和场合推荐搭配
录入这件衬衫                   → 拍照/上传图片，自动识别录入
这件衣服适合我吗？              → 种草咨询，给出搭配建议
帮我分析衣橱                   → 生成衣橱报告和购物建议
明天要见客户，帮我搭配一下    → 场景化推荐
我有哪些黑色上衣？             → 查询衣橱单品
```

## 🔗 与淘宝桌面版联动

StyleBuddy 可以与淘宝桌面版深度联动：

| 功能 | 说明 |
|------|------|
| 导入历史订单 | 识别订单中的服装商品，自动录入衣橱 |
| 导入购物车 | 未购买商品进入种草清单 |
| 导入收藏夹 | 收藏的宝贝也能管理 |
| 一键购买 | 种草清单中的商品可直接跳转购买 |

## 📊 数据存储

所有数据存储在本地 SQLite 数据库：
- 用户画像：身材信息、风格偏好
- 衣橱单品：品类、颜色、季节、来源
- 种草清单：想买的商品
- 搭配记录：历史搭配
```

---

## 六、实现优先级

### Phase 1：初始化流程（1-2天）
1. [ ] 数据库表结构更新
2. [ ] 初始化模块开发
3. [ ] 身材信息收集界面
4. [ ] 风格偏好收集界面
5. [ ] SKILL.md 更新

### Phase 2：淘宝数据导入（2-3天）
1. [ ] taobao-native 集成
2. [ ] 订单数据读取与解析
3. [ ] 购物车数据读取
4. [ ] 服装商品智能识别
5. [ ] 数据导入进度展示

### Phase 3：风格画像（1-2天）
1. [ ] 风格分析算法
2. [ ] 画像报告生成
3. [ ] 用户反馈收集
4. [ ] 报告可视化展示

### Phase 4：优化与测试（1天）
1. [ ] 错误处理优化
2. [ ] 边界情况测试
3. [ ] 性能优化
4. [ ] 文档完善

---

## 七、注意事项

1. **用户隐私**：所有数据存储在本地，不上传云端
2. **淘宝依赖**：taobao-native CLI 需要淘宝桌面版已登录
3. **数据识别**：服装识别依赖商品标题关键词，可能有误识别
4. **中断恢复**：导入过程中断支持断点续传

---

**版本历史**：
- v0.5.0 - 淘宝联动版，支持初始化流程和数据导入
- v0.4.3 - 安全合规版本