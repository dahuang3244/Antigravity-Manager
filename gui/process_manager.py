# -*- coding: utf-8 -*-
import os
import time
import platform
import subprocess
import psutil

# Use relative imports
from utils import info, error, warning, get_antigravity_executable_path, open_uri

def is_process_running(process_name=None):
    """检查 Antigravity 进程是否在运行
    
    使用跨平台的检测方式：
    - macOS: 检查路径包含 Antigravity.app
    - Windows: 检查进程名或路径包含 antigravity
    - Linux: 检查进程名或路径包含 antigravity
    """
    system = platform.system()
    
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            process_name_lower = proc.info['name'].lower() if proc.info['name'] else ""
            exe_path = proc.info.get('exe', '').lower() if proc.info.get('exe') else ""
            
            # 跨平台检测
            is_antigravity = False
            
            if system == "Darwin":
                # macOS: 检查路径包含 Antigravity.app
                is_antigravity = 'antigravity.app' in exe_path
            elif system == "Windows":
                # Windows: 检查进程名或路径包含 antigravity
                is_antigravity = (process_name_lower in ['antigravity.exe', 'antigravity'] or 
                                 'antigravity' in exe_path)
            else:
                # Linux: 检查进程名或路径包含 antigravity
                is_antigravity = (process_name_lower == 'antigravity' or 
                                 'antigravity' in exe_path)
            
            if is_antigravity:
                return True
                
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

def close_antigravity(timeout=10, force_kill=True):
    """优雅地关闭所有 Antigravity 进程
    
    关闭策略（三阶段，跨平台）：
    1. 平台特定的优雅退出方式
       - macOS: AppleScript
       - Windows: taskkill /IM (优雅终止)
       - Linux: SIGTERM
    2. 温和终止 (SIGTERM/TerminateProcess) - 给进程机会清理
    3. 强制杀死 (SIGKILL/taskkill /F) - 最后手段
    """
    info("正在尝试关闭 Antigravity...")
    system = platform.system()
    
    # Platform check
    if system not in ["Darwin", "Windows", "Linux"]:
        warning(f"未知系统平台: {system}，将尝试通用方法")
    
    try:
        # 阶段 1: 平台特定的优雅退出
        if system == "Darwin":
            # macOS: 使用 AppleScript
            info("尝试通过 AppleScript 优雅退出 Antigravity...")
            try:
                result = subprocess.run(
                    ["osascript", "-e", 'tell application "Antigravity" to quit'],
                    capture_output=True,
                    timeout=3
                )
                if result.returncode == 0:
                    info("已发送退出请求，等待应用响应...")
                    time.sleep(2)
            except Exception as e:
                warning(f"AppleScript 退出失败: {e}，将使用其他方式")
        
        elif system == "Windows":
            # Windows: 使用 taskkill 优雅终止（不带 /F 参数）
            info("尝试通过 taskkill 优雅退出 Antigravity...")
            try:
                # CREATE_NO_WINDOW = 0x08000000
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                result = subprocess.run(
                    ["taskkill", "/IM", "Antigravity.exe", "/T"],
                    capture_output=True,
                    timeout=3,
                    creationflags=0x08000000
                )
                if result.returncode == 0:
                    info("已发送退出请求，等待应用响应...")
                    time.sleep(2)
            except Exception as e:
                warning(f"taskkill 退出失败: {e}，将使用其他方式")
        
        # Linux 不需要特殊处理，直接使用 SIGTERM
        
        # 检查并收集仍在运行的进程
        target_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                process_name_lower = proc.info['name'].lower() if proc.info['name'] else ""
                exe_path = proc.info.get('exe', '').lower() if proc.info.get('exe') else ""
                
                # 排除自身进程
                if proc.pid == os.getpid():
                    continue
                
                # 排除当前应用目录下的所有进程 (防止误杀自己和子进程)
                # 在 PyInstaller 打包环境中，sys.executable 指向 exe 文件
                # 在开发环境中，它指向 python.exe
                try:
                    import sys
                    current_exe = sys.executable
                    current_dir = os.path.dirname(os.path.abspath(current_exe)).lower()
                    if exe_path and current_dir in exe_path:
                        # print(f"DEBUG: Skipping process in current dir: {proc.info['name']}")
                        continue
                except:
                    pass

                # 跨平台检测：检查进程名或可执行文件路径
                is_antigravity = False
                
                if system == "Darwin":
                    # macOS: 检查路径包含 Antigravity.app
                    is_antigravity = 'antigravity.app' in exe_path
                elif system == "Windows":
                    # Windows: 严格匹配进程名 antigravity.exe
                    # 或者路径包含 antigravity 且进程名不是 Antigravity Manager.exe
                    is_target_name = process_name_lower in ['antigravity.exe', 'antigravity']
                    is_in_path = 'antigravity' in exe_path
                    is_manager = 'manager' in process_name_lower
                    
                    is_antigravity = is_target_name or (is_in_path and not is_manager)
                else:
                    # Linux: 检查进程名或路径包含 antigravity
                    is_antigravity = (process_name_lower == 'antigravity' or 
                                     'antigravity' in exe_path)
                
                if is_antigravity:
                    info(f"发现目标进程: {proc.info['name']} ({proc.pid}) - {exe_path}")
                    target_processes.append(proc)
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if not target_processes:
            info("所有 Antigravity 进程已正常关闭")
            return True
        
        info(f"检测到 {len(target_processes)} 个进程仍在运行")

        # 阶段 2: 温和地请求进程终止 (SIGTERM)
        info("发送终止信号 (SIGTERM)...")
        for proc in target_processes:
            try:
                if proc.is_running():
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                continue
            except Exception as e:
                continue

        # 等待进程自然终止
        info(f"等待进程退出（最多 {timeout} 秒）...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            still_running = []
            for proc in target_processes:
                try:
                    if proc.is_running():
                        still_running.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if not still_running:
                info("所有 Antigravity 进程已正常关闭")
                return True
                
            time.sleep(0.5)

        # 阶段 3: 强制终止顽固进程 (SIGKILL)
        if still_running:
            still_running_names = ", ".join([f"{p.info['name']}({p.pid})" for p in still_running])
            warning(f"仍有 {len(still_running)} 个进程未退出: {still_running_names}")
            
            if force_kill:
                info("发送强制终止信号 (SIGKILL)...")
                for proc in still_running:
                    try:
                        if proc.is_running():
                            proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                # 最后检查
                time.sleep(1)
                final_check = []
                for proc in still_running:
                    try:
                        if proc.is_running():
                            final_check.append(proc)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                if not final_check:
                    info("所有 Antigravity 进程已被终止")
                    return True
                else:
                    final_list = ", ".join([f"{p.info['name']}({p.pid})" for p in final_check])
                    error(f"无法终止的进程: {final_list}")
                    return False
            else:
                error("部分进程未能关闭，请手动关闭后重试")
                return False
                
        return True

    except Exception as e:
        error(f"关闭 Antigravity 进程时发生错误: {str(e)}")
        return False

def start_antigravity(use_uri=True):
    """启动 Antigravity
    
    Args:
        use_uri: 是否使用 URI 协议启动（默认 True）
                 URI 协议更可靠，不需要查找可执行文件路径
    """
    info("正在启动 Antigravity...")
    system = platform.system()
    
    try:
        # 优先使用 URI 协议启动（跨平台通用）
        if use_uri:
            info("使用 URI 协议启动...")
            uri = "antigravity://oauth-success"
            
            if open_uri(uri):
                info("Antigravity URI 启动命令已发送")
                return True
            else:
                warning("URI 启动失败，尝试使用可执行文件路径...")
                # 继续执行下面的备用方案
        
        # 备用方案：使用可执行文件路径启动
        info("使用可执行文件路径启动...")
        if system == "Darwin":
            subprocess.Popen(["open", "-a", "Antigravity"])
        elif system == "Windows":
            path = get_antigravity_executable_path()
            if path and path.exists():
                # CREATE_NO_WINDOW = 0x08000000
                subprocess.Popen([str(path)], creationflags=0x08000000)
            else:
                error("找不到 Antigravity 可执行文件")
                warning("提示：可以尝试使用 URI 协议启动（use_uri=True）")
                return False
        elif system == "Linux":
            subprocess.Popen(["antigravity"])
        
        info("Antigravity 启动命令已发送")
        return True
    except Exception as e:
        error(f"启动进程时出错: {e}")
        # 如果 URI 启动失败，尝试使用可执行文件路径
        if use_uri:
            warning("URI 启动失败，尝试使用可执行文件路径...")
            return start_antigravity(use_uri=False)
        return False
