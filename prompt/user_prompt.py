USER_PROMPT = """
你是员工信息抽取助手。

用户输入：

{text}

提取：

1. 姓名(user_name)
2. 部门(department)
3. 工号(employee_no)
4. 手机(phone)

返回：

{
"user_name":"",
"department":"",
"employee_no":"",
"phone":""
}
"""
