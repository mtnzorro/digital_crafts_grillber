from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from flask import Flask, render_template, redirect, request, session, flash
import pg, os

tmp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask('Wiki', template_folder=tmp_dir)

db = pg.DB(
    dbname=os.environ.get('PG_DBNAME'),
    host=os.environ.get('PG_HOST'),
    user=os.environ.get('PG_USERNAME'),
    passwd=os.environ.get('PG_PASSWORD')
)

app.secret_key = 'keyur12345'



@app.route('/')
def login():
    return render_template(
    'grillber.html'
    )

@app.route('/reserve_date')
def render_date():
    return render_template(
    'reserve.html'
    )

@app.route('/login')
def log_in():
    return render_template(
    'login.html'
    )

@app.route('/logout')
def logout():
    del session['email']
    del session['name']
    del session['id']
    return render_template(
    'grillber.html'
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
            session['email'] = user.email
            session['name'] = user.name
            session['id'] = user.id
            return redirect('/')
    else:
        return redirect('/login')


@app.route('/submit_date', methods=['POST'])
def date_submit():
    date = request.form.get('date')
    query = db.query("Select distinct on (size.size) size.size, grill.id, size.reserve_btn_display from grill inner join size on size.id = grill.size_id and grill.id not in"
"(SELECT grill.id from grill left outer join reservation on grill.id = reservation.grill_id where reservation.reserve_date = $1"
")",date).namedresult()
    if len(query)>0:
        return render_template(
        'reserve_grill.html',
        query = query,
        date = date
        )
    else:
        flash ("All grills are booked on this day.")
    return redirect('/')


@app.route('/reserve_grill')
def reserve_grill():
    render_template(
    'reserve_grill.html'
    )

@app.route('/submit_reservation',methods =['POST'])

def reserve_confirmation():
    if ('id' in session):
        grill_id = request.form.get('id')
        email = session['email']
        cust_id = session['id']
        date = request.form.get('date')
        size = db.query("select size from size inner join grill on size.id = grill.size_id where grill.id=$1",grill_id).namedresult()[0].size
        db.insert('reservation',
        reserve_date = date,
        grill_id = grill_id,
        customer_id = cust_id)
        return render_template(
        'confirmation.html',
        date = date,
        size = size
        )
    else:
        flash('Please login to reserve.')
        return render_template(
        'login.html')

@app.route('/account')
def account():
    query = db.query("select reservation.id as rid, customer_id,reservation.reserve_date, size.size from reservation inner join grill on reservation.grill_id = grill.id inner join size on grill.size_id = size.id").namedresult()
    if (session['name'] == "owner"):
        return render_template(
        'owner_account.html',
        query= query
        )
    else:
        return render_template(
        'account.html',
        query = query
        )


@app.route('/submit_cancel',methods =['POST'])
def cancel_submit():
    reservation_id = request.form.get('cancel')
    print reservation_id
    query = db.query("select * from reservation where reservation.id = $1",reservation_id).namedresult()[0]
    reserve_date = query.reserve_date
    customer_id = query.customer_id
    grill_id = query.grill_id
    print reserve_date
    print customer_id
    print grill_id
    db.delete('reservation',
        id = reservation_id,
        reserve_date = query.reserve_date,
        customer_id = query.customer_id,
        grill_id = query.grill_id
    )
    flash('You have successfully cancelled your reservation')
    return redirect ('/account')



if __name__ == '__main__':
    app.run(debug=True)
