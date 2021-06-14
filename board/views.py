from flask import Blueprint, request, jsonify,current_app
from board.users import User
from flask_basicauth import BasicAuth
from board.utils import validate_data
board = Blueprint("leaderboard", __name__)


from board.logger import boardLogger
logHandle = boardLogger.getInstance()
basic_auth = BasicAuth()


@board.route('/add-user/', methods=['POST'])
@basic_auth.required
def add_user():
    data = request.json
    app_config = current_app._get_current_object()
    if request.method == 'POST':
        logHandle.info("Existing users are %s" %app_config.config['USERS_INFO'])
        try:
            validation_response = validate_data(request=request)
            if validation_response.get('error'):
                logHandle.error("Error in payload {}".format(validation_response.get('error')))
                return jsonify(validation_response), 400
            user = User(data)
            app_config.config['USERS_INFO'].update(user.to_json())
            logHandle.info("Updated users list {}".format(app_config.config['USERS_INFO']))
            return jsonify({"response": "Successfully Added User"})
        except Exception as e:
            logHandle.error("Error occured - {} while adding user".format(e))
            return jsonify({"response": "User not added"}), 400

@board.route('/list-user/', methods=['GET'])
@basic_auth.required
def list_user():
    try:
        users = []
        app_config = current_app._get_current_object()
        users_info = app_config.config['USERS_INFO']
        sorted_users = sorted(users_info.items(), key=lambda x: x[1]['points'], reverse=True)
        for user in sorted_users:
            users.append({user[0]: user[1]})
        logHandle.info("Sorted users list {}".format(users))
        return jsonify({"response": users})
    except Exception as e:
        logHandle.info("Error occured - {} while listing user".format(e))
        return jsonify({"response": "Unsuccessfull"}), 400


@board.route('/score/<int:id>/update/', methods=['PATCH'])
@basic_auth.required
def score_update(id):
    try:
        data = request.json
        app_config = current_app._get_current_object()
        users_info = app_config.config['USERS_INFO']
        user = users_info.get(id)
        user['points'] += data.get('points')
        logHandle.info("Update score for user - {} and id {}".format(user.get('name'), id))
        return jsonify({"response": "Updated score for user {} , score - {}".format(id, user.get('points'))})
    except TypeError:
        logHandle.info("No existing record found for user {}".format(id))
        return jsonify({"response": "No such user found"}), 400
    except Exception as e:
        logHandle.info("Error occured - {} while updating score for user".format(e))
        return jsonify({"response": "Unsuccessfull"}), 400


@board.route('/delete-user/<int:id>/', methods=['DELETE'])
@basic_auth.required
def delete_user(id):
    try:
        app_config = current_app._get_current_object()
        users_info = app_config.config['USERS_INFO']
        user = users_info.pop(id,'No Key found')
        if user == 'No Key found':
            logHandle.info("No existing record found for user {}".format(id))
            return jsonify({"response": "No such user found"}), 400
        logHandle.info("User {}-{} removed successfully".format(id, user.get('name')))
        return jsonify({"response": "{} User Removed".format(user.get('name'))})
    except Exception as e:
        logHandle.info("Error occured - {} while adding user".format(e))
        return jsonify({"response": "Unsuccessfull"}), 400