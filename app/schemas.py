from marshmallow import Schema, fields, validate


class TaskSchema(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    description = fields.String(required=True)
    status = fields.String(required=True, validate=validate.OneOf(['not started', 'in progress', 'completed']))
    priority = fields.String(required=True, validate=validate.OneOf(['low', 'medium', 'high']))
    due_date = fields.Date(required=True)

    class Meta:
        ordered = True


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)