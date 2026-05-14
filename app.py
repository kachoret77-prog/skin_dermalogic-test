import streamlit as st

from services.cv_service import load_model, predict_pigmentation
from services.llm_service import generate_product_recommendations
from services.result_service import build_cv_context, build_result
from ui.page import render_app
from ui.settings import PAGE_ICON, SERVICE_NAME


st.set_page_config(
    page_title=SERVICE_NAME,
    page_icon=PAGE_ICON,
    layout="wide",
)


@st.cache_resource
def get_model():
    return load_model()


def analyze_skin_image(image, user_profile):
    model = get_model()
    cv_result = predict_pigmentation(model, image)
    cv_context = build_cv_context(cv_result, user_profile)
    products = generate_product_recommendations(cv_context)
    return build_result(cv_result, user_profile, products)


def main():
    render_app(analyze_skin_image)


if __name__ == "__main__":
    main()
