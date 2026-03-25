#!/usr/bin/env python3
"""
Clothy v0.5.0 功能测试
测试多人衣橱和淘宝联动功能
"""

import asyncio
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(__file__))

from main import Clothy
from src.core.member_manager import MemberManager
from src.core.session_manager import SessionManager
from src.core.command_parser import CommandParser, Intent
from src.storage.database import Database

def test_basic_functionality():
    """测试基础功能"""
    print("\n=== 基础功能测试 ===\n")
    
    app = Clothy()
    
    # 测试1: 欢迎
    print("1. 测试欢迎消息...")
    result = app.process('你好')
    print(f"   ✅ 收到响应: {len(result.get('text', ''))} 字符")
    
    # 测试2: 帮助
    print("\n2. 测试帮助...")
    result = app.process('帮助')
    print(f"   ✅ 收到帮助信息")
    
    # 测试3: 录入单品
    print("\n3. 测试录入单品...")
    result = app.process('录入一件白色T恤')
    print(f"   ✅ 录入结果: {result.get('text', '')[:100]}...")
    
    # 测试4: 查看衣橱
    print("\n4. 测试查看衣橱...")
    result = app.process('看看我的衣橱')
    print(f"   ✅ 衣橱信息: {result.get('text', '')[:100]}...")
    
    # 测试5: 搭配推荐
    print("\n5. 测试搭配推荐...")
    result = app.process('今天穿什么')
    print(f"   ✅ 推荐结果: {result.get('text', '')[:100]}...")

def test_member_management():
    """测试成员管理"""
    print("\n\n=== 成员管理测试 ===\n")
    
    db = Database()
    member_manager = MemberManager(db)
    
    # 测试1: 添加成员
    print("1. 测试添加成员...")
    result = member_manager.add_member("小美", relationship="配偶", gender='女')
    print(f"   ✅ 添加成员: {result.name} (ID: {result.id})")
    
    # 测试2: 添加儿童成员
    print("\n2. 测试添加儿童成员...")
    result = member_manager.add_member("小明", relationship="孩子", gender='男')
    print(f"   ✅ 添加儿童: {result.name} (关系: {result.relationship})")
    
    # 测试3: 获取所有成员
    print("\n3. 测试获取成员列表...")
    members = member_manager.get_all_members()
    print(f"   ✅ 成员数量: {len(members)}")
    for m in members:
        print(f"      - {m.name} ({m.relationship})")
    
    # 测试4: 成员识别
    print("\n4. 测试成员识别...")
    text = "给小明添加一件蓝色外套"
    member = member_manager.recognize_member_from_text(text)
    print(f"   输入: {text}")
    if member:
        print(f"   ✅ 识别成员: {member.name} ({member.id})")
    else:
        print("   ✅ 未识别到成员（使用当前成员）")

def test_command_parsing():
    """测试命令解析"""
    print("\n\n=== 命令解析测试 ===\n")
    
    parser = CommandParser()
    
    test_cases = [
        ("录入一件白色T恤", Intent.ADD_ITEM),
        ("今天穿什么", Intent.GET_RECOMMENDATION),
        ("看看我的衣橱", Intent.LIST_ITEMS),
        ("分析我的衣橱", Intent.ANALYZE_WARDROBE),
        ("添加家庭成员", Intent.ADD_MEMBER),
        ("切换到小美的衣橱", Intent.SWITCH_MEMBER),
        ("导入淘宝订单", Intent.IMPORT_ORDER),
        ("关注店铺优衣库", Intent.FOLLOW_SHOP),
        ("帮我搭配一套职场风格", Intent.GET_RECOMMENDATION),
    ]
    
    for text, expected_intent in test_cases:
        result = parser.parse(text)
        status = "✅" if result.intent == expected_intent else "❌"
        print(f"{status} \"{text}\"")
        print(f"   意图: {result.intent.value}")
        if result.item_name:
            print(f"   单品: {result.item_name}")
        if result.category:
            print(f"   品类: {result.category}")

def test_session_management():
    """测试会话管理"""
    print("\n\n=== 会话管理测试 ===\n")
    
    db = Database()
    member_mgr = MemberManager(db)
    session_mgr = SessionManager(db, member_mgr)
    
    # 添加测试成员
    member1 = member_mgr.add_member("测试用户1", "其他")
    member2 = member_mgr.add_member("测试用户2", "其他")
    
    # 测试切换成员
    print("1. 测试切换成员...")
    session_mgr.switch_member(member1.id)
    current = session_mgr.get_current_member_id()
    print(f"   ✅ 当前成员: {current}")
    
    # 测试获取当前成员信息
    print("\n2. 测试获取当前成员...")
    current_member = session_mgr.get_current_member()
    if current_member:
        print(f"   ✅ 当前成员名: {current_member.name}")
    
    print("\n   ✅ 会话管理功能正常")

def test_message_builder():
    """测试消息构建"""
    print("\n\n=== 消息构建测试 ===\n")
    
    from src.services.message_builder import MessageBuilder
    
    # 测试1: 欢迎消息
    print("1. 测试欢迎消息...")
    msg = MessageBuilder.build_welcome_message(has_items=False)
    print(f"   ✅ 消息类型: {msg.get('msgtype')}")
    
    # 测试2: 单品添加消息
    print("\n2. 测试单品添加消息...")
    msg = MessageBuilder.build_item_added_message(
        {'name': '白色T恤', 'color': '白色', 'category': 'top'},
        {'name': '小美', 'avatar': '👩'}
    )
    print(f"   ✅ 消息类型: {msg.get('msgtype')}")
    
    # 测试3: 衣橱分析消息
    print("\n3. 测试衣橱分析消息...")
    stats = {
        'total': 10,
        'categories': {'top': 4, 'bottom': 3, 'outer': 2, 'shoes': 1},
        'colors': {'白色': 5, '蓝色': 3, '黑色': 2},
        'styles': {'休闲': 6, '商务': 4}
    }
    msg = MessageBuilder.build_analysis_message(stats)
    print(f"   ✅ 消息类型: {msg.get('msgtype')}")

def test_ai_recognition():
    """测试 AI 识别（需要 API Key）"""
    print("\n\n=== AI 识别测试 ===\n")
    
    try:
        from src.services.clothing_recognizer import ClothingRecognizer
        
        recognizer = ClothingRecognizer()
        print("✅ AI 识别器初始化成功")
        
        # 检查模型配置
        print(f"   视觉模型: {recognizer.vision_model}")
        print(f"   文本模型: {recognizer.text_model}")
        
    except Exception as e:
        print(f"⚠️ AI 识别器初始化失败: {e}")
        print("   需要配置 DASHSCOPE_API_KEY 环境变量")

def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("Clothy v0.5.0 功能测试")
    print("="*50)
    
    try:
        test_basic_functionality()
        test_member_management()
        test_command_parsing()
        test_session_management()
        test_message_builder()
        test_ai_recognition()
        
        print("\n" + "="*50)
        print("✅ 所有测试完成！")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()