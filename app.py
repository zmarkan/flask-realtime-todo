
# ./app.py

from flask import Flask, flash, render_template, request, jsonify, redirect
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, InputRequired



from pusher import Pusher
import json
import requests, time

# create flask app
app = Flask(__name__)
app.secret_key = 'unh4ck4bl3'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
  def __init__ (self, name):
    self.name = name

  def get_id(self):
    try:
        return self.name
    except AttributeError:
        raise NotImplementedError('No `id` attribute - override `get_id`')

  def __eq__(self, other):
    '''
    Checks the equality of two `UserMixin` objects using `get_id`.
    '''
    if isinstance(other, UserMixin):
        return self.get_id() == other.get_id()
    return NotImplemented


# configure pusher object
pusher = Pusher(
  app_id='459566',
  key='8d33551ec680cbe8f4e2',
  secret='4d711efa42f7753d8163',
  cluster='eu',
  ssl=True
)


class LoginForm(FlaskForm):
  name = StringField('name', validators=[InputRequired()])

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()

    print "form created"
    print form.validate_on_submit()
    if form.validate_on_submit():
        print "validate successfully"
        # return redirect('/')


        print "in the validation bit"
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = User(form.name.data)
        login_user(user)
        flash('Logged in successfully.')

        next = request.args.get('next')

        return redirect('/')

    return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# index route, shows index.html view
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
  return render_template('index.html')

# endpoint for storing todo item
@app.route('/add-todo', methods = ['POST'])
def addTodo():
  data = json.loads(request.data) # load JSON data from request
  pusher.trigger('todo', 'item-added', data) # trigger `item-added` event on `todo` channel
  return jsonify(data)

# endpoint for deleting todo item
@app.route('/remove-todo/<item_id>')
def removeTodo(item_id):
  data = {'id': item_id }
  pusher.trigger('todo', 'item-removed', data)
  return jsonify(data)

# endpoint for updating todo item
@app.route('/update-todo/<item_id>', methods = ['POST'])
def updateTodo(item_id):
  data = {
    'id': item_id,
    'completed': json.loads(request.data).get('completed', 0)
  }
  pusher.trigger('todo', 'item-updated', data)
  return jsonify(data)

@app.route('/make-req', methods = ['GET'])
def makeRequestToRequestBin():
  r = requests.post('https://requestb.in/16criga1', data={"ts":time.time()})
  print r.status_code
  print r.content
  return jsonify({'success': True})

@app.route("/pusher/auth", methods=['POST'])
def pusher_authentication():

  me = current_user
  print("current user:")
  print(me.name)


  auth = pusher.authenticate(
    channel = request.form['channel_name'],
    socket_id = request.form['socket_id'],
    custom_data = {
      u'user_id': me.name,
      u'user_info': {
        u'name': me.name
      }
    }
  )
  return json.dumps(auth)

# @app.route("/pusher/auth", methods=['POST'])
# def pusher_authentication():

#   auth = pusher.authenticate(
#     channel=request.form['channel_name'],
#     socket_id=request.form['socket_id']
#   )
#   return json.dumps(auth)

# run Flask app in debug mode
app.run(debug=True)