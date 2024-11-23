from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Relationship to documents and questions
    documents = relationship("Document", back_populates="user")
    questions = relationship("Question", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String, nullable=False)
    meta_info = Column(Text)

    # Relationship to user and questions
    user = relationship("User", back_populates="documents")
    questions = relationship("Question", back_populates="document")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    document_id = Column(Integer, ForeignKey("documents.id"))
    question = Column(Text)
    answer = Column(Text)

    # Relationships to user and document
    user = relationship("User", back_populates="questions")
    document = relationship("Document", back_populates="questions")
