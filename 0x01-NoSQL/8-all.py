#!/usr/bin/env python3
""" lists all documents in a collection """
import pymongo


def list_all(mongo_collection) -> list:
    """ Lists all documents in a collection
        Args:
            mongo_collection: pymongo collection of object

        Return:
            A list with documents, otherwise []
    """
    documents: list = []

    for document in mongo_collection.find():
        documents.append(document)

    return documents
