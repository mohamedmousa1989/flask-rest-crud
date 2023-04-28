import unittest
import datetime
from app.schemas import task_schema

class TestTaskSchema(unittest.TestCase):

    def test_task_schema_dump(self):
        data = {
            'id': 1,
            'title': 'Test Model',
            'description': 'Test description',
            'status': 'completed',
            'priority': 'low',
            'due_date': datetime.date(2023, 6, 3)
        }
        expected_data = {
            'id': 1,
            'title': 'Test Model',
            'description': 'Test description',
            'status': 'completed',
            'priority': 'low',
            'due_date': '2023-06-03'
        }
        result = task_schema.dump(data)
        self.assertEqual(result, expected_data)

    def test_task_schema_load(self):
        data = {
            'id': 1,
            'title': 'Test Model',
            'description': 'Test description',
            'status': 'completed',
            'priority': 'high',
            'due_date': '2023-06-03'
        }
        expected_data = {
            'id': 1,
            'title': 'Test Model',
            'description': 'Test description',
            'status': 'completed',
            'priority': 'high',
            'due_date': datetime.date(2023, 6, 3)
        }
        result = task_schema.load(data)
        self.assertEqual(result, expected_data)






