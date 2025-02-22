from .base_page import BasePage
from playwright.async_api import Page
from utils.error_handler import error_handler

class DNSSettingsPage(BasePage):
    """DNS 設定頁面處理類"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.primary_dns_input = '#SET_DNS1'
        
    @error_handler(retry_count=3)
    async def configure_dns_settings(self):
        """設定 DNS"""
        try:
            # 等待頁面元素載入
            await self.wait_for_selector(self.primary_dns_input)
            
            # 設定主要 DNS 伺服器為 Google DNS
            await self.page.fill(self.primary_dns_input, '8.8.8.8')
            self.logger.info("已設定主要 DNS 伺服器為 8.8.8.8")
            
            # 點擊下一步
            await self.click_next()
            self.logger.info("DNS 設定完成，已點擊下一步")
            
        except Exception as e:
            self.logger.error(f"設定 DNS 時發生錯誤: {e}")
            raise