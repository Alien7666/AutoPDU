import logging
import os
from pathlib import Path
from datetime import datetime

def setup_logger(name):
    """
    設置logger配置
    
    Args:
        name (str): logger名稱
        
    Returns:
        logging.Logger: 配置好的logger實例
    """
    # 建立logs目錄
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # 生成日誌文件名 (例如: 2025-02-20.log)
    log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d-%H')+'-PDU設定'}.log"
    
    # 創建logger
    logger = logging.getLogger(name)
    
    # 如果logger已經有handlers，就不需要再次設置
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.INFO)
    
    # 創建文件處理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # 創建控制台處理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 設置日誌格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加處理器到logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger