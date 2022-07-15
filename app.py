from flask import Flask, render_template

app = Flask(__name__)


# @app.route("/") # at the endpoint /
# def hello(): # call method hello
#   return 'Nathan is a Dorkus!'
#
#
# @app.route("/beautiful")
# def beautiful():
#   return 'I love you Butthead!!!'


# def factors(num):
#   return [x for x in range (1, num+1) if num % x == 0]
#
#
# @app.route('/')
# def home():
#   return '<a href="/factor_raw/100"> click here for an example</a>'
#
#
# @app.route('/factor_raw/<int:n>')
# def factors_display_raw_html(n):
#   list_factor = factors(int(n))
#   # adding "n" and placed at the top
#   html = "<h1> Factors of " + str(n) + " are</h1>" + "\n" + "<ul>"
#   # make a <li> item for every output (factor)
#   for f in list_factor:
#     html += "<li>" + str(f) + "</li>" + "\n"
#   html += "</ul> </body>" # closes tag at the end
#   return html


@app.route("/")
def home():
  return render_template("home.html")


@app.route("/kail")
def Kail():
  return "Kail is a NERD!!!"


@app.route("/about")
def about():
  return render_template("about.html")


if __name__ == '__main__': # on running python app.py
  app.run(debug=True)

