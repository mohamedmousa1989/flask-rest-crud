from app import db


class Task(db.Model):
    
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    status = db.Column(db.String(20))
    priority = db.Column(db.String(8))
    due_date = db.Column(db.Date)

    def __repr__(self):
        return "<Task: {}>".format(self.title)


db.create_all()
