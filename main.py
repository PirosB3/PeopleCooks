# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import libs
import api

# Define initial configuration
app = Flask(__name__)
app.config.from_object('settings')

# Register external handlers
app.register_blueprint(api.api_blueprint, url_prefix='/api')


# Register internal handlers
@app.route('/admin/')
def admin():
    return render_template('admin.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
