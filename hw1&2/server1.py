# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 18:18:32 2023

@author: Crist
"""

from flask import Flask, request, jsonify
import requests
from io import BytesIO
from PIL import Image
import os
app = Flask(__name__)
received_texts = []
# 创建一个空列表用于保存接收到的图片
received_images = []
# 定义接收小程序文字和图片的接口
@app.route('/receive/text', methods=['POST'])
def receive_message():
    # 获取小程序发送的数据
    data = request.json
    # 处理接收到的文字和图片
    text = data.get('text')
    # 将接收到的文字保存到列表中
    received_texts.append(text)
    # TODO: 在这里进行文字和图片的处理逻辑
    # 将接收到的文字保存到txt文件中
    with open('received_texts.txt', 'a') as f:
         f.write(text + '\n')

    response = {
        'message': 'Received message successfully',
        'text': text
       }

    return jsonify(response)
# 定义接收小程序图片的接口
# 导入所需模块

# 定义接收小程序图片的接口
@app.route('/receive/img', methods=['POST'])
def receive_image():
    # 获取上传的文件对象
    image_file = request.files['image']        
    # 保存图片到本地
   # image_path = 'C:/Users/Administrator/image111.jpg'
# 获取 images 文件夹下的所有 .jpg 文件数量
    image_count = len([filename for filename in os.listdir('images') if filename.endswith('.jpg')])
       # 生成一个唯一的文件名
    filename = 'image' + str(image_count+ 1) + '.jpg'
   # 拼接保存图片的路径
    image_path = os.path.join('images', filename)
   # 保存图片到指定路径
    image_file.save(image_path)
    # 生成对应的 txt 文件名
 # 返回图片路径和当前图片数量
    return jsonify({'message': 'Received and saved image successfully', 'image_path': image_path, 'image_count': image_count})


    

@app.route('/get/image', methods=['GET'])
def get_image():
    # 从内存中获取保存的图片
   # image_path = os.path.join('C:/Users/Administrator', 'image111.jpg')
    count = len([filename for filename in os.listdir('images') if filename.endswith('.jpg')])
         
    # 生成对应的图片文件路径
    image_path = os.path.join('images', f'image{count}.jpg')
   # 检查文件是否存在
    if not os.path.exists(image_path):
       return jsonify({'error': 'Image not found'}), 404
   
   # 从文件中读取图片数据
    with open(image_path, 'rb') as f:
       image_data = f.read()
   
   # 返回图片给小程序
    return image_data, 200, {'Content-Type': 'image/jpeg'}


@app.route('/texts', methods=['GET'])
def get_texts():
    # 返回保存的文字列表
    # 从txt文件中读取保存的文字列表
    with open('received_texts.txt', 'r') as f:
        texts = f.readlines()
# 去除每行文字末尾的换行符
        texts = [text.rstrip('\n') for text in texts]

# 返回保存的文字列表
    return jsonify({'texts': texts})

# 运行Flask应用
if __name__ == '__main__':
    app.run(host='10.0.4.8', port=5000,debug=True)
