from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('Home.html')

@app.route("/cfl")
def cfl():
    return render_template('cfl.html')

@app.route("/cfl/submit", methods=['post'])
def submit_cfl():
    data = request.form
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)