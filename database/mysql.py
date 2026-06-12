from sqlalchemy import create_engine

engine = create_engine(

    "mysql+pymysql://root:cwk123@localhost:3306/baizesi",

    pool_recycle=3600,

    echo=False
)