import os

from flask import render_template, send_from_directory

from structured_eligibility import app, api_client


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


# display information for the trial identified by the nct_id (or nci id)
@app.route('/display_trial/<trial_id>', methods=['GET'])
def display_trial(trial_id):
    # retrieving trial as dictionary from the CTRP API client
    trial_dict = api_client.get_trial_by_nct_id(trial_id)
    # Render template
    return render_template('display_trial.html', trial=trial_dict)
