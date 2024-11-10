from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

