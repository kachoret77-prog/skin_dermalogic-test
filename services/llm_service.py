import json
import os
from pathlib import Path

from utils.config import DEFAULT_LLM_MODEL, GEMINI_API_KEY_ENV


ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


MOCK_PRODUCTS = {
    "낮음": [
        {
            "name": "라운드랩 자작나무 수분 선크림",
            "effect": "자외선 차단과 수분 보습",
            "reason": "피부 톤이 안정적인 편이라 매일 쓰기 좋은 수분 선케어를 우선 추천했어요.",
            "uri": "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%EB%9D%BC%EC%9A%B4%EB%93%9C%EB%9E%A9%20%EC%9E%90%EC%9E%91%EB%82%98%EB%AC%B4%20%EC%84%A0%ED%81%AC%EB%A6%BC",
        },
        {
            "name": "아누아 어성초 77 수딩 토너",
            "effect": "진정과 가벼운 수분 공급",
            "reason": "부담이 적은 진정 보습 루틴으로 피부 밸런스를 유지하기 좋아요.",
            "uri": "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%EC%95%84%EB%88%84%EC%95%84%20%EC%96%B4%EC%84%B1%EC%B4%88%2077%20%EC%88%98%EB%94%A9%20%ED%86%A0%EB%84%88",
        },
    ],
    "보통": [
        {
            "name": "구달 청귤 비타C 잡티케어 세럼",
            "effect": "잡티 케어와 피부톤 관리",
            "reason": "톤 케어가 필요한 구간이라 비타민 C 유도체 기반 제품을 추천했어요.",
            "uri": "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%EA%B5%AC%EB%8B%AC%20%EC%B2%AD%EA%B7%A4%20%EB%B9%84%ED%83%80C%20%EC%9E%A1%ED%8B%B0%EC%BC%80%EC%96%B4%20%EC%84%B8%EB%9F%BC",
        },
        {
            "name": "토리든 다이브인 저분자 히알루론산 세럼",
            "effect": "수분 보탬과 장벽 보조",
            "reason": "기능성 케어 전후로 피부 장벽을 편안하게 받쳐주기 좋아요.",
            "uri": "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%ED%86%A0%EB%A6%AC%EB%93%A0%20%EB%8B%A4%EC%9D%B4%EB%B8%8C%EC%9D%B8%20%EC%84%B8%EB%9F%BC",
        },
    ],
    "높음": [
        {
            "name": "아이소이 잡티세럼",
            "effect": "색소침착 부위 집중 케어",
            "reason": "톤 고민 케어를 조금 더 우선해도 좋은 단계라 집중 세럼을 추천했어요.",
            "uri": "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%EC%95%84%EC%9D%B4%EC%86%8C%EC%9D%B4%20%EC%9E%A1%ED%8B%B0%EC%84%B8%EB%9F%BC",
        },
        {
            "name": "닥터지 그린 마일드 업 선 플러스",
            "effect": "민감 피부에 맞춘 무기자차 자외선 차단",
            "reason": "자외선 차단을 강화하면서도 민감 피부 부담을 줄이는 방향에 잘 맞아요.",
            "uri": "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%EB%8B%A5%ED%84%B0%EC%A7%80%20%EA%B7%B8%EB%A6%B0%20%EB%A7%88%EC%9D%BC%EB%93%9C%20%EC%97%85%20%EC%84%A0",
        },
    ],
}


def generate_product_recommendations(cv_context):
    """
    API 키가 있으면 LLM 추천을 시도하고, 없거나 실패하면 고정 추천을 반환합니다.
    """
    _load_local_env()
    if os.getenv(GEMINI_API_KEY_ENV):
        return _generate_with_llm(cv_context)

    return MOCK_PRODUCTS.get(cv_context["level"]["label"], MOCK_PRODUCTS["보통"])


def _generate_with_llm(cv_context):
    prompt = _build_recommendation_prompt(cv_context)
    model_name = os.getenv("GEMINI_MODEL") or DEFAULT_LLM_MODEL

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=os.getenv(GEMINI_API_KEY_ENV))
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                response_mime_type="application/json",
            ),
        )
        content = response.text
        return _parse_llm_products(content)
    except Exception:
        return MOCK_PRODUCTS.get(cv_context["level"]["label"], MOCK_PRODUCTS["보통"])


def _build_recommendation_prompt(cv_context):
    ingredients = ", ".join(cv_context.get("priority_ingredients", []))
    return f"""
너는 한국어로 답하는 화장품 추천 보조자야.
의료 진단, 치료 보장, 과장 광고 표현은 쓰지 마.
아래 피부 분석 컨텍스트를 바탕으로 화장품 추천 2개를 JSON 배열로만 작성해줘.

피부 컨디션 단계: {cv_context["level"]["label"]}
피부 컨디션 점수: {cv_context["score"]}
피부 타입: {cv_context["skin_type"]}
주요 고민: {cv_context["concern"]}
연령대: {cv_context["age_group"]}
우선 고려 성분: {ingredients}
케어 참고 문구: {cv_context["care_note"]}

각 항목은 아래 키만 포함해줘.
- name: 화장품 이름
- effect: 기대 효과를 20자 안팎으로 간결하게 작성
- reason: 왜 추천했는지 한 문장으로 간결하게 작성
- uri: 상품 정보 URL. 실제 URL을 확신하기 어렵다면 올리브영 검색 URL 형태로 작성

JSON 이외의 설명은 쓰지 마.
"""


def _parse_llm_products(content):
    content = content.strip()
    if content.startswith("```"):
        content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    products = json.loads(content)
    if not isinstance(products, list):
        raise ValueError("LLM 추천 결과는 리스트여야 합니다.")

    parsed_products = []
    for product in products[:3]:
        parsed_products.append(
            {
                "name": str(product["name"]),
                "effect": str(product["effect"]),
                "reason": str(product["reason"]),
                "uri": str(product["uri"]),
            }
        )

    if not parsed_products:
        raise ValueError("LLM 추천 결과가 비어 있습니다.")

    return parsed_products


def _load_local_env():
    if not ENV_PATH.exists():
        return

    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value
