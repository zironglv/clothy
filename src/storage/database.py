"""
SQLite 数据库模块
管理所有本地数据存储
支持多人衣橱
"""

import sqlite3
import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any

class Database:
    """SQLite 数据库管理器"""
    
    def __init__(self, db_path: str = "./assets/data/wardrobe.db"):
        self.db_path = db_path
        self._ensure_dir()
        self._init_tables()
    
    def _ensure_dir(self):
        """确保目录存在"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_tables(self):
        """初始化数据表"""
        with self._get_connection() as conn:
            # ===== 多人衣橱相关表 =====
            
            # 家庭表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS families (
                    id TEXT PRIMARY KEY,
                    name TEXT DEFAULT '我的家庭',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 家庭成员表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    id TEXT PRIMARY KEY,
                    family_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    relationship TEXT NOT NULL,  -- self/spouse/child/parent/other
                    avatar TEXT DEFAULT '👤',
                    gender TEXT,  -- male/female
                    is_initialized INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (family_id) REFERENCES families(id)
                )
            """)
            
            # 成员画像表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    member_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    gender TEXT,
                    relationship TEXT,
                    body TEXT,  -- JSON 身材数据
                    body_type TEXT,  -- 身材类型
                    skin_tone TEXT,  -- 肤色
                    style TEXT,  -- JSON 风格偏好
                    child TEXT,  -- JSON 儿童专属信息
                    occupation TEXT,  -- 职业
                    lifestyle TEXT,  -- 生活方式
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (member_id) REFERENCES members(id)
                )
            """)
            
            # 关注来源表（店铺、博主等）
            conn.execute("""
                CREATE TABLE IF NOT EXISTS followed_sources (
                    id TEXT PRIMARY KEY,
                    member_id TEXT,  -- 所属成员（可为空，表示家庭共享）
                    source_type TEXT NOT NULL,  -- taobao_shop/douyin_blogger/wechat_account
                    source_id TEXT,  -- 外部平台ID
                    name TEXT NOT NULL,
                    url TEXT,
                    avatar TEXT,
                    description TEXT,
                    follower_count INTEGER,
                    last_checked TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (member_id) REFERENCES members(id)
                )
            """)
            
            # 关注来源的商品表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS source_items (
                    id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    external_id TEXT,  -- 商品外部ID
                    name TEXT NOT NULL,
                    category TEXT,
                    color TEXT,
                    style TEXT,
                    price REAL,
                    original_price REAL,
                    image_url TEXT,
                    local_image_path TEXT,
                    description TEXT,
                    url TEXT,
                    is_new INTEGER DEFAULT 1,  -- 是否新品
                    is_analyzed INTEGER DEFAULT 0,  -- 是否已分析
                    analysis_result TEXT,  -- JSON 分析结果
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (source_id) REFERENCES followed_sources(id)
                )
            """)
            
            # 单品表（添加 member_id 字段）
            conn.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id TEXT PRIMARY KEY,
                    member_id TEXT,  -- 所属成员
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,  -- outer/top/bottom/shoes/accessory
                    color TEXT,
                    style TEXT,
                    season TEXT,
                    material TEXT,
                    brand TEXT,
                    price REAL,
                    source TEXT,  -- 来源：manual/taobao/photo
                    source_url TEXT,  -- 来源链接
                    image_path TEXT,
                    tags TEXT,  -- JSON array
                    wear_count INTEGER DEFAULT 0,  -- 穿着次数
                    last_worn DATE,  -- 最后穿着日期
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (member_id) REFERENCES members(id)
                )
            """)
            
            # 检查并添加新字段（兼容旧数据）
            self._migrate_items_table(conn)
            
            # 穿搭记录表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS outfits (
                    id TEXT PRIMARY KEY,
                    date DATE NOT NULL,
                    items TEXT NOT NULL,  -- JSON array of item_ids
                    occasion TEXT,
                    weather TEXT,  -- JSON object
                    notes TEXT,
                    rating INTEGER,  -- 1-5 stars
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 用户偏好表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 搭配模板使用记录
            conn.execute("""
                CREATE TABLE IF NOT EXISTS template_usage (
                    template_id TEXT PRIMARY KEY,
                    use_count INTEGER DEFAULT 0,
                    last_used DATE,
                    liked BOOLEAN DEFAULT 0
                )
            """)
            
            # 种草清单表（逛街看中但未购买的衣服）
            conn.execute("""
                CREATE TABLE IF NOT EXISTS wishlist (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT,
                    color TEXT,
                    style TEXT,
                    material TEXT,
                    price TEXT,
                    brand TEXT,
                    image_path TEXT,
                    reason TEXT,  -- 想买的原因/备注
                    store_location TEXT,  -- 店铺位置
                    purchased BOOLEAN DEFAULT 0,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    purchased_at TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def _migrate_items_table(self, conn):
        """迁移 items 表，添加新字段"""
        # 获取现有列
        cursor = conn.execute("PRAGMA table_info(items)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # 添加缺失的列
        migrations = [
            ("member_id", "TEXT"),
            ("brand", "TEXT"),
            ("price", "REAL"),
            ("source", "TEXT"),
            ("source_url", "TEXT"),
            ("wear_count", "INTEGER DEFAULT 0"),
            ("last_worn", "DATE")
        ]
        
        for col_name, col_type in migrations:
            if col_name not in columns:
                try:
                    conn.execute(f"ALTER TABLE items ADD COLUMN {col_name} {col_type}")
                except:
                    pass  # 列已存在
        
        # 为 outfits 表添加 member_id
        cursor = conn.execute("PRAGMA table_info(outfits)")
        outfit_columns = [col[1] for col in cursor.fetchall()]
        if "member_id" not in outfit_columns:
            try:
                conn.execute("ALTER TABLE outfits ADD COLUMN member_id TEXT")
            except:
                pass
        
        # 为 wishlist 表添加 member_id
        cursor = conn.execute("PRAGMA table_info(wishlist)")
        wishlist_columns = [col[1] for col in cursor.fetchall()]
        if "member_id" not in wishlist_columns:
            try:
                conn.execute("ALTER TABLE wishlist ADD COLUMN member_id TEXT")
            except:
                pass
    
    # ===== 家庭成员操作 =====
    
    def get_family(self) -> Optional[Dict]:
        """获取家庭信息"""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM families LIMIT 1")
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def create_family(self, name: str = "我的家庭") -> str:
        """创建家庭"""
        family_id = f"family_{uuid.uuid4().hex[:8]}"
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO families (id, name)
                VALUES (?, ?)
            """, (family_id, name))
            conn.commit()
        return family_id
    
    def get_all_members(self) -> List[Dict]:
        """获取所有家庭成员"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM members ORDER BY 
                CASE relationship 
                    WHEN 'self' THEN 1 
                    WHEN 'spouse' THEN 2 
                    WHEN 'child' THEN 3 
                    WHEN 'parent' THEN 4 
                    ELSE 5 
                END
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_member(self, member_id: str) -> Optional[Dict]:
        """获取指定成员"""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM members WHERE id = ?", (member_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def add_member(self, member: Dict) -> str:
        """添加家庭成员"""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO members (id, family_id, name, relationship, avatar, gender, is_initialized)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                member['id'],
                member['family_id'],
                member['name'],
                member['relationship'],
                member.get('avatar', '👤'),
                member.get('gender'),
                member.get('is_initialized', False)
            ))
            conn.commit()
        return member['id']
    
    def update_member(self, member_id: str, updates: Dict) -> bool:
        """更新成员信息"""
        if not updates:
            return False
        
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [member_id]
        
        with self._get_connection() as conn:
            conn.execute(f"UPDATE members SET {set_clause} WHERE id = ?", values)
            conn.commit()
        return True
    
    def delete_member(self, member_id: str) -> bool:
        """删除成员"""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM members WHERE id = ?", (member_id,))
            conn.commit()
        return True
    
    def delete_member_items(self, member_id: str):
        """删除成员的所有单品"""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM items WHERE member_id = ?", (member_id,))
            conn.commit()
    
    def delete_member_profile(self, member_id: str):
        """删除成员画像"""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM profiles WHERE member_id = ?", (member_id,))
            conn.commit()
    
    # ===== 成员画像操作 =====
    
    def create_profile(self, member_id: str, profile_data: Dict):
        """创建成员画像"""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO profiles (member_id, name, gender, relationship, body, style, child)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                member_id,
                profile_data.get('name', ''),
                profile_data.get('gender'),
                profile_data.get('relationship'),
                json.dumps(profile_data.get('body', {}), ensure_ascii=False),
                json.dumps(profile_data.get('style', {}), ensure_ascii=False),
                json.dumps(profile_data.get('child'), ensure_ascii=False) if profile_data.get('child') else None
            ))
            conn.commit()
    
    def get_profile(self, member_id: str) -> Optional[Dict]:
        """获取成员画像"""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM profiles WHERE member_id = ?", (member_id,))
            row = cursor.fetchone()
            if not row:
                return None
            
            profile = dict(row)
            # 解析 JSON 字段
            if profile.get('body'):
                profile['body'] = json.loads(profile['body'])
            if profile.get('style'):
                profile['style'] = json.loads(profile['style'])
            if profile.get('child'):
                profile['child'] = json.loads(profile['child'])
            return profile
    
    def update_profile(self, member_id: str, updates: Dict) -> bool:
        """更新成员画像"""
        if not updates:
            return False
        
        # 处理 JSON 字段
        json_fields = ['body', 'style', 'child']
        for field in json_fields:
            if field in updates and isinstance(updates[field], dict):
                updates[field] = json.dumps(updates[field], ensure_ascii=False)
        
        updates['updated_at'] = datetime.now().isoformat()
        
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [member_id]
        
        with self._get_connection() as conn:
            conn.execute(f"UPDATE profiles SET {set_clause} WHERE member_id = ?", values)
            conn.commit()
        return True
    
    # ===== 关注来源操作 =====
    
    def add_followed_source(self, source: Dict) -> str:
        """添加关注来源"""
        source_id = source.get('id') or f"source_{uuid.uuid4().hex[:8]}"
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO followed_sources 
                (id, member_id, source_type, source_id, name, url, avatar, description, follower_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                source_id,
                source.get('member_id'),
                source.get('source_type'),
                source.get('source_id'),
                source.get('name'),
                source.get('url'),
                source.get('avatar'),
                source.get('description'),
                source.get('follower_count')
            ))
            conn.commit()
        return source_id
    
    def get_followed_sources(self, member_id: Optional[str] = None) -> List[Dict]:
        """获取关注来源列表"""
        with self._get_connection() as conn:
            if member_id:
                cursor = conn.execute(
                    "SELECT * FROM followed_sources WHERE member_id = ? OR member_id IS NULL",
                    (member_id,)
                )
            else:
                cursor = conn.execute("SELECT * FROM followed_sources")
            return [dict(row) for row in cursor.fetchall()]
    
    def update_source_last_checked(self, source_id: str):
        """更新来源最后检查时间"""
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE followed_sources SET last_checked = ? WHERE id = ?",
                (datetime.now().isoformat(), source_id)
            )
            conn.commit()
    
    def delete_followed_source(self, source_id: str) -> bool:
        """删除关注来源"""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM followed_sources WHERE id = ?", (source_id,))
            conn.execute("DELETE FROM source_items WHERE source_id = ?", (source_id,))
            conn.commit()
        return True
    
    # ===== 关注商品操作 =====
    
    def add_source_item(self, item: Dict) -> str:
        """添加关注来源的商品"""
        item_id = item.get('id') or f"sitem_{uuid.uuid4().hex[:8]}"
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO source_items 
                (id, source_id, external_id, name, category, color, style, price, original_price, 
                 image_url, local_image_path, description, url, is_new, is_analyzed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item_id,
                item.get('source_id'),
                item.get('external_id'),
                item.get('name'),
                item.get('category'),
                item.get('color'),
                item.get('style'),
                item.get('price'),
                item.get('original_price'),
                item.get('image_url'),
                item.get('local_image_path'),
                item.get('description'),
                item.get('url'),
                item.get('is_new', 1),
                item.get('is_analyzed', 0)
            ))
            conn.commit()
        return item_id
    
    def get_source_items(self, source_id: str, is_new: Optional[bool] = None) -> List[Dict]:
        """获取关注来源的商品"""
        with self._get_connection() as conn:
            if is_new is not None:
                cursor = conn.execute(
                    "SELECT * FROM source_items WHERE source_id = ? AND is_new = ? ORDER BY added_at DESC",
                    (source_id, 1 if is_new else 0)
                )
            else:
                cursor = conn.execute(
                    "SELECT * FROM source_items WHERE source_id = ? ORDER BY added_at DESC",
                    (source_id,)
                )
            return [dict(row) for row in cursor.fetchall()]
    
    def mark_item_analyzed(self, item_id: str, analysis_result: Dict):
        """标记商品已分析"""
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE source_items SET is_analyzed = 1, analysis_result = ? WHERE id = ?",
                (json.dumps(analysis_result, ensure_ascii=False), item_id)
            )
            conn.commit()
    
    # ===== 单品操作 =====
    
    def add_item(self, item: Dict[str, Any], member_id: Optional[str] = None) -> str:
        """添加单品，自动检测重复"""
        import uuid
        
        # 如果没有指定 member_id，尝试从 item 中获取
        if not member_id:
            member_id = item.get('member_id')
        
        # 检查是否已存在（根据成员、名称和颜色）
        existing = self._find_duplicate(item, member_id)
        if existing:
            # 更新而不是新建
            item_id = existing['id']
            self.update_item(item_id, item)
            return item_id
        
        item_id = item.get('id') or f"item_{uuid.uuid4().hex[:8]}"
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO items (id, member_id, name, category, color, style, season, material, 
                                   brand, price, source, source_url, image_path, tags, wear_count, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item_id,
                member_id,
                item.get('name', ''),
                item.get('category', ''),
                item.get('color', ''),
                item.get('style', ''),
                item.get('season', ''),
                item.get('material', ''),
                item.get('brand'),
                item.get('price'),
                item.get('source'),
                item.get('source_url'),
                item.get('image_path', ''),
                json.dumps(item.get('tags', []), ensure_ascii=False),
                item.get('wear_count', 0),
                datetime.now().isoformat()
            ))
            conn.commit()
        
        return item_id
    
    def _find_duplicate(self, item: Dict, member_id: Optional[str] = None) -> Optional[Dict]:
        """查找重复单品（同成员内）"""
        name = item.get('name', '')
        color = item.get('color', '')
        category = item.get('category', '')
        
        with self._get_connection() as conn:
            # 在同成员内检查重复
            if member_id:
                cursor = conn.execute("""
                    SELECT * FROM items 
                    WHERE name = ? AND color = ? AND category = ? AND member_id = ?
                """, (name, color, category, member_id))
            else:
                # 兼容旧数据（无 member_id）
                cursor = conn.execute("""
                    SELECT * FROM items 
                    WHERE name = ? AND color = ? AND category = ? AND (member_id IS NULL OR member_id = '')
                """, (name, color, category))
            
            row = cursor.fetchone()
            if row:
                return self._row_to_dict(row)
        
        return None
    
    def get_item(self, item_id: str) -> Optional[Dict]:
        """获取单品详情"""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM items WHERE id = ?", (item_id,)
            ).fetchone()
            
            if row:
                return self._row_to_dict(row)
            return None
    
    def get_all_items(self, category: str = None, member_id: str = None) -> List[Dict]:
        """获取所有单品
        
        Args:
            category: 按品类筛选
            member_id: 按成员筛选
        """
        with self._get_connection() as conn:
            query = "SELECT * FROM items WHERE 1=1"
            params = []
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            if member_id:
                query += " AND member_id = ?"
                params.append(member_id)
            
            query += " ORDER BY created_at DESC"
            
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def count_items(self, member_id: str = None) -> int:
        """统计单品数量"""
        with self._get_connection() as conn:
            if member_id:
                cursor = conn.execute("SELECT COUNT(*) FROM items WHERE member_id = ?", (member_id,))
            else:
                cursor = conn.execute("SELECT COUNT(*) FROM items")
            return cursor.fetchone()[0]
    
    def update_item(self, item_id: str, updates: Dict[str, Any]) -> bool:
        """更新单品"""
        allowed_fields = ['name', 'category', 'color', 'style', 'season', 'material', 'image_path', 'tags']
        fields = []
        values = []
        
        for key, value in updates.items():
            if key in allowed_fields:
                fields.append(f"{key} = ?")
                if key == 'tags':
                    values.append(json.dumps(value, ensure_ascii=False))
                else:
                    values.append(value)
        
        if not fields:
            return False
        
        fields.append("updated_at = ?")
        values.append(datetime.now().isoformat())
        values.append(item_id)
        
        with self._get_connection() as conn:
            conn.execute(
                f"UPDATE items SET {', '.join(fields)} WHERE id = ?",
                values
            )
            conn.commit()
        
        return True
    
    def delete_item(self, item_id: str) -> bool:
        """删除单品"""
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def search_items(self, query: str) -> List[Dict]:
        """搜索单品"""
        with self._get_connection() as conn:
            pattern = f"%{query}%"
            rows = conn.execute("""
                SELECT * FROM items 
                WHERE name LIKE ? OR color LIKE ? OR style LIKE ? OR tags LIKE ?
                ORDER BY created_at DESC
            """, (pattern, pattern, pattern, pattern)).fetchall()
            
            return [self._row_to_dict(row) for row in rows]
    
    # ===== 穿搭记录操作 =====
    
    def add_outfit(self, outfit: Dict[str, Any]) -> str:
        """添加穿搭记录"""
        import uuid
        outfit_id = outfit.get('id') or f"outfit_{uuid.uuid4().hex[:8]}"
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO outfits (id, date, items, occasion, weather, notes, rating)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                outfit_id,
                outfit.get('date', datetime.now().strftime('%Y-%m-%d')),
                json.dumps(outfit.get('items', []), ensure_ascii=False),
                outfit.get('occasion', ''),
                json.dumps(outfit.get('weather', {}), ensure_ascii=False),
                outfit.get('notes', ''),
                outfit.get('rating', 0)
            ))
            conn.commit()
        
        return outfit_id
    
    def get_outfits(self, date: str = None, limit: int = 100) -> List[Dict]:
        """获取穿搭记录"""
        with self._get_connection() as conn:
            if date:
                rows = conn.execute(
                    "SELECT * FROM outfits WHERE date = ? ORDER BY date DESC LIMIT ?",
                    (date, limit)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM outfits ORDER BY date DESC LIMIT ?",
                    (limit,)
                ).fetchall()
            
            return [self._row_to_dict(row) for row in rows]
    
    def get_calendar_outfits(self, year: int, month: int) -> Dict[str, Dict]:
        """获取日历视图穿搭记录"""
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{(month+1):02d}-01"
        
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM outfits 
                WHERE date >= ? AND date < ?
                ORDER BY date
            """, (start_date, end_date)).fetchall()
            
            return {row['date']: self._row_to_dict(row) for row in rows}
    
    # ===== 用户偏好操作 =====
    
    def set_preference(self, key: str, value: str):
        """设置用户偏好"""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO preferences (key, value, updated_at)
                VALUES (?, ?, ?)
            """, (key, value, datetime.now().isoformat()))
            conn.commit()
    
    def get_preference(self, key: str, default: str = None) -> str:
        """获取用户偏好"""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT value FROM preferences WHERE key = ?", (key,)
            ).fetchone()
            
            return row['value'] if row else default
    
    def get_all_preferences(self) -> Dict[str, str]:
        """获取所有偏好"""
        with self._get_connection() as conn:
            rows = conn.execute("SELECT key, value FROM preferences").fetchall()
            return {row['key']: row['value'] for row in rows}
    
    # ===== 统计信息 =====
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._get_connection() as conn:
            # 单品统计
            item_count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
            
            # 分类统计
            cat_stats = conn.execute(
                "SELECT category, COUNT(*) as count FROM items GROUP BY category"
            ).fetchall()
            
            # 穿搭记录统计
            outfit_count = conn.execute("SELECT COUNT(*) FROM outfits").fetchone()[0]
            
            # 颜色统计
            color_stats = conn.execute(
                "SELECT color, COUNT(*) as count FROM items WHERE color IS NOT NULL GROUP BY color"
            ).fetchall()
            
            return {
                "total_items": item_count,
                "total_outfits": outfit_count,
                "by_category": {row['category']: row['count'] for row in cat_stats},
                "by_color": {row['color']: row['count'] for row in color_stats}
            }
    
    # ===== 备份/恢复 =====
    
    def export_data(self) -> Dict[str, Any]:
        """导出所有数据"""
        return {
            "items": self.get_all_items(),
            "outfits": self.get_outfits(),
            "preferences": self.get_all_preferences(),
            "exported_at": datetime.now().isoformat()
        }
    
    def import_data(self, data: Dict[str, Any]) -> Dict[str, int]:
        """导入数据"""
        counts = {"items": 0, "outfits": 0}
        
        with self._get_connection() as conn:
            # 导入单品
            for item in data.get('items', []):
                try:
                    conn.execute("""
                        INSERT OR REPLACE INTO items 
                        (id, name, category, color, style, season, material, image_path, tags, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        item.get('id'), item.get('name'), item.get('category'),
                        item.get('color'), item.get('style'), item.get('season'),
                        item.get('material'), item.get('image_path'),
                        json.dumps(item.get('tags', [])),
                        item.get('created_at'), item.get('updated_at')
                    ))
                    counts["items"] += 1
                except:
                    pass
            
            # 导入穿搭记录
            for outfit in data.get('outfits', []):
                try:
                    conn.execute("""
                        INSERT OR REPLACE INTO outfits 
                        (id, date, items, occasion, weather, notes, rating, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        outfit.get('id'), outfit.get('date'),
                        json.dumps(outfit.get('items', [])),
                        outfit.get('occasion'),
                        json.dumps(outfit.get('weather', {})),
                        outfit.get('notes'), outfit.get('rating'),
                        outfit.get('created_at')
                    ))
                    counts["outfits"] += 1
                except:
                    pass
            
            conn.commit()
        
        return counts
    
    # ===== 辅助方法 =====
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """将行转换为字典"""
        result = dict(row)
        
        # 解析 JSON 字段
        for key in ['tags', 'items', 'weather']:
            if key in result and result[key]:
                try:
                    result[key] = json.loads(result[key])
                except:
                    pass
        
        return result


    # ===== 种草清单操作 =====
    
    def add_to_wishlist(self, item: Dict) -> str:
        """添加商品到种草清单"""
        import uuid
        item_id = str(uuid.uuid4())[:8]
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO wishlist (id, name, category, color, style, material,
                                    price, brand, image_path, reason, store_location, added_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item_id,
                item.get('name', ''),
                item.get('category', ''),
                item.get('color', ''),
                item.get('style', ''),
                item.get('material', ''),
                item.get('price', ''),
                item.get('brand', ''),
                item.get('image_path', ''),
                item.get('reason', ''),
                item.get('store_location', ''),
                datetime.now().isoformat()
            ))
            conn.commit()
        
        return item_id
    
    def get_wishlist(self, purchased: bool = None) -> List[Dict]:
        """获取种草清单"""
        with self._get_connection() as conn:
            if purchased is None:
                rows = conn.execute(
                    "SELECT * FROM wishlist ORDER BY added_at DESC"
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM wishlist WHERE purchased = ? ORDER BY added_at DESC",
                    (purchased,)
                ).fetchall()
            
            return [self._row_to_dict(row) for row in rows]
    
    def mark_wishlist_purchased(self, item_id: str) -> bool:
        """标记种草商品为已购买"""
        with self._get_connection() as conn:
            result = conn.execute("""
                UPDATE wishlist 
                SET purchased = 1, purchased_at = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), item_id))
            conn.commit()
            return result.rowcount > 0
    
    def delete_from_wishlist(self, item_id: str) -> bool:
        """从种草清单删除"""
        with self._get_connection() as conn:
            result = conn.execute("DELETE FROM wishlist WHERE id = ?", (item_id,))
            conn.commit()
            return result.rowcount > 0
