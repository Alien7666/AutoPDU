# main.py
import sys
import ctypes
import asyncio
from utils.logger import setup_logger
from pdu_automation import PDUAutomation

logger = setup_logger(__name__)

def is_admin():
    """檢查是否具有管理員權限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

async def main():
    """主程式入口"""
    try:
        # 初始化 PDU 自動化實例
        pdu = PDUAutomation()
        # 執行自動化流程
        await pdu.run()
        logger.info("PDU 成功設定完成!")
        print(f"PDU 成功設定完成!")
        print(f" ______   _____     __  __    ")
        print(f"/\\  == \\ /\\  __-.  /\\ \\/\\ \\   ")
        print(f"\\ \\  _-/ \\ \\ \\/\\ \\ \\ \\ \\_\\ \\  ")
        print(f" \\ \\_\\    \\ \\____-  \\ \\_____\\ ")
        print(f"  \\/_/     \\/____/   \\/_____/ ")
        
    except Exception as e:
        logger.error(f"PDU自動設定失敗:{e}")
        sys.exit(1)

if __name__ == "__main__":
    if not is_admin():
        logger.warning("本程式沒有以系統管理員權限執行。正在要求提升權限...")
        # 使用 runas 重新以管理員權限啟動程序
        ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            sys.executable, 
            " ".join(sys.argv), 
            None,
            1
        )
    else:
        logger.info("以管理員權限運行")
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            logger.info("程式由使用者終止")
            sys.exit(0)
        except Exception as e:
            logger.error(f"意外錯誤：{e}")
            sys.exit(1)