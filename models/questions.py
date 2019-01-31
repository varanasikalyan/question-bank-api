#-------------------------------------------------------------------------------
# Name:        questions
# Purpose:
#
# Author:      kkrishnav
#
# Created:     11/10/2018
# Copyright:   (c) kkrishnav 2018
# Licence:     <your licence>
# Sample JSON: {"question":"Question 1","options":[{"option":"Option 1","question_id":1,"is_correct_option":1}]}
#-------------------------------------------------------------------------------
from root import db
from models.options import Options

class Questions(db.Model):
    __tablename__ =  "questions"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(2000), nullable=False)
    options = db.relationship('Options', backref='enquiry', lazy=True)

    def __repr__(self):
        return '{"id":{0}, "question":{1}}'.format(self.id, self.question)

    @classmethod
    def get_all_questions(classname):
        questions_list = Questions.query.all()
        questions = [question.serialize() for question in questions_list]
        return questions

    @classmethod
    def get_question_from_id(classname, id):
        question = classname.query.get(id)
        return question

    @classmethod
    def delete_question_from_id(classname, id):
        question = classname.get_question_from_id(id)
        if question is None:
            return None
        #first delete the options
        #TODO: currently the deletions of options and question is not atmoic
        options = Options.delete_options_from_qid(id)
        db.session.delete(question)
        db.session.commit()
        return question

    @classmethod
    def submit_question_from_json(classname, json_question):
        question = classname(question=json_question['question'])
        db.session.add(question)
        db.session.commit()
        #todo: make options and question creation atomic
        Options.submit_options_from_json(json_question['options'], question.id)
        return question

    #todo:json encoding needed
    def serialize(self):
        json_question = {
        'id' : self.id ,
        'question' : self.question,
        'options' : Options.serialize_all(self.options)
        }
        return json_question

    @staticmethod
    def validate_question(question):
        if ('question' in question):
            return True
        else:
            return False