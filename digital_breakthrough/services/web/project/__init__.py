import logging

from flask import Flask, render_template, url_for, redirect, abort, flash

from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from project.form import LoginForm
from project.config import Config
from project.database import Base, init_db
from project.models import *
from collections import namedtuple
from project.utils import *
import os
SECRET_KEY = os.urandom(32)

Layer = namedtuple("Layer", "name href")

app = Flask(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.config['SECRET_KEY'] = SECRET_KEY
#app.config.from_object(Config)
#db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

STATUS_ENUM = {
    0: "Не обработано",
    1: "Подтверждено",
    2: "Отклонено",
    3: "Брак"
}

COLOR_ENUM = {
    0: "#FFFFFF",
    1: "#28a745",
    2: "#dc3545",
    3: "#343a40"
}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index_without_id():
    event = Event.query.filter(Event.solved == 0)
    if event is not None:
        return redirect(url_for("index", event_id=str(event.first().id)))
    else:
        event = Event.query.filter(Event.solved != 0)
        if event is not None:
            return redirect(url_for("index", event_id=str(event.first().id)))
        else:
            return "Не найдено эвентов."

@app.route('/<int:event_id>')
def index(event_id):
    events = Event.query.all()
    unprepared_events = []
    prepared_events = []
    for i, event in enumerate(events):
        events[i].status = STATUS_ENUM[event.solved]
        events[i].color = COLOR_ENUM[event.solved]
        if i+1 == event_id:
            events[i].active = True
        else:
            events[i].active = False
        if event.solved == 0:
            unprepared_events.append(event)
        else:
            prepared_events.append(event)

    if current_user.is_authenticated:
        layers = [
            Layer(name="Спутник", href=url_for('static', filename='test.jpg')),
            Layer(name="Зелень", href=url_for('static', filename='interface.jpg')),
            Layer(name="НеЗелень", href=url_for('static', filename='test.jpg'))
        ]
        return render_template("index.html", unprepared_events=unprepared_events,
                               prepared_events=prepared_events, layers=layers)
    else:
        return redirect(url_for("login"))


@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/login/process', methods=['GET', 'POST'])
def login_process():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = User.query.filter(User.name == form.name.data).first()
        if user is None:
            flash('User not found.')
            return redirect(url_for('login'))
        if user.password != form.password.data:
            flash('Password is wrong.')
            return redirect(url_for('login'))

        login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('index_without_id'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()
