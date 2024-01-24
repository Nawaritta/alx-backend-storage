#!/usr/bin/env python3
"""This module contains list_all function"""


def list_all(mongo_collection):
    """returns all documents in a collection """
    documents = mongo_collection.find()
    return documents
