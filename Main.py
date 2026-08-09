import os
import time
import threading
from flask import Flask, render_template, request

app = Flask(__name__)

is_running = False

def convo_task(token, convo_id, hater_name, speed, messages):
    global is_running
    is_running = True
    print("--- Convo Task Started ---")
    
    idx = 0
    while is_running and messages:
        try:
            msg = messages[idx % len(messages)]
            full_msg = f"{hater_name} {msg}".strip()
            print(f"[SENDING TO {convo_id}] -> {full_msg}")
            
            time.sleep(float(speed))
            idx += 1
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    token = request.form.get('token')
    convo_id = request.form.get('convo_id')
    hater_name = request.form.get('hater_name')
    speed = request.form.get('speed', 5)
    
    file = request.files.get('message_file')
    messages = []
    if file:
        lines = file.read().decode('utf-8').splitlines()
        messages = [l.strip() for l in lines if l.strip()]
        
    with open("TS-TOKEN.txt", "w") as f: f.write(str(token))
    with open("TS-CONVO.txt", "w") as f: f.write(str(convo_id))
    with open("TS-NAME.txt", "w") as f: f.write(str(hater_name))
    with open("TS-SPEED.txt", "w") as f: f.write(str(speed))
    
    thread = threading.Thread(target=convo_task, args=(token, convo_id, hater_name, speed, messages), daemon=True)
    thread.start()
    
    return "<h2>Server Started Successfully!</h2><br><a href='/'>Go Back</a>"

@app.route('/stop', methods=['POST'])
def stop():
    global is_running
    is_running = False
    return "<h2>Server Stopped Successfully!</h2><br><a href='/'>Go Back</a>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
