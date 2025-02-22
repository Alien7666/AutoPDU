from .base_page import BasePage
from playwright.async_api import Page
from utils.error_handler import error_handler

class AccountPage(BasePage):
    """帳號設定頁面處理類"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.account_input = '#SET_Account'
        self.password_input = '#SET_Password'
        self.confirm_password_input = '#SET_Password1'
        
    @error_handler(retry_count=3)
    async def set_account(self):
        """設定預設帳號密碼"""
        try:
            # 等待頁面元素載入
            await self.wait_for_selector(self.account_input)
            await self.wait_for_selector(self.password_input)
            await self.wait_for_selector(self.confirm_password_input)
            
            # 填寫帳號
            await self.page.fill(self.account_input, 'admin')
            self.logger.info("已填寫帳號")
            
            # 填寫密碼
            await self.page.fill(self.password_input, 'admin')
            self.logger.info("已填寫密碼")
            
            # 填寫確認密碼
            await self.page.fill(self.confirm_password_input, 'admin')
            self.logger.info("已填寫確認密碼")
            
            # 點擊下一步
            await self.click_next()
            self.logger.info("帳號設定完成，已點擊下一步")
            
        except Exception as e:
            self.logger.error(f"設定帳號密碼時發生錯誤: {e}")
            raise