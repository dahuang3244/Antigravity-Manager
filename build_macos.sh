#!/bin/bash

# 设置错误时退出
set -e

echo "🚀 开始构建 Antigravity Manager (macOS)..."

# 1. 同步资源文件
echo "📦 同步资源文件..."
# 确保 gui/assets 目录存在
mkdir -p gui/assets
# 同步 assets 目录内容到 gui/assets
cp -R assets/* gui/assets/
# 同步 requirements.txt
cp requirements.txt gui/requirements.txt

# 2. 清理旧构建
echo "🧹 清理旧构建文件..."
rm -rf gui/build/macos

# 3. 执行构建
echo "🔨 开始编译..."
source .venv/bin/activate
cd gui

# 临时关闭 set -e，因为 flet build 可能会抛出 SystemExit: 0 的 traceback 但实际构建成功
set +e

# 确保不进入交互模式
unset PYTHONINSPECT

# 使用 python -c 直接调用 flet_cli，绕过可能的入口点问题，并重定向输入
python -c "import sys; from flet.cli import main; main()" build macos \
    --product "Antigravity Manager" \
    --org "com.ctrler.antigravity" \
    --copyright "Copyright (c) 2025 Ctrler" \
    --build-version "1.0.0" \
    --desc "Antigravity 账号管理工具" < /dev/null
EXIT_CODE=$?
set -e

# 返回根目录
cd ..

# 4. 检查构建产物并打包 DMG
APP_NAME="Antigravity Manager"
APP_PATH="gui/build/macos/$APP_NAME.app"
DMG_NAME="$APP_NAME.dmg"
OUTPUT_DMG="gui/build/macos/$DMG_NAME"

if [ -d "$APP_PATH" ]; then
    echo "✅ 检测到应用包，构建成功 (忽略 Flet CLI 的退出状态)"
else
    echo "❌ 构建失败，未找到应用包"
    exit $EXIT_CODE
fi

echo "📦 正在创建 DMG 安装包..."

# 创建临时目录用于制作 DMG
DMG_SOURCE="gui/build/macos/dmg_source"
rm -rf "$DMG_SOURCE"
mkdir -p "$DMG_SOURCE"

# 复制应用到临时目录
echo "📋 复制应用到临时目录..."
cp -R "$APP_PATH" "$DMG_SOURCE/"

# 创建 Applications 软链接
ln -s /Applications "$DMG_SOURCE/Applications"

# 使用 hdiutil 创建 DMG
echo "💿 创建 DMG 文件..."
rm -f "$OUTPUT_DMG"
TEMP_DMG="gui/build/macos/temp.dmg"
rm -f "$TEMP_DMG"

# 第一步：创建可读写的 DMG
hdiutil create -volname "$APP_NAME" -srcfolder "$DMG_SOURCE" -ov -format UDRW "$TEMP_DMG"

# 第二步：转换为压缩的只读 DMG
hdiutil convert "$TEMP_DMG" -format UDZO -o "$OUTPUT_DMG"

# 清理
rm -f "$TEMP_DMG"
rm -rf "$DMG_SOURCE"

echo "🎉 打包完成！"
echo "📂 应用位置: $APP_PATH"
echo "💿 DMG 文件: $OUTPUT_DMG"
