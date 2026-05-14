import streamlit as st
from PIL import Image

from services.cv_service import load_model, predict_pigmentation
from services.llm_service import generate_product_recommendations
from services.result_service import build_cv_context, build_result


st.set_page_config(
    page_title="DermaLogic",
    page_icon="D",
    layout="wide",
)


@st.cache_resource
def get_model():
    return load_model()


def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --primary: #0f766e;
            --primary-dark: #115e59;
            --accent: #f97316;
            --surface: #f8fafc;
            --line: #dbe4e6;
            --text: #172026;
        }
        .stApp {
            background: linear-gradient(180deg, #f6fbfa 0%, #ffffff 42%);
            color: var(--text);
        }
        .block-container {
            padding-top: 2.2rem;
            max-width: 1120px;
        }
        h1, h2, h3 {
            letter-spacing: 0;
        }
        h1 {
            color: var(--primary-dark);
            font-size: 2.3rem;
            margin-bottom: 0.25rem;
        }
        [data-testid="stSidebar"] {
            background: #edf7f5;
            border-right: 1px solid var(--line);
        }
        .stButton > button {
            width: 100%;
            border: 0;
            border-radius: 8px;
            background: var(--primary);
            color: white;
            font-weight: 700;
            padding: 0.72rem 1rem;
        }
        .stButton > button:hover {
            background: var(--primary-dark);
            color: white;
        }
        .result-box {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1rem;
            background: #ffffff;
            margin-bottom: 0.8rem;
        }
        .product-name {
            color: var(--primary-dark);
            font-size: 1.04rem;
            font-weight: 800;
            margin-bottom: 0.25rem;
        }
        .product-effect {
            margin-bottom: 0.45rem;
        }
        .small-muted {
            color: #5c6b70;
            font-size: 0.92rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    apply_theme()

    st.title("피부분석 및 화장품 추천서비스")
    st.caption("CV 모델로 색소침착 점수를 분석하고, 추천 모델이 필요한 상품 정보만 간결하게 제공합니다.")

    with st.sidebar:
        st.header("사용자 정보")
        skin_type = st.selectbox("피부 타입", ["건성", "지성", "복합성", "민감성"])
        concern = st.text_input("주요 고민", value="색소침착")
        age_group = st.selectbox("연령대", ["10대", "20대", "30대", "40대", "50대", "60대 이상"])

    uploaded_file = st.file_uploader(
        "피부 이미지를 업로드하세요",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file is None:
        st.info("이미지를 업로드하면 색소침착 점수와 추천 화장품을 확인할 수 있습니다.")
        return

    image = Image.open(uploaded_file).convert("RGB")
    user_profile = {
        "skin_type": skin_type,
        "concern": concern,
        "age_group": age_group,
    }

    left, right = st.columns([0.95, 1.05], gap="large")
    with left:
        st.image(image, caption="업로드 이미지", use_container_width=True)

    with right:
        if st.button("피부 분석하기"):
            run_analysis(image, user_profile)


def run_analysis(image, user_profile):
    try:
        model = get_model()
        with st.spinner("CV 모델로 색소침착 점수를 분석하는 중입니다."):
            cv_result = predict_pigmentation(model, image)

        cv_context = build_cv_context(cv_result, user_profile)
        products = generate_product_recommendations(cv_context)
        result = build_result(cv_result, user_profile, products)
        render_result(result)
    except FileNotFoundError as error:
        st.error(str(error))
    except Exception as error:
        st.error("분석 중 오류가 발생했습니다.")
        st.exception(error)


def render_result(result):
    level = result["level"]

    score_col, level_col = st.columns(2)
    score_col.metric("색소침착 점수", result["score"])
    level_col.metric("분석 단계", level["label"])

    st.markdown(
        f"""
        <div class="result-box">
            <strong>{level["tone"]}</strong><br>
            <span class="small-muted">{result["skin_type"]} 피부 기준: {result["care_note"]}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("추천 화장품")
    for product in result["products"]:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="product-name">{product["name"]}</div>
                <div class="product-effect">{product["effect"]}</div>
                <a href="{product["uri"]}" target="_blank">쇼핑몰 정보 보기</a>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
