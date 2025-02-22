from .base_page import BasePage
from playwright.async_api import Page
from utils.error_handler import error_handler
from config import NetworkConfig

class HostSettingsPage(BasePage):
    """Host Settings 頁面處理類"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.dhcp_checkbox = '#SET_Dhcp'
        self.host_input = '#SET_IP'
        self.gateway_input = '#SET_Gateway'
        
    @error_handler(retry_count=3)
    async def configure_host_settings(self):
        """設定 Host Settings"""
        try:
            # 等待頁面元素載入
            await self.wait_for_selector(self.dhcp_checkbox)
            await self.wait_for_selector(self.host_input)
            await self.wait_for_selector(self.gateway_input)
            
            # 取消勾選 DHCP
            is_checked = await self.page.is_checked(self.dhcp_checkbox)
            if is_checked:
                await self.page.uncheck(self.dhcp_checkbox)
                self.logger.info("已取消勾選 DHCP")
            
            # 填寫 Host IP
            await self.page.fill(self.host_input, NetworkConfig.REMOTE_SEGMENT['pdu_ip'])
            self.logger.info(f"已設定 Host IP: {NetworkConfig.REMOTE_SEGMENT['pdu_ip']}")
            
            # 填寫 Gateway
            await self.page.fill(self.gateway_input, NetworkConfig.REMOTE_SEGMENT['gateway'])
            self.logger.info(f"已設定 Gateway: {NetworkConfig.REMOTE_SEGMENT['gateway']}")
            
            # 點擊下一步
            await self.click_next()
            self.logger.info("Host Settings 設定完成，已點擊下一步")
            
        except Exception as e:
            self.logger.error(f"設定 Host Settings 時發生錯誤: {e}")
            raise