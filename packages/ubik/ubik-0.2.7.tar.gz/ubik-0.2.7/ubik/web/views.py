# coding: utf-8
import json
import platform
import ubik

import ubik.core as api

from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import g

from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user

from ubik.status import status
from ubik.database import Database

from ubik.web import app
from ubik.web import auth_db

@app.before_request
def before_request():
    g.api = api
    g.ubik_version = ubik.__version__
    g.system = platform.node()
    g.db = Database(json.load(open(api.conf.get('paths', 'local_db'))))

@app.route('/')
@login_required
def index():
    installed = sorted(g.db.get_installed(), key=lambda k: k.name)
    _all = sorted(g.db.packages.values(), key=lambda k: k.name)
    updates = sorted(g.db.get_upgrades(), key=lambda k: k.name)
    last_update = json.load(open(api.conf.get('paths', 'infos')))['last_update']

    return render_template('index.html',
        all=_all,
        installed=installed,
        updates=updates,
        last_update=last_update,
        status=status)

@app.route('/info')
@login_required
def info():
    infos = {}
    for section in api.conf.sections():
        infos[section] = {}
        for key, value in api.conf.items(section):
            infos[section][key] = value
    return render_template('info.html', infos=infos)

@app.route('/stats')
@login_required
def stats():
    _stats = {  'Packages installed': g.db.count_installed(),
                'Updates available': g.db.count_upgrades(),
                'Total packages': g.db.count_packages()}
    return render_template('stats.html', stats=_stats)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        remember = request.form.get("remember", "no") == "yes"
        print(auth_db.db)
        if auth_db.challenge(username, password):
            if login_user(auth_db.getUser(username), remember=remember):
                flash("Welcome on Ubik Web Interface %s!" % username, "success")
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Bad credentials.")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("login"))
