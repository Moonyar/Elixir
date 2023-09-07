from flask import Flask, render_template, jsonify, request
from databse import load_cfl, add_cfl

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


@app.route("/cfl/submit", methods=['post'])
def submit_cfl():
    data = request.form
    cfl_id=add_cfl(data)
    cfl=load_cfl(cfl_id)
    return render_template('cfl_confirmed.html', cfl=cfl)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
