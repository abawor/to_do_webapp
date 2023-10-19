import unittest
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class TestApp(unittest.TestCase):
    URL = 'http://127.0.0.1:5000/'
    title = 'test'
    new_title = 'test_edited'
    username = os.environ.get('USER_ID')
    password = os.environ.get('PASSWORD')
    auth = (username, password)

    def test_1_show_all_todos(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)
        print("Test 1 completed")

    def test_2_add_new_item(self):
        resp = requests.post(self.URL + 'add', data={'title': self.title}, auth=self.auth)
        self.todo_id = str(resp.json().get('id'))
        self.assertEqual(resp.status_code, 200)
        print("Test 2 completed")

    def test_3_update_item_status(self):
        resp = requests.get(self.URL + 'update/' + self.todo_id, auth=self.auth)
        self.assertEqual(resp.status_code, 200)
        print("Test 3 completed")

    def test_4_edit_item_name(self):
        resp_get = requests.get(self.URL + 'edit/' + self.todo_id, auth=self.auth)
        self.assertEqual(resp_get.status_code, 200)
        resp_post = requests.post(self.URL + 'edit/' + self.todo_id, data={'title': self.new_title}, auth=self.auth)
        self.assertEqual(resp_post.status_code, 200)
        print("Test 4 completed")

    def test_5_delete_item(self):
        resp = requests.get(self.URL + 'delete/' + self.todo_id, auth=self.auth)
        self.assertEqual(resp.status_code, 200)
        print("Test 5 completed")


if __name__ == "__main__":
    tester = TestApp()
    tester.test_1_show_all_todos()
    tester.test_2_add_new_item()
    tester.test_3_update_item_status()
    tester.test_4_edit_item_name()
    tester.test_5_delete_item()
