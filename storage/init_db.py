# storage/init_db.py

import pymysql

DB_CONFIG = {
"host": "localhost",
"port": 3306,
"user": "root",
"password": "cwk123",
"charset": "utf8mb4"
}

def init_database():

    # 连接MySQL（不指定数据库）
    conn = pymysql.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        charset=DB_CONFIG["charset"]
    )

    try:

        with conn.cursor() as cursor:

            # 创建数据库
            cursor.execute("""
            CREATE DATABASE IF NOT EXISTS baizesi
            DEFAULT CHARACTER SET utf8mb4
            COLLATE utf8mb4_general_ci
            """)

        conn.commit()

    finally:
        conn.close()

    # 连接到业务库
    conn = pymysql.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database="baizesi",
        charset=DB_CONFIG["charset"]
    )

    try:

        with conn.cursor() as cursor:
            
            # 用户表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_user
            (
                id BIGINT PRIMARY KEY AUTO_INCREMENT,

                account_id VARCHAR(100) NOT NULL UNIQUE COMMENT '账号唯一标识',

                employee_no VARCHAR(50) UNIQUE COMMENT '工号',

                user_name VARCHAR(50) NOT NULL COMMENT '姓名',

                department VARCHAR(100) COMMENT '部门',

                position_name VARCHAR(100) COMMENT '职位',

                phone VARCHAR(30),

                create_time DATETIME DEFAULT CURRENT_TIMESTAMP,

                update_time DATETIME DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP
            )
            """)
            
            # 订单表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_order
            (
                id BIGINT PRIMARY KEY AUTO_INCREMENT,

                user_id BIGINT NOT NULL,

                intent VARCHAR(50),

                slot_json JSON,

                create_time DATETIME DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT fk_order_user
                FOREIGN KEY(user_id)
                REFERENCES ai_user(id)
            )
            """)

            



        conn.commit()

        print("数据库初始化完成")

    finally:
        conn.close()
