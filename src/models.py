from datetime import datetime
from tkinter import CASCADE
from flask_mongoengine import MongoEngine
from mongoengine import fields
import json

db = MongoEngine()

class Post(db.Document):
    idOriginalPost = fields.ObjectIdField( default= None)
    createdDate = db.DateTimeField(default=datetime.now)
    updatedDate= db.DateTimeField(default=datetime.now)
    ownerId = db.IntField(required=True)
    location = db.StringField(default=None)
    description = db.StringField(required=True)
    comment = db.ListField(fields.ReferenceField('Comment'), default=None, reverse_delete_rule=CASCADE)
    reaction = db.ListField(fields.ReferenceField('Reaction'), default=None, reverse_delete_rule=CASCADE)
    report = db.ListField(fields.ReferenceField('Report'), default=None, reverse_delete_rule=CASCADE)
    contentElement = db.ListField(fields.ReferenceField('ContentElement'), default=None, reverse_delete_rule=CASCADE)

    def to_json(self):
        return str(json.dumps({
            "id_str": (self.id).__str__(),
            "createdDate": self.createdDate.__str__(),
            "updatedDate": self.updatedDate.__str__(),
            "ownerId": self.ownerId,
            "location": self.location,
            "description": self.description,
        }))


class Comment(db.Document):
    postId = fields.ReferenceField('Post', reverse_delete_rule=CASCADE, required=True)
    ownerId = db.IntField()
    createdDate = db.DateTimeField(default=datetime.now)
    updatedDate= db.DateTimeField(default=datetime.now)
    description = db.StringField()
    reaction = db.ListField(fields.ReferenceField('Reaction'), default=None, reverse_delete_rule=CASCADE)
    report = db.ListField(fields.ReferenceField('Report'), default=None, reverse_delete_rule=CASCADE)
    contentElement = db.ListField(fields.ReferenceField('ContentElement'), default=None, reverse_delete_rule=CASCADE)

    def to_json(self):
        return str(json.dumps({
            "id_str": self.id.__str__(),
            "postId": (self.postId.id).__str__(),
            "ownerId": self.ownerId,
            "description": self.description,
            "createdDate": self.createdDate.__str__(),
            "updatedDate": self.updatedDate.__str__()
        }))



class Report(db.Document):
    postId = fields.ReferenceField('Post', reverse_delete_rule=CASCADE, required=False)
    commentId = fields.ReferenceField('Comment', reverse_delete_rule=CASCADE, required=False)
    ownerId = db.IntField(required=True)
    cretedDate = db.DateTimeField(default=datetime.now, required=True)
    updateDate = db.DateTimeField(default=datetime.now, required=True)
    infraction = db.StringField()
    description = db.StringField()

class ContentElement(db.Document):
    postId = fields.ReferenceField('Post', reverse_delete_rule=CASCADE, required=False)
    commentId = fields.ReferenceField('Comment', reverse_delete_rule=CASCADE, required=False)
    description = db.StringField()
    mediaLocator = db.StringField()
    mediaType = db.StringField()


class Reaction(db.Document):
    postId = fields.ReferenceField('Post', reverse_delete_rule=CASCADE, required=False)
    commentId = fields.ReferenceField('Comment', reverse_delete_rule=CASCADE, required=False)
    ownerId = db.IntField()
    type = db.StringField()
    createdDate = db.DateTimeField(default=datetime.now)
    updatedDate = db.DateTimeField(default=datetime.now)



