# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 17:18:46 2023

@author: Administrator
"""

from scapy.all import *

def sniff_specific_port(port):
    def process_packet(packet):
        # 格式化输出数据包的相关信息
       # print(packet.summary())
        print(packet.show())
        with open('captured_packet4.txt', 'a') as f:
            f.write(str(packet) + '\n')
        
    # 开始嗅探特定端口的数据包
    sniff(filter=f"port {port}", prn=process_packet)

# 捕获特定端口的数据包（例如端口号为5000）
sniff_specific_port(5000)
