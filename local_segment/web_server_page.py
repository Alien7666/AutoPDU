from .base_page import BasePage
from playwright.async_api import Page
from utils.error_handler import error_handler

class WebServerPage(BasePage):
    """Web Server 設定頁面處理類"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.http_checkbox = '#SET_HttpOpen'
        self.https_checkbox = '#SET_HttpsOpen'
        
    @error_handler(retry_count=3)
    async def configure_web_server(self):
        """設定 Web Server"""
        try:
            # 等待頁面元素載入
            await self.wait_for_selector(self.http_checkbox)
            await self.wait_for_selector(self.https_checkbox)
            
            # 檢查並確保 HTTP 已勾選
            is_http_checked = await self.page.is_checked(self.http_checkbox)
            if is_http_checked:
                self.logger.info("已啟用 HTTP")
            else:
                await self.page.check(self.http_checkbox)
                self.logger.info("已啟用 HTTP")
            
            # 檢查並確保 HTTPS 已勾選
            is_https_checked = await self.page.is_checked(self.https_checkbox)
            if not is_https_checked:
                await self.page.check(self.https_checkbox)
                self.logger.info("已啟用 HTTPS")
            else:
                self.logger.info("HTTPS 已經是啟用狀態")
            
            # 點擊下一步
            await self.click_next()
            self.logger.info("Web Server 設定完成，已點擊下一步")
            
        except Exception as e:
            self.logger.error(f"設定 Web Server 時發生錯誤: {e}")
            raise