from .base_page import BasePageRemote
from playwright.async_api import Page
from utils.error_handler import error_handler

class LoginPage(BasePageRemote):
    """登入頁面處理類"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = '#auth_user'
        self.password_input = '#auth_passwd'
        self.login_button = '#Send_OK'
        
    @error_handler(retry_count=3)
    async def login(self):
        """執行登入操作"""
        try:
            # 等待頁面元素載入
            await self.wait_for_selector(self.username_input)
            await self.wait_for_selector(self.password_input)
            await self.wait_for_selector(self.login_button)
            
            # 填寫帳號密碼
            await self.page.fill(self.username_input, 'admin')
            self.logger.info("已填寫帳號")
            
            await self.page.fill(self.password_input, 'admin')
            self.logger.info("已填寫密碼")
            
            # 點擊登入按鈕
            await self.click_button(self.login_button)
            self.logger.info("已點擊登入按鈕")
            
            # 等待登入成功，跳轉到主頁面
            await self.page.wait_for_load_state('networkidle')
            self.logger.info("登入成功")
            
        except Exception as e:
            self.logger.error(f"登入時發生錯誤: {e}")
            raise