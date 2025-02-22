from .base_page import BasePageRemote
from playwright.async_api import Page
from utils.error_handler import error_handler
from config import NetworkConfig

class SNMPSettingsPage(BasePageRemote):
    """SNMP 設定頁面處理類"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        # 系統設定頁面的 URL
        self.system_url = f'http://{NetworkConfig.REMOTE_SEGMENT["pdu_ip"]}/system.csp'
        
        # SNMP 分頁的選擇器
        self.snmp_tab = '#ui-id-4'  # SNMP 分頁的 ID
        
        # SNMP 設定欄位的選擇器
        self.snmp_v2_enable = '#SnmpAgent_OpenV2'
        self.snmp_port = '#SnmpAgent_Port'
        self.snmp_read_community = '#SnmpAgent_RCommStr'
        self.snmp_write_enable = '#SnmpAgent_Write'
        self.snmp_write_community = '#SnmpAgent_WCommStr'
        
        # 儲存按鈕
        self.save_button = '#Save_BUTTON'
        
    @error_handler(retry_count=3)
    async def navigate_to_snmp_settings(self):
        """導航到 SNMP 設定頁面"""
        try:
            # 導航到系統設定頁面
            await self.page.goto(self.system_url)
            self.logger.info(f"已導航到系統設定頁面: {self.system_url}")
            
            # 等待並點擊 SNMP 分頁
            await self.wait_for_selector(self.snmp_tab)
            await self.page.click(self.snmp_tab)
            self.logger.info("已切換到 SNMP 設定分頁")
            
        except Exception as e:
            self.logger.error(f"導航到 SNMP 設定頁面時發生錯誤: {e}")
            raise
            
    @error_handler(retry_count=3)
    async def configure_snmp(self):
        """設定 SNMP"""
        try:
            # 等待頁面元素載入
            await self.wait_for_selector(self.snmp_v2_enable)
            
            # 確保 SNMP v1/v2c 已啟用
            is_v2_enabled = await self.page.is_checked(self.snmp_v2_enable)
            if not is_v2_enabled:
                await self.page.check(self.snmp_v2_enable)
                self.logger.info("已啟用 SNMP v1/v2c")
            
            # 確認連接埠是否為 161
            port_value = await self.page.get_attribute(self.snmp_port, 'value')
            if port_value != '161':
                await self.page.fill(self.snmp_port, '161')
                self.logger.info("已設定 SNMP 連接埠為 161")
            
            # 確認讀取權限是否為 hpnnm
            read_community = await self.page.get_attribute(self.snmp_read_community, 'value')
            if read_community != 'hpnnm':
                await self.page.fill(self.snmp_read_community, 'hpnnm')
                self.logger.info("已設定讀取權限為 hpnnm")
            
            # 確保 SNMP 寫入已啟用
            is_write_enabled = await self.page.is_checked(self.snmp_write_enable)
            if not is_write_enabled:
                await self.page.check(self.snmp_write_enable)
                self.logger.info("已啟用 SNMP 寫入")
            
            # 確認寫入權限是否為 private
            write_community = await self.page.get_attribute(self.snmp_write_community, 'value')
            if write_community != 'private':
                await self.page.fill(self.snmp_write_community, 'private')
                self.logger.info("已設定寫入權限為 private")
            
            # 點擊儲存按鈕
            await self.click_button(self.save_button)
            self.logger.info("已儲存 SNMP 設定")
            
        except Exception as e:
            self.logger.error(f"設定 SNMP 時發生錯誤: {e}")
            raise