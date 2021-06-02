import traceback
import logging.config
from flask import Flask
from flask import render_template, request, redirect, url_for

# Initialize the Flask application

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app log')

# Initialize the database session
from src.create_db import Steamreal, SteamManager
steam_manager = SteamManager(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        user_input1 = request.form.to_dict()['game_name']
        user_input2 = request.form.to_dict()['price']
        #print(type(user_input2))
        try:
            if user_input1 == "":
                if user_input2 == "":
                    return render_template('no_input.html')
                else:
                    steams = steam_manager.session.query(Steamreal.rec,Steamreal.price).filter(Steamreal.price<=float(user_input2)+0.01, Steamreal.price>=float(user_input2)-0.01).distinct().all()
                    return render_template('search.html', steams=steams, user_input=user_input2)
            else:
                if user_input2 == "":
                    steams = steam_manager.session.query(Steamreal).filter(Steamreal.searchname==user_input1).all()
                    return render_template('index.html', steams=steams, user_input=user_input1)
                else:
                    steams = steam_manager.session.query(Steamreal).filter(Steamreal.searchname==user_input1, Steamreal.price<=float(user_input2)+0.01, Steamreal.price>=float(user_input2)-0.01).all()
                    return render_template('index.html', steams=steams, user_input=user_input1)


        except:
            traceback.print_exc()
            logger.warning("Not able to display games, error page returned")
            return render_template('error.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gamenames')
def gamenames():
    return render_template('gamenames.html')

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
