
# ./app.py

from flask import Flask, render_template, request, jsonify
from flask.ext.login import LoginManager

from pusher import Pusher
import json
import requests, time


# create flask app
app = Flask(__name__)

# configure pusher object
pusher = Pusher(
  app_id='459566',
  key='8d33551ec680cbe8f4e2',
  secret='4d711efa42f7753d8163',
  cluster='eu',
  ssl=True
)

# index route, shows index.html view
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login')
def login():
  return "" //TODO:

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if password == username + "_secret":
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
        ''')

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

  auth = pusher.authenticate(
    channel = request.form['channel_name'],
    socket_id = request.form['socket_id'],
    custom_data = {
      u'user_id': u'1',
      u'user_info': {
        u'twitter': u'@pusher'
      }
    }
  )
  return json.dumps(auth)

# run Flask app in debug mode
app.run(debug=True)