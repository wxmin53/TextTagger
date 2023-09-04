# coding:utf-8
# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
import json, time
import pandas as pd

# content = '''请问对于肺炎支原体性肺炎的患者，治疗上有哪些常用的药物，结果请以json格式输出，其中key是“具体”的药物通用名（如“阿莫西林”）而不是药物类别或者某一类药物，value是对应药物的治疗目的（如“抗菌”、“止吐”），治疗目的尽量简洁，生成的药品尽可能多。'''
openai.api_key = "26269f4546934fa6afdad7606a44030d"

ori_path = "/Users/wxm/work/datasets/clean_data/用户-FAQ测试结果对比2309011708.xlsx"
data = pd.read_excel(ori_path)

for _, row in data.iterrows():
    question = row["输入问句"]
    model_answer = row["模型结果"]
    yun_answer = row["云小蜜结果"]
    if model_answer == "NONE" or yun_answer == "":
        continue
    # content = "【指令】你是不动产领域的专家，请你在【模型答案】和【云小蜜答案】中选择出关于【问题】的最优的回答，返回json 格式，比如【模型答案】更优，那么只返回：'杭州办理不动产证需要携带户口本吗？': '模型答案'。【问题】{}。【模型答案】{}。【云小蜜答案】{}".format(question, model_answer, yun_answer)
    # content = content[:40]
    content = "你好"
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      # model="gpt-4",
      temperature=0,
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content}
        ]
    )
    print(response)
    choices = response.get('choices', [])
    if len(choices) > 0:
        finish_reason = choices[0].get("finish_reason", '')
        if finish_reason == 'stop':
            answer = choices[0].get("message",{}).get("content",'')
            print(answer)

pass