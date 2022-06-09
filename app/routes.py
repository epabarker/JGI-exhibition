from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, SmellForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Smell
from werkzeug.urls import url_parse
import pandas as pd
import json
import plotly
import plotly.express as px

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home Page')


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/rating', methods=['GET','POST'])
def rating():
    form = SmellForm()
    if form.validate_on_submit():
        vanilla = Smell(smell="Vanilla", rating=form.va_rating.data, user_id=current_user.id)
        db.session.add(vanilla)
        coriander = Smell(smell="Coriander", rating=form.co_rating.data, user_id=current_user.id)
        db.session.add(coriander)
        violet = Smell(smell="Violet", rating=form.vi_rating.data, user_id=current_user.id)
        db.session.add(violet)
        db.session.commit()
        flash('Ratings submitted')
        return redirect(url_for('rating'))
    return render_template('rating.html',title='Smell rating', form=form)

@app.route('/statistics')
def statistics():
    df = pd.read_sql_table(table_name="smell",con=db.session.connection(), index_col="id")
    fig = px.histogram(df, x='rating', nbins=10, color="smell", facet_row="smell")
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    avg_vanilla = df.query('smell == "Vanilla"')['rating'].mean()
    avg_coriander = df.query('smell == "Coriander"')['rating'].mean()
    avg_violet = df.query('smell == "Violet"')['rating'].mean()
    return render_template('statistics.html', graphJSON=graphJSON, avg_vanilla=avg_vanilla, avg_coriander=avg_coriander, avg_violet=avg_violet)
