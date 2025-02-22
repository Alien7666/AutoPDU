from .base_page import BasePage
from playwright.async_api import Page
from utils.error_handler import error_handler

class LanguagePage(BasePage):
    """語言選擇頁面處理類"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.language_selector = '#SET_Language_List'

    @error_handler(retry_count=3)
    async def select_language(self):
        """選擇繁體中文語言"""
        try:
            # 等待語言選擇下拉選單出現
            await self.wait_for_selector(self.language_selector)
            
            # 選擇繁體中文選項
            await self.page.select_option(self.language_selector, 'cht')
            self.logger.info("已選擇繁體中文")
            
            # 點擊下一步
            await self.click_next()
            
        except Exception as e:
            self.logger.error(f"選擇語言時發生錯誤: {e}")
            raise