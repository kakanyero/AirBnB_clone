#!/usr/bin/python3
"""This module manages user details"""
from models.base_model import BaseModel


class User(BaseModel):
    """Inherits from BaseModel and manages user objects"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
