#!/usr/bin/env python3
"""
智能桌面自动化机器人
支持自然语言命令，自动分解和执行复杂任务
"""

import requests
import json
import time
import os
import subprocess
import re
from datetime import datetime
from pathlib import Path
import pyautogui
from PIL import Image

# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# 加载配置
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

CONFIG = {
    "telegram_bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
    "telegram_chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
    "screenshot_dir": Path.home() / "desktop-automation" / "screenshots",
}

CONFIG["screenshot_dir"].mkdir(parents=True, exist_ok=True)


class SmartDesktopBot:
    """智能桌面自动化机器人"""
    
    def __init__(self):
        self.token = CONFIG["telegram_bot_token"]
        self.chat_id = CONFIG["telegram_chat_id"]
        self.api_url = f"https://api.telegram.org/bot{self.token}"
        self.last_update_id = 0
        self.running = False
        self.task_history = []
        
        # 智能命令映射
        self.smart_commands = {
            # 基础操作
            "截图": self.smart_screenshot,
            "截屏": self.smart_screenshot,
            "屏幕截图": self.smart_screenshot,
            
            # 鼠标操作
            "点击": self.smart_click,
            "单击": self.smart_click,
            "双击": self.smart_double_click,
            "右键": self.smart_right_click,
            "移动鼠标": self.smart_move_mouse,
            "滚动": self.smart_scroll,
            "向上滚": self.smart_scroll_up,
            "向下滚": self.smart_scroll_down,
            
            # 键盘操作
            "输入": self.smart_type,
            "打字": self.smart_type,
            "按键": self.smart_press_key,
            "回车": lambda args: self.smart_press_key("enter"),
            "退格": lambda args: self.smart_press_key("backspace"),
            "删除": lambda args: self.smart_press_key("delete"),
            "制表": lambda args: self.smart_press_key("tab"),
            "全选": lambda args: self.smart_hotkey("ctrl a"),
            "复制": lambda args: self.smart_hotkey("ctrl c"),
            "粘贴": lambda args: self.smart_hotkey("ctrl v"),
            "撤销": lambda args: self.smart_hotkey("ctrl z"),
            "保存": lambda args: self.smart_hotkey("ctrl s"),
            
            # 文件操作
            "打开": self.smart_open,
            "运行": self.smart_run,
            "执行": self.smart_run,
            
            # 信息获取
            "鼠标位置": self.smart_get_position,
            "屏幕大小": self.smart_get_screen_size,
            "屏幕尺寸": self.smart_get_screen_size,
            
            # 高级操作
            "找图": self.smart_find_image,
            "等待": self.smart_wait,
            "循环": self.smart_loop,
            "定时": self.smart_schedule,
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
    
    def parse_natural_language(self, text):
        """解析自然语言命令"""
        text = text.strip().lower()
        
        # 尝试匹配智能命令
        for keyword, handler in self.smart_commands.items():
            if keyword in text:
                # 提取参数
                args = text.replace(keyword, "").strip()
                return handler, args
        
        # 如果没有匹配到，尝试作为终端命令执行
        return self.smart_run, text
    
    # ========== 智能命令处理 ==========
    
    def smart_screenshot(self, args):
        """智能截图"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = CONFIG["screenshot_dir"] / f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(str(filepath))
            
            self.send_photo(str(filepath), "📸 屏幕截图")
            return "✅ 截图完成"
        except Exception as e:
            return f"❌ 截图失败: {e}"
    
    def smart_click(self, args):
        """智能点击"""
        try:
            # 解析坐标
            coords = re.findall(r'\d+', args)
            if len(coords) >= 2:
                x, y = int(coords[0]), int(coords[1])
                pyautogui.click(x, y)
                return f"✅ 点击 ({x}, {y})"
            else:
                return "❌ 请提供坐标，例如：点击 500 300"
        except Exception as e:
            return f"❌ 点击失败: {e}"
    
    def smart_double_click(self, args):
        """智能双击"""
        try:
            coords = re.findall(r'\d+', args)
            if len(coords) >= 2:
                x, y = int(coords[0]), int(coords[1])
                pyautogui.doubleClick(x, y)
                return f"✅ 双击 ({x}, {y})"
            else:
                return "❌ 请提供坐标，例如：双击 500 300"
        except Exception as e:
            return f"❌ 双击失败: {e}"
    
    def smart_right_click(self, args):
        """智能右键"""
        try:
            coords = re.findall(r'\d+', args)
            if len(coords) >= 2:
                x, y = int(coords[0]), int(coords[1])
                pyautogui.rightClick(x, y)
                return f"✅ 右键点击 ({x}, {y})"
            else:
                return "❌ 请提供坐标，例如：右键 500 300"
        except Exception as e:
            return f"❌ 右键失败: {e}"
    
    def smart_move_mouse(self, args):
        """移动鼠标"""
        try:
            coords = re.findall(r'\d+', args)
            if len(coords) >= 2:
                x, y = int(coords[0]), int(coords[1])
                pyautogui.moveTo(x, y, duration=0.5)
                return f"✅ 鼠标移动到 ({x}, {y})"
            else:
                return "❌ 请提供坐标，例如：移动鼠标 500 300"
        except Exception as e:
            return f"❌ 移动失败: {e}"
    
    def smart_scroll(self, args):
        """智能滚动"""
        try:
            amount = int(re.search(r'-?\d+', args).group()) if re.search(r'-?\d+', args) else 3
            pyautogui.scroll(amount)
            direction = "上" if amount > 0 else "下"
            return f"✅ 滚动{direction} {abs(amount)} 格"
        except Exception as e:
            return f"❌ 滚动失败: {e}"
    
    def smart_scroll_up(self, args):
        """向上滚动"""
        amount = int(re.search(r'\d+', args).group()) if re.search(r'\d+', args) else 3
        pyautogui.scroll(amount)
        return f"✅ 向上滚动 {amount} 格"
    
    def smart_scroll_down(self, args):
        """向下滚动"""
        amount = int(re.search(r'\d+', args).group()) if re.search(r'\d+', args) else 3
        pyautogui.scroll(-amount)
        return f"✅ 向下滚动 {amount} 格"
    
    def smart_type(self, args):
        """智能输入"""
        try:
            if args:
                pyautogui.typewrite(args, interval=0.05)
                return f"✅ 输入: {args}"
            else:
                return "❌ 请输入要打字的内容，例如：输入 Hello World"
        except Exception as e:
            return f"❌ 输入失败: {e}"
    
    def smart_press_key(self, args):
        """按键"""
        try:
            key = args.strip().lower()
            if key:
                pyautogui.press(key)
                return f"✅ 按下: {key}"
            else:
                return "❌ 请提供按键名称，例如：按键 enter"
        except Exception as e:
            return f"❌ 按键失败: {e}"
    
    def smart_hotkey(self, args):
        """组合键"""
        try:
            keys = args.strip().split()
            if keys:
                pyautogui.hotkey(*keys)
                return f"✅ 组合键: {'+'.join(keys)}"
            else:
                return "❌ 请提供按键组合，例如：全选 或 ctrl c"
        except Exception as e:
            return f"❌ 组合键失败: {e}"
    
    def smart_open(self, args):
        """打开文件/应用"""
        try:
            if not args:
                return "❌ 请提供要打开的内容，例如：打开 计算器"
            
            # 特殊应用映射
            apps = {
                "计算器": "gnome-calculator" if os.name != "nt" else "calc",
                "记事本": "gedit" if os.name != "nt" else "notepad",
                "终端": "gnome-terminal" if os.name != "nt" else "cmd",
                "浏览器": "xdg-open https://google.com" if os.name != "nt" else "start https://google.com",
                "文件管理器": "nautilus" if os.name != "nt" else "explorer",
            }
            
            # 检查是否是特殊应用
            for app_name, command in apps.items():
                if app_name in args:
                    subprocess.Popen(command, shell=True)
                    return f"✅ 打开: {app_name}"
            
            # 尝试作为文件路径打开
            filepath = os.path.expanduser(args)
            if os.path.exists(filepath):
                if os.name == "nt":
                    os.startfile(filepath)
                else:
                    subprocess.run(["xdg-open", filepath])
                return f"✅ 打开: {filepath}"
            else:
                # 尝试作为命令执行
                subprocess.Popen(args, shell=True)
                return f"✅ 执行: {args}"
                
        except Exception as e:
            return f"❌ 打开失败: {e}"
    
    def smart_run(self, args):
        """运行命令"""
        try:
            if not args:
                return "❌ 请提供要执行的命令，例如：运行 ls -la"
            
            # 安全检查
            dangerous_commands = ["rm -rf /", "sudo rm", "mkfs", "dd if=", ":(){ :|:& };:"]
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
            
            return f"💻 命令: {args}\n\n📤 输出:\n{output}"
        except subprocess.TimeoutExpired:
            return "❌ 命令超时 (30秒)"
        except Exception as e:
            return f"❌ 执行失败: {e}"
    
    def smart_get_position(self, args):
        """获取鼠标位置"""
        pos = pyautogui.position()
        return f"🖱️ 鼠标位置: ({pos.x}, {pos.y})"
    
    def smart_get_screen_size(self, args):
        """获取屏幕尺寸"""
        size = pyautogui.size()
        return f"🖥️ 屏幕尺寸: {size.width} x {size.height}"
    
    def smart_find_image(self, args):
        """找图"""
        try:
            if not args:
                return "❌ 请提供图片路径，例如：找图 button.png"
            
            image_path = os.path.expanduser(args)
            if not os.path.exists(image_path):
                return f"❌ 图片不存在: {image_path}"
            
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)
            if location:
                center = pyautogui.center(location)
                return f"✅ 找到图片 at ({center.x}, {center.y})"
            else:
                return "❌ 未找到图片"
        except Exception as e:
            return f"❌ 找图失败: {e}"
    
    def smart_wait(self, args):
        """等待"""
        try:
            seconds = int(re.search(r'\d+', args).group()) if re.search(r'\d+', args) else 1
            time.sleep(seconds)
            return f"✅ 等待 {seconds} 秒"
        except Exception as e:
            return f"❌ 等待失败: {e}"
    
    def smart_loop(self, args):
        """循环执行"""
        try:
            # 解析循环命令，例如：循环3次 点击 500 300
            match = re.search(r'循环(\d+)次\s+(.+)', args)
            if match:
                count = int(match.group(1))
                command = match.group(2)
                
                results = []
                for i in range(count):
                    handler, cmd_args = self.parse_natural_language(command)
                    result = handler(cmd_args)
                    results.append(f"第{i+1}次: {result}")
                    time.sleep(0.5)
                
                return "✅ 循环完成:\n" + "\n".join(results)
            else:
                return "❌ 格式：循环3次 点击 500 300"
        except Exception as e:
            return f"❌ 循环失败: {e}"
    
    def smart_schedule(self, args):
        """定时执行"""
        try:
            # 解析定时命令，例如：定时5秒后 截图
            match = re.search(r'定时(\d+)秒后\s+(.+)', args)
            if match:
                delay = int(match.group(1))
                command = match.group(2)
                
                time.sleep(delay)
                handler, cmd_args = self.parse_natural_language(command)
                result = handler(cmd_args)
                return f"✅ 定时执行完成:\n{result}"
            else:
                return "❌ 格式：定时5秒后 截图"
        except Exception as e:
            return f"❌ 定时失败: {e}"
    
    # ========== 复合任务 ==========
    
    def execute_task_sequence(self, tasks):
        """执行任务序列"""
        results = []
        for i, task in enumerate(tasks, 1):
            handler, args = self.parse_natural_language(task)
            result = handler(args)
            results.append(f"步骤{i}: {result}")
            time.sleep(0.5)
        return "\n".join(results)
    
    # ========== 主循环 ==========
    
    def run(self):
        """运行机器人"""
        self.running = True
        
        welcome_msg = """🤖 <b>智能桌面自动化机器人</b>

我可以理解自然语言命令，帮你自动操作电脑！

📋 <b>基本命令：</b>
• 截图 - 截取屏幕
• 点击 500 300 - 点击指定位置
• 输入 Hello - 输入文本
• 复制 / 粘贴 / 全选 / 保存
• 运行 ls -la - 执行终端命令
• 打开 计算器 - 打开应用

🔧 <b>高级命令：</b>
• 循环3次 点击 500 300
• 定时5秒后 截图
• 找图 button.png

💡 <b>直接用自然语言描述你想做的事情！</b>"""
        
        self.send_message(welcome_msg)
        print("🤖 智能桌面自动化机器人已启动")
        print("按 Ctrl+C 停止")
        
        try:
            while self.running:
                updates = self.get_updates()
                
                for update in updates:
                    self.last_update_id = update["update_id"]
                    
                    message = update.get("message", {})
                    text = message.get("text", "")
                    chat_id = str(message.get("chat", {}).get("id", ""))
                    
                    if chat_id != self.chat_id:
                        continue
                    
                    if text:
                        print(f"收到命令: {text}")
                        
                        # 特殊命令处理
                        if text.lower() in ["/start", "/help"]:
                            response = welcome_msg
                        elif text.lower() == "/history":
                            response = self.get_history()
                        elif text.lower() == "/clear":
                            self.task_history = []
                            response = "✅ 历史记录已清除"
                        else:
                            # 智能解析和执行
                            handler, args = self.parse_natural_language(text)
                            response = handler(args)
                            
                            # 记录历史
                            self.task_history.append({
                                "command": text,
                                "result": response,
                                "time": datetime.now().strftime("%H:%M:%S")
                            })
                        
                        if response:
                            self.send_message(response)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n机器人已停止")
            self.send_message("🤖 机器人已停止")
    
    def get_history(self):
        """获取历史记录"""
        if not self.task_history:
            return "📝 暂无历史记录"
        
        lines = ["📝 <b>最近操作：</b>\n"]
        for item in self.task_history[-10:]:
            lines.append(f"⏰ {item['time']}")
            lines.append(f"📌 {item['command']}")
            lines.append(f"✅ {item['result'][:50]}...")
            lines.append("")
        
        return "\n".join(lines)


# ========== 主程序 ==========

if __name__ == "__main__":
    bot = SmartDesktopBot()
    bot.run()
