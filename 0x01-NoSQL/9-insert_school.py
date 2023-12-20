#!/usr/bin/env python3
"""
Module to interact with MongoDB collections.
"""

from pymongo.collection import Collection


def insert_school(mongo_collection: Collection, **kwargs) -> str:
    """
    Inserts a new document into a MongoDB collection based on keyword
    arguments.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB
        collection object.
        **kwargs: Arbitrary keyword arguments representing document fields.

    Returns:
        str: The new _id of the inserted document.
    """
    inserted_document = mongo_collection.insert_one(kwargs)
    return str(inserted_document.inserted_id)
