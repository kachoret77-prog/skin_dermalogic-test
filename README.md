# DermaLogic

CV 기반 피부분석 및 화장품 추천 Streamlit 앱입니다.

## 구조

- `app.py`: Streamlit 앱 진입점, 모델 로딩 캐시, 분석 서비스 연결
- `ui/page.py`: Streamlit 화면 구성, 업로드/결과/추천 영역 렌더링
- `ui/styles.py`: Streamlit 화면 CSS 테마
- `ui/settings.py`: 서비스명, 화면 옵션, 프로필 선택값 설정
- `ui/__init__.py`: `ui` 디렉토리를 파이썬 패키지로 인식시키는 파일
- `services/cv_service.py`: ResNet18 기반 색소침착 모델 로딩 및 예측
- `services/result_service.py`: CV 결과를 추천 컨텍스트와 케어 안내 문구로 변환
- `services/llm_service.py`: Gemini LLM 기반 추천 생성, API 키가 없거나 호출 실패 시 고정 추천 반환
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

## 팀원 최신 코드 반영

이미 저장소를 클론한 팀원은 PowerShell에서 프로젝트 폴더로 이동한 뒤 최신 `main`을 가져옵니다.

```powershell
git checkout main
git pull origin main
```

가상환경이 이미 준비되어 있다면 바로 실행합니다.

```powershell
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\streamlit.exe run app.py
```

처음 실행하는 환경이라면 가상환경을 만들고 의존성을 설치한 뒤 실행합니다.

```powershell
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\streamlit.exe run app.py
```

## Gemini API 키 설정

LLM 추천 기능을 확인하려면 각자 로컬에 `.env` 파일을 만들어 Google Gemini API 키를 입력합니다.
`.env` 파일은 보안상 GitHub에 올라가지 않습니다.

```powershell
Copy-Item .env.example .env
```

생성된 `.env` 파일을 열고 본인의 Google Gemini API 키를 입력합니다.

```env
GEMINI_API_KEY=본인_Google_Gemini_API_키
GEMINI_MODEL=gemini-2.5-flash
```

키를 입력한 뒤 앱을 실행하면 Gemini LLM이 피부 분석 결과에 맞춰 화장품 이름, 효과, 추천 이유, 상품 URL을 생성합니다.
키가 없거나 Gemini 호출에 실패하면 기존 고정 추천 데이터로 동작합니다.

## Streamlit 종료

터미널에서 실행 중인 경우 `Ctrl + C`를 누릅니다.

백그라운드로 실행된 서버를 종료해야 할 경우에는 8501 포트를 사용하는 프로세스를 종료합니다.

```powershell
Get-NetTCPConnection -LocalPort 8501 | ForEach-Object { Stop-Process -Id $_.OwningProcess }
```
