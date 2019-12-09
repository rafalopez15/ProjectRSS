from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from . import mongo
from werkzeug.exceptions import abort
from project.db import get_db
from .classes import RSSOperations

bp = Blueprint('feed', __name__)
ops = RSSOperations.RSSOperations()

@bp.route('/')
def index():
    feeds = mongo.db.RSS.find().sort("last_update")
    return render_template('feed/index.html', feeds=feeds)


@bp.route('/', methods=('GET', 'POST'))
def add_rss_feed():
    if request.method == 'POST':
        rss_name = request.form['rssname']
        rss_url = request.form['rssurl']
        error = None

        if not rss_name:
            error = 'Enter a name'
        if not rss_url:
            error = 'RSS URL is required'
        elif mongo.db.RSS.find_one(filter={'rss_name': rss_name}) is not None:
            error = 'RSS {} is already exists.'.format(rss_name)
        
        if error is None:
            ops.get_xml(rss_url)
            mongo.db.RSS.insert_one(
                {
                    "rss_name": rss_name,
                    "rss_xml": rss_url,
                    "last_update": ops.find_date()
                })
            ops.remove_file()
            return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('feed/index.html')


@bp.route('/<rssname>', methods=('POST',))
def delete(rssname):
    mongo.db.RSS.delete_one({'rss_name': rssname})
    return redirect(url_for('index'))