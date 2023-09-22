import os
from datetime import datetime

from flask import Flask, render_template, jsonify, request, url_for, redirect, flash, get_flashed_messages, session
from werkzeug.urls import url_parse

from database import load_cfl, add_cfl, get_all_cfls, update_cfl, delete_cfl, get_user_by_username, verify_password, \
    get_user_by_id
from flask_login import UserMixin, login_user, login_manager, login_required, logout_user, current_user, LoginManager

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
login = LoginManager(app)
login.login_view = "login"


class User(UserMixin):
    def __init__(self, id, username, full_name, position):
        self.id = id
        self.username = username
        self.full_name = full_name
        self.position = position


@login.user_loader
def load_user(user_id):
    user_data = get_user_by_id(user_id)  # You might need to write this function in `database.py`
    if user_data:
        return User(id=user_data['id'], username=user_data['username'], full_name=user_data['full_name'],
                    position=user_data['position'])
    return None


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)
        if user and verify_password(user['password'], password):
            user_obj = User(id=user['id'], username=user['username'], full_name=user['full_name'],
                            position=user['position'])
            login_user(user_obj)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home')
            return redirect(next_page)
        else:
            flash("Invalid credentials", "login_danger")

    return render_template('login.html')


@app.route("/")
@login_required
def home():
    return render_template('Home.html')


@app.route("/cfl")
@login_required
def cfl():
    return render_template('cfl.html')


@app.route("/cfl/<id>")
@login_required
def show_cfl(id):
    cfl = load_cfl(id)
    return jsonify(cfl)


@app.route("/cfl/submit", methods=['POST'])
@login_required
def confirmed_cfl():
    data = request.form
    cfl_id = add_cfl(data)
    cfl = load_cfl(cfl_id)
    return render_template('cfl_submit.html', cfl=cfl)


@app.route("/cfl/<cfl_id>/edit", methods=['POST', 'GET'])
@login_required
def edit_cfl(cfl_id):
    cfl = load_cfl(cfl_id)
    return render_template('cfl_edit.html', cfl=cfl)


@app.route("/cfl/edit/<cfl_id>/submit", methods=['POST'])
@login_required
def submit_edited_cfl(cfl_id):
    data = request.form
    cfl = load_cfl(cfl_id)
    update_cfl(cfl_id, data)
    cfl = load_cfl(cfl_id)
    return render_template('cfl_submit.html', cfl=cfl)


@app.route("/cfl/<cfl_id>/delete", methods=['POST', 'GET'])
@login_required
def cfl_delete(cfl_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    delete_cfl(cfl_id)
    if start_date and end_date:
        return redirect(url_for('view_logout', start_date=start_date, end_date=end_date))
    else:
        return redirect(url_for('cfl'))


@app.route("/logout/view", methods=['post', 'GET'])
@login_required
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
@login_required
def logout():
    return render_template('logout.html')


@app.route("/summary")
@login_required
def summary():
    return render_template('summary.html')


@app.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
