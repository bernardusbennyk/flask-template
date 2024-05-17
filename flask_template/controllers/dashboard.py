from flask import render_template
from flask_login import login_required
from flask_template import app

@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():               
    return render_template("dashboard.html", menu="Dashboard")