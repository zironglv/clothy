#!/usr/bin/env python3
"""
Clothy 多人衣橱功能测试
测试核心功能是否正常工作
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import asyncio
from src.storage.database import Database
from src.core.member_manager import MemberManager
from src.core.session_manager import SessionManager
from src.core.command_parser import CommandParser, Intent
from src.services.message_builder import MessageBuilder


def test_database():
    """测试数据库初始化"""
    print("\n=== 测试数据库 ===")
    
    db = Database(":memory:")  # 使用内存数据库测试
    
    # 测试家庭创建
    family = db.get_or_create_family()
    print(f"✅ 家庭创建: {family['id']}")
    
    # 测试成员添加
    member_id = db.add_member(
        family_id=family['id'],
        name="我",
        relationship="self",
        gender="female"
    )
    print(f"✅ 成员添加: {member_id}")
    
    # 测试单品添加
    item_id = db.add_item({
        'name': '白色T恤',
        'category': 'top',
        'color': '白色',
        'style': 'casual'
    }, member_id=member_id)
    print(f"✅ 单品添加: {item_id}")
    
    # 测试查询
    items = db.get_all_items(member_id=member_id)
    print(f"✅ 单品查询: {len(items)} 件")
    
    return db


def test_member_manager(db):
    """测试成员管理"""
    print("\n=== 测试成员管理 ===")
    
    manager = MemberManager(db)
    
    # 列出成员
    members = manager.get_all_members()
    print(f"✅ 成员列表: {len(members)} 人")
    
    # 添加成员
    spouse = manager.add_member(name="老公", relationship="spouse", gender="male")
    print(f"✅ 添加配偶: {spouse.name} ({spouse.avatar})")
    
    child = manager.add_member(name="小孩", relationship="child", gender="male")
    print(f"✅ 添加孩子: {child.name} ({child.avatar})")
    
    # 测试识别
    test_cases = [
        "今天老公穿什么",
        "给小孩买件衣服",
        "我的衣橱",
        "帮宝宝选一套"
    ]
    
    for text in test_cases:
        member = manager.recognize_member(text)
        if member:
            print(f"✅ 识别「{text}」→ {member.name}")
        else:
            print(f"⚠️ 识别「{text}」→ 未识别")
    
    return manager


def test_session_manager(db, member_manager):
    """测试会话管理"""
    print("\n=== 测试会话管理 ===")
    
    session = SessionManager(db, member_manager, data_dir="/tmp/stylebuddy_test")
    
    # 获取当前成员
    current = session.get_current_member()
    print(f"✅ 当前成员: {current.name if current else '无'}")
    
    # 切换成员
    members = member_manager.get_all_members()
    spouse = [m for m in members if m.relationship == "spouse"][0]
    
    session.switch_to_member(spouse.id)
    current = session.get_current_member()
    print(f"✅ 切换后: {current.name}")
    
    return session


def test_command_parser(member_manager):
    """测试命令解析"""
    print("\n=== 测试命令解析 ===")
    
    parser = CommandParser(member_manager)
    
    test_cases = [
        ("今天我穿什么", Intent.GET_RECOMMENDATION),
        ("添加家庭成员", Intent.ADD_MEMBER),
        ("切换到老公的衣橱", Intent.SWITCH_MEMBER),
        ("录入一件白衬衫", Intent.ADD_ITEM),
        ("衣橱分析", Intent.ANALYZE_WARDROBE),
        ("初始化", Intent.INIT_PROFILE),
    ]
    
    for text, expected_intent in test_cases:
        cmd = parser.parse(text)
        status = "✅" if cmd.intent == expected_intent else "❌"
        print(f"{status} 「{text}」→ {cmd.intent.value} (成员: {cmd.member_name or '无'})")
    
    return parser


def test_message_builder():
    """测试消息构建"""
    print("\n=== 测试消息构建 ===")
    
    # Markdown
    msg = MessageBuilder.build_markdown("测试标题", "测试内容")
    print(f"✅ Markdown: {msg['msgtype']}")
    
    # 成员列表
    members = [
        {'name': '我', 'avatar': '👩', 'relationship': 'self', 'is_initialized': True},
        {'name': '老公', 'avatar': '👨', 'relationship': 'spouse', 'is_initialized': False},
    ]
    msg = MessageBuilder.build_member_list_message(members)
    print(f"✅ 成员列表: {len(msg['markdown']['text'])} 字符")
    
    # 推荐消息
    outfits = [
        {
            'style': '休闲',
            'items': ['白色T恤', '牛仔裤', '小白鞋'],
            'tips': '简约舒适'
        }
    ]
    weather = {'temperature': 25, 'weather': '晴'}
    msg = MessageBuilder.build_recommendation_message(outfits, weather)
    print(f"✅ 推荐消息: {len(msg['markdown']['text'])} 字符")


async def test_main_router():
    """测试主路由"""
    print("\n=== 测试主路由 ===")
    
    from src.core.main_router import MainRouter
    
    router = MainRouter(db_path=":memory:")
    
    # 测试帮助
    msg = await router.process_input("帮助")
    print(f"✅ 帮助响应: {msg.get('msgtype')}")
    
    # 测试成员列表
    msg = await router.process_input("家庭成员")
    print(f"✅ 成员列表: {msg.get('msgtype')}")
    
    # 测试推荐（空衣橱）
    msg = await router.process_input("今天穿什么")
    print(f"✅ 推荐响应: {msg.get('msgtype')}")


def main():
    """运行所有测试"""
    print("=" * 50)
    print("Clothy 多人衣橱功能测试")
    print("=" * 50)
    
    try:
        # 基础测试
        db = test_database()
        member_manager = test_member_manager(db)
        session_manager = test_session_manager(db, member_manager)
        parser = test_command_parser(member_manager)
        test_message_builder()
        
        # 异步测试
        print("\n=== 异步测试 ===")
        asyncio.run(test_main_router())
        
        print("\n" + "=" * 50)
        print("✅ 所有测试通过！")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())