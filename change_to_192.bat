@echo off
echo changing network to 192.168.1.11 ...

rem 設定新IP
netsh interface ipv4 set address "乙太網路" static 192.168.1.11 255.255.255.0

rem 停用區域連線並啟用
netsh interface set interface "乙太網路" admin=disabled
timeout /t 1 /nobreak
netsh interface set interface "乙太網路" admin=enabled

echo IP已設定為 192.168.1.11
timeout /t 3 /nobreak
exit