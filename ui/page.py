import time

import streamlit as st
from PIL import Image

from ui.settings import AGE_GROUPS, SERVICE_NAME, SERVICE_TAGLINE, SKIN_TYPES
from ui.styles import apply_theme


AVERAGE_SCORE = 95
SKIN_TYPE_AVERAGES = {
    "건성": 88,
    "지성": 102,
    "복합성": 96,
    "민감성": 110,
}
AGE_GROUP_AVERAGES = {
    "10대": 72,
    "20대": 84,
    "30대": 98,
    "40대": 114,
    "50대": 128,
    "60대 이상": 140,
}


def render_app(analyze_skin_image):
    apply_theme()
    render_sidebar()
    render_intro()
    init_session_state()

    uploaded_file = st.file_uploader(
        "피부 사진 업로드",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if uploaded_file is None:
        st.info("피부 사진을 올리면 먼저 피부 점수를 계산하고, 다음 화면에서 상세 분석과 제품 추천을 보여드릴게요.")
        return

    image = Image.open(uploaded_file).convert("RGB")
    user_profile = get_user_profile()
    reset_result_when_upload_changes(uploaded_file)

    if st.session_state["analysis_result"] is None:
        render_analysis_entry(image, user_profile, analyze_skin_image)
        return

    if st.session_state["result_view"] == "detail":
        render_detail_page(image, st.session_state["analysis_result"])
        return

    render_quick_result_page(image, st.session_state["analysis_result"])


def init_session_state():
    if "analysis_result" not in st.session_state:
        st.session_state["analysis_result"] = None
    if "result_view" not in st.session_state:
        st.session_state["result_view"] = "quick"


def render_sidebar():
    with st.sidebar:
        st.header("피부 프로필")
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
        st.caption("현재 피부 점수는 사진에서 계산한 참고 지표이며, 프로필 정보는 설명과 추천 문구에 함께 반영됩니다.")


def render_intro():
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-copy">
                <div class="hero-kicker">{SERVICE_NAME}</div>
                <h1>{SERVICE_TAGLINE}</h1>
                <p>
                    사진 기반 피부 컨디션을 먼저 요약하고, 다음 화면에서 평균 비교와 추천 루틴까지 단계적으로 정리합니다.
                </p>
            </div>
            <div class="hero-badges">
                <span>AI 피부 분석</span>
                <span>평균 비교</span>
                <span>맞춤 추천</span>
            </div>
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
    st.session_state["result_view"] = "quick"


def render_analysis_entry(image, user_profile, analyze_skin_image):
    left, right = st.columns([0.95, 1.05], gap="large")
    with left:
        render_upload_preview(image)

    with right:
        st.markdown(
            f"""
            <div class="analysis-ready">
                <div class="section-label">STEP 2</div>
                <div class="section-title">AI 피부 컨디션 체크</div>
                <p>
                    이미지를 모델 입력 형태로 변환한 뒤 <strong>{user_profile["skin_type"]}</strong> 피부와
                    <strong>{user_profile["concern"]}</strong> 고민 기준으로 결과를 준비합니다.
                </p>
                <div class="profile-pills">
                    <span>{user_profile["skin_type"]}</span>
                    <span>{user_profile["age_group"]}</span>
                    <span>{user_profile["concern"]}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("분석 시작", type="primary"):
            run_analysis(image, user_profile, analyze_skin_image)


def run_analysis(image, user_profile, analyze_skin_image):
    try:
        with st.status("피부 이미지를 분석하고 있어요.", expanded=True) as status:
            st.write("이미지를 모델 입력 크기로 정리합니다.")
            st.write("피부 컨디션 점수를 계산합니다.")
            st.write("프로필에 맞는 추천 후보를 준비합니다.")

            result = analyze_skin_image(image, user_profile)
            st.session_state["analysis_result"] = result
            st.session_state["result_view"] = "quick"
            status.update(label="간단 분석 결과가 준비됐어요.", state="complete", expanded=False)

        st.rerun()
    except FileNotFoundError as error:
        st.error(str(error))
    except Exception as error:
        st.error("분석 중 오류가 발생했습니다.")
        st.exception(error)


def render_upload_preview(image):
    preview_image = image.copy()
    preview_image.thumbnail((420, 420))

    st.markdown(
        """
        <div class="section-label">STEP 1</div>
        <div class="section-title">피부 사진 미리보기</div>
        """,
        unsafe_allow_html=True,
    )
    st.image(preview_image, caption="업로드한 피부 사진")
    st.markdown(
        """
        <div class="privacy-note">
            업로드한 사진은 현재 분석 흐름에서만 사용하며, 피부 타입과 고민 정보는 설명과 추천에 반영됩니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_result_page(image, result):
    left, right = st.columns([0.9, 1.1], gap="large")
    with left:
        render_upload_preview(image)

    with right:
        level = result["level"]
        score_percent = get_score_percent(result["score"])
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-heading">
                    <div>
                        <div class="section-label">STEP 3</div>
                        <div class="section-title">간단 분석 결과</div>
                    </div>
                    <span class="status-badge">{level["label"]}</span>
                </div>
                <div class="score-row">
                    <div>
                        <div class="metric-label">피부 컨디션 점수</div>
                        <div class="metric-value">{result["score"]}</div>
                    </div>
                    <div class="score-caption">낮을수록 안정적인 참고 지표</div>
                </div>
                <div class="score-track">
                    <div class="score-fill" style="width: {score_percent}%;"></div>
                </div>
                <div class="result-tone">
                    <strong>{level["tone"]}</strong>
                    <div class="care-note">다음 화면에서 평균치와 비교해 더 자세히 풀어드릴게요.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("다음 페이지에서 상세 분석 보기", type="primary"):
            st.session_state["result_view"] = "detail"
            st.rerun()


def render_detail_page(image, result):
    if st.button("간단 결과로 돌아가기"):
        st.session_state["result_view"] = "quick"
        st.rerun()

    st.markdown(
        """
        <div class="section-label">STEP 4</div>
        <div class="section-title">상세 수치 분석</div>
        """,
        unsafe_allow_html=True,
    )

    score = float(result["score"])
    reference = get_reference_scores(result)
    overall_delta = score - reference["overall"]
    skin_delta = score - reference["skin_type"]
    age_delta = score - reference["age_group"]

    metric_cols = st.columns(4)
    metric_cols[0].metric("내 피부 점수", f"{score:.2f}")
    metric_cols[1].metric("전체 평균", reference["overall"], f"{overall_delta:+.1f}")
    metric_cols[2].metric(f"{result['skin_type']} 평균", reference["skin_type"], f"{skin_delta:+.1f}")
    metric_cols[3].metric(f"{result['age_group']} 평균", reference["age_group"], f"{age_delta:+.1f}")

    st.progress(min(max(score / 180, 0), 1), text="피부 점수 위치")

    tab_summary, tab_compare, tab_routine = st.tabs(["해석", "평균 비교", "추천 루틴"])
    with tab_summary:
        render_streamed_guide(result, result["guide"], result["safety_notice"])

    with tab_compare:
        render_comparison_panel(result, reference)

    with tab_routine:
        render_routine_panel(result)

    st.markdown(
        """
        <div class="section-label">STEP 5</div>
        <div class="section-title">맞춤 추천 화장품</div>
        """,
        unsafe_allow_html=True,
    )
    render_product_recommendations(result)


def get_reference_scores(result):
    return {
        "overall": AVERAGE_SCORE,
        "skin_type": SKIN_TYPE_AVERAGES.get(result["skin_type"], AVERAGE_SCORE),
        "age_group": AGE_GROUP_AVERAGES.get(result["age_group"], AVERAGE_SCORE),
    }


def render_comparison_panel(result, reference):
    score = float(result["score"])
    rows = [
        ("전체 평균", reference["overall"], score - reference["overall"]),
        (f"{result['skin_type']} 피부 평균", reference["skin_type"], score - reference["skin_type"]),
        (f"{result['age_group']} 평균", reference["age_group"], score - reference["age_group"]),
    ]

    for label, average, delta in rows:
        direction = "낮아 비교적 안정적인 편입니다" if delta <= 0 else "높아 조금 더 관리가 필요한 편입니다"
        st.markdown(
            f"""
            <div class="compare-row">
                <div>
                    <strong>{label}</strong>
                    <div class="small-muted">평균 {average}점 대비 {abs(delta):.1f}점 {direction}.</div>
                </div>
                <span>{delta:+.1f}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="notice-panel">
            <strong>해석 기준</strong><br>
            이 점수는 피부 사진에서 계산된 참고 지표입니다. 현재 결과는 {result["level"]["label"]} 단계이며,
            수치가 높게 나올수록 자외선 차단, 진정, 보습 루틴을 더 우선해서 보는 것이 좋습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_routine_panel(result):
    guide = result["guide"]
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            f"""
            <div class="mini-card">
                <div class="guide-title">아침 루틴</div>
                <div class="guide-text">{guide["morning"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            f"""
            <div class="mini-card">
                <div class="guide-title">저녁 루틴</div>
                <div class="guide-text">{guide["evening"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="mini-card">
            <div class="guide-title">우선 고려 성분</div>
            <div class="tag-row">{render_ingredient_tags(result["priority_ingredients"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_streamed_guide(result, guide, safety_notice):
    comment_placeholder = st.empty()
    streamed_text = ""
    for char in stream_text(guide["summary"]):
        streamed_text += char
        comment_placeholder.markdown(
            f"""
            <div class="care-comment">
                <div class="guide-title">오늘의 AI 케어 총평</div>
                <div class="guide-text">{streamed_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="notice-panel">
            <strong>주의사항</strong><br>
            {guide["caution"]}<br><br>
            {safety_notice}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_product_recommendations(result):
    for product in result["products"]:
        st.markdown(
            f"""
            <div class="product-card">
                <div class="product-tag">추천 제품</div>
                <div class="product-name">{product["name"]}</div>
                <div class="product-reason">추천 이유: {product.get("reason", "현재 톤 케어 단계와 피부 프로필에 맞춰 선택했어요.")}</div>
                <div class="product-effect">{product["effect"]}</div>
                <a class="product-link" href="{product["uri"]}" target="_blank">제품 정보 보기</a>
            </div>
            """,
            unsafe_allow_html=True,
        )


def stream_text(text):
    for char in text:
        yield char
        time.sleep(0.012)


def get_score_percent(score):
    return min(max(float(score) / 180 * 100, 6), 100)


def render_ingredient_tags(ingredients):
    return "".join(f"<span>{ingredient}</span>" for ingredient in ingredients)
