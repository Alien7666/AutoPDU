import subprocess
import time
import socket
import sys
import logging
from datetime import datetime
import os
import re

def setup_logger():
    """設定日誌"""
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}-乙太網路測試.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def get_ethernet_ip():
    """專門獲取乙太網路的IP地址，使用多種方法"""
    try:
        # 方法1：使用 netsh 命令（詳細模式）
        cmd = "netsh interface ip show addresses '乙太網路' | findstr /C:IP"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='big5')
        if result.stdout:
            ip_match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', result.stdout)
            if ip_match:
                ip = ip_match.group(0)
                logger.info(f"使用netsh命令找到IP: {ip}")
                return ip

        # 方法2：使用 ipconfig 命令
        cmd = "ipconfig | findstr '乙太網路' /C:IPv4"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='big5')
        if result.stdout:
            ip_match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', result.stdout)
            if ip_match:
                ip = ip_match.group(0)
                logger.info(f"使用ipconfig命令找到IP: {ip}")
                return ip

        # 方法3：使用 netsh interface show 獲取網卡配置
        cmd = "netsh interface ip show config name='乙太網路'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='big5')
        if result.stdout:
            ip_match = re.search(r'IP.*?:\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', result.stdout)
            if ip_match:
                ip = ip_match.group(1)
                logger.info(f"使用netsh config命令找到IP: {ip}")
                return ip

        # 如果都沒找到IP，檢查是否為靜態IP設定
        cmd = "netsh interface ip show config name='乙太網路'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='big5')
        if '固定' in result.stdout or 'Static' in result.stdout:
            logger.info("網卡設定為靜態IP，但無法讀取到IP地址")
        else:
            logger.info("網卡可能設定為DHCP模式")

        # 輸出完整配置以供診斷
        logger.debug(f"網卡完整配置:\n{result.stdout}")
        
        return None

    except Exception as e:
        logger.error(f"獲取乙太網路IP時發生錯誤: {e}")
        logger.debug("嘗試獲取更多網卡資訊進行診斷...")
        try:
            # 獲取所有網卡資訊作為診斷資訊
            diag_cmd = "ipconfig /all"
            diag_result = subprocess.run(diag_cmd, shell=True, capture_output=True, text=True, encoding='big5')
            logger.debug(f"完整網卡資訊:\n{diag_result.stdout}")
        except Exception as diag_error:
            logger.error(f"無法獲取診斷資訊: {diag_error}")
        return None

def verify_bat_execution(target_ip):
    """驗證BAT檔案執行結果"""
    max_attempts = 5  # 增加重試次數
    wait_time = 5
    
    for attempt in range(max_attempts):
        try:
            current_ip = get_ethernet_ip()
            # 檢查配置狀態
            config_cmd = "netsh interface ip show config name='乙太網路'"
            config_result = subprocess.run(config_cmd, shell=True, capture_output=True, text=True, encoding='big5')
            
            if current_ip == target_ip:
                logger.info(f"IP驗證成功: {current_ip}")
                return True
                
            # 記錄更詳細的狀態資訊
            logger.warning(f"第{attempt + 1}次驗證:")
            logger.warning(f"當前IP: {current_ip}")
            logger.warning(f"目標IP: {target_ip}")
            if config_result.stdout:
                logger.debug(f"網卡配置:\n{config_result.stdout}")
                
            time.sleep(wait_time)
            
        except Exception as e:
            logger.error(f"IP驗證過程發生錯誤: {e}")
            time.sleep(wait_time)
    
    return False

def switch_network(target):
    """切換網路並驗證"""
    try:
        # 設定目標參數
        if target == "192":
            bat_file = "change_to_192.bat"
            expected_ip = "192.168.1.11"
        else:
            bat_file = "change_to_10.bat"
            expected_ip = "10.248.250.60"
            
        # 獲取切換前的IP
        original_ip = get_ethernet_ip()
        logger.info(f"切換前IP: {original_ip}")
            
        # 執行BAT檔案
        logger.info(f"執行 {bat_file}")
        result = subprocess.run(
            bat_file,
            shell=True,
            capture_output=True,
            text=True,
            encoding='big5'
        )
        
        # 記錄執行結果
        if result.stdout:
            logger.info(f"BAT標準輸出:\n{result.stdout}")
        if result.stderr:
            logger.error(f"BAT錯誤輸出:\n{result.stderr}")
            
        # 等待網路重新啟動
        logger.info("等待網路重新啟動...")
        time.sleep(10)
        
        # 驗證IP是否正確切換
        if verify_bat_execution(expected_ip):
            logger.info(f"成功切換到 {target} 網段")
            return True
        else:
            logger.error(f"切換到 {target} 網段失敗")
            return False
            
    except Exception as e:
        logger.error(f"切換網路時發生錯誤: {e}")
        return False

def test_network_command():
    """測試網路配置命令是否可用"""
    try:
        result = subprocess.run(
            ['netsh', 'interface', 'ipv4', 'show', 'addresses'],
            capture_output=True
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"測試 netsh 命令時發生錯誤: {e}")
        return False

def check_prerequisites():
    """檢查必要的命令和檔案是否存在"""
    if not test_network_command():
        logger.error("netsh 命令執行失敗")
        return False
        
    if not os.path.exists("change_to_192.bat"):
        logger.error("找不到 change_to_192.bat 檔案")
        return False
        
    if not os.path.exists("change_to_10.bat"):
        logger.error("找不到 change_to_10.bat 檔案")
        return False
        
    try:
        result = subprocess.run(
            ['netsh', 'interface', 'show', 'interface', '乙太網路'],
            capture_output=True,
            text=True,
            encoding='big5'
        )
        if result.returncode != 0:
            logger.error("找不到乙太網路介面")
            return False
    except Exception as e:
        logger.error(f"檢查乙太網路介面時發生錯誤: {e}")
        return False
        
    return True

def run_test(test_count=3):
    """執行網路切換測試"""
    if not check_prerequisites():
        logger.error("前置檢查失敗，停止測試")
        return
        
    logger.info(f"開始執行網路切換測試，測試次數: {test_count}")
    
    success_count = 0
    failure_count = 0
    
    for i in range(test_count):
        logger.info(f"\n=== 測試回合 {i+1}/{test_count} ===")
        
        # 切換到192網段
        if switch_network("192"):
            success_count += 1
        else:
            failure_count += 1
            
        time.sleep(5)
        
        # 切換到10網段
        if switch_network("10"):
            success_count += 1
        else:
            failure_count += 1
            
        time.sleep(5)
    
    # 輸出統計結果
    total_tests = test_count * 2
    success_rate = (success_count / total_tests) * 100
    
    logger.info("\n=== 測試結果統計 ===")
    logger.info(f"總測試次數: {total_tests}")
    logger.info(f"成功次數: {success_count}")
    logger.info(f"失敗次數: {failure_count}")
    logger.info(f"成功率: {success_rate:.2f}%")

if __name__ == "__main__":
    logger = setup_logger()
    logger.info("開始乙太網路切換測試")
    
    try:
        # 記錄初始狀態
        initial_ip = get_ethernet_ip()
        logger.info(f"初始IP: {initial_ip}")
        
        # 執行測試
        run_test()
        
    except Exception as e:
        logger.error(f"測試過程中發生未預期的錯誤: {e}")
    finally:
        logger.info("測試結束")