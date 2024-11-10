from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Get the port from the environment variable, or default to 5000 if not set
    port = int(os.environ.get("PORT", 5000))
    # Bind to host '0.0.0.0' to be accessible externally
    app.run(host='0.0.0.0', port=port)
