# 桌面自动化插件

一个功能强大的 Python 桌面自动化库，支持鼠标操作、键盘操作、屏幕截图、图像识别和文件管理。

## 功能特性

- ✅ 鼠标操作（点击、移动、拖拽、滚动）
- ✅ 键盘操作（输入、快捷键、按键控制）
- ✅ 屏幕截图（全屏、区域截图）
- ✅ 图像识别（找图、等待图像出现）
- ✅ 窗口操作（获取位置、聚焦窗口）
- ✅ 文件管理（打开、复制、移动、删除）
- ✅ 任务录制与回放

## 安装

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install pyautogui pillow pynput
```

## 快速开始

```python
from desktop_automation import DesktopAutomation

# 创建自动化实例
auto = DesktopAutomation()

# 鼠标点击
auto.click(500, 300)

# 输入文本
auto.type_text("Hello, World!")

# 组合快捷键
auto.hotkey("ctrl", "s")

# 截图
auto.screenshot()
```

## 使用示例

### 鼠标操作

```python
auto = DesktopAutomation()

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

# 滚动
auto.scroll(3)  # 向上滚动3格
auto.scroll(-3)  # 向下滚动3格
```

### 键盘操作

```python
auto = DesktopAutomation()

# 输入文本
auto.type_text("Hello")

# 按下单个键
auto.press_key("enter")
auto.press_key("tab")

# 组合快捷键
auto.hotkey("ctrl", "c")  # 复制
auto.hotkey("ctrl", "v")  # 粘贴
auto.hotkey("alt", "tab")  # 切换窗口

# 按住按键
auto.key_down("shift")
auto.press_key("a")  # 输入大写 A
auto.key_up("shift")
```

### 屏幕截图

```python
auto = DesktopAutomation()

# 全屏截图
path = auto.screenshot()

# 指定文件名
path = auto.screenshot("my_screenshot.png")

# 区域截图
path = auto.screenshot_region(100, 100, 400, 300)
```

### 图像识别

```python
auto = DesktopAutomation()

# 查找图像
location = auto.find_on_screen("button.png")
if location:
    print(f"找到图像 at: {location}")

# 点击图像
auto.click_on_image("button.png")

# 等待图像出现
location = auto.wait_for_image("loading.png", timeout=30)
if location:
    auto.click(location[0], location[1])
```

### 文件操作

```python
auto = DesktopAutomation()

# 打开文件
auto.open_file("~/document.txt")

# 打开文件夹
auto.open_folder("~/Desktop")

# 创建文件夹
auto.create_folder("~/new_folder")

# 列出文件
files = auto.list_files("~/Desktop", "*.txt")

# 复制文件
auto.copy_file("~/file.txt", "~/backup/file.txt")

# 移动文件
auto.move_file("~/file.txt", "~/archive/file.txt")

# 删除文件
auto.delete_file("~/temp.txt")
```

### 任务录制与回放

```python
from desktop_automation import TaskRecorder

recorder = TaskRecorder()

# 开始录制
recorder.start_recording()

# 执行一些操作...
auto = DesktopAutomation()
auto.click(100, 100)
auto.type_text("test")

# 停止录制
tasks = recorder.stop_recording()

# 保存任务
recorder.save_tasks("my_task.json")

# 加载任务
recorder.load_tasks("my_task.json")

# 回放任务
recorder.replay(speed=2.0)  # 2倍速回放
```

## 安全设置

- `pyautogui.FAILSAFE = True` - 鼠标移到屏幕左上角触发安全异常
- `pyautogui.PAUSE = 0.5` - 每个操作间隔 0.5 秒

## 运行示例

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行示例
python examples.py

# 运行测试
python desktop_automation.py
```

## 文件结构

```
desktop-automation/
├── desktop_automation.py  # 主库文件
├── examples.py            # 使用示例
├── venv/                  # 虚拟环境
├── screenshots/           # 截图保存目录
└── README.md              # 说明文档
```

## 注意事项

1. **安全第一**：鼠标移到屏幕左上角可触发安全异常，终止自动化
2. **权限问题**：某些操作可能需要管理员权限
3. **分辨率依赖**：图像识别依赖屏幕分辨率，不同分辨率需要不同的模板
4. **延迟设置**：根据网络和系统性能调整 `PAUSE` 和 `default_wait`

## 扩展功能

- 添加更多图像识别算法
- 支持 OCR 文字识别
- 添加日志记录功能
- 支持多显示器
- 添加 Web 界面控制面板

## License

MIT
