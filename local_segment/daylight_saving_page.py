from .base_page import BasePage
from playwright.async_api import Page
from utils.error_handler import error_handler

class DaylightSavingPage(BasePage):
    """夏令時設定頁面處理類"""
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    @error_handler(retry_count=3)
    async def skip_daylight_saving(self):
        """跳過夏令時設定"""
        try:
            # 直接點擊下一步
            await self.click_next()
            self.logger.info("已跳過夏令時設定，使用預設的不啟用")
            
        except Exception as e:
            self.logger.error(f"跳過夏令時設定時發生錯誤: {e}")
            raise