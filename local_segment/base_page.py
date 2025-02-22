import re
from playwright.async_api import Page
from utils.logger import setup_logger
from utils.error_handler import error_handler

class BasePage:
    """基礎頁面類，提供共用的頁面操作方法"""
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = setup_logger(__name__)

    @error_handler(retry_count=3)
    async def click_next(self):
        """
        點擊下一步按鈕
        使用正則表達式匹配 next_1 到 next_10 的按鈕
        """
        try:
            # 使用正則表達式找到所有可能的下一步按鈕
            next_buttons = await self.page.query_selector_all('[id^="next_"]')
            
            for button in next_buttons:
                # 獲取按鈕的ID
                button_id = await button.get_attribute('id')
                # 檢查ID是否符合模式 next_1 到 next_10
                if re.match(r'next_([1-9]|10)$', button_id):
                    # 檢查按鈕是否可見
                    is_visible = await button.is_visible()
                    if is_visible:
                        await button.click()
                        self.logger.info(f"點擊下一步按鈕: {button_id}")
                        return
            
            raise Exception("找不到可見的下一步按鈕")
            
        except Exception as e:
            self.logger.error(f"點擊下一步按鈕時發生錯誤: {e}")
            raise

    @error_handler(retry_count=3)
    async def click_back(self):
        """
        點擊上一步按鈕
        使用正則表達式匹配 back_1 到 back_10 的按鈕
        """
        try:
            # 使用正則表達式找到所有可能的上一步按鈕
            back_buttons = await self.page.query_selector_all('[id^="back_"]')
            
            for button in back_buttons:
                # 獲取按鈕的ID
                button_id = await button.get_attribute('id')
                # 檢查ID是否符合模式 back_1 到 back_10
                if re.match(r'back_([1-9]|10)$', button_id):
                    # 檢查按鈕是否可見
                    is_visible = await button.is_visible()
                    if is_visible:
                        await button.click()
                        self.logger.info(f"點擊上一步按鈕: {button_id}")
                        return
            
            raise Exception("找不到可見的上一步按鈕")
            
        except Exception as e:
            self.logger.error(f"點擊上一步按鈕時發生錯誤: {e}")
            raise

    @error_handler(retry_count=3)
    async def wait_for_selector(self, selector: str, timeout: int = 5000):
        """
        等待元素出現
        Args:
            selector: CSS選擇器
            timeout: 超時時間(毫秒)
        """
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
        except Exception as e:
            self.logger.error(f"等待元素 {selector} 出現時超時: {e}")
            raise