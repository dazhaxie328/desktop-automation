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
- ✅ **Telegram 交互式控制**

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/dazhaxie328/desktop-automation.git
cd desktop-automation

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install pyautogui pillow pynput requests
```

### 配置 Telegram

在 `~/crypto-monitor/.env` 文件中配置：

```
TELEGRAM_BOT_TOKEN=你的Bot Token
TELEGRAM_CHAT_ID=你的Chat ID
```

### 运行

```bash
# 方式1：使用启动脚本
chmod +x start_bot.sh
./start_bot.sh

# 方式2：直接运行
source venv/bin/activate
python telegram_bot.py
```

## Telegram 命令

### 截图
```
/screenshot - 截取屏幕
```

### 鼠标操作
```
/click x y - 点击指定位置
/move x y - 移动鼠标
/scroll amount - 滚动 (正=上, 负=下)
/pos - 获取鼠标位置
/mouse - 鼠标画圆测试
```

### 键盘操作
```
/type text - 输入文本
/key keyname - 按下按键 (enter, tab, etc.)
/hotkey key1 key2 - 组合键 (ctrl c)
```

### 文件操作
```
/open filepath - 打开文件
```

### 系统命令
```
/screen - 获取屏幕尺寸
/run command - 运行终端命令
/help - 显示帮助
```

## 使用示例

### 1. 截图并发送
```
/screenshot
```

### 2. 点击指定位置
```
/click 500 300
```

### 3. 输入文本
```
/type Hello World
```

### 4. 组合快捷键
```
/hotkey ctrl s
```

### 5. 运行终端命令
```
/run ls -la
```

### 6. 打开文件
```
/open ~/document.txt
```

## Python API

```python
from desktop_automation import DesktopAutomation

auto = DesktopAutomation()

# 鼠标点击
auto.click(500, 300)

# 输入文本
auto.type_text("Hello")

# 快捷键
auto.hotkey("ctrl", "s")

# 截图
auto.screenshot()
```

## 文件结构

```
desktop-automation/
├── desktop_automation.py  # 核心库
├── telegram_bot.py        # Telegram 机器人
├── start_bot.sh           # 启动脚本
├── examples.py            # 使用示例
├── venv/                  # 虚拟环境
├── screenshots/           # 截图目录
└── README.md              # 说明文档
```

## 安全设置

- `pyautogui.FAILSAFE = True` - 鼠标移到屏幕左上角触发安全异常
- `pyautogui.PAUSE = 0.5` - 每个操作间隔 0.5 秒
- 危险命令会被拒绝执行 (rm -rf, sudo, etc.)

## 注意事项

1. **安全第一**：鼠标移到屏幕左上角可触发安全异常，终止自动化
2. **权限问题**：某些操作可能需要管理员权限
3. **分辨率依赖**：图像识别依赖屏幕分辨率
4. **网络要求**：Telegram 机器人需要稳定的网络连接

## License

MIT
