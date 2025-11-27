# -*- coding: utf-8 -*-
import sqlite3
import json
import os
from datetime import datetime

# Use relative imports
from utils import info, error, warning, debug, get_antigravity_db_paths

# 需要备份的键列表
KEYS_TO_BACKUP = [
    "antigravityAuthStatus",
    "jetskiStateSync.agentManagerInitState",
]



def get_db_connection(db_path):
    """获取数据库连接"""
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        error_msg = str(e)
        if "locked" in error_msg.lower():
            error(f"数据库被锁定: {e}")
            error("提示: 请确保 Antigravity 应用已完全关闭")
        else:
            error(f"连接数据库失败: {e}")
        return None
    except Exception as e:
        error(f"连接数据库时发生意外错误: {e}")
        return None

def backup_account(email, backup_file_path):
    """备份账号数据到 JSON 文件"""
    db_paths = get_antigravity_db_paths()
    if not db_paths:
        error("未找到 Antigravity 数据库路径")
        return False
    
    db_path = db_paths[0]
    if not db_path.exists():
        error(f"数据库文件不存在: {db_path}")
        return False
        
    info(f"正在从数据库备份数据: {db_path}")
    conn = get_db_connection(db_path)
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        data_map = {}
        
        # 1. 提取普通键值
        for key in KEYS_TO_BACKUP:
            cursor.execute("SELECT value FROM ItemTable WHERE key = ?", (key,))
            row = cursor.fetchone()
            if row:
                data_map[key] = row[0]
                debug(f"备份字段: {key}")
            else:
                debug(f"字段不存在: {key}")
        

        
        # 3. 添加元数据
        data_map["account_email"] = email
        data_map["backup_time"] = datetime.now().isoformat()
        
        # 4. 写入文件
        with open(backup_file_path, 'w', encoding='utf-8') as f:
            json.dump(data_map, f, ensure_ascii=False, indent=2)
            
        info(f"备份成功: {backup_file_path}")
        return True
        
    except sqlite3.Error as e:
        error(f"数据库查询出错: {e}")
        return False
    except Exception as e:
        error(f"备份过程出错: {e}")
        return False
    finally:
        conn.close()

def restore_account(backup_file_path):
    """从 JSON 文件恢复账号数据"""
    if not os.path.exists(backup_file_path):
        error(f"备份文件不存在: {backup_file_path}")
        return False
        
    try:
        with open(backup_file_path, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
    except Exception as e:
        error(f"读取备份文件失败: {e}")
        return False
        
    db_paths = get_antigravity_db_paths()
    if not db_paths:
        error("未找到 Antigravity 数据库路径")
        return False
    
    # 通常有两个数据库文件: state.vscdb 和 state.vscdb.backup
    # 我们需要同时恢复它们
    success_count = 0
    
    for db_path in db_paths:
        # 主数据库
        if _restore_single_db(db_path, backup_data):
            success_count += 1
            
        # 备份数据库 (如果存在)
        backup_db_path = db_path.with_suffix('.vscdb.backup')
        if backup_db_path.exists():
            if _restore_single_db(backup_db_path, backup_data):
                success_count += 1
                
    return success_count > 0

def _restore_single_db(db_path, backup_data):
    """恢复单个数据库文件"""
    if not db_path.exists():
        return False
        
    info(f"正在恢复数据库: {db_path}")
    conn = get_db_connection(db_path)
    if not conn:
        return False
        
    try:
        cursor = conn.cursor()
        restored_keys = []
        
        # 1. 恢复普通键值
        for key in KEYS_TO_BACKUP:
            if key in backup_data:
                value = backup_data[key]
                # 确保 value 是字符串
                if not isinstance(value, str):
                    value = json.dumps(value)
                    
                cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, value))
                restored_keys.append(key)
                debug(f"恢复字段: {key}")

            
        conn.commit()
        info(f"数据库恢复完成: {db_path}")
        return True
        
    except sqlite3.Error as e:
        error(f"数据库写入出错: {e}")
        return False
    except Exception as e:
        error(f"恢复过程出错: {e}")
        return False
    finally:
        conn.close()


def get_current_account_info():
    """从数据库中提取当前账号信息 (邮箱等)"""
    db_paths = get_antigravity_db_paths()
    if not db_paths:
        return None
    
    db_path = db_paths[0]
    if not db_path.exists():
        return None
        
    conn = get_db_connection(db_path)
    if not conn:
        return None
        
    try:
        cursor = conn.cursor()
        
        # 1. 尝试从 antigravityAuthStatus 获取
        cursor.execute("SELECT value FROM ItemTable WHERE key = ?", ("antigravityAuthStatus",))
        row = cursor.fetchone()
        if row:
            try:
                # 尝试解析 JSON
                data = json.loads(row[0])
                if isinstance(data, dict):
                    if "email" in data:
                        return {"email": data["email"]}
                    # 有些时候可能是 token，或者其他结构，这里做一个简单的遍历查找
                    for k, v in data.items():
                        if k.lower() == "email" and isinstance(v, str):
                            return {"email": v}
            except:
                pass

        # 2. 尝试从 google.antigravity 获取
        cursor.execute("SELECT value FROM ItemTable WHERE key = ?", ("google.antigravity",))
        row = cursor.fetchone()
        if row:
            try:
                data = json.loads(row[0])
                if isinstance(data, dict) and "email" in data:
                    return {"email": data["email"]}
            except:
                pass
                
        # 3. 尝试从 antigravityUserSettings.allUserSettings 获取
        cursor.execute("SELECT value FROM ItemTable WHERE key = ?", ("antigravityUserSettings.allUserSettings",))
        row = cursor.fetchone()
        if row:
            try:
                data = json.loads(row[0])
                if isinstance(data, dict) and "email" in data:
                    return {"email": data["email"]}
            except:
                pass
                
        return None
        
    except Exception as e:
        error(f"提取账号信息出错: {e}")
        return None
    finally:
        conn.close()


