#!/bin/bash

# 自动Git提交脚本
# 功能：自动添加、提交并推送Git更改

# 设置错误时退出
set -e

echo "开始自动Git提交流程..."

# 检查是否在Git仓库中
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "错误: 当前目录不是Git仓库！"
    exit 1
fi

# 处理参数，生成commit message
if [ $# -eq 0 ]; then
    # 没有参数，自动生成commit message
    commit_message="Auto commit at $(date '+%Y-%m-%d %H:%M:%S')"
else
    # 使用第一个参数作为commit message
    commit_message="$1"
fi

echo "提交信息: '$commit_message'"

# 步骤1: 添加所有更改的文件
echo "添加所有修改的文件..."
if ! git add .; then
    echo "错误: 添加文件失败！"
    exit 1
fi

# 步骤2: 检查是否有更改需要提交
if git diff --staged --quiet; then
    echo "没有检测到任何更改，无需提交。"
    exit 0
fi

# 步骤3: 提交更改
echo "提交更改..."
if ! git commit -m "$commit_message"; then
    echo "错误: 提交失败！"
    exit 1
fi

# 步骤4: 获取当前分支并推送到远程仓库
current_branch=$(git branch --show-current)
echo "推送到远程仓库的 $current_branch 分支..."

if ! git push origin "$current_branch"; then
    echo "错误: 推送失败！请检查远程仓库连接和权限。"
    exit 1
fi

echo "✓ 自动提交完成！"
echo "提交消息: '$commit_message'"
echo "已成功推送到远程仓库的 $current_branch 分支。"