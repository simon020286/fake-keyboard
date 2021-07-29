from flask import Flask, render_template, request
from flask_socketio import SocketIO
from keyboard import KeyboardProcess

app = Flask(__name__)
socketio = SocketIO(app)
count = 0

@app.route('/')
def  main():
  return render_template('main.html', nome='Simone', status=service.status())

@app.route('/start', methods=['POST'])
def start():
  content=request.json
  service.start(key=content['key'], timespan=content['timespan'])
  status = service.status()
  return {
    "status": status
  }

@app.route('/stop')
def stop():
  service.stop()
  status = service.status()
  return {
    "status": status
  }
  
@app.route('/status')
def status():
  status = service.status()
  return {
    "status": status
  }

@socketio.on('connect', namespace='/dd')
def ws_conn(auth):
    global count
    count = count + 1
    socketio.emit('msg', {'count': count}, namespace='/dd')
    
@socketio.on('disconnect', namespace='/dd')
def ws_disconn():
    global count
    count = count - 1
    socketio.emit('msg', {'count': count}, namespace='/dd')

service = KeyboardProcess()

def main():
    try:
      socketio.run(app, "0.0.0.0", port=5000)
        
    except KeyboardInterrupt:
        pass
         
if __name__ == '__main__':
  main()
