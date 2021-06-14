from flask import  Flask
from config import Config
from board.logger import boardLogger
boardLogger.loggerInit('leaderboard','board.log','./log')
logHandle = boardLogger.getInstance()
from board.views import board

def create_app(config_name="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_name)
    # register our blueprints
    app.register_blueprint(board)
    return app