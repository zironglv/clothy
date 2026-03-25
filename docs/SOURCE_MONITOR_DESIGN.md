# StyleBuddy 关注博主/店铺功能设计

> 自动追踪博主上新、店铺动态，智能推送种草推荐

---

## 一、功能概述

### 1.1 核心价值

```
┌─────────────────────────────────────────────────────────────────┐
│                    关注博主/店铺                                 │
│                                                                 │
│   用户添加关注的博主/店铺                                        │
│           │                                                     │
│           ▼                                                     │
│   系统每日自动检查上新                                           │
│           │                                                     │
│           ▼                                                     │
│   AI 提取风格特征 + 销售卖点                                     │
│           │                                                     │
│           ▼                                                     │
│   匹配用户画像 → 推送推荐                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**用户场景**：
- "我想关注这个淘宝店铺的新款"
- "这个小红书博主的穿搭我喜欢，帮我盯着"
- "每天早上推送我关注的店铺上新"

### 1.2 支持平台

| 平台 | 支持状态 | 说明 |
|------|---------|------|
| 淘宝店铺 | ✅ 优先支持 | 通过 taobao-native 获取，稳定可靠 |
| 小红书博主 | ⏸️ 暂缓 | 反爬机制严格，时间成本高，后续评估 |

---

## 二、功能设计

### 2.1 功能清单

| 功能 | 触发方式 | 说明 |
|------|---------|------|
| 添加关注 | "关注这个店铺：[链接]" | 添加到关注列表 |
| 查看关注 | "我关注了哪些店铺？" | 列出所有关注 |
| 取消关注 | "取消关注这个店铺" | 移除关注 |
| 手动刷新 | "检查店铺上新" | 立即检查一次 |
| 查看上新 | "最近有什么上新？" | 查看上新商品 |
| 推送设置 | "每天早上9点推送上新" | 配置推送时间 |

### 2.2 交互示例

```
用户："关注这个店铺 https://shop123.taobao.com/"

StyleBuddy：
┌─────────────────────────────────────────────────────────────────┐
│ ✅ 已添加关注                                                    │
│                                                                 │
│ 🏪 店铺名称：ONLY官方旗舰店                                     │
│ 📊 店铺风格：简约通勤、都市优雅                                  │
│ 📦 商品数量：约 1,200 件                                        │
│                                                                 │
│ ⚙️ 推送设置：                                                   │
│ • 推送时间：每日 09:00                                          │
│ • 推送内容：新品上架、风格匹配商品                              │
│                                                                 │
│ [立即检查上新] [修改推送设置] [取消关注]                         │
└─────────────────────────────────────────────────────────────────┘
```

```
定时推送示例：

StyleBuddy：
┌─────────────────────────────────────────────────────────────────┐
│ 🌅 早安！你关注的店铺有上新啦                                    │
│                                                                 │
│ 📅 2024-01-15 上新推送                                          │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                 │
│ 🏪 ONLY官方旗舰店（3件新品）                                    │
│                                                                 │
│ ① 米色羊毛大衣 ¥899                                            │
│    风格：通勤优雅 | 匹配度：⭐⭐⭐⭐⭐                           │
│    卖点：100%羊毛、双面呢、气质款                               │
│    "这款大衣很适合你的极简通勤风格，米色与你衣橱百搭"            │
│    [查看详情] [加入种草清单]                                    │
│                                                                 │
│ ② 黑色针织连衣裙 ¥399                                          │
│    风格：优雅知性 | 匹配度：⭐⭐⭐⭐                             │
│    卖点：显瘦版型、秋冬新款、可单穿可打底                       │
│    "你衣橱有类似款，确认是否需要"                               │
│    [查看详情] [加入种草清单]                                    │
│                                                                 │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                 │
│ 💡 今日推荐：米色羊毛大衣匹配度最高！                            │
│                                                                 │
│ [查看全部上新] [暂停推送3天] [取消关注]                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 三、技术设计

### 3.1 数据表设计

```sql
-- 关注来源表
CREATE TABLE followed_sources (
    id TEXT PRIMARY KEY,
    
    -- 基本信息
    source_type TEXT NOT NULL,        -- taobao_shop / xiaohongshu_user
    source_url TEXT NOT NULL,         -- 原始链接
    source_id TEXT,                   -- 平台ID（如淘宝店铺ID）
    source_name TEXT,                 -- 名称（店铺名/博主昵称）
    source_avatar TEXT,               -- 头像/店铺logo
    
    -- 风格标签（AI 识别）
    style_tags TEXT,                  -- JSON: ["简约通勤", "都市优雅"]
    target_audience TEXT,             -- 目标人群：女性/25-35/职场
    
    -- 抓取状态
    last_check_time TEXT,             -- 上次检查时间
    last_new_count INTEGER DEFAULT 0, -- 上次发现的新品数量
    check_status TEXT DEFAULT 'pending', -- pending/success/failed
    error_message TEXT,               -- 错误信息
    
    -- 推送设置
    push_enabled INTEGER DEFAULT 1,   -- 是否推送
    push_time TEXT DEFAULT '09:00',   -- 推送时间
    push_channel TEXT DEFAULT 'dingtalk', -- 推送渠道
    
    -- 用户备注
    user_notes TEXT,                  -- 用户备注
    
    created_at TEXT,
    updated_at TEXT
);

-- 上新商品表
CREATE TABLE new_arrivals (
    id TEXT PRIMARY KEY,
    
    -- 关联来源
    source_id TEXT NOT NULL,          -- 关联 followed_sources.id
    
    -- 商品信息
    item_id TEXT NOT NULL,            -- 平台商品ID
    item_url TEXT,                    -- 商品链接
    item_title TEXT,                  -- 商品标题
    item_image TEXT,                  -- 商品图片
    item_price REAL,                  -- 价格
    
    -- AI 提取
    category TEXT,                    -- 品类：外套/上衣/下装/鞋子/配饰
    color TEXT,                       -- 颜色
    style_tags TEXT,                  -- JSON: ["通勤", "优雅"]
    season TEXT,                      -- 季节
    selling_points TEXT,              -- JSON: ["100%羊毛", "显瘦版型"]
    target_match TEXT,                -- 适合人群
    
    -- 用户匹配
    match_score REAL,                 -- 与用户画像匹配度 0-100
    match_reason TEXT,                -- 匹配原因
    wardrobe_match TEXT,              -- JSON: 可搭配的衣橱单品
    
    -- 状态
    status TEXT DEFAULT 'new',        -- new/viewed/liked/passed/bought
    pushed_at TEXT,                   -- 推送时间
    user_feedback TEXT,               -- 用户反馈
    
    -- 时间
    publish_time TEXT,                -- 商品发布时间
    created_at TEXT,
    updated_at TEXT
);

-- 推送记录表
CREATE TABLE push_logs (
    id TEXT PRIMARY KEY,
    push_date TEXT NOT NULL,          -- 推送日期
    push_time TEXT,                   -- 推送时间
    push_channel TEXT,                -- 渠道
    
    source_count INTEGER,             -- 检查的来源数
    new_item_count INTEGER,           -- 发现的新品数
    pushed_item_count INTEGER,        -- 实际推送数量
    
    status TEXT,                      -- success/failed
    error_message TEXT,
    
    created_at TEXT
);
```

### 3.2 模块设计

```
src/services/
├── source_monitor.py       # 关注来源管理
├── shop_crawler.py         # 店铺爬虫（淘宝）
├── item_analyzer.py        # 商品分析（AI提取风格/卖点）
└── push_service.py         # 推送服务
```

#### 3.2.1 source_monitor.py - 关注管理

```python
"""
关注来源管理模块
管理用户关注的博主/店铺
"""

from typing import Dict, List, Optional
from datetime import datetime

class SourceMonitor:
    """关注来源管理器"""
    
    def __init__(self, db, taobao_client=None):
        self.db = db
        self.taobao_client = taobao_client
    
    def add_source(self, url: str, source_type: str = None) -> Dict:
        """
        添加关注来源
        
        Args:
            url: 店铺/博主链接
            source_type: 来源类型（可选，自动识别）
        
        Returns:
            添加结果
        """
        # 1. 识别来源类型
        if not source_type:
            source_type = self._detect_source_type(url)
        
        if source_type == "taobao_shop":
            return self._add_taobao_shop(url)
        elif source_type == "xiaohongshu_user":
            return self._add_xiaohongshu_user(url)
        else:
            return {"success": False, "error": "不支持的链接类型"}
    
    def _detect_source_type(self, url: str) -> Optional[str]:
        """识别链接类型"""
        if "taobao.com" in url or "tmall.com" in url:
            if "shop" in url:
                return "taobao_shop"
        elif "xiaohongshu.com" in url or "xhslink.com" in url:
            return "xiaohongshu_user"
        return None
    
    def _add_taobao_shop(self, url: str) -> Dict:
        """添加淘宝店铺"""
        # 1. 提取店铺ID
        shop_id = self._extract_shop_id(url)
        if not shop_id:
            return {"success": False, "error": "无法识别店铺ID"}
        
        # 2. 检查是否已关注
        if self.db.get_followed_source(shop_id=shop_id):
            return {"success": False, "error": "该店铺已关注"}
        
        # 3. 获取店铺信息（通过 taobao-native）
        shop_info = self._fetch_shop_info(shop_id)
        
        # 4. AI 识别店铺风格
        style_tags = self._analyze_shop_style(shop_info)
        
        # 5. 保存到数据库
        source_id = f"shop_{shop_id}"
        self.db.add_followed_source({
            "id": source_id,
            "source_type": "taobao_shop",
            "source_url": url,
            "source_id": shop_id,
            "source_name": shop_info.get("name"),
            "source_avatar": shop_info.get("logo"),
            "style_tags": style_tags,
            "created_at": datetime.now().isoformat()
        })
        
        return {
            "success": True,
            "source_id": source_id,
            "shop_name": shop_info.get("name"),
            "style_tags": style_tags
        }
    
    def _extract_shop_id(self, url: str) -> Optional[str]:
        """从 URL 提取店铺 ID"""
        import re
        # 匹配 shop123456.taobao.com 或 shop.m.taobao.com/shop/shop_index.htm?shop_id=123456
        patterns = [
            r'shop(\d+)\.taobao\.com',
            r'shop_id=(\d+)',
            r'shop/(\d+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def _fetch_shop_info(self, shop_id: str) -> Dict:
        """获取店铺信息"""
        # 通过 taobao-native 进入店铺页
        # 读取店铺名称、logo、商品列表等
        pass
    
    def _analyze_shop_style(self, shop_info: Dict) -> List[str]:
        """AI 分析店铺风格"""
        # 基于店铺名称、商品标题、商品图片分析风格
        pass
    
    def remove_source(self, source_id: str) -> bool:
        """取消关注"""
        return self.db.remove_followed_source(source_id)
    
    def list_sources(self) -> List[Dict]:
        """获取所有关注"""
        return self.db.list_followed_sources()
    
    def check_updates(self, source_id: str = None) -> Dict:
        """
        检查上新
        
        Args:
            source_id: 指定来源ID，为空则检查全部
        
        Returns:
            新品列表
        """
        sources = [self.db.get_followed_source(source_id)] if source_id \
                  else self.db.list_followed_sources()
        
        results = {
            "total_sources": len(sources),
            "total_new_items": 0,
            "items": []
        }
        
        for source in sources:
            if source["source_type"] == "taobao_shop":
                new_items = self._check_taobao_shop(source)
            elif source["source_type"] == "xiaohongshu_user":
                new_items = self._check_xiaohongshu_user(source)
            else:
                continue
            
            results["total_new_items"] += len(new_items)
            results["items"].extend(new_items)
            
            # 更新检查时间
            self.db.update_source_check_time(source["id"])
        
        return results
    
    def _check_taobao_shop(self, source: Dict) -> List[Dict]:
        """检查淘宝店铺上新"""
        # 1. 获取店铺商品列表
        # 2. 筛选新品（最近7天发布的）
        # 3. 与数据库比对，去重
        # 4. 分析新品风格、卖点
        # 5. 计算与用户画像匹配度
        # 6. 保存到数据库
        pass
```

#### 3.2.2 shop_crawler.py - 店铺爬虫

```python
"""
淘宝店铺爬虫模块
通过 taobao-native 获取店铺商品信息
"""

import json
import subprocess
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class TaobaoShopCrawler:
    """淘宝店铺爬虫"""
    
    def __init__(self, taobao_cli_path: str = "taobao-native"):
        self.taobao_cli = taobao_cli_path
    
    def get_shop_info(self, shop_id: str) -> Dict:
        """
        获取店铺基本信息
        
        通过 taobao-native:
        1. navigate 进入店铺页
        2. read_page_content 读取店铺信息
        """
        # 进入店铺页
        url = f"https://shop{shop_id}.taobao.com/"
        subprocess.run([
            self.taobao_cli, "navigate",
            "--args", json.dumps({"url": url})
        ], check=True)
        
        # 读取页面内容
        result = subprocess.run([
            self.taobao_cli, "read_page_content",
            "--args", json.dumps({}),
            "-o", "/tmp/shop_content.json"
        ], capture_output=True, text=True)
        
        with open("/tmp/shop_content.json") as f:
            content = json.load(f)
        
        return self._parse_shop_info(content)
    
    def get_shop_items(self, shop_id: str, 
                        category: str = None,
                        sort: str = "new",
                        limit: int = 50) -> List[Dict]:
        """
        获取店铺商品列表
        
        Args:
            shop_id: 店铺ID
            category: 商品分类（可选）
            sort: 排序方式 - new(最新上架)/sales(销量)/price_asc(价格升序)
            limit: 获取数量
        
        Returns:
            商品列表
        """
        # 构建店铺搜索 URL
        url = f"https://shop{shop_id}.taobao.com/search.htm"
        params = {"orderType": sort}
        if category:
            params["categoryId"] = category
        
        # 进入页面
        subprocess.run([
            self.taobao_cli, "navigate",
            "--args", json.dumps({"url": url, "params": params})
        ], check=True)
        
        # 滚动加载更多商品
        self._scroll_to_load(limit)
        
        # 读取商品列表
        result = subprocess.run([
            self.taobao_cli, "read_page_content",
            "--args", json.dumps({
                "selector": ".item .item-box"  # 商品卡片选择器
            }),
            "-o", "/tmp/shop_items.json"
        ], capture_output=True, text=True)
        
        with open("/tmp/shop_items.json") as f:
            items = json.load(f)
        
        return self._parse_items(items)
    
    def get_new_arrivals(self, shop_id: str, days: int = 7) -> List[Dict]:
        """
        获取店铺新品
        
        Args:
            shop_id: 店铺ID
            days: 最近N天的新品
        
        Returns:
            新品列表
        """
        # 按最新排序获取商品
        items = self.get_shop_items(shop_id, sort="new", limit=100)
        
        # 筛选发布时间
        cutoff_time = datetime.now() - timedelta(days=days)
        new_items = []
        
        for item in items:
            publish_time = item.get("publish_time")
            if publish_time:
                if datetime.fromisoformat(publish_time) >= cutoff_time:
                    new_items.append(item)
        
        return new_items
    
    def get_item_detail(self, item_id: str) -> Dict:
        """
        获取商品详情
        
        包括：标题、图片、价格、详情页、评价等
        """
        url = f"https://item.taobao.com/item.htm?id={item_id}"
        
        subprocess.run([
            self.taobao_cli, "navigate",
            "--args", json.dumps({"url": url})
        ], check=True)
        
        result = subprocess.run([
            self.taobao_cli, "read_page_content",
            "--args", json.dumps({}),
            "-o", f"/tmp/item_{item_id}.json"
        ], capture_output=True, text=True)
        
        with open(f"/tmp/item_{item_id}.json") as f:
            content = json.load(f)
        
        return self._parse_item_detail(content)
    
    def _scroll_to_load(self, target_count: int):
        """滚动页面加载更多商品"""
        # 执行 JavaScript 滚动
        pass
    
    def _parse_shop_info(self, content: Dict) -> Dict:
        """解析店铺信息"""
        return {
            "shop_id": content.get("shopId"),
            "name": content.get("shopName"),
            "logo": content.get("shopLogo"),
            "rating": content.get("shopRating"),
            "follower_count": content.get("followerCount"),
            "item_count": content.get("itemCount")
        }
    
    def _parse_items(self, items: List) -> List[Dict]:
        """解析商品列表"""
        result = []
        for item in items:
            result.append({
                "item_id": item.get("itemId"),
                "title": item.get("title"),
                "image": item.get("pic"),
                "price": float(item.get("price", 0)),
                "sales": item.get("sales"),
                "url": f"https://item.taobao.com/item.htm?id={item.get('itemId')}",
                "publish_time": item.get("publishTime")  # 需要从详情页获取
            })
        return result
    
    def _parse_item_detail(self, content: Dict) -> Dict:
        """解析商品详情"""
        return {
            "item_id": content.get("itemId"),
            "title": content.get("title"),
            "images": content.get("images", []),
            "price": content.get("price"),
            "original_price": content.get("originalPrice"),
            "sales": content.get("sales"),
            "description": content.get("desc"),
            "publish_time": content.get("publishTime"),
            "attributes": content.get("attributes", []),  # 颜色、尺码等
            "reviews": content.get("reviews", [])[:10]  # 前10条评价
        }
```

#### 3.2.3 item_analyzer.py - 商品分析

```python
"""
商品分析模块
AI 提取商品风格特征、销售卖点
"""

from typing import Dict, List
import json

class ItemAnalyzer:
    """商品分析器"""
    
    # 风格关键词映射
    STYLE_KEYWORDS = {
        "极简通勤": ["简约", "通勤", "职场", "基础款", "百搭", "经典"],
        "休闲舒适": ["休闲", "舒适", "宽松", "日常", "慵懒", "oversize"],
        "甜美可爱": ["甜美", "可爱", "少女", "粉色", "蝴蝶结", "蕾丝"],
        "酷帅街头": ["街头", "酷", "工装", "马丁靴", "黑色", "潮流"],
        "优雅知性": ["优雅", "知性", "气质", "温柔", "法式", "浪漫"],
        "复古文艺": ["复古", "文艺", "vintage", "格纹", "波点", "棉麻"],
        "运动活力": ["运动", "活力", "健身", "瑜伽", "跑步", "户外"]
    }
    
    # 卖点关键词
    SELLING_POINT_KEYWORDS = {
        "材质": ["羊毛", "真丝", "棉", "麻", "雪纺", "牛仔", "针织"],
        "工艺": ["双面呢", "手工", "刺绣", "印花", "水洗", "免烫"],
        "功能": ["显瘦", "遮肉", "显高", "透气", "防水", "保暖"],
        "设计": ["收腰", "A字", "直筒", "宽松", "修身", "高腰"],
        "品质": ["进口", "原单", "定制", "限量", "设计师"]
    }
    
    def __init__(self, db):
        self.db = db
    
    def analyze(self, item: Dict) -> Dict:
        """
        分析商品
        
        Args:
            item: 商品信息（包含标题、图片、详情等）
        
        Returns:
            分析结果
        """
        # 1. 识别品类
        category = self._detect_category(item)
        
        # 2. 提取颜色
        color = self._extract_color(item)
        
        # 3. 分析风格
        style_tags = self._analyze_style(item)
        
        # 4. 推断季节
        season = self._infer_season(item, category)
        
        # 5. 提取卖点
        selling_points = self._extract_selling_points(item)
        
        # 6. 目标人群
        target_match = self._analyze_target(item)
        
        return {
            "category": category,
            "color": color,
            "style_tags": style_tags,
            "season": season,
            "selling_points": selling_points,
            "target_match": target_match
        }
    
    def match_user_profile(self, item_analysis: Dict, user_profile: Dict) -> Dict:
        """
        计算与用户画像的匹配度
        
        Returns:
            {
                "match_score": 85,
                "match_reason": "风格匹配、颜色适合、身材适配",
                "wardrobe_match": [...]
            }
        """
        score = 0
        reasons = []
        
        # 1. 风格匹配
        item_styles = set(item_analysis.get("style_tags", []))
        user_styles = set(user_profile.get("style_preferences", []))
        style_match = item_styles & user_styles
        if style_match:
            score += 30
            reasons.append(f"风格匹配：{', '.join(style_match)}")
        
        # 2. 颜色偏好
        item_color = item_analysis.get("color")
        if item_color in user_profile.get("favorite_colors", []):
            score += 20
            reasons.append(f"颜色偏好：{item_color}")
        
        # 3. 避免元素检查
        avoid_elements = user_profile.get("avoid_elements", [])
        selling_points = item_analysis.get("selling_points", [])
        title = item_analysis.get("title", "")
        
        for avoid in avoid_elements:
            if avoid in title or any(avoid in sp for sp in selling_points):
                score -= 30
                reasons.append(f"包含你不喜欢的元素：{avoid}")
        
        # 4. 身材适配
        body_type = user_profile.get("body_type")
        if body_type:
            body_match = self._check_body_match(item_analysis, body_type)
            if body_match:
                score += 20
                reasons.append(body_match)
        
        # 5. 衣橱搭配
        wardrobe_match = self._find_wardrobe_match(item_analysis)
        if wardrobe_match:
            score += 15
            reasons.append(f"可与 {len(wardrobe_match)} 件衣橱单品搭配")
        
        return {
            "match_score": min(max(score, 0), 100),
            "match_reason": "；".join(reasons) if reasons else "普通匹配",
            "wardrobe_match": wardrobe_match
        }
    
    def _detect_category(self, item: Dict) -> str:
        """识别品类"""
        title = item.get("title", "")
        
        category_keywords = {
            "outer": ["外套", "大衣", "风衣", "羽绒服", "夹克", "西装", "棉服"],
            "top": ["T恤", "衬衫", "毛衣", "针织衫", "卫衣", "吊带", "背心"],
            "bottom": ["裤", "裙", "牛仔裤", "休闲裤", "半裙", "短裤", "阔腿裤"],
            "shoes": ["鞋", "靴", "高跟鞋", "运动鞋", "凉鞋", "帆布鞋"],
            "accessory": ["包", "围巾", "帽子", "腰带", "丝巾", "手套"]
        }
        
        for category, keywords in category_keywords.items():
            for kw in keywords:
                if kw in title:
                    return category
        
        return "unknown"
    
    def _extract_color(self, item: Dict) -> str:
        """提取颜色"""
        title = item.get("title", "")
        colors = ["黑", "白", "灰", "米", "卡其", "驼", "棕", "红", "粉", 
                  "橙", "黄", "绿", "蓝", "紫", "杏", "咖"]
        
        for color in colors:
            if color in title:
                return color
        
        return "未知"
    
    def _analyze_style(self, item: Dict) -> List[str]:
        """分析风格"""
        title = item.get("title", "")
        description = item.get("description", "")
        text = title + description
        
        styles = []
        for style, keywords in self.STYLE_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    styles.append(style)
                    break
        
        return styles[:3] if styles else ["其他"]
    
    def _infer_season(self, item: Dict, category: str) -> str:
        """推断季节"""
        title = item.get("title", "")
        
        summer_keywords = ["短袖", "薄", "雪纺", "纱", "凉鞋", "短裙", "短裤", "防晒"]
        winter_keywords = ["厚", "毛", "针织", "羽绒", "大衣", "靴", "围巾", "毛衣", "加绒"]
        
        for kw in winter_keywords:
            if kw in title:
                return "秋冬"
        
        for kw in summer_keywords:
            if kw in title:
                return "春夏"
        
        # 根据品类判断
        if category in ["outer"]:
            return "秋冬"
        elif category in ["top"]:
            return "四季"
        
        return "四季"
    
    def _extract_selling_points(self, item: Dict) -> List[str]:
        """提取卖点"""
        title = item.get("title", "")
        description = item.get("description", "")
        attributes = item.get("attributes", [])
        
        text = title + description + " ".join(attributes)
        
        selling_points = []
        for category, keywords in self.SELLING_POINT_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    selling_points.append(kw)
        
        return selling_points[:5]
    
    def _analyze_target(self, item: Dict) -> str:
        """分析目标人群"""
        title = item.get("title", "")
        
        if any(kw in title for kw in ["少女", "学生", "甜美"]):
            return "年轻女性"
        elif any(kw in title for kw in ["通勤", "职场", "气质"]):
            return "职场女性"
        elif any(kw in title for kw in ["妈妈", "孕"]):
            return "宝妈"
        
        return "女性"
    
    def _check_body_match(self, item_analysis: Dict, body_type: str) -> Optional[str]:
        """检查身材适配"""
        category = item_analysis.get("category")
        style_tags = item_analysis.get("style_tags", [])
        
        body_advice = {
            "pear": {
                "recommend": ["A字", "阔腿", "收腰", "泡泡袖", "高腰"],
                "avoid": ["紧身", "包臀"]
            },
            "apple": {
                "recommend": ["V领", "直筒", "宽松", "深色"],
                "avoid": ["紧身", "短款"]
            },
            "h": {
                "recommend": ["收腰", "腰带", "A字", "层叠"],
                "avoid": ["直筒连衣裙"]
            }
        }
        
        if body_type in body_advice:
            advice = body_advice[body_type]
            # 检查推荐元素
            # ...
        
        return None
    
    def _find_wardrobe_match(self, item_analysis: Dict) -> List[Dict]:
        """查找可搭配的衣橱单品"""
        # 查询数据库中可以搭配的单品
        pass
```

#### 3.2.4 push_service.py - 推送服务

```python
"""
推送服务模块
处理上新推送、消息格式化
"""

from typing import Dict, List
from datetime import datetime

class PushService:
    """推送服务"""
    
    def __init__(self, db, dingtalk_config: Dict = None):
        self.db = db
        self.dingtalk_config = dingtalk_config
    
    def push_new_arrivals(self, items: List[Dict], 
                          push_channel: str = "dingtalk") -> Dict:
        """
        推送新品
        
        Args:
            items: 新品列表（已分析、已匹配）
            push_channel: 推送渠道
        
        Returns:
            推送结果
        """
        # 1. 按匹配度排序
        sorted_items = sorted(items, key=lambda x: x.get("match_score", 0), reverse=True)
        
        # 2. 筛选高匹配度商品
        high_match_items = [i for i in sorted_items if i.get("match_score", 0) >= 60]
        
        # 3. 格式化消息
        message = self._format_push_message(high_match_items)
        
        # 4. 推送
        if push_channel == "dingtalk":
            result = self._push_to_dingtalk(message)
        else:
            result = {"success": False, "error": "不支持的推送渠道"}
        
        # 5. 记录推送日志
        self._log_push(len(items), len(high_match_items), result)
        
        return result
    
    def _format_push_message(self, items: List[Dict]) -> Dict:
        """
        格式化推送消息
        
        使用钉钉 ActionCard 格式
        """
        if not items:
            return None
        
        # 按来源分组
        by_source = {}
        for item in items:
            source_name = item.get("source_name", "未知店铺")
            if source_name not in by_source:
                by_source[source_name] = []
            by_source[source_name].append(item)
        
        # 构建消息
        title = f"🌅 早安！你关注的店铺有上新啦（{len(items)}件）"
        
        text_parts = [f"📅 {datetime.now().strftime('%Y-%m-%d')} 上新推送\n"]
        text_parts.append("━" * 30 + "\n")
        
        for source_name, source_items in by_source.items():
            text_parts.append(f"\n🏪 **{source_name}**（{len(source_items)}件新品）\n")
            
            for i, item in enumerate(source_items[:5], 1):  # 每个店铺最多5件
                match_stars = "⭐" * min(int(item.get("match_score", 0) / 20), 5)
                selling_points = "、".join(item.get("selling_points", [])[:3])
                
                text_parts.append(f"""
**{i}. {item.get('item_title', '未知商品')}** ¥{item.get('item_price', '-')}

> 风格：{', '.join(item.get('style_tags', []))} | 匹配度：{match_stars}
> 卖点：{selling_points}

💡 {item.get('match_reason', '')}
""")
        
        # 添加底部
        text_parts.append("\n" + "━" * 30)
        text_parts.append("\n💡 **今日推荐**：匹配度最高的商品最适合你！")
        
        return {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": "".join(text_parts),
                "btnOrientation": "1",
                "btns": [
                    {"title": "查看全部上新", "actionURL": "stylebuddy://new_arrivals"},
                    {"title": "暂停推送3天", "actionURL": "stylebuddy://pause_push"}
                ]
            }
        }
    
    def _push_to_dingtalk(self, message: Dict) -> Dict:
        """推送到钉钉"""
        import requests
        
        webhook = self.dingtalk_config.get("webhook")
        if not webhook:
            return {"success": False, "error": "未配置钉钉 Webhook"}
        
        response = requests.post(webhook, json=message)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("errcode") == 0:
                return {"success": True}
            else:
                return {"success": False, "error": result.get("errmsg")}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    
    def _log_push(self, total_count: int, pushed_count: int, result: Dict):
        """记录推送日志"""
        self.db.add_push_log({
            "push_date": datetime.now().strftime("%Y-%m-%d"),
            "push_time": datetime.now().isoformat(),
            "push_channel": "dingtalk",
            "source_count": 0,
            "new_item_count": total_count,
            "pushed_item_count": pushed_count,
            "status": "success" if result.get("success") else "failed",
            "error_message": result.get("error")
        })
```

### 3.3 定时任务设计

```python
"""
定时任务：每日检查上新
"""

# 使用 cron skill 创建定时任务
# 任务命令：
#   copaw run skill stylebuddy --task check_updates

# 任务配置
CRON_CONFIG = {
    "name": "stylebuddy_daily_check",
    "schedule": "0 9 * * *",  # 每天 9:00
    "command": "python3 -m stylebuddy.tasks.daily_check",
    "description": "StyleBuddy 每日检查关注的店铺上新"
}
```

#### daily_check.py - 定时任务脚本

```python
"""
每日检查上新任务
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.storage.database import Database
from src.services.source_monitor import SourceMonitor
from src.services.shop_crawler import TaobaoShopCrawler
from src.services.item_analyzer import ItemAnalyzer
from src.services.push_service import PushService
from src.models.profile import ProfileManager

def main():
    """每日检查上新主流程"""
    print(f"[{datetime.now()}] 开始每日检查上新...")
    
    # 初始化模块
    db = Database()
    monitor = SourceMonitor(db)
    crawler = TaobaoShopCrawler()
    analyzer = ItemAnalyzer(db)
    push_service = PushService(db)
    profile_manager = ProfileManager(db)
    
    # 1. 获取所有关注的来源
    sources = monitor.list_sources()
    if not sources:
        print("没有关注的店铺，跳过")
        return
    
    print(f"共关注 {len(sources)} 个店铺")
    
    # 2. 检查每个来源的新品
    all_new_items = []
    for source in sources:
        print(f"检查 {source['source_name']}...")
        
        try:
            if source["source_type"] == "taobao_shop":
                # 获取店铺新品
                new_items = crawler.get_new_arrivals(
                    source["source_id"], 
                    days=7
                )
                
                # 分析每个新品
                for item in new_items:
                    # 检查是否已存在
                    if db.get_new_arrival(item["item_id"]):
                        continue
                    
                    # AI 分析
                    analysis = analyzer.analyze(item)
                    item.update(analysis)
                    
                    # 用户画像匹配
                    user_profile = profile_manager.get_profile()
                    if user_profile:
                        match = analyzer.match_user_profile(analysis, user_profile)
                        item.update(match)
                    
                    # 保存到数据库
                    db.add_new_arrival({
                        "id": f"arrival_{item['item_id']}",
                        "source_id": source["id"],
                        "item_id": item["item_id"],
                        "item_url": item["url"],
                        "item_title": item["title"],
                        "item_image": item["image"],
                        "item_price": item["price"],
                        "category": analysis["category"],
                        "color": analysis["color"],
                        "style_tags": analysis["style_tags"],
                        "season": analysis["season"],
                        "selling_points": analysis["selling_points"],
                        "match_score": item.get("match_score", 0),
                        "match_reason": item.get("match_reason"),
                        "wardrobe_match": item.get("wardrobe_match"),
                        "status": "new"
                    })
                    
                    all_new_items.append(item)
            
            # 更新检查状态
            db.update_source_check_status(source["id"], "success")
            
        except Exception as e:
            print(f"检查失败: {e}")
            db.update_source_check_status(source["id"], "failed", str(e))
    
    # 3. 推送新品
    if all_new_items:
        print(f"发现 {len(all_new_items)} 件新品，准备推送...")
        result = push_service.push_new_arrivals(all_new_items)
        print(f"推送结果: {result}")
    else:
        print("没有发现新品")
    
    print(f"[{datetime.now()}] 每日检查完成")

if __name__ == "__main__":
    main()
```

---

## 四、数据流设计

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         关注博主/店铺 数据流                                 │
└─────────────────────────────────────────────────────────────────────────────┘

用户添加关注
      │
      ▼
┌─────────────────┐
│ followed_sources│ ──── 保存关注信息
└─────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│                     定时任务（每日 9:00）                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ 遍历关注来源 │───▶│ 获取店铺新品 │───▶│ 分析商品信息 │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                 │               │
│                                                 ▼               │
│                    ┌──────────────┐    ┌──────────────┐        │
│                    │ 保存到数据库 │◀───│ 匹配用户画像 │        │
│                    └──────────────┘    └──────────────┘        │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      推送服务                                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ 筛选高匹配度 │───▶│ 格式化消息   │───▶│ 推送到钉钉   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      用户收到推送                                │
├─────────────────────────────────────────────────────────────────┤
│  "早安！你关注的店铺有上新啦..."                                 │
│                                                                 │
│  [查看详情] [加入种草清单] [暂停推送]                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 五、用户交互命令

### 5.1 关注管理

```
# 添加关注
"关注这个店铺：https://shop123.taobao.com/"
"关注这个小红书博主：https://www.xiaohongshu.com/user/xxx"

# 查看关注
"我关注了哪些店铺？"
"显示我的关注列表"

# 取消关注
"取消关注 ONLY官方旗舰店"
"取消关注这个店铺"

# 修改设置
"把推送时间改成早上8点"
"暂停上新推送"
"恢复上新推送"
```

### 5.2 查看上新

```
# 查看最近上新
"最近有什么上新？"
"查看店铺新品"

# 手动刷新
"检查店铺上新"
"刷新关注列表"

# 按店铺查看
"ONLY官方旗舰店有什么新品？"
```

### 5.3 种草操作

```
# 加入种草清单
"这件加入种草清单"
"我要买这个"

# 跳转购买
"帮我买这件"
"打开商品页面"
```

---

## 六、实现优先级

| 阶段 | 内容 | 耗时 | 依赖 |
|------|------|------|------|
| **Phase 1** | 数据表创建 + 关注管理 API | 0.5天 | - |
| **Phase 2** | 店铺爬虫开发（taobao-native） | 1天 | taobao-native |
| **Phase 3** | 商品分析模块 | 1天 | - |
| **Phase 4** | 推送服务 + 定时任务 | 0.5天 | cron skill |
| **Phase 5** | 小红书支持（可选） | TBD | 评估反爬成本 |

---

## 七、风险与应对

| 风险 | 影响 | 应对策略 |
|------|------|---------|
| 淘宝店铺页面改版 | 爬虫失效 | 定期维护，预留降级方案 |
| taobao-native 不稳定 | 获取失败 | 重试机制 + 错误日志 |
| 商品识别不准 | 推荐质量差 | 用户反馈修正 + AI 优化 |
| 推送过于频繁 | 用户打扰 | 智能频率控制 + 用户设置 |
| 小红书反爬 | 无法获取 | 暂缓支持，后续评估 |

---

## 八、总结

### 新增功能：关注博主/店铺

**核心能力**：
- ✅ 添加/删除关注店铺
- ✅ 每日自动检查上新
- ✅ AI 提取风格特征 + 卖点
- ✅ 匹配用户画像计算推荐度
- ✅ 推送到钉钉

**平台支持**：
- ✅ 淘宝店铺（优先）
- ⏸️ 小红书博主（暂缓）

**数据存储**：
- `followed_sources` 表：关注列表
- `new_arrivals` 表：上新商品
- `push_logs` 表：推送日志

**定时任务**：
- 使用 cron skill
- 每日 9:00 执行
- 可自定义推送时间

---

**这个设计方案是否符合你的预期？有需要调整的地方吗？**