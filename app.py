# # encoding:utf-8
# # !/usr/bin/env python

import time
from threading import Lock
from flask import Flask, render_template
import Adafruit_DHT

from flask_socketio import SocketIO


sensor = Adafruit_DHT.DHT11
gpio = 18

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


# 后台线程 产生数据，即刻推送至前端
def background_thread():
    count = 0
    while True:
        socketio.sleep(5)
        count += 1
        t = time.strftime('%H:%M:%S', time.localtime())
        # 获取系统时间（只取分:秒）
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
        # 获取系统cpu使用率 non-blocking
        socketio.emit('server_response',
                      {'data': [t, humidity,temperature], 'count': count},
                      namespace='/test')
        # 注意：这里不需要客户端连接的上下文，默认 broadcast = True


@app.route('/')
def index():
    return render_template('test.html', async_mode=socketio.async_mode)


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send("come from web server: " + str(message))


if __name__ == '__main__':
    socketio.run(app, debug=True,host='0.0.0.0')

# import pymysql
# # 打开数据库连接
# db = pymysql.connect("192.168.122.102", "root", "qq111111", "device")

# # 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()