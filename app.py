import streamlit as st
from PIL import Image

from services.cv_service import load_model, predict_pigmentation
from services.llm_service import generate_product_recommendations
from services.result_service import build_cv_context, build_result


SERVICE_NAME = "GlowPick"
SERVICE_TAGLINE = "사진 한 장으로 확인하는 피부 컨디션과 맞춤 케어"


st.set_page_config(
    page_title=SERVICE_NAME,
    page_icon="G",
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
            --mint: #14b8a6;
            --mint-dark: #0f766e;
            --coral: #fb7185;
            --ink: #172026;
            --muted: #667085;
            --line: #e4ebe8;
            --surface: #ffffff;
            --soft: #f3fbf8;
        }
        .stApp {
            background:
                linear-gradient(180deg, #f4fbf8 0%, #ffffff 36%),
                #ffffff;
            color: var(--ink);
        }
        .block-container {
            max-width: 1120px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        h1, h2, h3, p {
            letter-spacing: 0;
        }
        h1 {
            color: var(--ink);
            font-size: 2.2rem;
            line-height: 1.2;
            margin-bottom: 0.35rem;
        }
        [data-testid="stSidebar"] {
            background: #f0faf7;
            border-right: 1px solid var(--line);
        }
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--mint-dark);
        }
        .stButton > button {
            width: 100%;
            min-height: 3rem;
            border: 0;
            border-radius: 8px;
            background: var(--ink);
            color: white;
            font-weight: 800;
        }
        .stButton > button:hover {
            background: var(--mint-dark);
            color: white;
        }
        .intro {
            padding: 1rem 0 1.35rem;
            border-bottom: 1px solid var(--line);
            margin-bottom: 1.25rem;
        }
        .intro-kicker {
            color: var(--coral);
            font-weight: 800;
            margin-bottom: 0.35rem;
        }
        .intro-copy {
            color: var(--muted);
            font-size: 1rem;
            margin: 0;
        }
        .panel {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1rem;
            background: var(--surface);
        }
        .soft-panel {
            border: 1px solid #d7f0e9;
            border-radius: 8px;
            padding: 1rem;
            background: var(--soft);
        }
        .metric-label {
            color: var(--muted);
            font-size: 0.88rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .metric-value {
            color: var(--mint-dark);
            font-size: 1.55rem;
            font-weight: 900;
            line-height: 1.15;
        }
        .care-note {
            color: var(--muted);
            margin-top: 0.45rem;
        }
        .product-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1rem;
            background: #ffffff;
            margin-bottom: 0.75rem;
        }
        .product-name {
            color: var(--ink);
            font-size: 1.02rem;
            font-weight: 900;
            margin-bottom: 0.3rem;
        }
        .product-effect {
            color: var(--muted);
            margin-bottom: 0.65rem;
        }
        .product-card a {
            color: var(--mint-dark);
            font-weight: 800;
            text-decoration: none;
        }
        .small-muted {
            color: var(--muted);
            font-size: 0.92rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    apply_theme()
    render_sidebar()
    render_intro()

    uploaded_file = st.file_uploader(
        "피부 사진 업로드",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if uploaded_file is None:
        st.info("피부 사진을 올리면 색소침착 점수와 맞춤 화장품 추천을 확인할 수 있어요.")
        return

    image = Image.open(uploaded_file).convert("RGB")
    user_profile = get_user_profile()

    left, right = st.columns([0.95, 1.05], gap="large")
    with left:
        st.image(image, caption="업로드한 피부 사진", use_container_width=True)
        st.caption("사진은 모델 분석에만 사용되며, 피부 타입과 고민 정보는 추천 문맥에 반영됩니다.")

    with right:
        st.markdown(
            """
            <div class="soft-panel">
                <div class="metric-label">분석 준비</div>
                <div class="metric-value">피부 컨디션 체크</div>
                <div class="care-note">이미지 분석 후 피부 타입과 고민에 맞춰 추천 제품을 정리합니다.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("내 피부에 맞는 제품 찾기"):
            run_analysis(image, user_profile)


def render_sidebar():
    with st.sidebar:
        st.header("내 피부 프로필")
        st.session_state["skin_type"] = st.selectbox(
            "피부 타입",
            ["건성", "지성", "복합성", "민감성"],
            key="skin_type_select",
        )
        st.session_state["concern"] = st.text_input(
            "가장 신경 쓰이는 고민",
            value="색소침착",
            key="concern_input",
        )
        st.session_state["age_group"] = st.selectbox(
            "연령대",
            ["10대", "20대", "30대", "40대", "50대", "60대 이상"],
            key="age_group_select",
        )
        st.markdown("---")
        st.caption("현재 모델 점수는 피부 사진으로 계산되고, 프로필은 추천 결과를 개인화하는 데 사용됩니다.")


def render_intro():
    st.markdown(
        f"""
        <div class="intro">
            <div class="intro-kicker">{SERVICE_NAME}</div>
            <h1>{SERVICE_TAGLINE}</h1>
            <p class="intro-copy">
                피부 사진을 분석해 색소침착 정도를 확인하고, 내 피부 타입에 맞는 케어 성분과 제품을 추천합니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_user_profile():
    return {
        "skin_type": st.session_state.get("skin_type", "건성"),
        "concern": st.session_state.get("concern", "색소침착"),
        "age_group": st.session_state.get("age_group", "20대"),
    }


def run_analysis(image, user_profile):
    try:
        with st.status("피부 분석과 추천을 준비하는 중입니다.", expanded=True) as status:
            st.write("이미지를 모델 입력 형식으로 변환하고 있어요.")
            model = get_model()

            st.write("피부 사진에서 색소침착 점수를 계산하고 있어요.")
            cv_result = predict_pigmentation(model, image)

            st.write("피부 프로필과 분석 결과를 연결하고 있어요.")
            cv_context = build_cv_context(cv_result, user_profile)

            st.write("추천 답변을 생성하고 있어요. LLM을 연결하면 이 단계에서 시간이 조금 걸릴 수 있어요.")
            products = generate_product_recommendations(cv_context)

            result = build_result(cv_result, user_profile, products)
            status.update(label="추천 결과가 준비됐어요.", state="complete", expanded=False)

        render_result(result)
    except FileNotFoundError as error:
        st.error(str(error))
    except Exception as error:
        st.error("분석 중 오류가 발생했습니다.")
        st.exception(error)


def render_result(result):
    level = result["level"]

    st.subheader("피부 분석 결과")
    score_col, level_col = st.columns(2)
    with score_col:
        st.markdown(
            f"""
            <div class="panel">
                <div class="metric-label">색소침착 점수</div>
                <div class="metric-value">{result["score"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with level_col:
        st.markdown(
            f"""
            <div class="panel">
                <div class="metric-label">분석 단계</div>
                <div class="metric-value">{level["label"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="soft-panel">
            <strong>{level["tone"]}</strong>
            <div class="care-note">{result["skin_type"]} 피부 기준: {result["care_note"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("추천 화장품")
    for product in result["products"]:
        st.markdown(
            f"""
            <div class="product-card">
                <div class="product-name">{product["name"]}</div>
                <div class="product-effect">{product["effect"]}</div>
                <a href="{product["uri"]}" target="_blank">제품 정보 보기</a>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
