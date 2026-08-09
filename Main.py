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
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Legend Romeo's Convo</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
    background-color: #0f172a;
    background-image: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.45)), url('https://ibb.co/JRBMhx0R');
    background-repeat: no-repeat;
    background-position: center center;
    background-size: cover;
    background-attachment: fixed;
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
}


        /* Pure Glass Effect - Background Image Always Visible */
        .card-container {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1.5px solid rgba(255, 255, 255, 0.25);
            border-radius: 20px;
            padding: 28px 22px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
            text-align: center;
        }

        .card-header {
            font-size: 22px;
            font-weight: 900;
            letter-spacing: 1.5px;
            color: #ffffff;
            margin-bottom: 20px;
            text-transform: uppercase;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.9);
        }

        .card-header span {
            color: #3b82f6;
            text-shadow: 0 0 12px rgba(59, 130, 246, 0.9);
        }

        .form-group {
            margin-bottom: 14px;
            text-align: left;
        }

        label {
            display: block;
            font-size: 12px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.9);
        }

        input[type="text"],
        input[type="number"],
        select,
        input[type="file"] {
            width: 100%;
            padding: 11px 14px;
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: #ffffff;
            font-weight: 700;
            border-radius: 10px;
            font-size: 13px;
            outline: none;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
        }

        input[type="text"]::placeholder,
        input[type="number"]::placeholder {
            color: rgba(255, 255, 255, 0.75);
            font-weight: 600;
        }

        select option {
            background: #111827;
            color: #ffffff;
        }

        input[type="file"]::file-selector-button {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.4);
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 800;
            margin-right: 10px;
        }

        .btn {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 900;
            cursor: pointer;
            text-transform: uppercase;
            margin-top: 15px;
            letter-spacing: 1px;
        }

        .btn-run {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: #ffffff;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.6);
        }

        .btn-stop {
            background: linear-gradient(135deg, #dc2626, #b91c1c);
            color: #ffffff;
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.6);
        }

        .divider {
            height: 1px;
            background: rgba(255, 255, 255, 0.25);
            margin: 20px 0;
        }
    </style>
</head>
<body>

<div class="card-container">
    <div class="card-header">
        R0M30 <span>TH3e</span> L3G3ND
    </div>

    <form action="/submit" method="POST" enctype="multipart/form-data">
        <div class="form-group">
            <label>Select Token Option</label>
            <select name="token_option" id="tokenOption" onchange="toggleTokenInput()">
                <option value="single">Single Token</option>
                <option value="multi">Multi Token</option>
            </select>
        </div>

        <!-- Single Token Input Field -->
        <div class="form-group" id="singleTokenBox">
            <label>Enter Single Token</label>
            <input type="text" name="token" placeholder="Enter Your Access Token" autocomplete="off">
        </div>

        <!-- Multi Token File Field -->
        <div class="form-group" id="multiTokenBox" style="display: none;">
            <label>Choose Token File (.txt)</label>
            <input type="file" name="token_file" accept=".txt">
        </div>

        <div class="form-group">
            <label>Enter Inbox / Convo ID</label>
            <input type="text" name="convo_id" placeholder="Enter Target Convo/Group ID" required autocomplete="off">
        </div>

        <div class="form-group">
            <label>Enter Your Hater Name</label>
            <input type="text" name="hater_name" placeholder="Enter Hater / Prefix Name" required autocomplete="off">
        </div>

        <div class="form-group">
            <label>Speed (in Seconds)</label>
            <input type="number" name="speed" value="5" min="1" required>
        </div>

        <div class="form-group">
            <label>Choose Message File (.txt)</label>
            <input type="file" name="message_file" accept=".txt" required>
        </div>

        <button type="submit" class="btn btn-run">Run Server</button>
    </form>

    <div class="divider"></div>

    <form action="/stop" method="POST">
        <div class="form-group">
            <label>Enter Task ID to Stop</label>
            <input type="text" name="task_id" placeholder="Optional Task ID">
        </div>
        <button type="submit" class="btn btn-stop">Stop Server</button>
    </form>
</div>

<script>
    function toggleTokenInput() {
        var option = document.getElementById("tokenOption").value;
        var singleBox = document.getElementById("singleTokenBox");
        var multiBox = document.getElementById("multiTokenBox");

        if (option === "multi") {
            singleBox.style.display = "none";
            multiBox.style.display = "block";
        } else {
            singleBox.style.display = "block";
            multiBox.style.display = "none";
        }
    }
</script>

</body>
</html>
