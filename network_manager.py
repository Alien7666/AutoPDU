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
        使用cmd更改網路設定
        Args:
            local_ip (str): 要設定的本機IP
            subnet_mask (str): 子網路遮罩
        Returns:
            bool: 是否成功更改網路設定
        """
        try:
            command = f'netsh interface ipv4 set address "乙太網路" static {local_ip} {subnet_mask}'
            
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                self.logger.error("網路變更命令超時")
                return False

            # 驗證網路設定是否成功變更
            if not self._verify_network_change(local_ip, timeout=3):
                self.logger.error("網絡變更驗證失敗")
                return False

            self.logger.info(f"成功更改IP至 {local_ip}")
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

    def _verify_network_change(self, target_ip, timeout=3):
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
                addresses = socket.gethostbyname_ex(socket.gethostname())[2]
                if target_ip in addresses:
                    return True
                time.sleep(0.5)
            except socket.error:
                continue
        return False