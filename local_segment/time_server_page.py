from .base_page import BasePage
from playwright.async_api import Page
from utils.error_handler import error_handler
from config import NetworkConfig

class TimeServerPage(BasePage):
    """時間伺服器設定頁面處理類"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.time_sync_checkbox = '#SET_TimeSync_Kind2'
        self.time_server_input = '#SET_TimeSync_TimeServer'
        
    @error_handler(retry_count=3)
    async def configure_time_server(self):
        """設定時間伺服器"""
        try:
            # 等待頁面元素載入
            await self.wait_for_selector(self.time_sync_checkbox)
            await self.wait_for_selector(self.time_server_input)
            
            # 確保時間同步已啟用
            is_sync_checked = await self.page.is_checked(self.time_sync_checkbox)
            if not is_sync_checked:
                await self.page.check(self.time_sync_checkbox)
                self.logger.info("已啟用時間伺服器同步")
            else:
                self.logger.info("時間伺服器同步已經是啟用狀態")
            
            # 設定時間伺服器
            await self.page.fill(self.time_server_input, NetworkConfig.REMOTE_SEGMENT['timezone_server'])
            self.logger.info(f"已設定時間伺服器: {NetworkConfig.REMOTE_SEGMENT['timezone_server']}")
            
            # 點擊下一步
            await self.click_next()
            self.logger.info("時間伺服器設定完成，已點擊下一步")
            
        except Exception as e:
            self.logger.error(f"設定時間伺服器時發生錯誤: {e}")
            raise