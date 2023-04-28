import json
import unittest
import datetime
from app import app, db
from app.models import Task
from app.utils import configure_resources_routing


class TestTaskAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # code to run once before any tests in this class
        configure_resources_routing()

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_tasks(self):
        # Creating tasks in database
        task_1 = {
            'title': 'test title',
            'description': 'test description',
            'priority': 'high',
            'status': 'in progress',
            'due_date': datetime.datetime(2024, 4, 12)
        }
        task_2 = {
            'title': 'test title 2',
            'description': 'test description 2',
            'priority': 'high',
            'status': 'in progress',
            'due_date': datetime.datetime(2024, 4, 18)
        }
        db.session.add(Task(**task_1))
        db.session.add(Task(**task_2))
        db.session.commit()

        response = self.app.get('/tasks')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['title'], 'test title')
        self.assertEqual(response_data[1]['title'], 'test title 2')

    def test_get_tasks__filter_priority(self):
        # Creating tasks in database
        task_1 = {
            'title': 'test title',
            'description': 'test description',
            'priority': 'high',
            'status': 'in progress',
            'due_date': datetime.datetime(2024, 4, 12)
        }
        task_2 = {
            'title': 'test title 2',
            'description': 'test description 2',
            'priority': 'low',
            'status': 'in progress',
            'due_date': datetime.datetime(2024, 4, 18)
        }
        db.session.add(Task(**task_1))
        db.session.add(Task(**task_2))
        db.session.commit()

        response = self.app.get('/tasks?priority=high')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['priority'], 'high')

    def test_get_tasks__filter_status(self):
        # Creating tasks in database
        task_1 = {
            'title': 'test title',
            'description': 'test description',
            'priority': 'high',
            'status': 'in progress',
            'due_date': datetime.datetime(2024, 4, 12)
        }
        task_2 = {
            'title': 'test title 2',
            'description': 'test description 2',
            'priority': 'low',
            'status': 'completed',
            'due_date': datetime.datetime(2024, 4, 18)
        }
        db.session.add(Task(**task_1))
        db.session.add(Task(**task_2))
        db.session.commit()

        response = self.app.get('/tasks?status=in%20progress')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['status'], 'in progress')

    def test_create_task(self):
        data = {
            'title': 'test title',
            'description': 'test description',
            'status': 'completed',
            'priority': 'high',
            'due_date': '2024-4-3'
        }
        response = self.app.post('/tasks', json=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.query.count(), 1)
        self.assertEqual(Task.query.first().title, 'test title')
        self.assertEqual(Task.query.first().priority, 'high')
    
    def test_create_task__missing_data(self):
        data = { # 'title' is missing here
            'description': 'test description',
            'status': 'completed',
            'priority': 'high',
            'due_date': '2024-4-3'
        }
        response = self.app.post('/tasks', json=data)
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response_data, {'title': ['Missing data for required field.']})

    def test_create_task__wrong_status_value(self):
        data = { 
            'title': 'test title',
            'description': 'test description',
            'status': 'wrong value',
            'priority': 'high',
            'due_date': '2024-4-3'
        }
        response = self.app.post('/tasks', json=data)
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response_data, {'status': ['Must be one of: not started, in progress, completed.']})

    def test_create_task__wrong_priority_value(self):
        data = { 
            'title': 'test title',
            'description': 'test description',
            'status': 'in progress',
            'priority': 'wrong value',
            'due_date': '2024-4-3'
        }
        response = self.app.post('/tasks', json=data)
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response_data, {'priority': ['Must be one of: low, medium, high.']})   

    def test_get_task_by_id(self):
        task_1 = {
            'id': 1,
            'title': 'test title',
            'description': 'test description',
            'priority': 'high',
            'status': 'in progress',
            'due_date': datetime.datetime(2024, 4, 12)
        }
        db.session.add(Task(**task_1))
        db.session.commit()

        response = self.app.get('/tasks/1')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['id'], 1)
        self.assertEqual(response_data['title'], 'test title')

    def test_update_task(self):
        test_data = {
            'id': 1,
            'title': 'test title',
            'description': 'test description',
            'priority': 'medium',
            'status': 'in progress',
            'due_date': datetime.datetime(2024, 4, 12)
        }
        updated_data = {
            'title': 'test title 2',
            'description': 'test description 2',
            'priority': 'high',
            'status': 'completed',
            'due_date': '2024-4-18'
        }
        task_1 = Task(**test_data)
        db.session.add(task_1)
        db.session.commit()

        response = self.app.put('/tasks/1', json=updated_data)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['title'], 'test title 2')
        self.assertEqual(response_data['priority'], 'high')
        self.assertEqual(Task.query.get(1).status, 'completed')
        self.assertEqual(Task.query.get(1).due_date, datetime.date(2024, 4, 18))

    def test_delete_task(self):
        test_data = {
            'id': 1,
            'title': 'test title',
            'description': 'test description',
            'priority': 'medium',
            'status': 'in progress',
            'due_date': datetime.datetime(2024, 4, 12)
        }
        task_1 = Task(**test_data)
        db.session.add(task_1)
        db.session.commit()

        self.assertEqual(Task.query.count(), 1)
        response = self.app.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.query.count(), 0)
