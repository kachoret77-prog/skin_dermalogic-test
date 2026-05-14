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


def classify_score(score):
    for level in SCORE_LEVELS:
        if score <= level["max"]:
            return level
    return SCORE_LEVELS[-1]


def build_cv_context(cv_result, user_profile):
    score = float(cv_result["score"])
    skin_type = user_profile.get("skin_type", "건성")
    skin_rule = SKIN_TYPE_RULES.get(skin_type, SKIN_TYPE_RULES["건성"])

    return {
        "condition": cv_result.get("condition", "pigmentation"),
        "score": score,
        "level": classify_score(score),
        "skin_type": skin_type,
        "concern": user_profile.get("concern", "색소침착"),
        "age_group": user_profile.get("age_group", "20대"),
        "priority_ingredients": skin_rule["ingredients"],
        "care_note": skin_rule["note"],
    }


def build_result(cv_result, user_profile, products):
    context = build_cv_context(cv_result, user_profile)
    return {
        **context,
        "products": products,
    }
