from flask import Flask
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/demo')
def demo():
    return 'demo'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
