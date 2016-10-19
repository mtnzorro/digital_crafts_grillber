# from flask import Flask, render_template, redirect, request, session, flash
# import pg
#
# app = Flask('app')
#
# @app.route('/')
# def login():
#
#     return render_template(
#     'grillber.html'
#     )
#
# @app.route('/submit_reservation', methods=['POST'])
# def submit_reservation():
#     shift = request.form.get('shift')
#     date = request.form.get('date')
#     size = request.form.get('size')
#
#     print "Shift : %s, Date: %s, Size: %s" % (shift,date,size)
#     return redirect('/')
#
#
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, redirect, request, session, flash
import pg

app = Flask('app')
db = pg.DB(dbname='grillber_db')

app.secret_key = 'keyur12345'


@app.route('/')
def login():
    return render_template(
    'grillber.html'
    )

@app.route('/login')
def log_in():
    return render_template(
    'login.html'
    )
@app.route('/signup')
def sign_up():
    return render_template(
    'signup.html'
    )

@app.route('/submit_signup', methods=['POST'])
def submit_signup():
    email = request.form.get('email')
    password = request.form.get('password')
    street = request.form.get('street')
    zip_code = request.form.get('zip_code')
    phone = request.form.get('phone')
    name = request.form.get('name')
    print email+password+street

    db.insert('customer',
    email = email,
    password = password,
    street = street,
    zip_code = zip_code,
    phone = phone,
    name = name
    )

    return redirect('/login')


@app.route('/submit_login', methods=['POST'])
def submit_login():
    email = request.form.get('email')
    password = request.form.get('password')
    query = db.query("Select * from customer where email=$1",email).namedresult()

    if len(query)>0:
        user = query[0]
        if user.password == password:
            session['user'] = user.name
            print "UEEEEEEEERTSRET!!!!"
            print session['user']
            return redirect('/')
        else:
            return redirect('/login')
    else:
        return redirect('/login')



# @app.route('/submit_reservation', methods=['POST'])
# def submit_reservation():
#     shift = request.form.get('shift')
#     date = request.form.get('date')
#     size = request.form.get('size')
#     print "Shift : %s, Date: %s, Size: %s" % (shift,date,size)
#     return redirect('/')





if __name__ == '__main__':
    app.run(debug=True)
