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
                st.session_state["analysis_result"],
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
        <div class="hero">
            <div class="hero-copy">
                <div class="hero-kicker">{SERVICE_NAME}</div>
                <h1>{SERVICE_TAGLINE}</h1>
                <p>
                    피부 사진을 바탕으로 톤 케어 지표를 확인하고, 내 피부 프로필에 맞는 케어 성분과 제품을 정리해드려요.
                </p>
            </div>
            <div class="hero-badges">
                <span>AI 피부 분석</span>
                <span>맞춤 화장품 추천</span>
                <span>케어 루틴 안내</span>
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


def render_upload_preview(image):
    st.markdown(
        """
        <div class="section-label">STEP 1</div>
        <div class="section-title">피부 사진 미리보기</div>
        """,
        unsafe_allow_html=True,
    )
    st.image(image, caption="업로드한 피부 사진", use_container_width=True)
    st.markdown(
        """
        <div class="privacy-note">
            업로드한 사진은 현재 분석 흐름에서만 사용되며, 피부 타입과 고민 정보는 추천 문맥에 반영됩니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_analysis_panel(image, user_profile, analyze_skin_image, product_container):
    st.markdown(
        f"""
        <div class="analysis-ready">
            <div class="section-label">STEP 2</div>
            <div class="section-title">AI 피부 컨디션 체크</div>
            <p>이미지 분석 후 <strong>{user_profile["skin_type"]}</strong> 피부와 <strong>{user_profile["concern"]}</strong> 고민에 맞춰 결과를 정리합니다.</p>
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
        render_product_recommendations(result, product_container)
    except FileNotFoundError as error:
        st.error(str(error))
    except Exception as error:
        st.error("분석 중 오류가 발생했습니다.")
        st.exception(error)


def render_result_summary(result):
    level = result["level"]
    guide = result["guide"]
    score_percent = get_score_percent(result["score"])

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-heading">
                <div>
                    <div class="section-label">STEP 3</div>
                    <div class="section-title">피부 분석 결과</div>
                </div>
                <span class="status-badge">{level["label"]}</span>
            </div>
            <div class="score-row">
                <div>
                    <div class="metric-label">피부 컨디션 점수</div>
                    <div class="metric-value">{result["score"]}</div>
                </div>
                <div class="score-caption">톤 케어 참고 지표</div>
            </div>
            <div class="score-track">
                <div class="score-fill" style="width: {score_percent}%;"></div>
            </div>
            <div class="result-tone">
                <strong>{level["tone"]}</strong>
                <div class="care-note">{result["skin_type"]} 피부 기준: {result["care_note"]}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_streamed_guide(result, guide, result["safety_notice"])


def render_streamed_guide(result, guide, safety_notice):
    comment_placeholder = st.empty()
    streamed_text = ""
    for char in stream_text(guide["summary"]):
        streamed_text += char
        comment_placeholder.markdown(
            f"""
            <div class="care-comment">
                <div class="section-label">STEP 4</div>
                <div class="guide-title">오늘의 AI 케어 총평</div>
                <div class="guide-text">{streamed_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    positive_col, routine_col = st.columns(2)
    with positive_col:
        st.markdown(
            f"""
            <div class="mini-card">
                <div class="guide-title">긍정 분석</div>
                <div class="guide-text">{result["skin_type"]} 피부 기준으로 현재 단계에 맞는 성분과 제형을 함께 고려했어요.</div>
                <div class="tag-row">
                    {render_ingredient_tags(result["priority_ingredients"])}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with routine_col:
        st.markdown(
            f"""
            <div class="mini-card">
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
            <strong>주의사항</strong><br>
            {guide["caution"]}<br><br>
            {safety_notice}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_product_recommendations(result, container):
    with container:
        st.markdown('<div class="image-column-spacer"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="section-label">STEP 5</div>
            <div class="section-title">맞춤 추천 화장품</div>
            """,
            unsafe_allow_html=True,
        )
        for product in result["products"]:
            st.markdown(
                f"""
                <div class="product-card">
                    <div class="product-tag">추천 제품</div>
                    <div class="product-name">{product["name"]}</div>
                    <div class="product-reason">추천 이유: 현재 톤 케어 단계와 피부 프로필에 맞춰 선택했어요.</div>
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
