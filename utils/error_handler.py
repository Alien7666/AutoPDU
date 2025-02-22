import asyncio
from typing import Optional, Callable, Any
import functools
from .logger import setup_logger

logger = setup_logger(__name__)

class PDUError(Exception):
    """PDU操作相關的基礎異常類"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class NetworkError(PDUError):
    """網路相關錯誤"""
    pass

class PDUConnectionError(PDUError):
    """PDU連線錯誤"""
    pass

class PDUConfigError(PDUError):
    """PDU配置錯誤"""
    pass

def error_handler(retry_count: int = 3, retry_delay: int = 1) -> Callable:
    """
    錯誤處理裝飾器
    
    Args:
        retry_count (int): 重試次數
        retry_delay (int): 重試延遲時間(秒)
        
    Returns:
        Callable: 裝飾器函數
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            attempts = 0
            last_error = None
            
            while attempts < retry_count:
                try:
                    return await func(*args, **kwargs)
                except PDUConnectionError as e:
                    last_error = e
                    attempts += 1
                    if attempts < retry_count:
                        logger.warning(f"因為錯誤原因: {e} , 所以正在重試 {func.__name__} (重試次數: {attempts}/{retry_count})")
                        import asyncio
                        await asyncio.sleep(retry_delay)
                    else:
                        logger.error(f"達到 {func.__name__}的最大重試次數：{e}")
                except PDUError as e:
                    logger.error(f"PDU設定中的 {func.__name__} 功能錯誤,原因: {e}")
                    raise
                except Exception as e:
                    logger.error(f"在{func.__name__}發生未預期的錯誤,原因: {e}")
                    raise
            
            if last_error:
                raise last_error
                
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            attempts = 0
            last_error = None
            
            while attempts < retry_count:
                try:
                    return func(*args, **kwargs)
                except PDUConnectionError as e:
                    last_error = e
                    attempts += 1
                    if attempts < retry_count:
                        logger.warning(f"由於連線錯誤，正在重試 {func.__name__} : {e} （重試次數 {attempts}/{retry_count})")
                        import time
                        time.sleep(retry_delay)
                    else:
                        logger.error(f"達到{func.__name__}的最大重試次數：{e}")
                except PDUError as e:
                    logger.error(f"PDU設定中的 {func.__name__} 功能錯誤,原因: {e}")
                    raise
                except Exception as e:
                    logger.error(f"在{func.__name__}發生未預期的錯誤,原因: {e}")
                    raise
            
            if last_error:
                raise last_error
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator