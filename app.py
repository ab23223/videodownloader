from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'albums')
TEMPLATE_FILE = os.path.join(os.getcwd(), 'album_template.html')

# 🔒 Replace these with your real Cloudinary credentials
cloudinary.config(
    cloud_name='dfqreujbo',
    api_key='467879367759351',
    api_secret='tgJspwPABIOzKQrG3YSeb7YAx2g'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    album_name = request.form['album_name']
    album_desc = request.form['album_desc']
    album_date = datetime.now().strftime('%Y-%m-%d')
    files = request.files.getlist('images')
    
    urls = []
    folder = f"intence/{album_name.replace(' ', '_')}_{album_date}"
    
    for file in files:
        result = cloudinary.uploader.upload(file, folder=folder)
        urls.append(result['secure_url'])

    # Generate HTML
    with open(TEMPLATE_FILE, 'r') as f:
        template = f.read()

    image_js = ",\n".join(f'"{url}"' for url in urls)
    filled = template.replace('{{title}}', album_name)
    filled = filled.replace('{{desc}}', album_desc)
    filled = filled.replace('{{images}}', image_js)

    filename = f"{album_name.replace(' ', '_')}_{album_date}.html"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(filled)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
