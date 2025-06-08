from flask import Flask, render_template, request, flash
from subnetter.subnetter import Subnetter
from config import key

app = Flask(__name__)
app.config['SECRET_KEY'] = key


@app.route("/")
def portfolio():
    return render_template("portfolio.html")


@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route('/subnetter', methods=('GET', 'POST'))
def subnetter():
    if request.method == 'POST':
        ip = request.form['ip']
        mask = request.form['mask'].strip('/')

        try:
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
        except ValueError as error:
            flash(error)
       #  if not ip:
       #      flash('Valid IP Address is required!')
       #  elif not mask:
       #      flash('Valid Subnet Mask is required!')
       #  else:
            # try:
                # query = Subnetter(ip, mask)
    return render_template('subnetter.html')


@app.route("/eagleeye")
def eagleeye():
    return render_template("eagleeye.html")


@app.route("/webpage")
def webpage():
    return render_template("webpage.html")


@app.route("/honerable-mentions")
def honerableMentions():
    return render_template("honerable-mentions.html")


#@app.route("/cisco")
#def cisco():
#    return render_template("cisco.html")


# def valid_ip(ip):
#     octets = ip.split('.')
#     if len(octets) != 4:
#         return False
#     for idx, octet in enumerate(octets):
#         try:
#             if not 0 <= int(octet) <= 255:
#                 print('here')
#                 return False
#         except ValueError:
#             return False
#     return True
# 
# 
# def valid_mask(mask):
#     try:
#         if not 0 <= int(mask) <= 32:
#             return False
#     except ValueError:
#         octets = mask.split('.')
#         for octet in octets:
#             print(octet)
#             try:
#                 if not 0 <= int(octet) <= 255:
#                     return False
#             except ValueError:
#                 return False
#             finally:
#                 if int(octet) == 255:
#                     octet = str(int(octet) + 1)
#                 print(octet)
#                 if not (int(octet) and (not (int(octet) & (int(octet) - 1)))):
#                     return False


if __name__ == '__main__':
    app.run(debug=True)
