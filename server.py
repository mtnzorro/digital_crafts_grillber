from flask import Flask, render_template, redirect, request, session, flash
import pg

app = Flask('app')

@app.route('/')
def login():


    return render_template(
    'grillber.html'
    )

@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    shift = request.form.get('shift')
    date = request.form.get('date')
    size = request.form.get('size')
    print "Shift : %s, Date: %s, Size: %s" % (shift,date,size)
    return redirect('/')





if __name__ == '__main__':
    app.run(debug=True)
