# 프롬프트를 간단히 작성하는 경우

def get_system_prompt(role="default"):
    prompts = {
        "default": {"role": "system", "content": "당신은 친절하고 유능한 AI 어시스턴트입니다."},
        "translator": {"role": "system", "content": "당신은 영어와 한국어를 잘 번역하는 전문가입니다."},
        "coder": {"role": "system", "content": "당신은 소프트웨어 개발자입니다. Python 코드를 작성합니다."}
    }
    return prompts.get(role, prompts["default"])

# 프롬프트가 복잡한 경우 json파일로 만들고 여기서 불러온 뒤 메인에서 합치는 방식

# import json

# def get_system_prompt(role="default"):
#     with open("prompts.json", "r", encoding="utf-8") as f:
#         prompts = json.load(f)
#     return prompts.get(role, prompts["default"])