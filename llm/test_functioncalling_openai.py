#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
该脚本使用标准的openai库测试指定的大模型API是否支持function calling功能
通过定义几个测试函数并发送给模型调用请求，验证模型是否能正确返回函数调用信息
测试模型地址: http://192.168.101.180:30080/v1/chat/completions
测试模型名称: qwen3-1.7b
API密钥: gpustack_1fbe163632cb5698_a8eddb7fc49ee0e56b24c559174b8ad1
"""

import json
from openai import OpenAI

# 模型API配置
API_URL = "http://10.2.69.242:18080/v1"
MODEL_NAME = "qwen3-8b"
API_KEY = ""

# 创建OpenAI客户端
client = OpenAI(base_url=API_URL, api_key=API_KEY)

# 定义测试用的函数
functions = [
    {
        "name": "get_current_weather",
        "description": "获取指定城市的当前天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名，例如：北京、上海"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "calculate",
        "description": "执行简单的数学计算",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "数学表达式，例如: 2+3*4"
                }
            },
            "required": ["expression"]
        }
    }
]

def test_function_calling():
    """
    测试模型的function calling功能（使用传统functions参数）
    """
    try:
        # 构造聊天消息
        messages = [
            {"role": "user", "content": "今天北京的天气怎么样？"}
        ]
        
        # 发送请求到模型API
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            functions=functions,
            temperature=0.7
        )
        
        # 解析响应
        result = response.model_dump()
        print("=== 模型API响应 ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 检查是否有函数调用
        choice = result["choices"][0]
        message = choice.get("message", {})
        # 检查function_call字段是否存在且不为None
        if "function_call" in message and message["function_call"] is not None:
            function_call = message["function_call"]
            print("\n=== 检测到函数调用 ===")
            print(f"函数名: {function_call['name']}")
            print(f"参数: {function_call['arguments']}")
            return True
        else:
            print("\n=== 未检测到函数调用 ===")
            print("模型响应:", message.get("content", "无内容"))
            return False
            
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def test_with_tools_parameter():
    """
    使用tools参数测试函数调用(OpenAI兼容格式)
    """
    try:
        messages = [
            {"role": "user", "content": "计算2+3*4的结果"}
        ]
        
        # 使用tools参数而不是functions参数
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "执行简单的数学计算",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "数学表达式，例如: 2+3*4"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            }
        ]
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto",  # auto表示让模型自己决定是否需要调用工具
            temperature=0.7
        )
        
        result = response.model_dump()
        print("\n\n=== Tools参数测试(OpenAI兼容格式) ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 检查是否有工具调用
        choice = result["choices"][0]
        message = choice.get("message", {})
        # 检查tool_calls字段
        if "tool_calls" in message and message["tool_calls"]:
            tool_calls = message["tool_calls"]
            print("\n=== 检测到工具调用 ===")
            for tool_call in tool_calls:
                print(f"工具ID: {tool_call.get('id', 'N/A')}")
                print(f"工具类型: {tool_call.get('type', 'N/A')}")
                function_data = tool_call.get('function', {})
                print(f"函数名: {function_data.get('name', 'N/A')}")
                print(f"参数: {function_data.get('arguments', 'N/A')}")
            return True
        else:
            print("\n=== 未检测到工具调用 ===")
            print("模型响应:", message.get("content", "无内容"))
            return False
            
    except Exception as e:
        print(f"Tools参数测试失败: {e}")
        return False

def test_parallel_function_calling():
    """
    测试并行函数调用功能
    """
    try:
        messages = [
            {"role": "user", "content": "请同时计算2+3*4的结果和查询北京的天气"}
        ]
        
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "执行简单的数学计算",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "数学表达式，例如: 2+3*4"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "获取指定城市的当前天气",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "城市名，例如：北京、上海"
                            }
                        },
                        "required": ["city"]
                    }
                }
            }
        ]
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.7
        )
        
        result = response.model_dump()
        print("\n\n=== 并行函数调用测试 ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 检查是否有工具调用
        choice = result["choices"][0]
        message = choice.get("message", {})
        if "tool_calls" in message and message["tool_calls"]:
            tool_calls = message["tool_calls"]
            print("\n=== 检测到并行工具调用 ===")
            for i, tool_call in enumerate(tool_calls):
                print(f"\n工具 #{i+1}:")
                function_data = tool_call.get('function', {})
                print(f"  函数名: {function_data.get('name', 'N/A')}")
                print(f"  参数: {function_data.get('arguments', 'N/A')}")
            return True
        else:
            print("\n=== 未检测到并行工具调用 ===")
            print("模型响应:", message.get("content", "无内容"))
            return False
            
    except Exception as e:
        print(f"并行函数调用测试失败: {e}")
        return False

def query_available_functions():
    """
    查询模型支持的函数列表
    注意：大多数模型不会直接暴露可用函数列表，需要通过文档或约定了解
    """
    print("\n=== 关于查询模型支持的函数 ===")
    print("大多数大语言模型不会直接暴露其支持的函数列表")
    print("可用函数通常由开发者在调用时提供，模型从中选择合适的函数调用")
    print("您需要查阅模型文档或API提供商文档来了解支持的函数")
    
    # 展示我们定义的测试函数作为示例
    print("\n=== 当前测试中使用的函数定义 ===")
    print(json.dumps(functions, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    print(f"正在测试模型 {MODEL_NAME} 的 function calling 功能...")
    print(f"API 地址: {API_URL}")
    print(f"API 密钥: {API_KEY}")
    
    # 执行各种测试
    print("\n" + "="*50)
    print("测试1: 基础函数调用")
    print("="*50)
    success1 = test_function_calling()
    
    print("\n" + "="*50)
    print("测试2: Tools参数(OpenAI兼容)")
    print("="*50)
    success2 = test_with_tools_parameter()
    
    print("\n" + "="*50)
    print("测试3: 并行函数调用")
    print("="*50)
    success3 = test_parallel_function_calling()
    
    # 查询可用函数信息
    query_available_functions()
    
    print("\n" + "="*50)
    print("测试总结")
    print("="*50)
    if success1 or success2 or success3:
        print("\n🎉 模型至少在某些形式下支持 function calling!")
        if success1:
            print("  ✓ 传统functions参数格式")
        if success2:
            print("  ✓ OpenAI兼容tools参数格式")
        if success3:
            print("  ✓ 并行函数调用")
    else:
        print("\n❌ 模型可能不支持 function calling 或配置有误")