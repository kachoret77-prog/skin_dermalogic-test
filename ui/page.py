import time

import streamlit as st
from PIL import Image

from ui.settings import AGE_GROUPS, SERVICE_NAME, SERVICE_TAGLINE, SKIN_TYPES
from ui.styles import apply_theme


def render_app(analyze_skin_image):
    apply_theme()
    render_sidebar()
    render_intro()
    if "analysis_result" not in st.session_state:
        st.session_state["analysis_result"] = None

    uploaded_file = st.file_uploader(
        "피부 사진 업로드",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if uploaded_file is None:
        st.info("피부 사진을 올리면 피부 컨디션 점수와 맞춤 화장품 추천을 확인할 수 있어요.")
        return

    image = Image.open(uploaded_file).convert("RGB")
    user_profile = get_user_profile()
    reset_result_when_upload_changes(uploaded_file)

    left, right = st.columns([0.95, 1.05], gap="large")
    with left:
        render_upload_preview(image)
        product_container = st.container()
        if st.session_state["analysis_result"] is not None:
            render_product_recommendations(
                st.session_state["analysis_result"]["products"],
                product_container,
            )
    with right:
        render_analysis_panel(image, user_profile, analyze_skin_image, product_container)


def render_sidebar():
    with st.sidebar:
        st.header("내 피부 프로필")
        st.session_state["skin_type"] = st.selectbox(
            "피부 타입",
            SKIN_TYPES,
            key="skin_type_select",
        )
        st.session_state["concern"] = st.text_input(
            "가장 신경 쓰이는 고민",
            value="색소침착",
            key="concern_input",
        )
        st.session_state["age_group"] = st.selectbox(
            "연령대",
            AGE_GROUPS,
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


def reset_result_when_upload_changes(uploaded_file):
    current_upload_id = f"{uploaded_file.name}:{uploaded_file.size}"
    if st.session_state.get("upload_id") == current_upload_id:
        return

    st.session_state["upload_id"] = current_upload_id
    st.session_state["analysis_result"] = None


def render_upload_preview(image):
    st.image(image, caption="업로드한 피부 사진", use_container_width=True)
    st.caption("사진은 모델 분석에만 사용되며, 피부 타입과 고민 정보는 추천 문맥에 반영됩니다.")


def render_analysis_panel(image, user_profile, analyze_skin_image, product_container):
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
    if not st.button("내 피부에 맞는 제품 찾기"):
        return

    try:
        with st.status("피부 분석과 추천을 준비하는 중입니다.", expanded=True) as status:
            st.write("이미지를 모델 입력 형식으로 변환하고 있어요.")
            st.write("피부 사진에서 컨디션 지표를 계산하고 있어요.")
            st.write("추천 답변을 생성하고 있어요. LLM을 연결하면 이 단계에서 시간이 조금 걸릴 수 있어요.")

            result = analyze_skin_image(image, user_profile)
            st.session_state["analysis_result"] = result
            status.update(label="추천 결과가 준비됐어요.", state="complete", expanded=False)

        render_result_summary(result)
        render_product_recommendations(result["products"], product_container)
    except FileNotFoundError as error:
        st.error(str(error))
    except Exception as error:
        st.error("분석 중 오류가 발생했습니다.")
        st.exception(error)


def render_result_summary(result):
    level = result["level"]
    guide = result["guide"]

    st.subheader("피부 분석 결과")
    score_col, level_col = st.columns(2)
    with score_col:
        st.markdown(
            f"""
            <div class="panel">
                <div class="metric-label">피부 컨디션 점수</div>
                <div class="metric-value">{result["score"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with level_col:
        st.markdown(
            f"""
            <div class="panel">
                <div class="metric-label">톤 케어 단계</div>
                <div class="metric-value">{level["label"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="soft-panel result-tone">
            <strong>{level["tone"]}</strong>
            <div class="care-note">{result["skin_type"]} 피부 기준: {result["care_note"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_streamed_guide(guide, result["safety_notice"])


def render_streamed_guide(guide, safety_notice):
    comment_placeholder = st.empty()
    streamed_text = ""
    for char in stream_text(guide["summary"]):
        streamed_text += char
        comment_placeholder.markdown(
            f"""
            <div class="guide-panel">
                <div class="guide-title">AI 케어 코멘트</div>
                <div class="guide-text">{streamed_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    guide_col, routine_col = st.columns(2)
    with guide_col:
        st.markdown(
            f"""
            <div class="guide-panel">
                <div class="guide-title">추천 이유</div>
                <div class="guide-text">{guide["reason"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with routine_col:
        st.markdown(
            f"""
            <div class="guide-panel">
                <div class="guide-title">오늘의 루틴 예시</div>
                <div class="guide-text">
                    아침: {guide["morning"]}<br>
                    저녁: {guide["evening"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="notice-panel">
            <strong>케어 주의점</strong><br>
            {guide["caution"]}<br><br>
            {safety_notice}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_product_recommendations(products, container):
    with container:
        st.markdown('<div class="image-column-spacer"></div>', unsafe_allow_html=True)
        st.subheader("추천 화장품")
        for product in products:
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


def stream_text(text):
    for char in text:
        yield char
        time.sleep(0.012)
