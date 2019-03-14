#-------------------------------------------------------------------------------
# Name:        options
# Purpose:
#
# Author:      kkrishnav
#
# Created:     11/10/2018
# Copyright:   (c) kkrishnav 2018
# Licence:     <your licence>
# Sample JSON: {"option":"Option 2","question_id":1,"is_correct_option":0}
#-------------------------------------------------------------------------------
from root import db
from datetime import datetime

class Options(db.Model):
    __tablename__ =  "options"
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String(200), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    is_correct_option = db.Column(db.Integer, nullable=False, default=0)
    insert_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


    def __rept__(self):
        return "'id': {0}, 'option': {1}, 'question_id': {2}".format(self.id, self.option, self.question_id)
        
    @classmethod
    def get_all_options(classname):
        return [option.serialize() for option in classname.query.all()]

    @classmethod
    def get_options_from_qid(classname, question_id):
        options = classname.query.filter_by(question_id=question_id)
        return options

    @classmethod
    def submit_options_from_json(classname, json_options, question_id):
        for json_option in json_options:
            option = Options(option=json_option['option'], question_id=question_id,
                       is_correct_option=json_option['is_correct_option'] )
            db.session.add(option)
        db.session.commit()


    @classmethod
    def delete_options_from_qid(classname, question_id):
        options = classname.get_options_from_qid(question_id)
        if options is None:
            return None

        for option in options:
            db.session.delete(option)
        db.session.commit()
        return options

    def serialize(self):
        json_option = {
            'id' : self.id,
            'option' : self.option,
            'question_id' : self.question_id,
            'is_correct_option' : self.is_correct_option,
            'insert_date': str(self.insert_date),
            'update_date': str(self.update_date)
        }
        return json_option

    #todo:json encoding needed
    @staticmethod
    def serialize_all(options):
        return [option.serialize() for option in options]

    @staticmethod
    def validate_option(option):
        if ('id' in option and 'option' in option and 'question_id' in option and 'is_correct_option' in option):
            return True
        else:
            return False