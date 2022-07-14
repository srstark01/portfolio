from flask import Flask

app = Flask(__name__)


@app.route("/") # at the endpoint /
def hello(): # call method hello
  return 'Hello World!!!'


if __name__ == '__main__': # on running python app.py
  app.run(host='0.0.0.0')

