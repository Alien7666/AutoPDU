import subprocess
import time
import socket
from config import NetworkConfig
from utils.logger import setup_logger

class NetworkManager:
    def __init__(self):
        self.logger = setup_logger(__name__)

    def change_network(self, local_ip, subnet_mask):
        """
        使用 bat 檔案更改網路設定
        Args:
            local_ip (str): 要設定的本機IP
            subnet_mask (str): 子網路遮罩
        Returns:
            bool: 是否成功更改網路設定
        """
        try:
            # 根據目標 IP 選擇對應的 bat 檔案
            if local_ip == "192.168.1.11":
                bat_file = "change_to_192.bat"
            elif local_ip == "10.248.250.60":
                bat_file = "change_to_10.bat"
            else:
                self.logger.error(f"不支援的目標 IP: {local_ip}")
                return False
                
            # 執行 bat 檔案
            subprocess.run(bat_file, shell=True)
            
            # 等待網路重新啟動
            time.sleep(5)
            
            self.logger.info(f"已執行網路切換至 {local_ip}")
            return True
                
        except Exception as e:
            self.logger.error(f"無法更改網絡設定：{e}")
            return False

    def get_current_ip(self):
        """
        獲取當前網路IP
        Returns:
            str: 當前IP地址，如果獲取失敗則返回None
        """
        try:
            addresses = socket.gethostbyname_ex(socket.gethostname())[2]
            # 過濾出符合我們需要網段的IP
            for ip in addresses:
                if ip.startswith('192.168.1.') or ip.startswith('10.248.250.'):
                    return ip
            return None
        except Exception as e:
            self.logger.error(f"無法取得當前IP: {e}")
            return None

    def _verify_network_change(self, target_ip, timeout=30):
        """
        驗證網路設定是否成功變更
        Args:
            target_ip (str): 目標IP
            timeout (int): 超時時間（秒）
        Returns:
            bool: 是否成功驗證
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # 使用 ipconfig 命令檢查 IP
                result = subprocess.run(
                    'ipconfig',
                    capture_output=True,
                    text=True,
                    shell=True
                )
                
                # 檢查輸出中是否包含目標 IP
                if target_ip in result.stdout:
                    return True
                    
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"驗證網路設定時發生錯誤: {e}")
                time.sleep(1)
                continue
        
        return False