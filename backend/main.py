from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String,DateTime,Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
# import requests

Base = declarative_base()


app = Flask(__name__)

#  Tables
class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    created_at = Column(DateTime, default=datetime.now)
    status = Column(Integer,default=0)

    def __init__(self,name):
        self.name = name
        # self.created_at = created_at
        # self.status = status

    def __repr__(self):
        return f"{self.id} {self.name} {self.created_at} {self.status}"

engine = create_engine('sqlite:///todo.db', echo = True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine) 
session = Session()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/todo", methods=['POST', 'GET'])
def create_task():
    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        # created_at = data['created_at']
        status = data['status']

        task = Tasks(name=name, status=status)
        # , created_at=created_at, status=status
        session.add(task)
        session.commit()

        response_body = {"id": task.id, "name":task.name,"status":task.status }
        # "created_at":task.created_at, "status":task.status

        return jsonify(response_body),201

    else:

        tasks = session.query(Tasks).all()
        response_body=[]
        for task in tasks:
            response_body.append({"id": task.id, "name":task.name, "created_at":task.created_at, "status":task.status})
            # 
        return jsonify(response_body),200

        








if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
