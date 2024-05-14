#!/usr/bin/env python3
""" returns all students sorted by average score  """
import pymongo


def top_students(mongo_collection):
    """
        Args:
            mongo_collection: Collection to find avg top

        Return:
            List all top students
    """
    top_students = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return top_students
