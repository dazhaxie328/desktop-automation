#!/bin/bash
# 智能桌面自动化机器人启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/smart_bot.py"

# 检查虚拟环境
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv "$SCRIPT_DIR/venv"
    source "$SCRIPT_DIR/venv/bin/activate"
    pip install pyautogui pillow pynput requests -q
else
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# 检查 .env 文件
ENV_FILE="$HOME/crypto-monitor/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "错误: 未找到 .env 文件"
    echo "请先配置 Telegram Bot Token 和 Chat ID"
    exit 1
fi

echo "=========================================="
echo "🤖 智能桌面自动化机器人"
echo "=========================================="
echo "启动时间: $(date)"
echo "按 Ctrl+C 停止"
echo "=========================================="

# 运行机器人
python3 "$PYTHON_SCRIPT"
