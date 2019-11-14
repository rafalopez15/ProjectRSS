from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from datetime import datetime
import requests
import math
import os
import xml.etree.ElementTree as ET

from project.db import get_db

bp = Blueprint('feed', __name__)

@bp.route('/')
def index():
    db = get_db()
    feeds = db.execute(
        'SELECT * FROM rss'
    ).fetchall()
    return render_template('feed/index.html', feeds=feeds)


@bp.route('/', methods=('GET', 'POST'))
def add_rss_feed():
    if request.method == 'POST':
        rss_name = request.form['rssname']
        rss_url = request.form['rssurl']
        db = get_db()
        error = None

        if not rss_name:
            error = 'Enter a name'
        if not rss_url:
            error = 'RSS URL is required'
        elif db.execute(
            'SELECT rssname FROM rss WHERE rssname = ?', (rss_name.upper(),)
        ).fetchone() is not None:
            error = 'RSS {} is already exists.'.format(rss_name)
        
        if error is None:
            get_xml(rss_url)
            db.execute(
                'INSERT INTO rss (rssname, rssurl, rssdate) VALUES (?, ?, ?)',
                (rss_name.upper(), rss_url, find_date())
            )
            db.commit()
            os.remove('rss-feed.xml')
            return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('feed/index.html')


# Function to get RSS Feed in XML via HTTP request.
def get_xml(url):
    """
    Writes an XML file pulled from a company file to the local directory.

    Parameters
    ----------
    url : str
        Takes in a url as a string that should contain the RSS Feed URL.
    """
    response = requests.get(url)
    with open('rss-feed.xml', 'wb') as file:
        file.write(response.content)

def find_date():
    """
    Finds a tag which contains the date of the last updated item.
    Parameters
    ----------
    root : Element
        A root to the elements of the tree.
    
    Returns
    -------
    str
        A date in string format.
    """
    # Search XML tree for first 'pubDate' tag which corresponds to the latest publish date
    tree = ET.parse('rss-feed.xml')
    root = tree.getroot()
    try:
        return next(root.iter('pubDate')).text # The iterable object is the list of matches found
    except StopIteration:
        return '' # Return empty string if no element matches were found