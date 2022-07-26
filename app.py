from flask import Flask, render_template, request, url_for, flash, redirect
from subnetter.subnetter import Subnetter

app = Flask(__name__)
app.config['SECRET_KEY'] = '9c00d036a14dc8ebf17b61b1079b7d69c0e2097bbe6faf13'


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


# @app.route("/kail")
# def Kail():
#   return "Kail is a NERD!!!"


@app.route("/resume")
def resume():
  return render_template("resume.html")


# messages = [{'title': 'Message One',
#              'content': 'Message One Content'},
#             {'title': 'Message Two',
#              'content': 'Message Two Content'}
#             ]


# @app.route('/index')
# def index():
#     return render_template('index.html', messages=messages)


# @app.route('/contact', methods=('GET', 'POST'))
# def contact():
#   if request.method == 'POST':
#     name = request.form['name']
#     email = request.form['email']
#     subject = request.form['subject']
#     message = request.form['message']
#
#     if not name:
#       flash('Name is required!')
#     elif not email:
#       flash('Email is required!')
#     elif not subject:
#       flash('Subject is required!')
#     elif not message:
#       flash('Message is required!')
#
#   # else:
#   #   messages.append({'title': title, 'content': content})
#   #   return redirect(url_for('index'))
#
#   return render_template('contact.html')


@app.route('/subnetter', methods=('GET', 'POST'))
def subnetter():
  if request.method == 'POST':
    ip = request.form['ip']
    mask = request.form['mask'].strip('/')

    if not ip or not validIP(ip):
        flash('Vaild IP Address is required!')
    elif not mask or (not validIP(mask) and not valid_cidr(mask)):
        flash('Valid Subnet Mask is required!')
    else:
      query = Subnetter(ip, mask)
      data = [{
          'ip': ip,
          'network': query.network()[0],
          'subnet': query.network()[1],
          'wildcard': query.wildcard(),
          'first': query.first(),
          'last': query.last(),
          'broadcast': query.broadcast(),
          'hosts': query.hosts(),
          'cidr': query.cidr()
          }]
      return render_template('subnetter.html', data=data)
  return render_template('subnetter.html')


@app.route("/cisco")
def cisco():
  return render_template("cisco.html")


def validIP(ip):
  octets = ip.split('.')
  if len(octets) != 4:
    return False
  for idx, octet in enumerate(octets):
    try:
      if not 0 <= int(octet) <= 255:
        print('here')
        return False
    except ValueError:
      return False
  return True


def valid_cidr(cidr):
  try:
    if not 0 <= int(cidr) <= 32:
      return False
  except ValueError:
    return False
  return True



if __name__ == '__main__': # on running python app.py
  app.run(debug=True)

