from .base_page import BasePage
from playwright.async_api import Page
from utils.error_handler import error_handler

class TimezonePage(BasePage):
    """時區設定頁面處理類"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.timezone_hour_select = '#SET_TimeSync_TZHour'
        
    @error_handler(retry_count=3)
    async def configure_timezone(self):
        """設定時區"""
        try:
            # 等待頁面元素載入
            await self.wait_for_selector(self.timezone_hour_select)
            
            # 設定時區為 GMT+8
            await self.page.select_option(self.timezone_hour_select, '8')
            self.logger.info("已設定時區為 GMT+8")
            
            # 點擊下一步
            await self.click_next()
            self.logger.info("時區設定完成，已點擊下一步")
            
        except Exception as e:
            self.logger.error(f"設定時區時發生錯誤: {e}")
            raise