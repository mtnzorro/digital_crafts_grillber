from flask import Flask, render_template, redirect, request, session, flash
import pg

app = Flask('app')

@app.route('/')
def login():


    return render_template(
    'grillber.html'
    )


if __name__ == '__main__':
    app.run(debug=True)
