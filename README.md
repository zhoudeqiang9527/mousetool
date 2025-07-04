# 键鼠操作工具

一个基于Python和Tkinter开发的图形化鼠标自动化操作工具，支持自定义坐标点击、智能滚轮操作和实时鼠标位置跟踪。

## 功能特性

### 🖱️ 核心功能
- **自定义坐标点击**：支持指定X、Y坐标进行精确点击
- **批量点击操作**：可设置点击次数，自动执行多次点击
- **智能位置调整**：每次点击后自动向下移动指定像素
- **智能滚轮操作**：当Y坐标超过阈值时自动执行滚轮滚动
- **实时鼠标跟踪**：显示当前鼠标光标的X、Y坐标位置

### 🛡️ 安全特性
- **安全中断机制**：鼠标移动到屏幕左上角可紧急停止操作
- **输入验证**：自动验证坐标和点击数的有效性
- **屏幕边界检测**：防止坐标超出屏幕范围
- **异常处理**：完善的错误处理和用户提示

### 🎨 用户界面
- **直观的GUI界面**：基于Tkinter的现代化界面设计
- **实时状态显示**：操作状态和进度实时反馈
- **进度条显示**：可视化显示操作执行进度
- **颜色状态指示**：不同颜色表示不同的操作状态

### ⚙️ 配置化设计
- **JSON配置文件**：所有参数通过config.json统一管理
- **热配置支持**：修改配置文件后重启即可生效
- **默认配置回退**：配置文件缺失时自动使用默认配置

## 安装要求

### 系统要求
- Python 3.7+
- Windows/macOS/Linux

### 依赖库
- `tkinter`：GUI界面（Python内置）
- `pyautogui>=0.9.54`：鼠标键盘自动化

## 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd 键鼠操作
```

2. **安装依赖**
```bash
# 使用uv（推荐）
uv sync

# 或使用pip
pip install pyautogui>=0.9.54
```

3. **运行程序**
```bash
# 使用uv
uv run python main.py

# 或直接运行
python main.py
```

## 使用说明

### 基本操作

1. **设置坐标**：在"坐标X"和"坐标Y"输入框中输入目标坐标
2. **设置点击数**：在"点击数"输入框中输入要执行的点击次数
3. **执行操作**：点击"执行鼠标点击"按钮开始自动化操作
4. **监控进度**：通过进度条和状态标签监控操作进度

### 实时坐标跟踪

- 程序启动后会自动显示当前鼠标光标的X、Y坐标
- 坐标信息每100毫秒更新一次（可通过配置文件调整）
- 蓝色字体显示，便于快速识别当前鼠标位置

### 智能滚轮机制

当鼠标Y坐标超过930像素时（默认值，可配置）：
1. 自动点击当前位置确保焦点正确
2. 执行向下滚轮操作
3. 重置Y坐标到起始位置
4. 继续后续点击操作

### 安全停止

- **紧急停止**：将鼠标快速移动到屏幕左上角可立即停止操作
- **正常停止**：等待当前循环完成后自动停止

## 配置文件说明

配置文件 `config.json` 包含以下配置项：

### UI配置 (`ui`)
```json
{
  "window_title": "键鼠操作工具",    // 窗口标题
  "window_width": 550,              // 窗口宽度
  "window_height": 300,             // 窗口高度
  "window_resizable": false,        // 是否可调整大小
  "padding": "20"                   // 内边距
}
```

### 鼠标操作配置 (`mouse`)
```json
{
  "default_x": 100,                 // 默认X坐标
  "default_y": 100,                 // 默认Y坐标
  "default_click_count": 1,          // 默认点击次数
  "move_step": 5,                   // 每次点击后向下移动像素
  "scroll_threshold_y": 930,        // 滚轮触发的Y坐标阈值
  "scroll_amount": -300,            // 滚轮滚动量（负数向下）
  "click_delay": 0.1,               // 点击操作间隔（秒）
  "scroll_delay": 0.2               // 滚轮操作间隔（秒）
}
```

### PyAutoGUI配置 (`pyautogui`)
```json
{
  "failsafe": true,                 // 启用安全模式
  "pause": 0.1                      // 操作间全局暂停时间
}
```

### 跟踪配置 (`tracking`)
```json
{
  "update_interval_ms": 100         // 鼠标位置更新间隔（毫秒）
}
```

### UI文本配置 (`ui_text`)
包含所有界面显示的文本内容，支持国际化定制。

### 消息配置 (`messages`)
包含所有提示消息和错误信息的文本内容。

## 项目结构

```
键鼠操作/
├── main.py              # 主程序文件
├── config.json          # 配置文件
├── pyproject.toml       # 项目依赖配置
├── README.md            # 项目说明文档
├── .gitignore           # Git忽略文件
├── .python-version      # Python版本指定
└── uv.lock              # 依赖锁定文件
```

## 技术架构

### 核心类：`MouseKeyboardTool`

- **配置管理**：`load_config()` 和 `get_default_config()`
- **UI构建**：`setup_ui()` 创建图形界面
- **输入验证**：`validate_inputs()` 验证用户输入
- **核心功能**：`execute_mouse_clicks()` 执行自动化操作
- **实时跟踪**：`update_mouse_position()` 更新鼠标位置

### 设计模式

- **配置驱动**：通过JSON文件驱动程序行为
- **异常处理**：完善的错误处理和用户反馈
- **状态管理**：清晰的操作状态和进度管理

## 常见问题

### Q: 滚轮操作在某些应用中无效？
A: 程序已优化，在执行滚轮操作前会先点击当前位置确保焦点正确，提高兼容性。

### Q: 如何修改滚轮触发条件？
A: 编辑 `config.json` 文件中的 `scroll_threshold_y` 值，设置触发滚轮的Y坐标阈值。

### Q: 程序意外停止怎么办？
A: 检查是否触发了安全机制（鼠标移动到左上角），或查看错误提示信息。

### Q: 如何调整操作速度？
A: 修改 `config.json` 中的 `click_delay` 和 `scroll_delay` 参数。

## 开发说明

### 代码规范
- 遵循PEP 8 Python编码规范
- 使用类型注解提高代码可读性
- 完善的注释和文档字符串

### 扩展建议
- 添加更多鼠标操作类型（右键、双击等）
- 支持键盘操作自动化
- 添加操作录制和回放功能
- 实现操作脚本化和批处理

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

---

**注意**：使用本工具时请遵守相关法律法规，仅用于合法的自动化操作。