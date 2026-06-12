# storage/db.py
import pymysql
import json

class DB:

    def __init__(self):

        self.conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="cwk123",
            database="baizesi",
            charset="utf8mb4"
        )

    def save_order(
            self,
            user_id,
            intent,
            slots
    ):

        sql = """
        insert into ai_order(
            user_id,
            intent,
            slot_json
        )
        values(%s,%s,%s)
        """

        with self.conn.cursor() as cursor:

            cursor.execute(
                sql,
                (
                    user_id,
                    intent,
                    json.dumps(
                        slots,
                        ensure_ascii=False
                    )
                )
            )

            self.conn.commit()