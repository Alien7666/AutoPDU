from .base_page import BasePage
from playwright.async_api import Page
from utils.error_handler import error_handler

class TimeFormatPage(BasePage):
    """時間格式設定頁面處理類"""
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    @error_handler(retry_count=3)
    async def skip_time_format(self):
        """跳過時間格式設定"""
        try:
            # 直接點擊下一步
            await self.click_next()
            self.logger.info("已跳過時間格式設定,選擇預設的YYYY/MM/DD HH:MM:SS")
            
        except Exception as e:
            self.logger.error(f"跳過時間格式設定時發生錯誤: {e}")
            raise