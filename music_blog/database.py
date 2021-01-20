from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr


class BaseModel(Model):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        attr = getattr(self, '__repr_attr__', 'id')
        value = getattr(self, attr, 'unknown')
        return f'<{self.__class__.__name__} {value}>'


db = SQLAlchemy(model_class=BaseModel)
