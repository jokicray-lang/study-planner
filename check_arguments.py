import json

from tools import calculate_study_budget

# 模拟模型返回的工具参数，目前不请求模型
arguments_text = '{"days": 7, "minutes_per_day": 30}'

# 把 JSON 字符串解析为 Python 字典
arguments = json.loads(arguments_text)

print("解析前的类型：", type(arguments_text))
print("解析后的类型：", type(arguments))
print("解析后的内容：", arguments)

# 从字典取出参数，调用工具
result = calculate_study_budget(
    days=arguments["days"],
    minutes_per_day=arguments["minutes_per_day"],
)

print("工具执行结果：", result)