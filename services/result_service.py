from utils.config import SCORE_LEVELS


SKIN_TYPE_RULES = {
    "건성": {
        "ingredients": ["나이아신아마이드", "세라마이드", "히알루론산"],
        "note": "보습 장벽을 함께 보강하는 제품이 잘 맞아요.",
    },
    "지성": {
        "ingredients": ["나이아신아마이드", "비타민 C 유도체", "가벼운 젤 제형"],
        "note": "무겁지 않고 산뜻하게 마무리되는 제형이 좋아요.",
    },
    "복합성": {
        "ingredients": ["나이아신아마이드", "판테놀", "부위별 보습"],
        "note": "T존과 U존을 나누어 조절하는 구성이 좋아요.",
    },
    "민감성": {
        "ingredients": ["판테놀", "세라마이드", "징크옥사이드"],
        "note": "자극 가능성을 낮춘 진정 중심 제품이 잘 맞아요.",
    },
}


LEVEL_GUIDES = {
    "낮음": {
        "summary": "피부 톤이 비교적 안정적으로 보이는 편이에요. 지금은 큰 변화를 주기보다 자외선 차단과 수분 밸런스를 꾸준히 유지하는 쪽이 좋아 보여요.",
        "reason": "현재 단계에서는 강한 기능성 제품보다 매일 쓰기 편한 선케어와 진정 보습 제품을 우선 추천합니다.",
        "morning": "아침에는 가벼운 수분 제품을 바른 뒤 선크림을 충분히 발라 주세요.",
        "evening": "저녁에는 피부를 편안하게 진정시키고 보습 장벽을 채우는 루틴이 좋아요.",
        "caution": "피부 컨디션이 안정적일 때도 자외선 노출이 잦으면 톤 고민이 다시 올라올 수 있어요.",
    },
    "보통": {
        "summary": "피부 톤 케어를 시작하기 좋은 구간이에요. 수분 장벽을 지키면서 나이아신아마이드나 비타민 C 유도체처럼 톤 관리에 쓰이는 성분을 천천히 더해보면 좋아요.",
        "reason": "피부 부담을 줄이면서 톤 케어와 보습을 함께 챙길 수 있는 제품을 중심으로 추천했습니다.",
        "morning": "아침에는 선크림을 중심으로 루틴을 잡고, 피부가 편안한 날에는 산뜻한 톤 케어 제품을 함께 사용해 보세요.",
        "evening": "저녁에는 세안 후 보습 세럼이나 크림으로 피부 장벽을 먼저 안정시키는 구성이 좋아요.",
        "caution": "고농도 기능성 제품을 한 번에 여러 개 쓰면 자극이 생길 수 있으니 하나씩 추가하는 편이 안전해요.",
    },
    "높음": {
        "summary": "톤 고민 케어를 조금 더 우선해도 좋은 상태로 보여요. 다만 피부가 예민해지지 않도록 진정, 보습, 자외선 차단을 같이 가져가는 것이 중요해요.",
        "reason": "톤 관리 성분과 자외선 차단 제품을 함께 추천해, 낮에는 보호하고 밤에는 부담을 줄이는 케어 흐름을 만들었습니다.",
        "morning": "아침에는 자외선 차단제를 꼼꼼히 바르고, 외출 시간이 길다면 덧바르는 습관을 추천해요.",
        "evening": "저녁에는 톤 케어 세럼을 소량부터 사용하고, 보습 크림으로 마무리해 피부 부담을 줄여 주세요.",
        "caution": "갑자기 짙어진 반점, 통증, 출혈, 빠른 크기 변화가 있다면 화장품 케어보다 피부과 상담을 먼저 권장합니다.",
    },
}


SAFETY_NOTICE = (
    "이 결과는 의료 진단이 아니라 피부 케어 참고용 안내입니다. "
    "통증, 출혈, 급격한 변화, 심한 염증이 있다면 피부과 상담을 권장합니다."
)


def classify_score(score):
    for level in SCORE_LEVELS:
        if score <= level["max"]:
            return level
    return SCORE_LEVELS[-1]


def build_cv_context(cv_result, user_profile):
    score = float(cv_result["score"])
    skin_type = user_profile.get("skin_type", "건성")
    skin_rule = SKIN_TYPE_RULES.get(skin_type, SKIN_TYPE_RULES["건성"])
    level = classify_score(score)
    level_guide = LEVEL_GUIDES[level["label"]]

    return {
        "condition": cv_result.get("condition", "pigmentation"),
        "score": score,
        "level": level,
        "skin_type": skin_type,
        "concern": user_profile.get("concern", "색소침착"),
        "age_group": user_profile.get("age_group", "20대"),
        "priority_ingredients": skin_rule["ingredients"],
        "care_note": skin_rule["note"],
        "guide": level_guide,
        "safety_notice": SAFETY_NOTICE,
    }


def build_result(cv_result, user_profile, products):
    context = build_cv_context(cv_result, user_profile)
    return {
        **context,
        "products": products,
    }
