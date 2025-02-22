# setup_vendor.py
import os
import shutil
from pathlib import Path
import site
import sys

def find_package_path(package_name):
    """尋找套件的安裝路徑"""
    import pkg_resources
    try:
        package = pkg_resources.working_set.by_key[package_name]
        return package.location
    except KeyError:
        return None

def setup_playwright_vendor():
    """設置 playwright 及其依賴"""
    try:
        # 尋找 playwright 的安裝路徑
        playwright_base = find_package_path('playwright')
        if not playwright_base:
            print("找不到 playwright 的安裝路徑")
            return
        
        # 建立 vendor 目錄
        vendor_path = Path('vendor')
        vendor_path.mkdir(parents=True, exist_ok=True)
        
        # 複製 playwright 相關檔案
        src_path = os.path.join(playwright_base, 'playwright')
        dst_path = vendor_path / 'playwright'
        if os.path.exists(src_path):
            print(f"正在複製 playwright 從 {src_path} 到 {dst_path}")
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path)
            shutil.copytree(src_path, dst_path)
        
        # 複製 pyee
        pyee_base = find_package_path('pyee')
        if pyee_base:
            src_path = os.path.join(pyee_base, 'pyee')
            dst_path = vendor_path / 'pyee'
            if os.path.exists(src_path):
                print(f"正在複製 pyee 從 {src_path} 到 {dst_path}")
                if os.path.exists(dst_path):
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)
                
    except Exception as e:
        print(f"設置 playwright vendor 時發生錯誤: {e}")
        raise

def setup_tqdm_vendor():
    """設置 tqdm"""
    try:
        # 尋找 tqdm 的安裝路徑
        tqdm_base = find_package_path('tqdm')
        if not tqdm_base:
            print("找不到 tqdm 的安裝路徑")
            return
            
        vendor_path = Path('vendor')
        vendor_path.mkdir(parents=True, exist_ok=True)
        
        # 複製 tqdm 相關檔案
        src_path = os.path.join(tqdm_base, 'tqdm')
        dst_path = vendor_path / 'tqdm'
        if os.path.exists(src_path):
            print(f"正在複製 tqdm 從 {src_path} 到 {dst_path}")
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path)
            shutil.copytree(src_path, dst_path)
            
    except Exception as e:
        print(f"設置 tqdm vendor 時發生錯誤: {e}")
        raise

def install_dependencies():
    """安裝必要的依賴套件"""
    try:
        import subprocess
        print("正在安裝必要的依賴套件...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyee"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
        print("依賴套件安裝完成")
    except Exception as e:
        print(f"安裝依賴套件時發生錯誤: {e}")
        raise

if __name__ == "__main__":
    try:
        # 安裝依賴
        install_dependencies()
        
        # 設置 vendor 目錄
        print("正在設置 vendor 目錄...")
        setup_playwright_vendor()
        setup_tqdm_vendor()
        print("設置完成！")
    except Exception as e:
        print(f"發生錯誤: {e}")
        sys.exit(1)