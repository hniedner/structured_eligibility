import os

from flask import render_template, send_from_directory

from structured_eligibility import app


# favicon serving
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# home page - redirecting straight to search form
@app.route('/')
def home():
    # Render template
    return render_template('home.html')
