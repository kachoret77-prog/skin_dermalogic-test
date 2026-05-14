from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "skin_pro_final.pth"

IMAGE_SIZE = 224
PIGMENTATION_OUTPUT_DIM = 1

# ResNet 계열 ImageNet 전처리 기준입니다.
IMAGE_MEAN = [0.485, 0.456, 0.406]
IMAGE_STD = [0.229, 0.224, 0.225]

DEFAULT_LLM_MODEL = "gpt-4o-mini"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"

SCORE_LEVELS = (
    {
        "max": 80,
        "label": "낮음",
        "tone": "피부 톤이 비교적 안정적으로 관찰됐어요.",
    },
    {
        "max": 140,
        "label": "보통",
        "tone": "피부 톤 케어를 시작하기 좋은 구간이에요.",
    },
    {
        "max": float("inf"),
        "label": "높음",
        "tone": "피부 톤 케어와 자외선 차단을 조금 더 신경 써 주세요.",
    },
)
