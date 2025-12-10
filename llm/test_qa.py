#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
该脚本用于调用大模型API生成高考作文
"""

import json
import requests
import time

# 模型API配置
API_URL = "http://192.168.101.131:18080/v1/chat/completions"
MODEL_NAME = "qwen3-8b"

def generate_essay():
    """
    生成一篇高考作文《我的区长父亲》
    """
    # 构造聊天消息
    messages = [
        {
            "role": "user", 
            "content": "请生成一篇800字的高考作文，题目为《我的区长父亲》/no_think"
        }
    ]
    
    # 构造请求数据
    data = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        # 记录开始时间
        start_time = time.time()
        
        # 发送POST请求到模型API
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            timeout=60
        )
        
        # 记录结束时间
        end_time = time.time()
        
        # 解析响应
        result = response.json()
        
        # 提取作文内容
        if "choices" in result and len(result["choices"]) > 0:
            essay_content = result["choices"][0]["message"]["content"]
            print("=== 生成的作文 ===")
            print(essay_content)
            
            # 提取token信息
            usage = result.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)
            
            # 计算时间和速度
            elapsed_time = end_time - start_time
            tokens_per_second = completion_tokens / elapsed_time if elapsed_time > 0 else 0
            
            print("\n=== Token统计信息 ===")
            print(f"输入token数量: {prompt_tokens}")
            print(f"输出token数量: {completion_tokens}")
            print(f"总token数量: {total_tokens}")
            print(f"生成耗时: {elapsed_time:.2f} 秒")
            print(f"Token输出速度: {tokens_per_second:.2f} tokens/秒")
            
            return True
        else:
            print("API响应格式不正确")
            return False
            
    except Exception as e:
        print(f"请求失败: {e}")
        return False

if __name__ == "__main__":
    print(f"正在调用模型 {MODEL_NAME} 生成作文...")
    print(f"API 地址: {API_URL}")
    
    generate_essay()