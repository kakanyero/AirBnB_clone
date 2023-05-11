#!/usr/bin/python3
"""This modules is the base model"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """Defines all common attributes/methods for other classes"""
    def __init__(self, *args, **kwargs):
        """Initialize a new instance of the class"""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Return a string representation of the instance"""
        return "[{}] ({}) {}".
        format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Update the update datetime to the current time"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Return a dictionary represenation of the instance"""
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = type(self).__name__
        obj_dict['created_at'] = obj_dict['created_at'].isoformat()
        obj_dict['updated_at'] = obj_dict['updated_at'].isoformat()
        return obj_dict
