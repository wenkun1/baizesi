# main.py

from storage.init_db import init_database
from register.register_manager import RegisterManager
from session.session_manager import SessionManager
from workflow.workflow_engine import WorkflowEngine
from user.user_manager import UserManager

# 启动时初始化数据库

init_database()

# 初始化会话管理器和工作流引擎
session = SessionManager()


user_manager = UserManager()

user = user_manager.get_user_by_account(
    session.account_id
)

if not user:

    session.register_mode = True

    print("首次使用，请完成注册")

    print("AI: 请输入姓名")

else:

    session.user_id = user["id"]

engine = WorkflowEngine()

while True:

    text = input("用户：")

    # ===================
    # 注册流程
    # ===================
    if session.register_mode:

        if "user_name" not in session.register_slots:

            session.register_slots[
                "user_name"
            ] = text

        elif "department" not in session.register_slots:

            session.register_slots[
                "department"
            ] = text

        elif "employee_no" not in session.register_slots:

            session.register_slots[
                "employee_no"
            ] = text

        missing = RegisterManager.get_missing(
            session.register_slots
        )

        if missing:

            print(
                "AI:",
                RegisterManager.next_question(
                    session.register_slots
                )
            )

            continue

        user_id = user_manager.create_user(
        account_id=session.account_id,
        user_name=session.register_slots["user_name"],
        department=session.register_slots["department"],
        employee_no=session.register_slots["employee_no"]
        )

        session.user_id = user_id

        session.register_mode = False

        print(
        f"注册完成，用户ID：{user_id}"
        )

        print(
        "AI: 注册成功，请输入业务申请"
        )


        continue

    # ===================
    # 业务流程
    # ===================

    result = engine.process(
        session,
        text
    )

    print(
        "AI:",
        result["reply"]
    )