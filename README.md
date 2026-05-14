# DermaLogic

CV 기반 피부분석 및 화장품 추천 Streamlit 앱입니다.

## 구조

- `app.py`: Streamlit UI
- `services/cv_service.py`: ResNet18 기반 색소침착 모델 로딩 및 예측
- `services/result_service.py`: CV 결과를 추천 컨텍스트로 변환
- `services/llm_service.py`: 추후 LLM/웹검색 추천 연결 자리, 현재는 고정 추천 반환
- `utils/config.py`: 모델 경로와 분석 단계 설정

## 모델

`models/skin_pro_final.pth` 파일을 사용합니다.
모델 구조는 `ResNet18 + fc regression head(output=1)` 기준입니다.

## Streamlit 실행

PowerShell에서 프로젝트 폴더로 이동한 뒤 실행합니다.

```powershell
venv\Scripts\streamlit.exe run app.py
```

브라우저에서 아래 주소로 접속합니다.

```text
http://localhost:8501
```

## Streamlit 종료

터미널에서 실행 중인 경우 `Ctrl + C`를 누릅니다.

백그라운드로 실행된 서버를 종료해야 할 경우에는 8501 포트를 사용하는 프로세스를 종료합니다.

```powershell
Get-NetTCPConnection -LocalPort 8501 | ForEach-Object { Stop-Process -Id $_.OwningProcess }
```
