# PaperBanana 배포 가이드

PaperBanana는 학술 논문의 그림과 도표를 자동으로 생성하는 멀티 에이전트 프레임워크입니다. 이 가이드는 Windows, Mac, Linux에서 PaperBanana를 설치하고 실행하는 방법을 설명합니다.

## 📋 목차

- [시스템 요구사항](#시스템-요구사항)
- [설치 방법](#설치-방법)
  - [Windows](#windows)
  - [Mac/Linux](#maclinux)
- [실행 방법](#실행-방법)
- [API 키 설정](#api-키-설정)
- [문제 해결](#문제-해결)
- [추가 정보](#추가-정보)

---

## 시스템 요구사항

### 필수 요구사항
- **Python**: 3.10 이상 (권장: 3.12)
- **uv**: Python 패키지 관리자 ([설치 가이드](https://docs.astral.sh/uv/getting-started/installation/))
- **인터넷 연결**: API 호출을 위해 필수

### 선택 사항
- **Git**: 저장소 클론 시 필요
- **API 키**: 다음 중 하나 이상 필요
  - Google Gemini API 키
  - OpenAI API 키
  - Anthropic API 키

### 권장 사양
- **CPU**: 멀티코어 프로세서 (병렬 처리 시 성능 향상)
- **메모리**: 8GB 이상
- **디스크**: 2GB 이상 (데이터셋 포함 시 더 필요)

---

## 설치 방법

### Windows

#### 1단계: uv 설치

1. [uv 공식 설치 페이지](https://docs.astral.sh/uv/getting-started/installation/)에서 Windows 설치 프로그램 다운로드
2. 설치 프로그램 실행 및 설치 완료
3. 명령 프롬프트(cmd) 또는 PowerShell 재시작

#### 2단계: 초기 설정 실행

프로젝트 디렉토리에서 다음 명령어 실행:

```bash
setup.bat
```

이 스크립트는 다음을 자동으로 수행합니다:
- ✅ uv 설치 확인
- ✅ Python 가상환경 생성 (`.venv` 디렉토리)
- ✅ 필수 패키지 설치 (`requirements.txt`)
- ✅ 설정 파일 복사 (`model_config.yaml`)

#### 3단계: API 키 설정

1. `configs/model_config.yaml` 파일을 텍스트 에디터로 열기
2. 다음 정보 입력:
   ```yaml
   defaults:
     model_name: "gemini-3-pro-preview"  # 사용할 모델명
     image_model_name: "gemini-3-pro-image-preview"  # 이미지 생성 모델
   
   api_keys:
     google_api_key: "YOUR_GOOGLE_API_KEY"  # Google API 키
     openai_api_key: ""  # OpenAI API 키 (선택)
     anthropic_api_key: ""  # Anthropic API 키 (선택)
   ```
3. 파일 저장

#### 4단계: Streamlit 실행

```bash
start.bat
```

또는 명령줄에서 직접:

```bash
streamlit run demo.py
```

브라우저가 자동으로 열리고 `http://localhost:8501`에서 인터페이스를 사용할 수 있습니다.

---

### Mac/Linux

#### 1단계: uv 설치

터미널에서 다음 명령어 실행:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

설치 후 터미널 재시작 또는 다음 명령어 실행:

```bash
source $HOME/.cargo/env
```

#### 2단계: 초기 설정 실행

프로젝트 디렉토리에서 다음 명령어 실행:

```bash
chmod +x setup.sh
./setup.sh
```

이 스크립트는 다음을 자동으로 수행합니다:
- ✅ uv 설치 확인
- ✅ Python 가상환경 생성 (`.venv` 디렉토리)
- ✅ 필수 패키지 설치 (`requirements.txt`)
- ✅ 설정 파일 복사 (`model_config.yaml`)

#### 3단계: API 키 설정

1. `configs/model_config.yaml` 파일을 텍스트 에디터로 열기:
   ```bash
   nano configs/model_config.yaml
   # 또는
   vim configs/model_config.yaml
   ```

2. 다음 정보 입력:
   ```yaml
   defaults:
     model_name: "gemini-3-pro-preview"  # 사용할 모델명
     image_model_name: "gemini-3-pro-image-preview"  # 이미지 생성 모델
   
   api_keys:
     google_api_key: "YOUR_GOOGLE_API_KEY"  # Google API 키
     openai_api_key: ""  # OpenAI API 키 (선택)
     anthropic_api_key: ""  # Anthropic API 키 (선택)
   ```

3. 파일 저장 (nano: Ctrl+O, Enter, Ctrl+X / vim: :wq)

#### 4단계: Streamlit 실행

```bash
chmod +x start.sh
./start.sh
```

또는 명령줄에서 직접:

```bash
source .venv/bin/activate
streamlit run demo.py
```

브라우저가 자동으로 열리고 `http://localhost:8501`에서 인터페이스를 사용할 수 있습니다.

---

## 실행 방법

### Streamlit 인터랙티브 데모 (권장)

가장 쉬운 방법으로 웹 인터페이스를 통해 PaperBanana를 사용할 수 있습니다.

**Windows:**
```bash
start.bat
```

**Mac/Linux:**
```bash
./start.sh
```

#### 주요 기능

**1. Generate Candidates 탭**
- 논문의 방법 섹션 내용 입력 (Markdown 권장)
- 그림 캡션 제공
- 설정 구성:
  - Pipeline Mode: 사용할 에이전트 파이프라인 선택
  - Retrieval Setting: 참고 이미지 검색 방식
  - Number of Candidates: 생성할 후보 개수 (1-20)
  - Aspect Ratio: 이미지 비율
  - Critic Rounds: 반복 개선 횟수
- "Generate Candidates" 클릭하여 병렬 처리 시작
- 결과를 그리드로 확인하고 개별 또는 배치 다운로드

**2. Refine Image 탭**
- 생성된 이미지 또는 기존 다이어그램 업로드
- 원하는 변경사항 설명
- 해상도 선택 (2K/4K)
- 비율 선택
- 고해상도 출력 다운로드

### 명령줄 인터페이스

고급 사용자를 위한 명령줄 실행 방법:

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

#### 사용 가능한 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--dataset_name` | 사용할 데이터셋 | `PaperBananaBench` |
| `--task_name` | 작업 유형 (`diagram` 또는 `plot`) | `diagram` |
| `--split_name` | 데이터셋 분할 | `test` |
| `--exp_mode` | 실험 모드 | `dev_full` |
| `--retrieval_setting` | 검색 전략 (`auto`, `manual`, `random`, `none`) | `auto` |

#### 실험 모드

| 모드 | 설명 |
|------|------|
| `vanilla` | 계획 및 개선 없이 직접 생성 |
| `dev_planner` | Planner → Visualizer |
| `dev_planner_stylist` | Planner → Stylist → Visualizer |
| `dev_planner_critic` | Planner → Visualizer → Critic (다중 라운드) |
| `dev_full` | 모든 에이전트를 포함한 전체 파이프라인 |
| `demo_planner_critic` | 데모 모드 (평가 제외) |
| `demo_full` | 데모 모드 (전체 파이프라인, 평가 제외) |

### 파이프라인 진행 상황 시각화

생성 과정의 중간 결과를 확인할 수 있습니다:

```bash
streamlit run visualize/show_pipeline_evolution.py
```

### 평가 결과 확인

생성된 이미지의 평가 결과를 확인할 수 있습니다:

```bash
streamlit run visualize/show_referenced_eval.py
```

---

## API 키 설정

### Google Gemini API 키 획득

1. [Google AI Studio](https://aistudio.google.com/app/apikey)에 접속
2. "Create API Key" 클릭
3. 생성된 API 키 복사
4. `configs/model_config.yaml`의 `google_api_key`에 붙여넣기

### OpenAI API 키 획득

1. [OpenAI Platform](https://platform.openai.com/api-keys)에 접속
2. 로그인 후 "Create new secret key" 클릭
3. 생성된 API 키 복사
4. `configs/model_config.yaml`의 `openai_api_key`에 붙여넣기

### Anthropic API 키 획득

1. [Anthropic Console](https://console.anthropic.com/)에 접속
2. 로그인 후 API 키 생성
3. 생성된 API 키 복사
4. `configs/model_config.yaml`의 `anthropic_api_key`에 붙여넣기

### 환경 변수로 설정 (선택)

YAML 파일 대신 환경 변수로 API 키를 설정할 수 있습니다:

**Windows (명령 프롬프트):**
```bash
set GOOGLE_API_KEY=your_key_here
set OPENAI_API_KEY=your_key_here
set ANTHROPIC_API_KEY=your_key_here
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your_key_here"
$env:OPENAI_API_KEY="your_key_here"
$env:ANTHROPIC_API_KEY="your_key_here"
```

**Mac/Linux:**
```bash
export GOOGLE_API_KEY="your_key_here"
export OPENAI_API_KEY="your_key_here"
export ANTHROPIC_API_KEY="your_key_here"
```

---

## 문제 해결

### 1. "uv가 설치되지 않았습니다" 오류

**원인**: uv 패키지 관리자가 설치되지 않았거나 PATH에 등록되지 않음

**해결 방법**:
1. [uv 공식 설치 페이지](https://docs.astral.sh/uv/getting-started/installation/)에서 설치
2. 설치 후 터미널/명령 프롬프트 재시작
3. `uv --version` 명령어로 설치 확인

### 2. "가상환경 활성화 실패" 오류

**원인**: 가상환경이 손상되었거나 Python이 제대로 설치되지 않음

**해결 방법**:
```bash
# 기존 가상환경 삭제
rm -rf .venv  # Mac/Linux
rmdir /s .venv  # Windows

# 다시 설정 스크립트 실행
setup.bat  # Windows
./setup.sh  # Mac/Linux
```

### 3. "패키지 설치 실패" 오류

**원인**: 인터넷 연결 문제 또는 패키지 호환성 문제

**해결 방법**:
1. 인터넷 연결 확인
2. `requirements.txt` 파일 확인
3. 다음 명령어로 수동 설치:
   ```bash
   source .venv/bin/activate  # Mac/Linux
   .venv\Scripts\activate.bat  # Windows
   uv pip install -r requirements.txt
   ```

### 4. "Streamlit 실행 실패" 오류

**원인**: Streamlit이 설치되지 않았거나 포트가 사용 중

**해결 방법**:
1. 가상환경 활성화 확인
2. Streamlit 재설치:
   ```bash
   uv pip install streamlit
   ```
3. 다른 포트로 실행:
   ```bash
   streamlit run demo.py --server.port 8502
   ```

### 5. "API 키 오류" 또는 "인증 실패"

**원인**: API 키가 잘못되었거나 설정되지 않음

**해결 방법**:
1. `configs/model_config.yaml` 파일 확인
2. API 키가 올바르게 입력되었는지 확인
3. API 키의 공백 제거
4. 각 API 제공자의 콘솔에서 키 활성화 상태 확인

### 6. "모듈을 찾을 수 없음" 오류

**원인**: 필수 패키지가 설치되지 않음

**해결 방법**:
```bash
# 가상환경 활성화
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate.bat  # Windows

# 패키지 재설치
uv pip install -r requirements.txt
```

### 7. "포트 8501이 이미 사용 중" 오류

**원인**: 다른 Streamlit 인스턴스가 실행 중

**해결 방법**:
```bash
# 다른 포트로 실행
streamlit run demo.py --server.port 8502

# 또는 기존 프로세스 종료 (Mac/Linux)
lsof -ti:8501 | xargs kill -9

# 또는 기존 프로세스 종료 (Windows)
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### 8. "메모리 부족" 오류

**원인**: 시스템 메모리가 부족하거나 너무 많은 후보 생성

**해결 방법**:
1. 생성할 후보 개수 감소 (1-5개로 시작)
2. 다른 애플리케이션 종료
3. 시스템 메모리 확인

---

## 추가 정보

### 프로젝트 구조

```
PaperBanana/
├── .venv/                          # Python 가상환경
├── agents/                         # 에이전트 구현
│   ├── retriever_agent.py         # 참고 이미지 검색
│   ├── planner_agent.py           # 생성 계획 수립
│   ├── stylist_agent.py           # 스타일 적용
│   ├── visualizer_agent.py        # 이미지 생성
│   └── critic_agent.py            # 품질 개선
├── configs/
│   ├── model_config.template.yaml # 설정 템플릿
│   └── model_config.yaml          # 실제 설정 (생성됨)
├── data/                          # 데이터셋 (선택)
├── prompts/                       # 프롬프트 템플릿
├── utils/                         # 유틸리티 함수
├── visualize/                     # 시각화 도구
├── demo.py                        # Streamlit 데모
├── main.py                        # 명령줄 인터페이스
├── requirements.txt               # 패키지 의존성
├── setup.bat                      # Windows 설정 스크립트
├── setup.sh                       # Mac/Linux 설정 스크립트
├── start.bat                      # Windows 실행 스크립트
├── start.sh                       # Mac/Linux 실행 스크립트
└── DEPLOY.md                      # 이 파일
```

### 필수 패키지

| 패키지 | 용도 |
|--------|------|
| `streamlit` | 웹 인터페이스 |
| `google-genai` | Google Gemini API |
| `openai` | OpenAI API |
| `anthropic` | Anthropic API |
| `pillow` | 이미지 처리 |
| `numpy` | 수치 계산 |
| `pyyaml` | YAML 설정 파일 |
| `python-dotenv` | 환경 변수 관리 |
| `aiofiles` | 비동기 파일 I/O |
| `tqdm` | 진행률 표시 |

### 데이터셋 (선택)

더 나은 결과를 위해 PaperBananaBench 데이터셋을 다운로드할 수 있습니다:

1. [Hugging Face](https://huggingface.co/datasets/dwzhu/PaperBananaBench)에서 다운로드
2. `data/PaperBananaBench/` 디렉토리에 배치
3. Retriever 에이전트가 참고 이미지를 자동으로 검색합니다

### 성능 최적화

- **병렬 처리**: 여러 후보를 동시에 생성하여 시간 단축
- **API 동시성**: 높은 동시성을 지원하는 API 키 사용
- **로컬 캐싱**: 생성된 이미지는 자동으로 캐시됨

### 지원 및 피드백

- 문제 발생 시: [GitHub Issues](https://github.com/dwzhu-pku/PaperBanana/issues)
- 기능 제안: [GitHub Discussions](https://github.com/dwzhu-pku/PaperBanana/discussions)
- 논문: [arXiv:2601.23265](https://arxiv.org/abs/2601.23265)

---

## 남부 서버 배포 (팀 공용)

팀원들이 공용으로 사용할 수 있도록 남부 서버에 PaperBanana를 배포하는 방법입니다.

### 🎯 특징

- **사용자별 API Key**: 각 팀원이 자신의 API Key로 로그인
- **남부 네트워크만 접근**: 방화벽으로 외부 접근 차단
- **결과물 중앙 저장**: 생성된 이미지를 서버에 자동 저장

### 📋 사전 준비

**서버 요구사항:**
- OS: Ubuntu 20.04+ / CentOS 8+
- CPU: 4코어 이상
- RAM: 8GB 이상
- Docker & Docker Compose 설치

**팀원 준비물:**
- Google AI Studio API Key (개인별 발급)
- 남부 네트워크 접근 권한 (VPN 또는 사낧망)

### 🚀 배포 방법 (관리자용)

#### 1단계: Docker Compose 파일 생성

`docker-compose.server.yml` 파일을 생성합니다:

```yaml
version: '3.8'
services:
  paperbanana:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
    volumes:
      - ./results:/app/results
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 8G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

#### 2단계: 실행

```bash
# 저장소 클론
git clone https://github.com/dwzhu-pku/PaperBanana.git
cd PaperBanana

# Docker Compose 실행
docker-compose -f docker-compose.server.yml up -d

# 상태 확인
docker-compose ps
docker-compose logs -f
```

#### 3단계: 방화벽 설정

```bash
# 남부 네트워크만 허용 (예: 192.168.x.x)
sudo ufw allow from 192.168.0.0/16 to any port 8501

# 또는 특정 서브넷만 허용
sudo ufw allow from 10.0.0.0/8 to any port 8501
```

### 👥 팀원 사용 방법

#### 접속 정보

- **URL**: `http://서버IP:8501` (관리자에게 정확한 IP 문의)
- **VPN**: 외부에서 접근 시 VPN 연결 필요

#### 사용 절차

1. **브라우저로 접속**
   ```
   http://서버IP:8501
   ```

2. **API Key 설정**
   - 우측 상단 **"🔐 API 설정"** 버튼 클릭
   - [Google AI Studio](https://aistudio.google.com/app/apikey)에서 발급받은 API Key 입력
   - **"💾 저장"** 클릭

3. **사용 시작**
   - 후보 생성 탭에서 논문 내용 입력
   - 이미지 생성 및 다운로드

### ⚠️ 주의사항

**보안:**
- API Key는 각자 개인적으로 발급받아 사용
- API Key는 브라우저에만 저장되며 서버에 저장되지 않음
- 남부 네트워크에서만 접근 가능

**결과물:**
- 생성된 이미지는 서버의 `results/` 폴터에 자동 저장
- 중요한 이미지는 꼭 로컬에도 다운로드

**사용량:**
- 동시에 많은 사용자가 접속하면 느려질 수 있음
- API 비용은 각자 부담 (월 $1~$5 예상)

### 🔧 유지보수 (관리자용)

```bash
# 로그 확인
docker-compose logs -f paperbanana

# 재시작
docker-compose restart paperbanana

# 업데이트
git pull origin main
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# 결과물 백업
tar -czvf results-backup-$(date +%Y%m%d).tar.gz results/
```

---

**마지막 업데이트**: 2026년 2월

**라이선스**: Apache-2.0

**저자**: Dawei Zhu, Rui Meng, Yale Song, Xiyu Wei, Sujian Li, Tomas Pfister, Jinsung Yoon
