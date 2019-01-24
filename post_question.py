import pandas as pd
import os

def get_question_file():
    for folder, _, files in os.walk(os.path.join('.','question data')):
        return os.path.join(folder,files[0])

qfile = get_question_file()
print('Question file: {}'.format(qfile))

# read excel file
xf = pd.ExcelFile(qfile)

print('Question structure')
df_struct = pd.read_excel(xf, 'structure', index_col=0)
print(df_struct.head())

print('Questions')
df_questions = pd.read_excel(xf, 'questions', index_col=0)
print(df_questions.head())

## first post the questions, get the reference, update the exam 
questions = []
for index, row in df_questions.iterrows():
    choices = [x.strip() for x in row.loc['choices'].split(',')]
    question = {
        'question_text': row.loc['question_text'],
        'choices': choices,
        'answer': row.loc['answer'],
        'explanation': row.loc['explanation'],
    }
    questions.append(question)

question_set = {
    'title': df_struct.loc['title','value'],
    'description': df_struct.loc['description','value'],
    'questions': questions
}
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("firebase_service.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

qset_ref = db.collection(u'question_sets').document()
print('uploading question set')
qset_ref.set(question_set)
print('Question set uploaded!')

print('Exam structure')
examStruct = {
    'costing': df_struct.loc['costing','value'],
    'negative_mark': df_struct.loc['negative mark','value'],
    'unit_mark': df_struct.loc['unit mark','value'],
    'question_set': qset_ref
}
print(examStruct)

print('Exam reference')
exam_reference = df_struct.loc['exam reference','value']
print(exam_reference)

print('Updating exam...')
examUpdateRef = db.collection(u'exams').document(exam_reference).collection('question_sets').document()
examUpdateRef.set(examStruct)
print('Exam updated!')
