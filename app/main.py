from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session
from contextlib import asynccontextmanager

from app import settings

class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str

conn_str: str = str(settings.DATABASE_URL).replace( 
"postgresql", "postgresql+psycopg"
)

engine = create_engine(conn_str)

def create_db_tables():
    print("create_db_tables")
    SQLModel.metadata.create_all(engine)
    print("done")

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Server Startup")
    create_db_tables()
    yield

app: FastAPI = FastAPI(lifespan=lifespan)


@app.get("/")
def hello():
    return {"Hello": "World"}

@app.get("/db")
def db_var():
    return {"DB":settings.DATABASE_URL, "Connection": conn_str}

@app.post("/todo")
def create_todo(todo_data: Todo):
    with Session(engine) as session:
        session.add(todo_data)
        session.commit()
        session.refresh(todo_data)
        return todo_data