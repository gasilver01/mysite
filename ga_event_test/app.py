from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select')
def select():
    s1 = request.args.get('select1')
    s2 = request.args.get('select2')
    return render_template('select.html',select1 = s1, select2 = s2)

app.run(debug=True)