import openai

# pip install openai

openai.api_key = "YOUR_API_KEY"

messages = [
  {"role": "system", "content": "당신은 친절하고 도움이 되는 AI 어시스턴트입니다."},
  {"role": "user", "content": "안녕하세요! 오늘 날씨가 어떤지 알려주실 수 있나요?"},
  {"role": "assistant", "content": "안녕하세요! 오늘은 대체로 맑고 포근한 날씨가 예상됩니다. 낮 최고기온은 22도까지 오르겠네요. 야외 활동하기 좋은 날씨에요. 계획 있으신가요?"},
  {"role": "user", "content": "딱히 계획은 없는데 이런 날 뭐하면 좋을까요?"}
]

completion = openai.ChatCompletion.create(
  model="gpt-4o", 
  messages=messages
)

assistant_reply = completion.choices[0].message.content
print(assistant_reply)

messages.append({"role": "assistant", "content": assistant_reply})
messages.append({"role": "user", "content": "와 완전 좋은 제안이네요. 그렇게 해야겠어요!"})

completion = openai.ChatCompletion.create(
  model="gpt-4o", 
  messages=messages
)

print(completion.choices[0].message.content)
