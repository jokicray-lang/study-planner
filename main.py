import os
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from tools import STUDY_BUDGET_TOOL, calculate_study_budget

# 1. 读取与 main.py 同一文件夹里的 .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

# 2. 获取配置
api_key = os.getenv("LLM_API_KEY")
base_url = os.getenv("LLM_BASE_URL")
model = os.getenv("LLM_MODEL")

if not all([api_key, base_url, model]):
    raise ValueError("请检查 .env：密钥、接口地址和模型名称都需要填写。")

# 3. 创建客户端，指定请求发送到你的中转站
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
    timeout=60.0,
    max_retries=0,
)

# 4. 获取用户的学习需求
goal = input("请输入学习目标、天数和每天的学习时间：").strip()

if not goal:
    print("学习需求不能为空，请重新运行。")
    raise SystemExit

# 5. 将用户需求和工具说明一起发给模型
print("正在识别学习时间……")

response = client.responses.create(
    model=model,
    instructions=(
        "你是一个学习规划助手。"
        "请根据用户明确提供的学习天数和每天的分钟数，"
        "调用 calculate_study_budget 工具。"
        "如果缺少时间信息，请询问用户，不要自行编造参数。"
    ),
    input=goal,
    tools=[STUDY_BUDGET_TOOL],
    store=False,
)

# 6. 查看模型是否提出了工具调用请求
found_tool_call = False

tool_outputs = []

for item in response.output:
    if item.type == "function_call":
        found_tool_call = True
        print("模型请求调用的工具：", item.name)
        print("模型提供的参数：", item.arguments)

        if item.name == "calculate_study_budget":
            arguments = json.loads(item.arguments)
            result = calculate_study_budget(
                days=arguments["days"],
                minutes_per_day=arguments["minutes_per_day"],
            )
            print("工具执行结果：", result)

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(result, ensure_ascii=False),
            })

if not found_tool_call:
    print("本次没有返回工具调用。")
    print("模型回复：", response.output_text)

# 7. 将工具结果传回模型，生成学习计划
if tool_outputs:
    # 按顺序整理用户需求、模型输出和工具结果
    input_items = [{"role": "user", "content": goal}]
    input_items.extend(response.output)
    input_items.extend(tool_outputs)

    print("正在生成学习计划……")

    final_response = client.responses.create(
        model=model,
        instructions=(
            "你是一个学习规划助手。"
            "根据用户的学习目标和工具返回的时间预算，"
            "用中文生成适合初学者的逐日学习计划。"
            "计划天数和每天的学习分钟数必须与工具结果一致。"
            "每天列出学习内容、具体操作和预计用时，"
            "每天各项任务的用时之和必须等于当天的时间预算。"
        ),
        input=input_items,
        store=False,
    )

    print("\n学习计划：")
    print(final_response.output_text)