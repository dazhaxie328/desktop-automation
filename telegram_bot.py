#!/usr/bin/env python3
"""
Telegram 交互式桌面自动化
通过 Telegram 消息控制电脑
"""

import requests
import json
import time
import os
import subprocess
from datetime import datetime
from pathlib import Path
import pyautogui

# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

# 加载 .env 文件
def load_env_file():
    env_file = Path.home() / "crypto-monitor" / ".env"
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

load_env_file()

# 配置
CONFIG = {
    "telegram_bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
    "telegram_chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
    "screenshot_dir": Path.home() / "desktop-automation" / "screenshots",
}

CONFIG["screenshot_dir"].mkdir(parents=True, exist_ok=True)


class TelegramDesktopBot:
    """Telegram 桌面自动化机器人"""
    
    def __init__(self):
        self.token = CONFIG["telegram_bot_token"]
        self.chat_id = CONFIG["telegram_chat_id"]
        self.api_url = f"https://api.telegram.org/bot{self.token}"
        self.last_update_id = 0
        self.running = False
        
        # 命令映射
        self.commands = {
            "/start": self.cmd_start,
            "/help": self.cmd_help,
            "/screenshot": self.cmd_screenshot,
            "/click": self.cmd_click,
            "/type": self.cmd_type,
            "/key": self.cmd_key,
            "/hotkey": self.cmd_hotkey,
            "/move": self.cmd_move,
            "/scroll": self.cmd_scroll,
            "/pos": self.cmd_position,
            "/screen": self.cmd_screen_size,
            "/run": self.cmd_run_command,
            "/open": self.cmd_open_file,
            "/mouse": self.cmd_mouse_circle,
        }
    
    def send_message(self, text, parse_mode="HTML"):
        """发送消息"""
        url = f"{self.api_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        try:
            resp = requests.post(url, json=payload, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            print(f"发送消息失败: {e}")
            return False
    
    def send_photo(self, photo_path, caption=""):
        """发送图片"""
        url = f"{self.api_url}/sendPhoto"
        with open(photo_path, "rb") as photo:
            files = {"photo": photo}
            data = {"chat_id": self.chat_id, "caption": caption}
            try:
                resp = requests.post(url, files=files, data=data, timeout=30)
                return resp.status_code == 200
            except Exception as e:
                print(f"发送图片失败: {e}")
                return False
    
    def get_updates(self):
        """获取新消息"""
        url = f"{self.api_url}/getUpdates"
        params = {"offset": self.last_update_id + 1, "timeout": 5}
        try:
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok"):
                    return data.get("result", [])
        except Exception as e:
            print(f"获取更新失败: {e}")
        return []
    
    def process_command(self, text):
        """处理命令"""
        parts = text.strip().split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command in self.commands:
            return self.commands[command](args)
        else:
            return f"❌ 未知命令: {command}\n发送 /help 查看帮助"
    
    # ========== 命令处理 ==========
    
    def cmd_start(self, args):
        """开始命令"""
        return """🤖 <b>桌面自动化机器人</b>

欢迎！我可以通过 Telegram 控制你的电脑。

📋 <b>可用命令：</b>

📸 <b>截图：</b>
/screenshot - 截取屏幕

🖱️ <b>鼠标：</b>
/click x y - 点击指定位置
/move x y - 移动鼠标
/scroll amount - 滚动 (正=上, 负=下)
/pos - 获取鼠标位置
/mouse - 鼠标画圆测试

⌨️ <b>键盘：</b>
/type text - 输入文本
/key keyname - 按下按键 (enter, tab, etc.)
/hotkey key1 key2 - 组合键 (ctrl c)

📁 <b>文件：</b>
/open filepath - 打开文件

💻 <b>系统：</b>
/screen - 获取屏幕尺寸
/run command - 运行终端命令
/help - 显示帮助

⚠️ <b>安全：</b>
鼠标移到屏幕左上角可终止自动化"""
    
    def cmd_help(self, args):
        """帮助命令"""
        return self.cmd_start(args)
    
    def cmd_screenshot(self, args):
        """截图命令"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = CONFIG["screenshot_dir"] / f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(str(filepath))
            
            self.send_photo(str(filepath), "📸 屏幕截图")
            return None  # 已经发送了图片，不需要再发消息
        except Exception as e:
            return f"❌ 截图失败: {e}"
    
    def cmd_click(self, args):
        """点击命令"""
        try:
            parts = args.split()
            if len(parts) < 2:
                return "❌ 用法: /click x y\n例如: /click 500 300"
            
            x, y = int(parts[0]), int(parts[1])
            button = parts[2] if len(parts) > 2 else "left"
            
            pyautogui.click(x, y, button=button)
            return f"✅ 点击 ({x}, {y}) - {button}键"
        except ValueError:
            return "❌ 坐标必须是数字"
        except Exception as e:
            return f"❌ 点击失败: {e}"
    
    def cmd_type(self, args):
        """输入命令"""
        try:
            if not args:
                return "❌ 用法: /type 文本\n例如: /type Hello World"
            
            pyautogui.typewrite(args, interval=0.05)
            return f"✅ 输入: {args}"
        except Exception as e:
            return f"❌ 输入失败: {e}"
    
    def cmd_key(self, args):
        """按键命令"""
        try:
            if not args:
                return "❌ 用法: /key 按键名\n例如: /key enter"
            
            pyautogui.press(args)
            return f"✅ 按下: {args}"
        except Exception as e:
            return f"❌ 按键失败: {e}"
    
    def cmd_hotkey(self, args):
        """组合键命令"""
        try:
            if not args:
                return "❌ 用法: /hotkey key1 key2 ...\n例如: /hotkey ctrl c"
            
            keys = args.split()
            pyautogui.hotkey(*keys)
            return f"✅ 组合键: {'+'.join(keys)}"
        except Exception as e:
            return f"❌ 组合键失败: {e}"
    
    def cmd_move(self, args):
        """移动鼠标命令"""
        try:
            parts = args.split()
            if len(parts) < 2:
                return "❌ 用法: /move x y\n例如: /move 500 300"
            
            x, y = int(parts[0]), int(parts[1])
            pyautogui.moveTo(x, y, duration=0.5)
            return f"✅ 鼠标移动到 ({x}, {y})"
        except ValueError:
            return "❌ 坐标必须是数字"
        except Exception as e:
            return f"❌ 移动失败: {e}"
    
    def cmd_scroll(self, args):
        """滚动命令"""
        try:
            if not args:
                return "❌ 用法: /scroll 数量\n例如: /scroll 3 (向上) 或 /scroll -3 (向下)"
            
            amount = int(args)
            pyautogui.scroll(amount)
            direction = "上" if amount > 0 else "下"
            return f"✅ 滚动{direction} {abs(amount)} 格"
        except ValueError:
            return "❌ 数量必须是数字"
        except Exception as e:
            return f"❌ 滚动失败: {e}"
    
    def cmd_position(self, args):
        """获取鼠标位置"""
        try:
            pos = pyautogui.position()
            return f"🖱️ 鼠标位置: ({pos.x}, {pos.y})"
        except Exception as e:
            return f"❌ 获取位置失败: {e}"
    
    def cmd_screen_size(self, args):
        """获取屏幕尺寸"""
        try:
            size = pyautogui.size()
            return f"🖥️ 屏幕尺寸: {size.width} x {size.height}"
        except Exception as e:
            return f"❌ 获取尺寸失败: {e}"
    
    def cmd_run_command(self, args):
        """运行终端命令"""
        try:
            if not args:
                return "❌ 用法: /run 命令\n例如: /run ls -la"
            
            # 安全检查
            dangerous_commands = ["rm -rf", "sudo", "mkfs", "dd"]
            for cmd in dangerous_commands:
                if cmd in args.lower():
                    return f"❌ 危险命令被拒绝: {args}"
            
            result = subprocess.run(
                args, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            output = result.stdout or result.stderr or "(无输出)"
            if len(output) > 2000:
                output = output[:2000] + "\n...(截断)"
            
            return f"💻 <b>命令:</b> <code>{args}</code>\n\n📤 <b>输出:</b>\n<pre>{output}</pre>"
        except subprocess.TimeoutExpired:
            return "❌ 命令超时 (30秒)"
        except Exception as e:
            return f"❌ 执行失败: {e}"
    
    def cmd_open_file(self, args):
        """打开文件"""
        try:
            if not args:
                return "❌ 用法: /open 文件路径\n例如: /open ~/document.txt"
            
            filepath = os.path.expanduser(args)
            if not os.path.exists(filepath):
                return f"❌ 文件不存在: {filepath}"
            
            if os.name == "nt":
                os.startfile(filepath)
            else:
                subprocess.run(["xdg-open", filepath])
            
            return f"✅ 打开: {filepath}"
        except Exception as e:
            return f"❌ 打开失败: {e}"
    
    def cmd_mouse_circle(self, args):
        """鼠标画圆测试"""
        try:
            import math
            radius = int(args) if args else 100
            
            center = pyautogui.position()
            steps = 20
            
            for i in range(steps + 1):
                angle = 2 * math.pi * i / steps
                x = center.x + radius * math.cos(angle)
                y = center.y + radius * math.sin(angle)
                pyautogui.moveTo(x, y, duration=0.05)
            
            return f"✅ 鼠标画圆完成 (半径: {radius})"
        except Exception as e:
            return f"❌ 画圆失败: {e}"
    
    # ========== 主循环 ==========
    
    def run(self):
        """运行机器人"""
        self.running = True
        
        # 发送启动消息
        self.send_message("🤖 <b>桌面自动化机器人已启动</b>\n\n发送 /help 查看可用命令")
        
        print("🤖 Telegram 桌面自动化机器人已启动")
        print("按 Ctrl+C 停止")
        
        try:
            while self.running:
                updates = self.get_updates()
                
                for update in updates:
                    self.last_update_id = update["update_id"]
                    
                    message = update.get("message", {})
                    text = message.get("text", "")
                    chat_id = str(message.get("chat", {}).get("id", ""))
                    
                    # 只处理指定用户的消息
                    if chat_id != self.chat_id:
                        continue
                    
                    if text:
                        print(f"收到命令: {text}")
                        response = self.process_command(text)
                        if response:
                            self.send_message(response)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n机器人已停止")
            self.send_message("🤖 机器人已停止")


# ========== 主程序 ==========

if __name__ == "__main__":
    bot = TelegramDesktopBot()
    bot.run()
