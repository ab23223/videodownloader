from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'albums')
TEMPLATE_FILE = os.path.join(os.getcwd(), 'album_template.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_album():
    data = request.json
    album_name = data['album_name']
    album_desc = data['album_desc']
    urls = data['image_urls']
    album_date = datetime.now().strftime('%Y-%m-%d')

    # Build album HTML
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

    return jsonify({'success': True, 'message': 'Album created', 'filename': filename})

if __name__ == '__main__':
    app.run(debug=True)
