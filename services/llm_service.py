import os

from utils.config import DEFAULT_LLM_MODEL, OPENAI_API_KEY_ENV


MOCK_PRODUCTS = {
    "낮음": [
        {
            "name": "라운드랩 자작나무 수분 선크림",
            "effect": "자외선 차단과 수분 보습",
            "uri": "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%EB%9D%BC%EC%9A%B4%EB%93%9C%EB%9E%A9%20%EC%9E%90%EC%9E%91%EB%82%98%EB%AC%B4%20%EC%84%A0%ED%81%AC%EB%A6%BC",
        },
        {
            "name": "아누아 어성초 77 수딩 토너",
            "effect": "진정과 가벼운 수분 공급",
            "uri": "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%EC%95%84%EB%88%84%EC%95%84%20%EC%96%B4%EC%84%B1%EC%B4%88%2077%20%EC%88%98%EB%94%A9%20%ED%86%A0%EB%84%88",
        },
    ],
    "보통": [
        {
            "name": "구달 청귤 비타C 잡티케어 세럼",
            "effect": "잡티 케어와 피부톤 관리",
            "uri": "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%EA%B5%AC%EB%8B%AC%20%EC%B2%AD%EA%B7%A4%20%EB%B9%84%ED%83%80C%20%EC%9E%A1%ED%8B%B0%EC%BC%80%EC%96%B4%20%EC%84%B8%EB%9F%BC",
        },
        {
            "name": "토리든 다이브인 저분자 히알루론산 세럼",
            "effect": "수분 보충과 장벽 보조",
            "uri": "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%ED%86%A0%EB%A6%AC%EB%93%A0%20%EB%8B%A4%EC%9D%B4%EB%B8%8C%EC%9D%B8%20%EC%84%B8%EB%9F%BC",
        },
    ],
    "높음": [
        {
            "name": "아이소이 잡티세럼",
            "effect": "색소침착 부위 집중 케어",
            "uri": "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%EC%95%84%EC%9D%B4%EC%86%8C%EC%9D%B4%20%EC%9E%A1%ED%8B%B0%EC%84%B8%EB%9F%BC",
        },
        {
            "name": "닥터지 그린 마일드 업 선 플러스",
            "effect": "민감 피부용 무기자차 자외선 차단",
            "uri": "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%EB%8B%A5%ED%84%B0%EC%A7%80%20%EA%B7%B8%EB%A6%B0%20%EB%A7%88%EC%9D%BC%EB%93%9C%20%EC%97%85%20%EC%84%A0",
        },
    ],
}


def generate_product_recommendations(cv_context):
    """
    현재는 LLM이 연결되지 않았으므로 고정 추천을 반환합니다.
    LLM 연결 시 이 함수 내부의 mock 분기만 실제 웹검색/LLM 호출로 교체하면 됩니다.
    """
    if os.getenv(OPENAI_API_KEY_ENV):
        return _generate_with_llm(cv_context)

    return MOCK_PRODUCTS.get(cv_context["level"]["label"], MOCK_PRODUCTS["보통"])


def _generate_with_llm(cv_context):
    client = _build_placeholder_client()
    if client is None:
        return MOCK_PRODUCTS.get(cv_context["level"]["label"], MOCK_PRODUCTS["보통"])

    # TODO: 웹검색 가능한 LLM 연결 후 name/effect/uri만 반환하도록 교체합니다.
    return MOCK_PRODUCTS.get(cv_context["level"]["label"], MOCK_PRODUCTS["보통"])


def _build_placeholder_client():
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        return None

    try:
        from openai import OpenAI

        os.getenv("OPENAI_MODEL", DEFAULT_LLM_MODEL)
        return OpenAI(api_key=api_key)
    except Exception:
        return None
