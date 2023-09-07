from datetime import datetime

from flask import Flask, render_template, jsonify, request, url_for, redirect, flash
from database import load_cfl, add_cfl, get_all_cfls, update_cfl

app = Flask(__name__)


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
def submit_cfl():
    data = request.form
    cfl_id = add_cfl(data)
    cfl = load_cfl(cfl_id)
    return render_template('cfl_confirmed.html', cfl=cfl)


@app.route("/cfl/edit/<int:cfl_id>", methods=['GET', 'POST'])
def edit_cfl(cfl_id):
    # Retrieve the record by ID
    cfl = load_cfl(cfl_id)  # You'll need to define this function
    if not cfl:
        # Provide a flash message or some error to the user to indicate the problem.
        # You can use Flask's flash function for this.
        flash('CFL not found!', 'error')

    if request.method == 'POST':
        # Here you handle the updating of the record
        update_cfl(cfl_id, request.form)
        return redirect(url_for('/logout/view'))# or wherever you want to redirect after editing

    return render_template('edit_cfl.html', cfl=cfl)


@app.route("/logout/view", methods=['post'])
def view_logout():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
    end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')

    cfls = get_all_cfls(start_date, end_date)

    return render_template('view_logout.html', cfls=cfls)


@app.route("/logout")
def logout():
    return render_template('logout.html')


@app.route("/summary")
def summary():
    return render_template('summary.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
