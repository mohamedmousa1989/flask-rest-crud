from app import app, api
from app.resources import TaskListCreate, TaskGetUpdateDelete

def configure_resources_routing():
    api.add_resource(TaskListCreate, '/tasks')
    api.add_resource(TaskGetUpdateDelete, '/tasks/<int:task_id>')