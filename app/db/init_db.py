from sqlmodel import SQLModel
from app.db.session import engine


"""创建数据表"""
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def cleanup_resources():
    pass





