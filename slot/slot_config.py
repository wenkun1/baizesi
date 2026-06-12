# 意图槽位配置
INTENT_SLOTS = {

    # ========================
    # 请假申请
    # ========================
    "leave": [
        "leave_type",
        "start_date",
        "end_date",
        "days",
        "reason"
    ],

    # ========================
    # 加班申请
    # ========================
    "overtime": [
        "overtime_date",
        "start_time",
        "end_time",
        "reason"
    ],

    # ========================
    # 出差申请
    # ========================
    "business_trip": [
        "destination",
        "start_date",
        "end_date",
        "trip_purpose"
    ],

    # ========================
    # 报销申请
    # ========================
    "expense": [
        "expense_type",
        "amount",
        "expense_date",
        "reason"
    ],

    # ========================
    # 采购申请
    # ========================
    "purchase": [
        "item_name",
        "quantity",
        "budget",
        "supplier",
        "reason"
    ],

    # ========================
    # 会议室申请
    # ========================
    "meeting_room": [
        "meeting_topic",
        "meeting_date",
        "meeting_time",
        "meeting_room",
        "participants"
    ],

    # ========================
    # 用章申请
    # ========================
    "seal_apply": [
        "seal_type",
        "document_name",
        "document_count",
        "reason"
    ],

    # ========================
    # 权限申请
    # ========================
    "permission_apply": [
        "system_name",
        "permission_type",
        "reason"
    ],

    # ========================
    # 合同审批
    # ========================
    "contract_apply": [
        "contract_name",
        "contract_party",
        "contract_amount",
        "contract_period"
    ],

    # ========================
    # 付款申请
    # ========================
    "payment_apply": [
        "payee",
        "bank_name",
        "bank_account",
        "payment_amount",
        "payment_reason"
    ],

    # ========================
    # 资产领用
    # ========================
    "asset_apply": [
        "asset_name",
        "asset_quantity",
        "usage"
    ]
}