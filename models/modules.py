#-------------------------------------------------------------------------------------------------------------------------
# Name:        modules
# Purpose:
#
# Author:      kkrishnav
#
# Created:     11/10/2018
# Copyright:   (c) kkrishnav 2018
# Licence:     <your licence>
# Sample JSON: {"module":"Module Name", "parent_module_id": null, "description": "Description", "creator_id": 1, "is_active": true}
#-------------------------------------------------------------------------------------------------------------------------
from root import db
from models.options import Options
from datetime import datetime

class Modules(db.Model):
    __tablename__ =  "modules"
    id = db.Column(db.Integer, primary_key=True)
    module = db.Column(db.String(50), nullable=False)
    parent_module_id = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(2000), nullable=True)
    creator_id = db.Column(db.Integer, nullable=False)    
    is_active = db.Column(db.Boolean, default=True)
    insert_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return '{"id":{0}, "module":{1}, "parent":{2}}, "creator_id": {3}'.format(self.id, self.module, self.parent_module_id, self.creator_id)

    @classmethod
    def get_all_modules(classname):
        modules_list = Modules.query.all()
        modules = [module.serialize() for module in modules_list]
        return modules

    @classmethod
    def get_modules_latest_count(classname, _count, id=None):
        if id == None:
            modules_list = Modules.query.order_by(classname.insert_date.desc()).limit(_count)
        else: 
            modules_list = Modules.query.filter_by(creator_id=id).order_by(classname.insert_date.desc()).limit(_count)
        modules = [module.serialize() for module in modules_list]
        return modules

    @classmethod
    def get_module_from_id(classname, id):
        module = classname.query.get(id)
        return module

    @classmethod
    def get_module_from_creator_id(classname, id):
        modules_list = classname.query.filter_by(creator_id=id)
        modules = [module.serialize() for module in modules_list]
        return modules

    @classmethod
    def delete_module_from_id(classname, id):
        module = classname.get_module_from_id(id)
        if module is None:
            return None
        db.session.delete(module)
        db.session.commit()
        return module

    @classmethod
    def submit_module_from_json(classname, json_module):        
        module = classname(module=json_module['module'],
            parent_module_id=json_module['parent_module_id'],
            description=json_module['description'],
            creator_id=json_module['creator_id'],
            is_active=json_module['is_active'])
        db.session.add(module)
        db.session.commit()
        return module

    #todo:json encoding needed
    def serialize(self):
        json_module = {
        'id' : self.id ,
        'module' : self.module,
        'parent_module_id' : self.parent_module_id,
        'description': self.description,
        'creator_id': self.creator_id,
        'is_active': self.is_active,
        'insert_date': str(self.insert_date),
        'update_date': str(self.update_date)
        }
        return json_module

    @staticmethod
    def validate_module(module):
        if ('module' in module):
            return True
        else:
            return False