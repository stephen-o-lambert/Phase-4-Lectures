from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
#Review: Serializer rules, validations
db = SQLAlchemy()
#There are many ways to include constraints in models
#db.CheckConstraint
#nullable = False
#unique = True
#@validates('')

class Production(db.Model, SerializerMixin):
    __tablename__ = 'productions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    director = db.Column(db.String)
    description = db.Column(db.String)
    ongoing = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    crew_members = db.relationship('CrewMember', backref='production')
        
    # serialize_rules = ('-crew_members.production',)
    #to exclude cast members 
    serialize_rules = ('-crew_members','-created_at','-updated_at',)
    #add a validation using @validates()

    @validates("title")
    def validate_title(self, key , value):
        if not value:
            raise ValueError("Title cannot be empty")
        return value

    def __repr__(self):
        return f'<Production Title:{self.title}, Genre:{self.genre}, Budget:{self.budget}, Image:{self.image}, Director:{self.director},ongoing:{self.ongoing}>'

class CrewMember(db.Model, SerializerMixin):
    __tablename__ = 'crew_members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    role = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    production_id = db.Column(db.Integer, db.ForeignKey('productions.id'))

    #to exclude production
    serialize_rules = ('-production',)
    
    # serialize_rules = ('-production.crew_members',)
    #add a validation using @validates()
    @validates('role')
    def validate_role(self, key, value):
        if not value:
            raise ValueError('Role Cannot be empty')
        return value
    
    def __repr__(self):
        return f'<Production Name:{self.name}, Role:{self.role}'
