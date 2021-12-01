from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect  
import time
import serial
import random

async_mode = None

app = Flask(__name__)

ser = serial.Serial('/dev/ttyACM0', 115200) #open serial port
# ser = serial.Serial('/dev/ttyACM1', 115200) #open serial port
ser.baudrate = 115200


app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock() 


def background_thread(args):
    count = 0            
    while True:
        read_ser = ser.read() # read up to 1 byte
#         print(read_ser)
        fo = open("static/files/LightLevel.txt","a+")
        fo.write("Light Level: %s\r\n" %read_ser)

        #socketio.sleep(.1)
        count += 1
            
        socketio.emit('my_response',
                      {'data': read_ser, 'count': count},
                      namespace='/test')  

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/db')
def db():
    return render_template('database.html', async_mode=socketio.async_mode)

@socketio.on('my_event', namespace='/test')
def test_message(message):   
    session['receive_count'] = session.get('receive_count', 0) + 1   
    emit('my_response',
         {'data': message['value'], 'count': session['receive_count']})
 
@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    ser.write("stop\n")

@socketio.on('connect', namespace='/test')
def test_connect():
    ser.write("start\n")
    read_ser = ser.read()
    fo = open('static/files/LightLevel.txt','w').close()
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
    emit('my_response', {'data': 'Connected!', 'count': 0})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)