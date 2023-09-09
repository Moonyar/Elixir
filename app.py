import os
from datetime import datetime

from flask import Flask, render_template, jsonify, request, url_for, redirect, flash, get_flashed_messages
from database import load_cfl, add_cfl, get_all_cfls, update_cfl, delete_cfl

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')


@app.route("/")
def home():
    return render_template('Home.html')


@app.route("/cfl")
def cfl():
    return render_template('cfl.html')


@app.route("/cfl/<id>")
def show_cfl(id):
    cfl = load_cfl(id)
    return jsonify(cfl)


@app.route("/cfl/submit", methods=['POST'])
def confirmed_cfl():
    data = request.form
    cfl_id = add_cfl(data)
    cfl = load_cfl(cfl_id)
    return render_template('cfl_submit.html', cfl=cfl)


@app.route("/cfl/<cfl_id>/edit", methods=['POST', 'GET'])
def edit_cfl(cfl_id):
    cfl = load_cfl(cfl_id)
    return render_template('cfl_edit.html', cfl=cfl)


@app.route("/cfl/edit/<cfl_id>/submit", methods=['POST'])
def submit_edited_cfl(cfl_id):
    data = request.form
    cfl = load_cfl(cfl_id)
    update_cfl(cfl_id, data)
    cfl = load_cfl(cfl_id)
    return render_template('cfl_submit.html', cfl=cfl)


@app.route("/cfl/<cfl_id>/delete", methods=['POST', 'GET'])
def cfl_delete(cfl_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    delete_cfl(cfl_id)
    if start_date and end_date:
        return redirect(url_for('view_logout', start_date=start_date, end_date=end_date))
    else:
        return redirect(url_for('cfl'))


@app.route("/logout/view", methods=['post', 'GET'])
def view_logout():
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
    else:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

    if "T" in start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')

    if "T" in end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

    cfls = get_all_cfls(start_date, end_date)

    if not cfls:
        flash("No CFLs found for the specified date range.", "cfl_warning")
        return redirect(url_for('logout'))
    else:
        return render_template('view_logout.html', cfls=cfls, start_date=start_date,
                           end_date=end_date)


@app.route("/logout")
def logout():
    return render_template('logout.html')


@app.route("/summary")
def summary():
    return render_template('summary.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
