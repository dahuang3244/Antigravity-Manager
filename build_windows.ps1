# build_windows.ps1

Write-Host "🚀 开始构建 Antigravity Manager (Windows)..." -ForegroundColor Cyan

# 1. 检查环境
if (-not (Get-Command "flet" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ 未找到 flet 命令，正在安装..." -ForegroundColor Yellow
    pip install flet
}
if (-not (Get-Command "pyinstaller" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ 未找到 pyinstaller 命令，正在安装..." -ForegroundColor Yellow
    pip install pyinstaller
}

# 安装项目依赖
if (Test-Path "requirements.txt") {
    Write-Host "📦 正在安装/更新项目依赖..." -ForegroundColor Green
    pip install -r requirements.txt
}

# 2. 清理旧构建
Write-Host "🧹 清理旧构建文件..." -ForegroundColor Green
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }

# 3. 准备资源
# 确保 gui/assets 存在并是最新的
Write-Host "📦 同步资源文件..." -ForegroundColor Green
if (-not (Test-Path "gui/assets")) { New-Item -ItemType Directory -Path "gui/assets" | Out-Null }
Copy-Item "assets/*" "gui/assets/" -Recurse -Force

# 4. 执行构建
Write-Host "🔨 开始编译..." -ForegroundColor Green

# 使用 flet pack 打包
# build_windows.ps1

Write-Host "🚀 开始构建 Antigravity Manager (Windows)..." -ForegroundColor Cyan

# 1. 检查环境
if (-not (Get-Command "flet" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ 未找到 flet 命令，正在安装..." -ForegroundColor Yellow
    pip install flet
}
if (-not (Get-Command "pyinstaller" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ 未找到 pyinstaller 命令，正在安装..." -ForegroundColor Yellow
    pip install pyinstaller
}

# 2. 清理旧构建
Write-Host "🧹 清理旧构建文件..." -ForegroundColor Green
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }

# 3. 准备资源
# 确保 gui/assets 存在并是最新的
Write-Host "📦 同步资源文件..." -ForegroundColor Green
if (-not (Test-Path "gui/assets")) { New-Item -ItemType Directory -Path "gui/assets" | Out-Null }
Copy-Item "assets/*" "gui/assets/" -Recurse -Force

# 4. 执行构建
Write-Host "🔨 开始编译..." -ForegroundColor Green

# 使用 flet pack 打包
# --icon: 指定图标
# --add-data: 添加资源文件 (格式: 源路径;目标路径)
# --name: 指定输出文件名
# --noconsole: 不显示控制台窗口 (如果需要调试，可以去掉这个参数)
# gui/main.py: 入口文件

# 4. 执行 PyInstaller 打包
Write-Host "📦 正在打包..." -ForegroundColor Yellow

# 使用 PyInstaller 直接打包
# --onefile: 打包成单文件
# --windowed: 无控制台 (GUI应用)
# --add-data: 添加资源文件 (格式: 源路径;目标路径)
# --hidden-import: 强制导入可能被遗漏的模块
pyinstaller --noconfirm --onefile --windowed --clean `
    --name "Antigravity Manager" `
    --icon "assets/icon.ico" `
    --add-data "assets;assets" `
    --add-data "gui;gui" `
    --noconsole `
    --paths "gui" `
    --hidden-import "views" `
    --hidden-import "views.home_view" `
    --hidden-import "views.settings_view" `
    --hidden-import "account_manager" `
    --hidden-import "db_manager" `
    --hidden-import "process_manager" `
    --hidden-import "utils" `
    --hidden-import "theme" `
    --hidden-import "icons" `
    "gui/main.py"

# 检查结果
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 打包失败！" -ForegroundColor Red
    exit 1
}

# 5. 检查结果
if (Test-Path "dist/Antigravity Manager.exe") {
    Write-Host "`n🎉 构建成功！" -ForegroundColor Green
    Write-Host "文件位置: dist/Antigravity Manager.exe" -ForegroundColor Cyan
} else {
    Write-Host "❌ 未找到生成的 exe 文件" -ForegroundColor Red
    exit 1
}
