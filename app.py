from flask import Flask, render_template, request, jsonify, redirect, url_for, session, Response
import os, json
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.secret_key = 'hi'  # You can change this to something secure
USERNAME = 'admin'
PASSWORD = 'intencemedia2025'

ALBUMS_FILE = 'albums.json'
ALBUM_FOLDER = os.path.join('static', 'albums')
TEMPLATE_FILE = os.path.join('templates', 'album_template.html')

# -------------------------
# Login System
# -------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# -------------------------
# Admin Console (Protected)
# -------------------------
@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/adminconsole')
def index():
    return render_template('index.html')

import json

@app.route('/generate', methods=['POST'])
def generate_album():
    data = request.json
    album_name = data['album_name']
    album_desc = data['album_desc']
    urls = data['image_urls']
    album_date = datetime.now().strftime('%Y-%m-%d')

    with open(TEMPLATE_FILE, 'r') as f:
        template = f.read()

    image_js = json.dumps(urls)

    # Replace placeholders correctly
    filled = template.replace('{{title}}', album_name)
    filled = filled.replace('{{desc}}', album_desc)
    filled = filled.replace('{{images}}', image_js)

    filename = f"{album_name.replace(' ', '_')}_{album_date}.html"
    filepath = os.path.join(ALBUM_FOLDER, filename)

    os.makedirs(ALBUM_FOLDER, exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(filled)

    preview_url = f"/static/albums/{filename}"

    # Return the preview URL AND the full HTML code
    return jsonify({
        'success': True,
        'message': 'Album created',
        'filename': filename,
        'preview_url': preview_url,
        'html_code': filled  # send the entire HTML code string
    })


if __name__ == '__main__':
    app.run(debug=True)
