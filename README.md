# 🚀 Antigravity Manager (反重力账号管理器)

> **专为 macOS & Windows 设计的现代化 Antigravity 多账号管理工具**

Antigravity Manager 是一个功能强大的辅助工具，旨在解决 Antigravity 客户端无法原生支持多账号切换的痛点。通过接管应用的配置状态，它允许用户在无限个账号之间一键无缝切换，同时提供了自动备份、进程守护和可视化的管理界面。

---

## ✨ 核心特性

### 🛡️ 账号安全与管理
*   **无限账号快照**：创建任意数量的账号备份，完整保存登录凭证、用户配置和本地状态。
*   **智能识别**：自动从数据库中读取当前登录账号的邮箱和 ID，无需手动输入。
*   **自动备份机制**：
    *   **启动备份**：每次启动管理器时自动备份当前状态，防止意外覆盖。
    *   **切换备份**：在切换账号前自动保存当前账号的最新状态。
*   **详细元数据**：记录每个存档的创建时间、最后使用时间、邮箱和唯一 ID。

### ⚡️ 无缝体验
*   **一键切换**：只需点击一次，即可完成“关闭应用 -> 替换数据 -> 重启应用”的全流程。
*   **进程守护**：
    *   **优雅退出**：优先使用 AppleScript (macOS) 或 taskkill (Windows) 通知应用正常退出，保护数据完整性。
    *   **强制兜底**：如果应用卡死，会自动升级为强制终止策略，确保切换成功。
*   **跨平台支持**：完美适配 macOS (Intel/Apple Silicon) 和 Windows 10/11。

### 🎨 现代化界面
*   **Flet 驱动**：基于 Flutter 的高性能 GUI，响应迅速。
*   **原生融合**：自动适配系统的深色/浅色模式，提供原生的窗口体验。
*   **交互友好**：清晰的列表视图、直观的操作按钮和友好的确认弹窗。

---

## 🛠️ 快速开始

### 环境要求
*   **操作系统**: macOS 10.15+ 或 Windows 10+
*   **Python**: 3.10 或更高版本
*   **Antigravity**: 必须已安装并运行过至少一次

### 1. 安装依赖
在项目根目录下运行以下命令安装所需库：

```bash
pip install -r requirements.txt
```

### 2. 运行应用

#### 🖥️ 图形界面模式 (GUI) - 推荐
启动图形界面，体验完整的交互功能：

```bash
# macOS / Linux
python gui/main.py

# Windows
python gui\main.py
```

#### ⌨️ 命令行模式 (CLI)
适合脚本集成或极客用户。

**交互式菜单**:
```bash
python main.py
```

**常用命令**:
```bash
# 列出所有存档
python main.py list

# 备份当前账号 (自动获取名称)
python main.py add

# 指定名称备份
python main.py add -n "工作账号"

# 切换账号 (使用 ID 或 列表序号)
python main.py switch -i 1

# 删除备份
python main.py delete -i 1
```

---

## 📦 打包与部署

本项目内置了自动化构建脚本，可生成无需 Python 环境的独立可执行文件。

### 🍎 macOS 打包
构建 `.app` 应用和 `.dmg` 安装包。

```bash
# 1. 赋予脚本执行权限
chmod +x build_macos.sh

# 2. 运行构建
./build_macos.sh
```
*   **产物路径**: `gui/build/macos/`
*   **包含**: `Antigravity Manager.app`, `Antigravity Manager.dmg`
*   **架构**: Universal Binary (支持 Intel & M1/M2/M3)

### 🪟 Windows 打包
构建单文件 `.exe` 可执行程序。

```powershell
# 在 PowerShell 中运行
./build_windows.ps1
```
*   **产物路径**: `dist/`
*   **包含**: `Antigravity Manager.exe`
*   **特点**: 无控制台黑窗口，单文件便携运行。

---

## 🧩 技术架构

### 目录结构
```
antigravity_manager/
├── assets/                 # 静态资源 (图标等)
├── gui/                    # 核心代码库
│   ├── main.py             # GUI 入口点
│   ├── account_manager.py  # 账号逻辑 (增删改查)
│   ├── process_manager.py  # 进程控制 (跨平台进程管理)
│   ├── db_manager.py       # 数据持久化 (文件操作)
│   ├── views/              # UI 视图组件
│   └── utils.py            # 通用工具类
├── main.py                 # CLI 入口点
├── build_macos.sh          # macOS 构建脚本
├── build_windows.ps1       # Windows 构建脚本
└── requirements.txt        # Python 依赖
```

### 数据存储
*   **配置文件**: `~/.antigravity-agent/accounts.json` (存储账号列表索引)
*   **备份数据**: `~/.antigravity-agent/backups/*.json` (实际的账号数据快照)
*   **日志文件**: `~/.antigravity-agent/app.log`

---

## ❓ 常见问题 (FAQ)

**Q: 切换账号后，Antigravity 没有自动启动？**
A: 请确保 Antigravity 安装在标准路径（macOS 为 `/Applications`，Windows 为默认安装目录）。如果使用了自定义路径，程序会尝试通过 URI 协议 (`antigravity://`) 启动。

**Q: 备份文件存在哪里？**
A: 所有数据都存储在用户主目录下的 `.antigravity-agent` 文件夹中。您可以随时手动备份此文件夹。

**Q: 为什么 Windows 上杀毒软件会报毒？**
A: 使用 PyInstaller 打包的单文件 exe 偶尔会被误报。这是 PyInstaller 的已知问题。请将应用加入白名单，或直接使用 Python 源码运行。

---

## 📄 许可证

本项目采用 MIT 许可证。欢迎提交 Issue 和 Pull Request。

Copyright (c) 2025 Ctrler. All rights reserved.
