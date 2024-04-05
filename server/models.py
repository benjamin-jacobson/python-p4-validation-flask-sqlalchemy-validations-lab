from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_author_name(self,key,name):
        if not name:
            raise ValueError("Failed: all authors have a name.")
        author_name = db.session.query(Author.id).filter_by(name = name).first()
        if author_name is not None:
            raise ValueError("Authur name already used.")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self,key,phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Author phone numbers are exactly 10 digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('title')
    def validates_title(self,key,title):
        if not title:
            raise ValueError('Must have title')
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError("No clickbait found")
        return title

    @validates('content')
    def validates_content(self,key,content):
        if len(content) < 250:
            raise ValueError('Post content is at least 250 characters')
        return content

    @validates('summary')
    def validates_summary(self,key,summary):
        if len(summary) > 250:
            raise ValueError('summary content is less than 250 characters')
        return summary

    @validates('category')
    def validates_category(self,key,category):
        if category not in ['Fiction','Non-Fiction']:
            raise ValueError('category')
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
