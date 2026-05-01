#!/usr/bin/env python3
"""
桌面自动化插件
功能：鼠标操作、键盘操作、屏幕截图、图像识别、文件管理
"""

import pyautogui
import time
import os
import json
from datetime import datetime
from pathlib import Path
from PIL import Image
import subprocess

# 安全设置
pyautogui.FAILSAFE = True  # 鼠标移到左上角触发安全异常
pyautogui.PAUSE = 0.5  # 每个操作间隔 0.5 秒

# 配置
CONFIG = {
    "screenshot_dir": Path.home() / "desktop-automation" / "screenshots",
    "log_file": Path.home() / "desktop-automation" / "automation.log",
    "default_wait": 1.0,  # 默认等待时间（秒）
}


class DesktopAutomation:
    """桌面自动化类"""
    
    def __init__(self):
        """初始化"""
        self.screenshot_dir = CONFIG["screenshot_dir"]
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.log("桌面自动化插件初始化完成")
    
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        try:
            with open(CONFIG["log_file"], "a") as f:
                f.write(log_msg + "\n")
        except:
            pass
    
    # ========== 鼠标操作 ==========
    
    def click(self, x, y, clicks=1, interval=0.1, button="left"):
        """
        点击指定位置
        
        参数:
            x, y: 屏幕坐标
            clicks: 点击次数
            interval: 多次点击间隔
            button: 鼠标按钮 (left, right, middle)
        """
        self.log(f"点击 ({x}, {y}) - {button}键 x{clicks}")
        pyautogui.click(x, y, clicks=clicks, interval=interval, button=button)
        time.sleep(CONFIG["default_wait"])
    
    def double_click(self, x, y):
        """双击指定位置"""
        self.click(x, y, clicks=2)
    
    def right_click(self, x, y):
        """右键点击"""
        self.click(x, y, button="right")
    
    def move_to(self, x, y, duration=0.5):
        """移动鼠标到指定位置"""
        self.log(f"移动鼠标到 ({x}, {y})")
        pyautogui.moveTo(x, y, duration=duration)
    
    def drag_to(self, x, y, duration=0.5, button="left"):
        """拖拽到指定位置"""
        self.log(f"拖拽到 ({x}, {y})")
        pyautogui.dragTo(x, y, duration=duration, button=button)
    
    def scroll(self, amount, x=None, y=None):
        """
        滚动鼠标滚轮
        
        参数:
            amount: 滚动量（正数向上，负数向下）
            x, y: 滚动位置（可选）
        """
        self.log(f"滚动 {amount} 格")
        if x is not None and y is not None:
            pyautogui.scroll(amount, x, y)
        else:
            pyautogui.scroll(amount)
    
    # ========== 键盘操作 ==========
    
    def type_text(self, text, interval=0.05):
        """
        输入文本
        
        参数:
            text: 要输入的文本
            interval: 每个字符间隔
        """
        self.log(f"输入文本: {text[:20]}...")
        pyautogui.typewrite(text, interval=interval)
    
    def press_key(self, key):
        """
        按下单个键
        
        参数:
            key: 键名 (enter, tab, space, backspace, delete, escape, etc.)
        """
        self.log(f"按下键: {key}")
        pyautogui.press(key)
    
    def hotkey(self, *keys):
        """
        组合快捷键
        
        参数:
            *keys: 键名列表 (如 'ctrl', 'c')
        """
        self.log(f"快捷键: {'+'.join(keys)}")
        pyautogui.hotkey(*keys)
    
    def key_down(self, key):
        """按下并保持按键"""
        self.log(f"按下并保持: {key}")
        pyautogui.keyDown(key)
    
    def key_up(self, key):
        """释放按键"""
        self.log(f"释放按键: {key}")
        pyautogui.keyUp(key)
    
    # ========== 屏幕截图 ==========
    
    def screenshot(self, filename=None, region=None):
        """
        截取屏幕
        
        参数:
            filename: 保存文件名（可选）
            region: 截图区域 (x, y, width, height)（可选）
        
        返回:
            截图文件路径
        """
        if filename is None:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        filepath = self.screenshot_dir / filename
        self.log(f"截图保存到: {filepath}")
        
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        
        screenshot.save(str(filepath))
        return str(filepath)
    
    def screenshot_region(self, x, y, width, height, filename=None):
        """截取指定区域"""
        return self.screenshot(filename=filename, region=(x, y, width, height))
    
    # ========== 图像识别 ==========
    
    def find_on_screen(self, image_path, confidence=0.8):
        """
        在屏幕上查找图像
        
        参数:
            image_path: 图像文件路径
            confidence: 匹配置信度 (0-1)
        
        返回:
            匹配位置 (x, y) 或 None
        """
        self.log(f"查找图像: {image_path}")
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                self.log(f"找到图像 at ({center.x}, {center.y})")
                return (center.x, center.y)
            else:
                self.log("未找到图像")
                return None
        except Exception as e:
            self.log(f"查找失败: {e}")
            return None
    
    def click_on_image(self, image_path, confidence=0.8, clicks=1):
        """
        点击屏幕上的图像
        
        参数:
            image_path: 图像文件路径
            confidence: 匹配置信度
            clicks: 点击次数
        """
        location = self.find_on_screen(image_path, confidence)
        if location:
            self.click(location[0], location[1], clicks=clicks)
            return True
        return False
    
    def wait_for_image(self, image_path, timeout=30, confidence=0.8):
        """
        等待图像出现
        
        参数:
            image_path: 图像文件路径
            timeout: 超时时间（秒）
            confidence: 匹配置信度
        
        返回:
            匹配位置或 None
        """
        self.log(f"等待图像出现: {image_path} (超时: {timeout}s)")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            location = self.find_on_screen(image_path, confidence)
            if location:
                return location
            time.sleep(1)
        
        self.log(f"等待超时: {image_path}")
        return None
    
    # ========== 文件操作 ==========
    
    def open_file(self, filepath):
        """打开文件"""
        self.log(f"打开文件: {filepath}")
        if os.name == "nt":  # Windows
            os.startfile(filepath)
        else:  # Linux/Mac
            subprocess.run(["xdg-open", filepath])
    
    def open_folder(self, folderpath):
        """打开文件夹"""
        self.log(f"打开文件夹: {folderpath}")
        if os.name == "nt":
            os.startfile(folderpath)
        else:
            subprocess.run(["xdg-open", folderpath])
    
    def create_folder(self, folderpath):
        """创建文件夹"""
        self.log(f"创建文件夹: {folderpath}")
        os.makedirs(folderpath, exist_ok=True)
    
    def list_files(self, folderpath, pattern="*"):
        """列出文件夹中的文件"""
        self.log(f"列出文件: {folderpath}/{pattern}")
        return list(Path(folderpath).glob(pattern))
    
    def copy_file(self, src, dst):
        """复制文件"""
        self.log(f"复制文件: {src} -> {dst}")
        import shutil
        shutil.copy2(src, dst)
    
    def move_file(self, src, dst):
        """移动文件"""
        self.log(f"移动文件: {src} -> {dst}")
        import shutil
        shutil.move(src, dst)
    
    def delete_file(self, filepath):
        """删除文件"""
        self.log(f"删除文件: {filepath}")
        os.remove(filepath)
    
    # ========== 窗口操作 ==========
    
    def get_window_position(self, window_title):
        """获取窗口位置"""
        try:
            import pygetwindow as gw
            windows = gw.getWindowsWithTitle(window_title)
            if windows:
                win = windows[0]
                return (win.left, win.top, win.width, win.height)
        except:
            pass
        return None
    
    def focus_window(self, window_title):
        """聚焦窗口"""
        self.log(f"聚焦窗口: {window_title}")
        try:
            import pygetwindow as gw
            windows = gw.getWindowsWithTitle(window_title)
            if windows:
                windows[0].activate()
                return True
        except:
            pass
        return False
    
    # ========== 工具函数 ==========
    
    def wait(self, seconds):
        """等待"""
        self.log(f"等待 {seconds} 秒")
        time.sleep(seconds)
    
    def get_mouse_position(self):
        """获取当前鼠标位置"""
        pos = pyautogui.position()
        return (pos.x, pos.y)
    
    def get_screen_size(self):
        """获取屏幕尺寸"""
        size = pyautogui.size()
        return (size.width, size.height)
    
    def move_mouse_circle(self, radius=100, steps=20):
        """鼠标画圆（用于测试）"""
        self.log("鼠标画圆测试")
        import math
        center = pyautogui.position()
        for i in range(steps + 1):
            angle = 2 * math.pi * i / steps
            x = center.x + radius * math.cos(angle)
            y = center.y + radius * math.sin(angle)
            pyautogui.moveTo(x, y, duration=0.05)


# ========== 任务录制与回放 ==========

class TaskRecorder:
    """任务录制器"""
    
    def __init__(self):
        self.tasks = []
        self.recording = False
    
    def start_recording(self):
        """开始录制"""
        self.tasks = []
        self.recording = True
        print("开始录制...")
    
    def stop_recording(self):
        """停止录制"""
        self.recording = False
        print(f"停止录制，共 {len(self.tasks)} 个操作")
        return self.tasks
    
    def record_click(self, x, y, button="left"):
        """记录点击操作"""
        if self.recording:
            self.tasks.append({
                "type": "click",
                "x": x,
                "y": y,
                "button": button,
                "time": time.time()
            })
    
    def record_type(self, text):
        """记录输入操作"""
        if self.recording:
            self.tasks.append({
                "type": "type",
                "text": text,
                "time": time.time()
            })
    
    def save_tasks(self, filepath):
        """保存任务"""
        with open(filepath, "w") as f:
            json.dump(self.tasks, f, indent=2)
        print(f"任务已保存到: {filepath}")
    
    def load_tasks(self, filepath):
        """加载任务"""
        with open(filepath, "r") as f:
            self.tasks = json.load(f)
        print(f"已加载 {len(self.tasks)} 个任务")
        return self.tasks
    
    def replay(self, speed=1.0):
        """回放任务"""
        if not self.tasks:
            print("没有可回放的任务")
            return
        
        print(f"开始回放 {len(self.tasks)} 个操作...")
        auto = DesktopAutomation()
        
        for i, task in enumerate(self.tasks):
            print(f"执行 {i+1}/{len(self.tasks)}: {task['type']}")
            
            if task["type"] == "click":
                auto.click(task["x"], task["y"], button=task.get("button", "left"))
            elif task["type"] == "type":
                auto.type_text(task["text"])
            
            # 控制回放速度
            if i < len(self.tasks) - 1:
                wait_time = (self.tasks[i+1]["time"] - task["time"]) / speed
                time.sleep(min(wait_time, 5))  # 最多等待5秒
        
        print("回放完成！")


# ========== 主程序 ==========

if __name__ == "__main__":
    # 创建自动化实例
    auto = DesktopAutomation()
    
    # 测试功能
    print("=" * 50)
    print("桌面自动化插件测试")
    print("=" * 50)
    
    # 获取屏幕信息
    width, height = auto.get_screen_size()
    print(f"屏幕尺寸: {width} x {height}")
    
    # 获取鼠标位置
    x, y = auto.get_mouse_position()
    print(f"鼠标位置: ({x}, {y})")
    
    # 截图测试
    screenshot_path = auto.screenshot()
    print(f"截图已保存: {screenshot_path}")
    
    print("\n✅ 测试完成！")
    print("\n使用示例:")
    print("  from desktop_automation import DesktopAutomation")
    print("  auto = DesktopAutomation()")
    print("  auto.click(100, 200)  # 点击 (100, 200)")
    print("  auto.type_text('Hello')  # 输入文本")
    print("  auto.hotkey('ctrl', 'c')  # 复制")
    print("  auto.screenshot()  # 截图")
