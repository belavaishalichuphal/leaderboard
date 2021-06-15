# flask_testing/test_base.py
import json
import unittest
from board.utils import validate_data
from board import create_app
from  base64 import b64encode
from flask import current_app

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.data = {
                    "name": "bela",
                    "age": "11",
                    "address": "goa, india",
                    "points": 10
                    }

    def tearDown(self):
        self.app_context.pop()

    def get_api_headers(self):
        return {
            'Authorization': 'Basic ' + b64encode(
                ('api-key:generatesomesecurekeyforthis').encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_a_404(self):
        res = self.client.get('/wrong/url',
            headers=self.get_api_headers())
        self.assertEqual(res.status_code, 404)


    def test_b_mandatoryparams(self):
        response = validate_data(data=self.data)
        self.assertEqual(response.get('response'), 'Data is valid')
        # remove name
        self.data.pop('name')
        response = validate_data(data=self.data)
        self.assertEqual(response.get('error'), 'Name, age and address are manadatory fields,')
        # remove age
        self.data.update({"name": "bela"})
        self.data.pop('age')
        response = validate_data(data=self.data)
        self.assertEqual(response.get('error'), 'Name, age and address are manadatory fields,')
        # remove address
        self.data.update({"age": 18})
        self.data.pop('address')
        response = validate_data(data=self.data)
        self.assertEqual(response.get('error'), 'Name, age and address are manadatory fields,')

    def test_c_user_has_zero_intially(self):
        response = self.client.post("user/",
                                    headers=self.get_api_headers(),
                                    data=json.dumps(self.data))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['response'], 'Successfully Added User')
        app = current_app._get_current_object()
        user_score = app.config['USERS_INFO']
        self.index = app.config['GLOBAL_INDEX']
        self.assertEqual(user_score[app.config['GLOBAL_INDEX']]['points'], 0)

    def test_d_user_score_plus(self):
        query = {"operation": "plus"}
        response = self.client.patch("score/1/", query_string = query,
                                    headers=self.get_api_headers(), data="{}"
                                    )
        self.assertEqual(response.status_code, 200)
        app = current_app._get_current_object()
        user_score = app.config['USERS_INFO']
        self.assertEqual(user_score[1]['points'], 10)

    def test_e_user_score_minus(self):
        query = {"operation": "minus"}
        response = self.client.patch("score/1/", query_string = query,
                                    headers=self.get_api_headers(),
                                     data="{}"
                                    )
        self.assertEqual(response.status_code, 200)
        app = current_app._get_current_object()
        user_score = app.config['USERS_INFO']
        self.assertEqual(user_score[1]['points'], 0)

    def test_f_user_list(self):
        response = self.client.get("user/",
                                    headers=self.get_api_headers(), data="{}")
        self.assertEqual(response.status_code, 200)
        app = current_app._get_current_object()
        user_score = app.config['USERS_INFO']
        response = json.loads(response.get_data(as_text=True))
        self.assertEqual(user_score[1], response['response'][0]['1'])

    def test_g_user_delete(self):
        response = self.client.delete("user/1/",
                                    headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        app = current_app._get_current_object()
        user = app.config['USERS_INFO']
        self.assertEqual(user, {})


if __name__ == '__main__':
    unittest.main()