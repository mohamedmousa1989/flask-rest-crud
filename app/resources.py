import json
from flask import jsonify, request, Response
from flask_restful import Resource, abort
from app import api, db
from app.models import Task
from app.schemas import task_schema, tasks_schema
from marshmallow import ValidationError

class TaskListCreate(Resource):
    def get(self):
        if request.args:
            if request.args.get('status'):
                tasks = Task.query.filter_by(status=request.args.get('status').strip())
            elif request.args.get('priority'):
                tasks = Task.query.filter_by(priority=request.args.get('priority').strip())
            else:
                tasks = []
        else:
            tasks = Task.query.order_by(Task.id).all()

        return tasks_schema.dump(tasks)

    def post(self):
        try:
            task_data = task_schema.load(request.json)
            task = Task(**task_data)
        except ValidationError as err:
            return err.messages, 422

        db.session.add(task)
        db.session.commit()

        return task_schema.dump(task), 201


class TaskGetUpdateDelete(Resource):
    def get(self, task_id):
        task = Task.query.get(int(task_id))
        if not task:
            abort(404, message='Task not found')

        return task_schema.dump(task)

    def put(self, task_id):
        task = Task.query.get(int(task_id))
        if not task:
            abort(404, message='Task not found')

        try:
            task_data = task_schema.load(request.json)
        except ValidationError as err:
            return err.messages, 422

        task.title = task_data['title']
        task.description = task_data['description']
        task.priority = task_data['priority']
        task.status = task_data['status']
        task.due_date = task_data['due_date']
        
        db.session.commit()

        return task_schema.dump(task)

    def delete(self, task_id):
        task = Task.query.get(int(task_id))
        if not task:
            abort(404, message='Task not found')

        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Task deleted successfully'})
