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
            result = subprocess.run(bat_file, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                self.logger.error(f"執行 BAT 檔案時發生錯誤: {result.stderr}")
                return False
            
            # 等待網路重新啟動
            time.sleep(10)
            
            # 驗證網路設定是否成功變更
            if not self._verify_network_change(local_ip, timeout=30):
                self.logger.error("網路設定驗證失敗")
                return False
                
            # 測試網路連通性
            target_ip = "10.248.250.53" if local_ip.startswith("10.") else "192.168.1.10"
            if not self._test_connectivity(target_ip):
                self.logger.error(f"無法連線到目標設備: {target_ip}")
                return False
                
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
    def _test_connectivity(self, target_ip, timeout=5):
        """
        測試網路連通性
        Args:
            target_ip (str): 目標IP
            timeout (int): 超時時間（秒）
        Returns:
            bool: 是否可以連通
        """
        try:
            ping_count = "-n" if os.name == "nt" else "-c"
            command = f"ping {ping_count} 1 -w {timeout*1000} {target_ip}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"ping 測試失敗: {e}")
            return False