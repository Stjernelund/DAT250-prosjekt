from flask import Flask
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'