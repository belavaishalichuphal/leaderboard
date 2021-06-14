from flask import current_app

class User:
    def __init__(self, data):
        self.name = data.get('name')
        self.age = data.get('age')
        self.address = data.get('address')


    def to_json(self):
        app = current_app._get_current_object()
        app.config['GLOBAL_INDEX'] = app.config['GLOBAL_INDEX']+1
        return {app.config['GLOBAL_INDEX'] :{
            'name': self.name,
            'age':self.age,
            'address': self.address,
            'points': 0
        }}