STUDY_BUDGET_TOOL = {
    "type": "function",
    "name": "calculate_study_budget",
    "description": "根据学习天数和每天的学习分钟数，计算总学习时间。两个参数都必须是正整数。",
    "parameters": {
        "type": "object",
        "properties": {
            "days": {
                "type": "integer",
                "description": "计划学习的天数，例如 7",
            },
            "minutes_per_day": {
                "type": "integer",
                "description": "每天学习的分钟数，例如 30",
            },
        },
        "required": ["days", "minutes_per_day"],
        "additionalProperties": False,
    },
}

def calculate_study_budget(days: int, minutes_per_day: int) -> dict:
    """根据学习天数和每天的分钟数，计算总学习时间。"""

    # 先检查类型
    if type(days) is not int:
        raise TypeError("days 必须是整数")

    if type(minutes_per_day) is not int:
        raise TypeError("minutes_per_day 必须是整数")

    # 再检查数值
    if days <= 0 or minutes_per_day <= 0:
        raise ValueError("天数和每天的学习分钟数必须大于 0")

    total_minutes = days * minutes_per_day

    return {
        "days": days,
        "minutes_per_day": minutes_per_day,
        "total_minutes": total_minutes,
        "total_hours": total_minutes / 60,
    }


if __name__ == "__main__":
    cases = [
        (5, 40),
        (7, 30),
        (0, 30),
        (5, -10),
        ("5", 40),
        (5, 40.5),
        (True, 40),
        (5, False),
    ]

    for days, minutes_per_day in cases:
        try:
            result = calculate_study_budget(days, minutes_per_day)
            print(f"参数：{days!r}, {minutes_per_day!r} → {result}")
        except (TypeError, ValueError) as error:
            print(
                f"参数：{days!r}, {minutes_per_day!r} → "
                f"{type(error).__name__}: {error}"
            )