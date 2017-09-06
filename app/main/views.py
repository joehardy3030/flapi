from flask import render_template, session, redirect, url_for, current_app, jsonify, request
from .. import db
from ..models import User, Stock
from ..email import send_email
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLAPI_ADMIN']:
                send_email(current_app.config['FLAPI_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))


@main.route('/api/v1.0/user/get', methods=['GET', 'POST'])
def get_user():
    user_query_result = User.query.filter_by(username='Joe').first()
    return jsonify({'user_id':user_query_result.id})


@main.route('/api/v1.0/user/post', methods=['GET', 'POST'])
def post_user():
    """Take a username as the body of a HTTP POST, add user if not already in database"""
    if not request.json or not 'username' in request.json:
        abort(400)
    #Look for the user
    user = User.query.filter_by(username=request.json['username']).first()
    if user is None:
        #Add the user if not already there
        user=User(username=request.json['username'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'added':user.username}),201
    else:
        return jsonify({'repeat':user.username})


@main.route('/api/v1.0/user/add_stock', methods=['GET', 'POST'])
def add_stock():
    """Take a stock as the body of a HTTP POST, add it to database"""
    if not request.json or not 'symbol' in request.json:
        abort(400)
    #Look for the user
    #user = User.query.filter_by(username=request.json['username']).first()
    #if user is None:
    #Add the user if not already there
    #stock=Stock(symbol=request.json['symbol'])
    #stock=Stock(shares=request.json['shares'])
    stock=Stock(price=request.json['price'],shares=request.json['shares'],symbol=request.json['symbol'])
    #stock=Stock(date=request.json['date'])
    db.session.add(stock)
    db.session.commit()
    return jsonify({'added':stock.symbol}),201


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@main.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@main.route('/api/v1.0/tasks/p', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201
