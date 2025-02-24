import sys
import os
from pathlib import Path
import asyncio
from network_manager import NetworkManager
from config import NetworkConfig
from utils.logger import setup_logger
from utils.error_handler import error_handler
from tqdm import tqdm
import time

# 語言頁面
from local_segment import LanguagePage 
# 預設帳號頁面
from local_segment import AccountPage
# Host頁面
from local_segment import HostSettingsPage
# DNS頁面
from local_segment import DNSSettingsPage
# web server頁面
from local_segment import WebServerPage
# 時間格式頁面
from local_segment import TimeFormatPage
# 時間伺服器頁面
from local_segment import TimeServerPage
# 時區設定
from local_segment import TimezonePage
# 日光節約設定
from local_segment import DaylightSavingPage
# 一般設定頁面
from local_segment import GeneralSettingPage

#10網段
#登入頁面
from remote_segment import LoginPage
#SNMP頁面
from remote_segment import SNMPSettingsPage


class PDUAutomation:
    def __init__(self):
        self.network_manager = NetworkManager()
        self.logger = setup_logger(__name__)
        
        # 添加vendor目錄到Python路徑
        vendor_path = Path(__file__).parent / 'vendor'
        sys.path.insert(0, str(vendor_path))
        from playwright.async_api import async_playwright
        self.playwright = async_playwright
        self.browser = None

    async def run(self):
        try:
            # 檢查當前網段
            current_ip = self.network_manager.get_current_ip()
            self.logger.info(f"現在IP為: {current_ip}")

            async with self.playwright() as p:
                # 啟動瀏覽器，設定視窗大小和超時時間
                browser = await p.chromium.launch(
                    headless=False,  # 設為 False 以便觀察自動化過程
                    args=['--start-maximized']
                )
                
                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080}
                )

                page = await browser.new_page()
                page.set_default_timeout(30000)

                # 根據當前網段決定流程
                if current_ip and current_ip.startswith('10.260.258.'):
                    self.logger.info("開始進行10網段的設定")
                    await self._handle_remote_segment(page)
                else:
                    self.logger.info("正在切換到192網段並且開始設定...")
                    await self._handle_local_segment(page)

                await self.browser.close()

        except Exception as e:
            self.logger.error(f"PDU自動設定錯誤，錯誤原因: {e}")
            raise
    async def _create_new_page(self):
        """創建新的頁面"""
        try:
            if self.browser:
                page = await self.browser.new_page()
                page.set_default_timeout(30000)
                return page
            else:
                raise Exception("瀏覽器實例尚未初始化")
        except Exception as e:
            self.logger.error(f"創建新頁面時發生錯誤: {e}")
            raise

    async def _handle_local_segment(self, page):
        
        """處理192網段(192.168.0.x)的設定"""
        try:
            # 切換到192網段
            if not self.network_manager.change_network(
                NetworkConfig.LOCAL_SEGMENT['local_ip'],
                NetworkConfig.LOCAL_SEGMENT['subnet_mask']
            ):
                raise Exception("無法切換到192網段")

            # 連接到PDU
            await page.goto(f"http://{NetworkConfig.LOCAL_SEGMENT['pdu_ip']}")

            
            # *******************語言設定*******************
            language_page = LanguagePage(page)
            await language_page.select_language()
            # self.logger.info("完成語言設定")
            # *******************語言設定*******************
            # *****************預設帳號設定*****************
            account_page = AccountPage(page)
            await account_page.set_account()
            # self.logger.info("完成預設帳號設定")
            # *****************預設帳號設定*****************
            time.sleep(3)
            # ******************HOST設定*******************
            host_page = HostSettingsPage(page)
            await host_page.configure_host_settings()
            # self.logger.info("完成host設定")
            # ******************HOST設定*******************
            time.sleep(3)
            # ******************DNS設定********************
            dns_page = DNSSettingsPage(page)
            await dns_page.configure_dns_settings()
            # self.logger.info("完成DNS設定")
            # ******************DNS設定********************
            time.sleep(3)
            # ****************Web Server設定***************
            web_server_page = WebServerPage(page)
            await web_server_page.configure_web_server()
            # self.logger.info("完成Web Server設定")
            # ****************Web Server設定***************
            time.sleep(3)
            # ******************時間格式設定***************
            time_format_page = TimeFormatPage(page)
            await time_format_page.skip_time_format()
            # self.logger.info("完成時間格式設定")
            # ******************時間格式設定***************
            time.sleep(3)
            # ******************時間伺服器設定**************
            time_server_page = TimeServerPage(page)
            await time_server_page.configure_time_server()
            # self.logger.info("完成時間伺服器設定")
            # ******************時間伺服器設定**************
            time.sleep(3)
            # *********************時區設定*****************
            time_zone_page = TimezonePage(page)
            await time_zone_page.configure_timezone()
            # self.logger.info("完成時區設定")
            # *********************時區設定*****************
            time.sleep(3)
            # *******************日光節約設定***************
            daylight_saving_page = DaylightSavingPage(page)
            await daylight_saving_page.skip_daylight_saving()
            # self.logger.info("完成日光節約設定")
            # *******************日光節約設定***************
            time.sleep(3)
            # *********************一般設定*****************
            general_setting_page = GeneralSettingPage(page)
            await general_setting_page.skip_general_setting()
            # self.logger.info("完成一般設定")
            # *********************一般設定*****************


            # 等待PDU重啟
            self.logger.info("正在等待PDU重啟")
            for _ in tqdm(range(75), desc="PDU重啟中", bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [等待時間: {elapsed}<{remaining}]'):
                await asyncio.sleep(1)
            # Todo 測試ping狀態，若是可以依靠ping來判斷就依照ping而不是秒數
            # PDU重啟後切換到遠端網段
            #await _handle_remote_segment(page)
            await page.goto(f"http://{NetworkConfig.REMOTE_SEGMENT['pdu_ip']}/login.csp")
            
            # 登入動作
            login_page = LoginPage(page)
            await login_page.login()
            time.sleep(3)
            # self.logger.info("10網段登入成功")
            # SNMP設定動作
            snmp_setting_page = SNMPSettingsPage(page)
            await snmp_setting_page.navigate_to_snmp_settings()
            time.sleep(3)
            await snmp_setting_page.configure_snmp()
            time.sleep(3)


        except Exception as e:
            self.logger.error(f"192網段初始設定錯誤,錯誤原因: {e}")
            raise

        async def _handle_remote_segment(self, page=None):
            """處理10網段(10.260.258.x)的設定
            Args:
                page: 可選的Page物件，如果為None則創建新的頁面
            """
            try:
                # 如果沒有提供page或page已關閉，則創建新的page
                try:
                    if page is None or page.is_closed():
                        self.logger.info("創建新的頁面用於遠端設定")
                        page = await self._create_new_page()
                except Exception:
                    self.logger.info("當前頁面可能已關閉，創建新的頁面")
                    page = await self._create_new_page()

                # 切換到10網段
                if not self.network_manager.change_network(
                    NetworkConfig.REMOTE_SEGMENT['local_ip'],
                    NetworkConfig.REMOTE_SEGMENT['subnet_mask']
                ):
                    raise Exception("無法切換到10網段")

                # 連接到PDU
                await page.goto(f"http://{NetworkConfig.REMOTE_SEGMENT['pdu_ip']}/login.csp")
                
                # 登入動作
                login_page = LoginPage(page)
                await login_page.login()
                time.sleep(3)
                
                # SNMP設定動作
                snmp_setting_page = SNMPSettingsPage(page)
                await snmp_setting_page.navigate_to_snmp_settings()
                time.sleep(3)
                await snmp_setting_page.configure_snmp()
                time.sleep(3)

            except Exception as e:
                self.logger.error(f"10網段設定出錯,錯誤原因: {e}")
                raise