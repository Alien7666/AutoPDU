class NetworkConfig:
    """
    網路設定配置
    Attributes:
        local_ip: 本機網卡要設定的IP
        subnet_mask: 子網路遮罩
        gateway: PDU網路設定中的預設閘道
        pdu_ip: PDU的連線IP
        timezone_server: 時間伺服器
    """
    
    LOCAL_SEGMENT = {
        'local_ip': '192.168.1.11',
        'subnet_mask': '255.255.255.0',
        'gateway': '192.168.0.1',
        'pdu_ip' : '192.168.1.1'
    }
    
    REMOTE_SEGMENT = {
        'local_ip': '10.248.250.60',
        'subnet_mask': '255.255.255.0',
        'gateway': '10.248.250.254',
        'pdu_ip' : '10.248.250.53',
        'timezone_server' : '10.248.250.253'
    }

class PDUConfig:
    """PDU相關配置
    Attributes:
        RESTART_WAIT_TIME: PDU重啟等待時間(秒)
        CONNECTION_TIMEOUT: 連線超時時間(秒)
    """
    RESTART_WAIT_TIME = 60
    CONNECTION_TIMEOUT = 10