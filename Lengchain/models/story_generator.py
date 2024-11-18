from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
from typing import Dict

# pip install langchain openai

# ---- 환경 변수 로드 ----
load_dotenv()

# OpenAI API 키 설정
openai_api_key = os.getenv("OPENAI_API_KEY")

# ---- 설정 ----
PROMPT_FILE_PATH = "storyprompts/love.txt"
DEFAULT_AFFECTION = 50

# 게임 상태를 서버 내에서 관리하기 위한 변수 (세션 상태처럼)
user_game_state = {}


# ---- LangChain 기반 설정 ----
# LangChain을 사용하여 OpenAI 모델 정의
llm = OpenAI(
    openai_api_key=openai_api_key,
    model="gpt-4",
    temperature=0.7,
    max_tokens=300,
)

# ---- Prompt 템플릿 ----
# 스토리 시작용 프롬프트 템플릿
start_game_prompt_template = PromptTemplate(
    input_variables=["genre"],
    template=(
        "이 이야기는 {genre} 장르로 시작됩니다. "
        "당신은 도심 속 작은 카페에서 일하는 바리스타입니다. "
        "오늘은 우연히 매일 오던 단골손님, 민재와 눈이 마주칩니다. "
        "민재는 항상 밝은 표정을 지니고 있어 마음이 끌립니다. "
        "이 이야기를 시작하세요."
    ),
)

# 스토리 생성용 프롬프트 템플릿
generate_story_prompt_template = PromptTemplate(
    input_variables=["user_input", "affection"],
    template=(
        "이전 컷에서 사용자는 다음과 같은 선택을 했습니다: '{user_input}'.\n"
        "다음 이야기를 이어서 만들어주세요. 호감도는 {affection}입니다. "
        "사용자가 선택할 수 있는 옵션을 추가하여 이야기를 이어가세요. "
        "선택지는 자연스럽게 이어지도록 하며 2~3개로 작성해주세요."
    ),
)

# ---- LangChain 체인 ----
start_game_chain = LLMChain(llm=llm, prompt=start_game_prompt_template)
generate_story_chain = LLMChain(llm=llm, prompt=generate_story_prompt_template)


# ---- 게임 시작 로직 ----
async def start_game(genre: str) -> Dict:
    try:
        # LangChain을 사용하여 초기 스토리 생성
        initial_story = start_game_chain.run(genre=genre)

        # 초기 게임 상태 설정
        user_game_state["cut"] = 1
        user_game_state["affection"] = DEFAULT_AFFECTION

        return {
            "story": initial_story.strip(),
            "affection": DEFAULT_AFFECTION,
            "step": 1,
        }
    except Exception as e:
        raise Exception(f"Error starting game: {e}")


# ---- 스토리 생성 로직 ----
async def generate_story(user_input: str) -> Dict:
    try:
        # 게임 상태 확인
        cut = user_game_state.get("cut", 1)
        affection = user_game_state.get("affection", DEFAULT_AFFECTION)

        # 게임 종료 처리
        if cut == 11:
            ending = (
                "축하합니다! 당신은 연인이 되었습니다!"
                if affection >= 80
                else "아쉽지만, 연애에 실패했습니다. 다음 기회를 노려보세요."
            )
            return {"story": ending, "affection": affection, "cut": cut}

        # LangChain을 사용하여 스토리 생성
        story = generate_story_chain.run(
            user_input=user_input,
            affection=affection,
        )

        # 호감도 업데이트
        if "친절" in story:
            affection += 10
        elif "불친절" in story:
            affection -= 5

        # 호감도 제한
        affection = max(0, min(100, affection))

        # 게임 상태 갱신
        user_game_state["cut"] = cut + 1
        user_game_state["affection"] = affection

        return {
            "story": story.strip(),
            "affection": affection,
            "cut": cut + 1,
        }

    except Exception as e:
        raise Exception(f"Error generating story: {e}")

