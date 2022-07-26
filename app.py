from flask import Flask, render_template, request, flash
from subnetter.subnetter import Subnetter

app = Flask(__name__)
app.config['SECRET_KEY'] = '9c00d036a14dc8ebf17b61b1079b7d69c0e2097bbe6faf13'


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route('/subnetter', methods=('GET', 'POST'))
def subnetter():
    if request.method == 'POST':
        ip = request.form['ip']
        mask = request.form['mask'].strip('/')

        if not ip or not valid_ip(ip):
            flash('Valid IP Address is required!')
        elif not mask or (not valid_ip(mask) and not valid_cidr(mask)):
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


def valid_ip(ip):
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


if __name__ == '__main__':
    app.run(debug=True)
