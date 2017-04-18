from flask import Flask
from flask_bootstrap import Bootstrap
from flask_bower import Bower

from structured_eligibility.config import configure_app

# Initialize the Flask application
app = Flask(__name__)

# Install our Bootstrap extension
Bootstrap(app)
# Install Bower extension
Bower(app)

configure_app(app)

# Pulling in the routes
import structured_eligibility.views
