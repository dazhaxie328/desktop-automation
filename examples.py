#!/usr/bin/env python3
"""
桌面自动化使用示例
"""

from desktop_automation import DesktopAutomation, TaskRecorder
import time

def example_mouse_operations():
    """鼠标操作示例"""
    print("\n=== 鼠标操作示例 ===")
    auto = DesktopAutomation()
    
    # 获取鼠标位置
    x, y = auto.get_mouse_position()
    print(f"当前鼠标位置: ({x}, {y})")
    
    # 移动鼠标
    auto.move_to(500, 300)
    
    # 点击
    auto.click(500, 300)
    
    # 双击
    auto.double_click(500, 300)
    
    # 右键点击
    auto.right_click(500, 300)
    
    # 拖拽
    auto.drag_to(600, 400)

def example_keyboard_operations():
    """键盘操作示例"""
    print("\n=== 键盘操作示例 ===")
    auto = DesktopAutomation()
    
    # 输入文本
    auto.type_text("Hello, World!")
    
    # 按下回车
    auto.press_key("enter")
    
    # 组合快捷键
    auto.hotkey("ctrl", "a")  # 全选
    auto.hotkey("ctrl", "c")  # 复制
    auto.hotkey("ctrl", "v")  # 粘贴

def example_screenshot():
    """截图示例"""
    print("\n=== 截图示例 ===")
    auto = DesktopAutomation()
    
    # 全屏截图
    path = auto.screenshot()
    print(f"全屏截图: {path}")
    
    # 区域截图
    path = auto.screenshot_region(100, 100, 400, 300)
    print(f"区域截图: {path}")

def example_image_recognition():
    """图像识别示例"""
    print("\n=== 图像识别示例 ===")
    auto = DesktopAutomation()
    
    # 先截取一个区域作为模板
    template_path = auto.screenshot_region(100, 100, 50, 50, "template.png")
    
    # 在屏幕上查找该图像
    location = auto.find_on_screen("template.png")
    if location:
        print(f"找到图像 at: {location}")
        auto.click(location[0], location[1])
    else:
        print("未找到图像")

def example_file_operations():
    """文件操作示例"""
    print("\n=== 文件操作示例 ===")
    auto = DesktopAutomation()
    
    # 创建文件夹
    auto.create_folder("~/desktop-automation/test_folder")
    
    # 列出文件
    files = auto.list_files("~/desktop-automation")
    print(f"文件列表: {files}")

def example_task_recording():
    """任务录制示例"""
    print("\n=== 任务录制示例 ===")
    recorder = TaskRecorder()
    
    # 开始录制
    recorder.start_recording()
    
    # 模拟一些操作
    auto = DesktopAutomation()
    auto.click(100, 100)
    auto.type_text("test")
    auto.press_key("enter")
    
    # 停止录制
    tasks = recorder.stop_recording()
    
    # 保存任务
    recorder.save_tasks("~/desktop-automation/test_task.json")
    
    # 回放任务
    print("\n回放任务...")
    recorder.replay(speed=2.0)

def main():
    """主函数"""
    print("=" * 50)
    print("桌面自动化使用示例")
    print("=" * 50)
    
    print("\n选择示例:")
    print("1. 鼠标操作")
    print("2. 键盘操作")
    print("3. 截图")
    print("4. 图像识别")
    print("5. 文件操作")
    print("6. 任务录制")
    print("7. 运行全部")
    print("0. 退出")
    
    choice = input("\n请选择: ").strip()
    
    examples = {
        "1": example_mouse_operations,
        "2": example_keyboard_operations,
        "3": example_screenshot,
        "4": example_image_recognition,
        "5": example_file_operations,
        "6": example_task_recording,
    }
    
    if choice == "7":
        for example in examples.values():
            example()
    elif choice in examples:
        examples[choice]()
    elif choice == "0":
        print("退出")
    else:
        print("无效选择")

if __name__ == "__main__":
    main()
