import math

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms

from utils.config import IMAGE_MEAN, IMAGE_SIZE, IMAGE_STD, MODEL_PATH


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose(
    [
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(IMAGE_MEAN, IMAGE_STD),
    ]
)


def load_model():
    """
    models/skin_pro_final.pth에 저장된 ResNet18 기반 색소침착 회귀 모델을 불러옵니다.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {MODEL_PATH}")

    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 1)
    state_dict = torch.load(MODEL_PATH, map_location=device)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model


def load_skin_model():
    return load_model()


def predict_pigmentation(model, image):
    """
    업로드된 피부 이미지를 모델에 넣고 추천 서비스가 사용하기 쉬운 결과 dict를 반환합니다.
    """
    if not isinstance(image, Image.Image):
        raise TypeError("PIL.Image 형식의 이미지만 분석할 수 있습니다.")

    rgb_image = image.convert("RGB")
    input_tensor = transform(rgb_image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)

    score = float(output.detach().cpu().reshape(-1)[0].item())
    if not math.isfinite(score):
        raise ValueError("CV 모델이 유효하지 않은 점수를 반환했습니다.")

    score = round(max(0.0, score), 2)
    return {
        "condition": "pigmentation",
        "score": score,
        "model": "ResNet18 pigmentation regression",
    }
