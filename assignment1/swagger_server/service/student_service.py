import os
import tempfile
from functools import reduce
from pymongo import MongoClient

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
client = MongoClient(MONGODB_HOST, MONGODB_PORT)
dbname = client['tutorial1']
collection_name = dbname['student_db']

def add(student=None):
    query = { 'first_name': student.first_name, 'last_name': student.last_name }
    res = collection_name.find_one(query)
    if res != None:
        return 'already exists', 409

    doc_id = collection_name.insert_one(student.to_dict())
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = collection_name.find_one({ 'student_id': student_id})
    if not student:
        return 'not found', 404
    return parse_student(student)

def delete(student_id=None):
    student = collection_name.find({ 'student_id': student_id})
    if not student:
        return 'not found', 404
    collection_name.delete_many({ 'student_id': student_id})
    return student_id

def parse_student(student_doc):
    student = {
        'first_name': student_doc['first_name'],
        'gradeRecords': student_doc['grade_records'],
        'last_name': student_doc['last_name'],
        'student_id': student_doc['student_id']
    }
    return student