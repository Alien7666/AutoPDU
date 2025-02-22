from playwright.async_api import Page
from utils.logger import setup_logger
from utils.error_handler import error_handler

class BasePageRemote:
    """遠端頁面的基礎頁面類"""
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = setup_logger(__name__)

    @error_handler(retry_count=3)
    async def click_button(self, selector: str):
        """點擊按鈕
        Args:
            selector: 按鈕的選擇器
        """
        try:
            await self.wait_for_selector(selector)
            await self.page.click(selector)
            self.logger.info(f"已點擊按鈕: {selector}")
        except Exception as e:
            self.logger.error(f"點擊按鈕時發生錯誤: {e}")
            raise

    @error_handler(retry_count=3)
    async def wait_for_selector(self, selector: str, timeout: int = 5000):
        """等待元素出現
        Args:
            selector: CSS選擇器
            timeout: 超時時間(毫秒)
        """
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
        except Exception as e:
            self.logger.error(f"等待元素 {selector} 出現時超時: {e}")
            raise