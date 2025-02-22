from .base_page import BasePage
from playwright.async_api import Page
from utils.error_handler import error_handler

class GeneralSettingPage(BasePage):
    """一般設定頁面處理類"""
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    @error_handler(retry_count=3)
    async def skip_general_setting(self):
        """跳過一般設定設定"""
        try:
            # 直接點擊完成
            await self.click_next()
            self.logger.info("已跳過一般設定設定")
            
        except Exception as e:
            self.logger.error(f"跳過一般設定設定時發生錯誤: {e}")
            raise