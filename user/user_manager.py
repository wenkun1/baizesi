
import pymysql
class UserManager:
    def __init__(self):

        self.conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="cwk123",
            database="baizesi",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

    def get_user_by_account(
            self,
            account_id
    ):

        sql = """
        select *
        from ai_user
        where account_id=%s
        """

        with self.conn.cursor() as cursor:

            cursor.execute(
                sql,
                (account_id,)
            )

            return cursor.fetchone()


    def create_user(
            self,
            account_id,
            user_name,
            department,
            employee_no
    ):

        sql = """
        insert into ai_user(
            account_id,
            user_name,
            department,
            employee_no
        )
        values(%s,%s,%s,%s)
        """

        with self.conn.cursor() as cursor:

            cursor.execute(
                sql,
                (
                    account_id,
                    user_name,
                    department,
                    employee_no
                )
            )

            self.conn.commit()

            return cursor.lastrowid

    def register_if_not_exists(
            self,
            account_id
    ):
        user = self.get_user_by_account(account_id)

        if not user:

            return self.create_user(
                account_id,
                "",
                "",
                ""
            )
        return user





