# -*- coding: utf-8 -*-
import argparse
import sys
import os

# 将 gui 目录添加到 sys.path，以便内部模块可以相互导入 (例如 account_manager 导入 utils)
sys.path.append(os.path.join(os.path.dirname(__file__), "gui"))

# 支持直接运行和作为模块导入
# 支持直接运行和作为模块导入
try:
    from gui.utils import info, error, warning
    from gui.account_manager import (
        list_accounts_data,
        add_account_snapshot,
        switch_account,
        delete_account
    )
    from gui.process_manager import start_antigravity, close_antigravity
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def show_menu():
    """显示主菜单"""
    print("\n" + "="*50)
    print("🚀 Antigravity 账号管理工具")
    print("="*50)
    print("\n请选择操作：")
    print("  1. 📋 列出所有备份")
    print("  2. ➕ 添加/更新备份")
    print("  3. 🔄 切换/恢复备份")
    print("  4. 🗑️  删除备份")
    print("  5. ▶️  启动 Antigravity")
    print("  6. ⏹️  关闭 Antigravity")
    print("  0. 🚪 退出")
    print("-"*50)

def list_accounts():
    """列出所有账号"""
    accounts = list_accounts_data()
    if not accounts:
        info("暂无存档")
        return []
    else:
        print("\n" + "="*50)
        info(f"共有 {len(accounts)} 个存档:")
        print("="*50)
        for idx, acc in enumerate(accounts, 1):
            print(f"\n{idx}. {acc['name']}")
            print(f"   📧 邮箱: {acc['email']}")
            print(f"   🆔 ID: {acc['id']}")
            print(f"   ⏰ 最后使用: {acc['last_used']}")
            print("-" * 50)
        return accounts

def add_account():
    """添加账号备份"""
    print("\n" + "="*50)
    print("➕ 添加/更新账号备份")
    print("="*50)
    
    name = input("\n请输入账号名称（留空自动生成）: ").strip()
    email = input("请输入邮箱（留空自动识别）: ").strip()
    
    name = name if name else None
    email = email if email else None
    
    print()
    if add_account_snapshot(name, email):
        info("✅ 操作成功！")
    else:
        error("❌ 操作失败！")

def switch_account_interactive():
    """交互式切换账号"""
    accounts = list_accounts()
    if not accounts:
        return
    
    print("\n" + "="*50)
    print("🔄 切换/恢复账号")
    print("="*50)
    
    choice = input("\n请输入要切换的账号序号: ").strip()
    
    if not choice:
        warning("已取消操作")
        return
    
    real_id = resolve_id(choice)
    if not real_id:
        error(f"❌ 无效的序号: {choice}")
        return
    
    print()
    if switch_account(real_id):
        info("✅ 切换成功！")
    else:
        error("❌ 切换失败！")

def delete_account_interactive():
    """交互式删除账号"""
    accounts = list_accounts()
    if not accounts:
        return
    
    print("\n" + "="*50)
    print("🗑️  删除账号备份")
    print("="*50)
    
    choice = input("\n请输入要删除的账号序号: ").strip()
    
    if not choice:
        warning("已取消操作")
        return
    
    real_id = resolve_id(choice)
    if not real_id:
        error(f"❌ 无效的序号: {choice}")
        return
    
    # 确认删除
    confirm = input(f"\n⚠️  确定要删除该账号吗？(y/N): ").strip().lower()
    if confirm != 'y':
        warning("已取消删除")
        return
    
    print()
    if delete_account(real_id):
        info("✅ 删除成功！")
    else:
        error("❌ 删除失败！")

def interactive_mode():
    """交互式菜单模式"""
    while True:
        show_menu()
        choice = input("请输入选项 (0-6): ").strip()
        
        if choice == "1":
            list_accounts()
            input("\n按回车键继续...")
            
        elif choice == "2":
            add_account()
            input("\n按回车键继续...")
            
        elif choice == "3":
            switch_account_interactive()
            input("\n按回车键继续...")
            
        elif choice == "4":
            delete_account_interactive()
            input("\n按回车键继续...")
            
        elif choice == "5":
            print()
            start_antigravity()
            input("\n按回车键继续...")
            
        elif choice == "6":
            print()
            close_antigravity()
            input("\n按回车键继续...")
            
        elif choice == "0":
            print("\n👋 再见！")
            sys.exit(0)
            
        else:
            error("❌ 无效的选项，请重新选择")
            input("\n按回车键继续...")

def cli_mode():
    """命令行模式"""
    parser = argparse.ArgumentParser(description="Antigravity 账号管理工具 (纯 Python 版)")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # List
    subparsers.add_parser("list", help="列出所有存档")

    # Add
    add_parser = subparsers.add_parser("add", help="将当前状态保存为新存档")
    add_parser.add_argument("--name", "-n", help="存档名称 (可选，默认自动生成)")
    add_parser.add_argument("--email", "-e", help="关联邮箱 (可选，默认从数据库读取)")

    # Switch
    switch_parser = subparsers.add_parser("switch", help="切换到指定存档")
    switch_parser.add_argument("--id", "-i", required=True, help="存档 ID")

    # Delete
    del_parser = subparsers.add_parser("delete", help="删除存档")
    del_parser.add_argument("--id", "-i", required=True, help="存档 ID")
    
    # Process Control
    subparsers.add_parser("start", help="启动 Antigravity")
    subparsers.add_parser("stop", help="关闭 Antigravity")

    args = parser.parse_args()

    if args.command == "list":
        list_accounts()

    elif args.command == "add":
        if add_account_snapshot(args.name, args.email):
            info("存档添加成功")
        else:
            sys.exit(1)

    elif args.command == "switch":
        real_id = resolve_id(args.id)
        if not real_id:
            error(f"无效的 ID 或序号: {args.id}")
            sys.exit(1)
            
        if switch_account(real_id):
            info("切换成功")
        else:
            sys.exit(1)

    elif args.command == "delete":
        real_id = resolve_id(args.id)
        if not real_id:
            error(f"无效的 ID 或序号: {args.id}")
            sys.exit(1)

        if delete_account(real_id):
            info("删除成功")
        else:
            sys.exit(1)
            
    elif args.command == "start":
        start_antigravity()
        
    elif args.command == "stop":
        close_antigravity()

    else:
        # 没有参数时，进入交互式模式
        interactive_mode()

def main():
    """主入口"""
    # 如果没有命令行参数，进入交互式模式
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        cli_mode()

def resolve_id(input_id):
    """解析 ID，支持 UUID 或 序号"""
    accounts = list_accounts_data()
    
    # 1. 尝试作为序号处理
    if input_id.isdigit():
        idx = int(input_id)
        if 1 <= idx <= len(accounts):
            return accounts[idx-1]['id']
            
    # 2. 尝试作为 UUID 匹配
    for acc in accounts:
        if acc['id'] == input_id:
            return input_id
            
    return None

if __name__ == "__main__":
    main()
