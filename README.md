# <div align="center">PaperBanana 🍌</div>
<div align="center">
<strong>학술 논문 도식화 자동화 멀티 에이전트 프레임워크</strong>
<br><br>
Dawei Zhu, Rui Meng, Yale Song, Xiyu Wei, Sujian Li, Tomas Pfister and Jinsung yoon
<br><br>
</div>

<div align="center">
<a href="https://huggingface.co/papers/2601.23265"><img src="assets/paper-page-xl.svg" alt="Paper page on HF"></a>
<a href="https://huggingface.co/datasets/dwzhu/PaperBananaBench"><img src="assets/dataset-on-hf-xl.svg" alt="Dataset on HF"></a>
</div>

---

> **참고**: 이 저장소는 원본 PaperVizAgent를 기반으로 한국어 문서화와 개선된 사용자 경험을 제공하는 버전입니다. 원본 PaperBanana는 Google-Research에서 [PaperVizAgent](https://github.com/google-research/papervizagent)로 오픈소스화되었습니다.

---

## 📖 소개

**PaperBanana**는 AI를 활용하여 학술 논문의 도표와 다이어그램을 자동으로 생성하는 레퍼런스 기반 멀티 에이전트 프레임워크입니다. 전문화된 에이전트들로 구성된 크리에이티브 팀처럼 작동하며, **Retriever(검색자), Planner(기획자), Stylist(스타일리스트), Visualizer(시각화 도구), Critic(비평가)** 에이전트들로 구성된 파이프라인을 통해 논문의 방법론 섹션을 출판 가능한 수준의 다이어그램과 플롯으로 변환합니다.

### 예시 출력

![Examples](assets/teaser_figure.jpg)

---

## 🏗️ 시스템 아키텍처

![PaperBanana Framework](assets/method_diagram.png)

PaperBanana는 5단계 에이전트 파이프라인을 통해 고품질의 학술 도식화를 생성합니다:

1. **Retriever Agent (검색자)** - 큐레이션된 컬렉션에서 관련 레퍼런스 다이어그램을 검색
2. **Planner Agent (기획자)** - 논문의 방법론을 포괄적인 텍스트 설명으로 변환
3. **Stylist Agent (스타일리스트)** - 학술적 미학 기준에 맞게 설명을 다듬음
4. **Visualizer Agent (시각화 도구)** - 텍스트 설명을 시각적 결과물로 변환
5. **Critic Agent (비평가)** - Visualizer와 협력하여 품질을 반복적으로 개선

---

## 🚀 빠른 시작

### 시스템 요구사항

- **Python**: 3.10 이상 (권장: 3.12)
- **uv**: Python 패키지 관리자 ([설치 가이드](https://docs.astral.sh/uv/getting-started/installation/))
- **API 키**: Google Gemini API 키 필요 ([발급 방법](#api-key-발급))

### 설치 및 실행

#### Windows

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/PaperBanana.git
cd PaperBanana

# 2. 초기 설정 (자동)
setup.bat

# 3. 실행
start.bat
```

#### Mac/Linux

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/PaperBanana.git
cd PaperBanana

# 2. 초기 설정 (자동)
chmod +x setup.sh
./setup.sh

# 3. 실행
chmod +x start.sh
./start.sh
```

브라우저가 자동으로 열리고 `http://localhost:8501`에서 PaperBanana에 접속할 수 있습니다.

---

## 🔧 수동 설치 (고급)

### 1단계: uv 설치

**Windows:**
- [uv 공식 설치 페이지](https://docs.astral.sh/uv/getting-started/installation/)에서 설치 프로그램 다운로드

**Mac/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2단계: 가상환경 및 패키지 설치

```bash
# 가상환경 생성
uv venv

# 활성화
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows

# Python 3.12 설치
uv python install 3.12

# 패키지 설치
uv pip install -r requirements.txt
```

### 3단계: API 키 설정

`configs/model_config.yaml` 파일을 생성하고 설정:

```yaml
defaults:
  model_name: "gemini-2.0-flash-exp"
  image_model_name: "gemini-2.0-flash-exp-image-generation"

api_keys:
  google_api_key: "YOUR_GOOGLE_API_KEY"
  openai_api_key: ""      # 선택사항
  anthropic_api_key: ""   # 선택사항
```

### 4단계: 실행

```bash
streamlit run demo.py
```

---

## 🔑 API Key 발급

### Google Gemini API 키

1. [Google AI Studio](https://aistudio.google.com/app/apikey) 접속
2. Google 계정으로 로그인
3. **"Create API Key"** 클릭
4. 프로젝트 선택 또는 생성
5. 생성된 API 키 복사 (예: `AIza...`)

> 💡 **참고**: Google AI Studio는 물론 사용량 한도 내에서 물론으로 제공됩니다.
> - 일일 요청: 1,500회
> - 분당 요청: 15회
> - 이미지 생성: 물론 티어 내 무제한

---

## 📊 사용 방법

### 웹 인터페이스 (Streamlit)

#### 1️⃣ 후보 생성 탭

논문의 방법론을 입력하여 여러 다이어그램 후보를 생성합니다.

**입력:**
- **방법론 섹션**: 논문의 Method 섹션을 Markdown 형식으로 입력
- **그림 캡션**: 생성할 다이어그램의 설명 (예: "Figure 1: Overview of our proposed framework")

**설정 옵션:**

| 설정 | 설명 | 권장값 |
|------|------|--------|
| **파이프라인 모드** | 사용할 에이전트 조합 | `demo_planner_critic` |
| **검색 설정** | 참조 다이어그램 검색 방식 | `auto` |
| **후보 개수** | 생성할 이미지 수 (1-20) | 10개 |
| **화면 비율** | 출력 이미지 비율 | `16:9` 또는 `21:9` |
| **최대 평가자 라운드** | 품질 개선 반복 횟수 | 3회 |

**실행:**
- **"🚀 후보 생성"** 버튼 클릭
- 1-3분 소요 후 결과 확인
- 원하는 후보 선택하여 다운로드

#### 2️⃣ 이미지 개선 탭

생성된 이미지나 기존 이미지를 고해상도로 개선합니다.

**사용법:**
1. 이미지 파일 업로드 (PNG, JPG, JPEG)
2. 편집 지침 입력 (예: "학술 논문 스타일로 변경")
3. 목표 해상도 선택: `2K` 또는 `4K`
4. 종횡비 선택
5. **"✨ 이미지 개선"** 버튼 클릭

---

### 명령줄 인터페이스 (CLI)

고급 사용자를 위한 명령줄 실행:

```bash
# 기본 설정으로 실행
python main.py

# 커스텀 설정으로 실행
python main.py \
  --dataset_name "PaperBananaBench" \
  --task_name "diagram" \
  --split_name "test" \
  --exp_mode "dev_full" \
  --retrieval_setting "auto"
```

**실험 모드:**

| 모드 | 설명 |
|------|------|
| `vanilla` | 계획 및 개선 없이 직접 생성 |
| `dev_planner` | Planner → Visualizer |
| `dev_planner_stylist` | Planner → Stylist → Visualizer |
| `dev_planner_critic` | Planner → Visualizer → Critic (다중 라운드) |
| `dev_full` | 모든 에이전트를 포함한 전체 파이프라인 |

---

## 💰 API 비용 안내

### 예상 사용 비용 (10개 후보 + 3회 평가자 라운드 기준)

| 항목 | API 호출 횟수 | 예상 비용 (USD) | 예상 비용 (KRW) |
|-----|--------------|----------------|----------------|
| **Retriever** (검색) | 10회 | $0.07 | ~₩95 |
| **Planner** (기획) | 10회 | $0.09 | ~₩122 |
| **Visualizer** (이미지 생성) | 40회 | $0.01 | ~₩19 |
| **Critic** (평가) | 30회 | $0.07 | ~₩97 |
| **총합** | **90회** | **~$0.24** | **~₩330** |

### 비용 절감 방법

| 방법 | 효과 |
|-----|------|
| 후보 개수 감소 (10개 → 5개) | 50% 절감 |
| 평가자 라운드 감소 (3회 → 2회) | 30% 절감 |
| 검색 설정 변경 ("auto" → "none") | Retriever 생략 |

---

## 🗂️ 프로젝트 구조

```
PaperBanana/
├── agents/                    # 에이전트 구현
│   ├── retriever_agent.py    # 참고 이미지 검색
│   ├── planner_agent.py      # 생성 계획 수립
│   ├── stylist_agent.py      # 스타일 적용
│   ├── visualizer_agent.py   # 이미지 생성
│   └── critic_agent.py       # 품질 개선
├── configs/
│   ├── model_config.template.yaml  # 설정 템플릿
│   └── model_config.yaml           # 실제 설정 (생성됨)
├── data/                      # 데이터셋 (선택)
│   └── PaperBananaBench/
├── prompts/                   # 프롬프트 템플릿
├── utils/                     # 유틸리티 함수
├── visualize/                 # 시각화 도구
├── demo.py                    # Streamlit 데모
├── main.py                    # 명령줄 인터페이스
├── requirements.txt           # 패키지 의존성
├── setup.bat / setup.sh      # 설정 스크립트
├── start.bat / start.sh      # 실행 스크립트
└── README.md                  # 이 파일
```

---

## 🛠️ 문제 해결

### 자주 발생하는 문제

#### "API Key 오류"
- `configs/model_config.yaml` 파일 확인
- API 키가 올바르게 입력되었는지 확인
- 키의 앞뒤 공백 제거

#### "uv가 설치되지 않았습니다"
- [uv 공식 설치 페이지](https://docs.astral.sh/uv/getting-started/installation/)에서 설치
- 설치 후 터미널/명령 프롬프트 재시작

#### "포트 8501이 이미 사용 중"
```bash
# 다른 포트로 실행
streamlit run demo.py --server.port 8502
```

#### "메모리 부족"
- 후보 개수를 5개 이하로 줄이기
- 더 작은 해상도(2K) 선택

자세한 문제 해결은 [DEPLOY.md](PaperBanana/docs/DEPLOY.md)를 참조하세요.

---

## 📚 문서

- **[DEPLOY.md](PaperBanana/docs/DEPLOY.md)** - 상세 설치 및 배포 가이드
- **[USER_MANUAL.md](PaperBanana/docs/USER_MANUAL.md)** - 상세 사용자 매뉴얼
- **[CONTRIBUTING.md](PaperBanana/CONTRIBUTING.md)** - 기여 가이드

---

## 🤝 커뮤니티 지원

이 프로젝트와 관련된 훌륭한 커뮤니티 기여들:

- [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana)
- [efradeca/freepaperbanana](https://github.com/efradeca/freepaperbanana)

관련 프로젝트:
- [ResearAI/AutoFigure-Edit](https://github.com/ResearAI/AutoFigure-Edit)
- [OpenDCAI/Paper2Any](https://github.com/OpenDCAI/Paper2Any)
- [BIT-DataLab/Edit-Banana](https://github.com/BIT-DataLab/Edit-Banana)

---

## 📄 라이선스

Apache-2.0

## 📖 인용

```bibtex
@article{zhu2026paperbanana,
  title={PaperBanana: Automating Academic Illustration for AI Scientists},
  author={Zhu, Dawei and Meng, Rui and Song, Yale and Wei, Xiyu and Li, Sujian and Pfister, Tomas and Yoon, Jinsung},
  journal={arXiv preprint arXiv:2601.23265},
  year={2026}
}
```

## ⚠️ 면책 조항

이것은 공식적으로 지원되는 Google 제품이 아닙니다. 핵심 방법론은 Google 인턴십 기간 동안 개발되었으며, Google에서 특허를 출원했습니다. 이는 오픈 소스 연구 활동에는 영향을 미치지 않지만, 유사한 로직을 사용하는 제3자의 상업적 애플리케이션은 제한될 수 있습니다.

---

<div align="center">

**PaperBanana** - 연구자들을 위한 학술 도식화 자동화 도구

[⬆️ 맨 위로](#-paperbanana-)

</div>

