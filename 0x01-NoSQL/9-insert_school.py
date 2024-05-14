#!/usr/bin/env python3
"""  inserts a new document in a collection based on kwargs """
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
        Args:
            pymongo collection
            kwargs: Dictionary with elements to put

        Return:
            Id of the new element
    """
    new_school = mongo_collection.insert_one(kwargs)

    return (new_school.inserted_id)
