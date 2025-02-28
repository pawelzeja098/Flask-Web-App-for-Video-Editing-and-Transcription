"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from SocketIOTest import app
from SocketIOTest.globaldata import folder_path
import os
# @app.route('/')
# @app.route('/home')
# def home():
#     """Renders the home page."""
#     return render_template(
#         'index.html',
#         title='Home Page',
#         year=datetime.now().year,
#     )

@app.route('/video_catalogue')
def video_catalogue():
    """Renders the video catalogue page"""
    files = os.listdir(f"{folder_path}")
    
    files_mp4 = [f for f in files if f.endswith("mp4")]

    files = [{"video": f} for f in files_mp4]
    return render_template(
        'video_catalogue.html',
        title='Video Catalogue',
        year=datetime.now().year,
        files = files
    )



@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/')
@app.route('/home')
def home():
    """Render the index.html template on the root URL."""
    return render_template('index.html')


