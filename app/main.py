from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import SQLModel, Field, create_engine, Session, select
from contextlib import asynccontextmanager

from app import settings

# Database Table Schema

class Todo(SQLModel,table =True):
    id: int | None = Field(default=None, primary_key=True)
    title: str


# Connection to the database
connection_string: str =str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(connection_string)

def create_db_tables():
    print("create_db_tables")
    SQLModel.metadata.create_all(engine)
    print("done")

@asynccontextmanager
async def lifespan(todo_server:FastAPI):
    print("Server Startup")
    create_db_tables()
    yield

# Table Data Save, Get


todo_server: FastAPI = FastAPI(lifespan=lifespan)

def get_session():
    with Session(engine) as session:
        yield session

@todo_server.get("/")
def hello_world():
    return{"Greet": "Hello WOrld"}


@todo_server.post("/todo")
def create_todo(try_content: Todo, session: Annotated[Session, Depends(get_session)]):
        session.add(try_content)
        session.commit()
        session.refresh(try_content)
        return try_content

# Get All Todos Data

@todo_server.get("/todo")
def get_all_todos(new_concept: Annotated[Session, Depends(get_session)]):
    query = select(Todo)
    all_todos = new_concept.exec(query).all()
    return all_todos
