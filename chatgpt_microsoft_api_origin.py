# coding:utf-8
#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import json
import openai
import pandas as pd
openai.api_type = "azure"
openai.api_base = "https://hmopenairesource.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = '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'
result = []

# test
question = "什么是不动产登记证明？"
content = question+'\n给出十种问法，要求语意相同'
response = openai.ChatCompletion.create(
  engine="test",
  messages = [{"role": "system", "content": "You are a helpful assistant."},
              # {"role": "user", "content": "下面是一道判断题，请判断是否正确"},
                                {"role": "user", "content": content}],
  # temperature=0.7,
  # temperature=0,
  # max_tokens=800,
  # n=3,
  top_p=0,
  timeout=3,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)
choices = response.get('choices', [])


xs = pd.read_excel('/Users/huoyun/Documents/VTE常见问题_微调.xlsx', keep_default_na=False, sheet_name=0)
for index, line in xs.iterrows():
    question = str(line['问题微调']).strip()
    content = question+'\n给出十种问法，要求语意相同'
    response = openai.ChatCompletion.create(
      engine="test",
      messages = [{"role": "system", "content": "You are a helpful assistant."},
                  # {"role": "user", "content": "下面是一道判断题，请判断是否正确"},
                                    {"role": "user", "content": content}],
      # temperature=0.7,
      # temperature=0,
      # max_tokens=800,
      # n=3,
      top_p=0,
      timeout=3,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None)
    choices = response.get('choices', [])
    for choice in choices:
        finish_reason = choice.get("finish_reason", '')
        if finish_reason == 'stop':
            answer = choice.get("message", {}).get("content", '')
            print(index, '-'*50)
            print(question)
            print(answer)
            result.append([index,question,answer])
    # print(json.dumps(response, indent=4, ensure_ascii=False))

print(len(result))
data_node = pd.DataFrame(result, columns=['index','question', 'answer'])
data_node.to_csv("output/need_review_question_data.csv", index=False)