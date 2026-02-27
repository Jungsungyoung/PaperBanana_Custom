# PaperBanana 에이전트 설치 참고 가이드

> **목적**: AI 에이전트가 PaperBanana를 자동으로 설치할 수 있도록 단계별 프로세스를 문서화
> 
> **대상**: OpenCode Agent, Claude, GPT 등 AI 에이전트
> **환경**: Ubuntu 20.04+ / Windows 10+ / macOS 11+

---

## 📋 설치 전 체크리스트

### 1. 시스템 요구사항 확인
```bash
# 실행 전 반드시 확인할 것
- OS: Linux (권장), Windows, macOS
- CPU: 4코어 이상 (병렬 처리용)
- RAM: 8GB 이상 권장
- 디스크: 2GB 이상 여유
- 인터넷: API 호출용 연결 필수
- Docker: 서버 배포 시 필요
```

### 2. 사전 설치 확인 명령어
```bash
# Python 버전 확인 (3.10+ 필요)
python3 --version
# 또는
python --version

# Git 확인
git --version

# Docker 확인 (서버 배포 시)
docker --version
docker-compose --version

# 메모리 확인
free -h  # Linux
systeminfo | findstr "Total Physical Memory"  # Windows
```

---

## 🚀 표준 설치 프로세스 (로컬)

### Step 1: 저장소 클론
```bash
# 작업 디렉토리로 이동
cd /home/user/projects  # Linux
# 또는
cd C:\Users\User\Projects  # Windows

# 저장소 클론
git clone https://github.com/dwzhu-pku/PaperBanana.git
cd PaperBanana
```

**확인 포인트**:
- [ ] PaperBanana 디렉토리가 생성되었는가?
- [ ] demo.py 파일이 존재하는가?
- [ ] requirements.txt 파일이 존재하는가?

### Step 2: uv 설치 (Python 패키지 관리자)

**Linux/macOS**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
uv --version  # 설치 확인
```

**Windows**:
```powershell
# PowerShell 관리자 권한으로 실행
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# 터미널 재시작 후
uv --version
```

**확인 포인트**:
- [ ] `uv --version` 명령이 실행되는가?
- [ ] 버전 정보가 출력되는가?

**오류 시 대안**:
```bash
# uv 설치 실패 시 pip 사용
pip install uv
```

### Step 3: 초기 설정 실행

**Linux/macOS**:
```bash
chmod +x setup.sh
./setup.sh
```

**Windows**:
```cmd
setup.bat
```

**setup 스크립트가 하는 일**:
1. uv 설치 확인
2. Python 3.12 설치 (없는 경우)
3. 가상환경 생성 (.venv/)
4. requirements.txt 패키지 설치
5. configs/model_config.template.yaml → model_config.yaml 복사

**확인 포인트**:
- [ ] .venv/ 디렉토리가 생성되었는가?
- [ ] "Setup Complete!" 메시지가 출력되었는가?
- [ ] configs/model_config.yaml 파일이 생성되었는가?

### Step 4: 설정 파일 구성

**필수 설정** (configs/model_config.yaml):
```yaml
defaults:
  model_name: "gemini-2.0-flash-exp"
  image_model_name: "gemini-2.0-flash-exp-image-generation"

api_keys:
  google_api_key: ""  # 사용자에게 입력받아야 함
```

**에이전트 작업**:
```bash
# 설정 파일이 제대로 복사되었는지 확인
cat configs/model_config.yaml

# API Key는 사용자가 직접 입력해야 하므로
# 웹 UI에서 입력하는 방식을 안내하거나
# 환경변수로 설정할 수 있도록 안내
```

### Step 5: 실행 테스트

**Linux/macOS**:
```bash
chmod +x start.sh
./start.sh
```

**Windows**:
```cmd
start.bat
```

**확인 포인트**:
- [ ] "Starting PaperBanana Streamlit Demo" 메시지 출력
- [ ] "Browser will open automatically" 메시지 출력
- [ ] http://localhost:8501 접속 가능

**백그라운드 실행 (서버용)**:
```bash
# Linux/macOS
.venv/bin/python -m streamlit run demo.py --server.headless true &

# 프로세스 확인
ps aux | grep streamlit

# 종료 시
pkill -f streamlit
```

---

## 🖥️ 서버 배포 프로세스 (Docker)

### Step 1: Docker 설치 확인
```bash
docker --version
docker-compose --version

# 미설치 시 설치 (Ubuntu)
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
# 재로그인 필요
```

### Step 2: docker-compose.server.yml 생성
```bash
cat > docker-compose.server.yml << 'EOF'
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
EOF
```

### Step 3: Docker 이미지 빌드 및 실행
```bash
# 이미지 빌드
docker-compose -f docker-compose.server.yml build

# 실행
docker-compose -f docker-compose.server.yml up -d

# 상태 확인
docker-compose -f docker-compose.server.yml ps
docker-compose -f docker-compose.server.yml logs -f
```

### Step 4: 방화벽 설정
```bash
# 남부 네트워크만 허용 (예시)
sudo ufw allow from 192.168.0.0/16 to any port 8501
# 또는
sudo ufw allow from 10.0.0.0/8 to any port 8501

# 상태 확인
sudo ufw status
```

**확인 포인트**:
- [ ] `docker ps`에서 paperbanana 컨테이너가 실행 중인가?
- [ ] http://서버IP:8501 접속 가능한가?
- [ ] 방화벽에서 8501 포트가 열려있는가?

---

## 🔧 문제 해결 가이드

### 문제 1: "uv: command not found"
**원인**: uv가 PATH에 없음
**해결**:
```bash
# Linux/macOS
source $HOME/.cargo/env
export PATH="$HOME/.cargo/bin:$PATH"

# Windows
# PowerShell 재시작 또는
$env:PATH += ";$HOME\.cargo\bin"
```

### 문제 2: "permission denied" (setup.sh)
**원인**: 실행 권한 없음
**해결**:
```bash
chmod +x setup.sh start.sh
./setup.sh
```

### 문제 3: 가상환경 생성 실패
**원인**: Python 권한 문제 또는 기존 .venv 손상
**해결**:
```bash
# 기존 .venv 삭제
rm -rf .venv

# 수동으로 생성
uv venv
source .venv/bin/activate  # Linux/macOS
# 또는
.venv\Scripts\activate.bat  # Windows

# 패키지 설치
uv pip install -r requirements.txt
```

### 문제 4: 패키지 설치 실패
**원인**: 네트워크 문제 또는 의존성 충돌
**해결**:
```bash
# 가상환경 활성화 확인
which python  # Linux/macOS
where python  # Windows

# 수동 설치
uv pip install streamlit google-genai pillow numpy pyyaml python-dotenv
```

### 문제 5: 포트 8501 충돌
**원인**: 다른 Streamlit 인스턴스가 실행 중
**해결**:
```bash
# Linux/macOS: 프로세스 종료
lsof -ti:8501 | xargs kill -9

# Windows: 프로세스 종료
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# 다른 포트 사용
streamlit run demo.py --server.port 8502
```

### 문제 6: Windows 인코딩 오류
**원인**: UTF-8 미설정
**해결**:
```powershell
# PowerShell에서 실행
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
```

---

## ✅ 설치 완료 검증

### 검증 테스트 1: 기본 실행
```bash
# 프로세스 확인
ps aux | grep streamlit  # Linux/macOS
tasklist | findstr streamlit  # Windows

# 로그 확인
docker-compose logs -f paperbanana  # Docker
# 또는
tail -f ~/.streamlit/logs/*.log  # 로컬
```

### 검증 테스트 2: 웹 접속
```bash
# curl로 테스트
curl -I http://localhost:8501

# 응답 확인
# HTTP/1.1 200 OK 가 반환되어야 함
```

### 검증 테스트 3: API 설정 UI 확인
```bash
# 브라우저에서 접속 후 확인:
# 1. http://localhost:8501 접속
# 2. 우측 상단 "🔐 API 설정" 버튼 확인
# 3. 클릭 시 다이얼로그 열림 확인
```

---

## 📝 에이전트용 설치 스크립트

### 자동화 스크립트 (Linux/macOS)
```bash
#!/bin/bash
# install_paperbanana.sh

set -e  # 오류 발생 시 중단

echo "🍌 PaperBanana 설치 시작..."

# 1. 저장소 클론
if [ ! -d "PaperBanana" ]; then
    git clone https://github.com/dwzhu-pku/PaperBanana.git
fi
cd PaperBanana

# 2. uv 설치
if ! command -v uv &> /dev/null; then
    echo "📦 uv 설치 중..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# 3. 설정 실행
echo "⚙️ 초기 설정 중..."
chmod +x setup.sh
./setup.sh

# 4. 설정 파일 확인
if [ ! -f "configs/model_config.yaml" ]; then
    echo "⚠️ 설정 파일이 생성되지 않았습니다."
    exit 1
fi

# 5. 실행 테스트
echo "🚀 Streamlit 실행 테스트..."
.venv/bin/python -m streamlit run demo.py --server.headless true &
STREAMLIT_PID=$!

# 5초 대기 후 프로세스 확인
sleep 5
if ps -p $STREAMLIT_PID > /dev/null; then
    echo "✅ 설치 완료! http://localhost:8501 에서 접속 가능"
    echo "⚠️ API Key는 웹 UI에서 설정해주세요."
else
    echo "❌ 실행 실패"
    exit 1
fi
```

### 자동화 스크립트 (Windows PowerShell)
```powershell
# install_paperbanana.ps1

Write-Host "🍌 PaperBanana 설치 시작..." -ForegroundColor Green

# 1. 저장소 클론
if (-Not (Test-Path "PaperBanana")) {
    git clone https://github.com/dwzhu-pku/PaperBanana.git
}
Set-Location PaperBanana

# 2. uv 설치
if (-Not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "📦 uv 설치 중..." -ForegroundColor Yellow
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
}

# 3. 설정 실행
Write-Host "⚙️ 초기 설정 중..." -ForegroundColor Yellow
.\setup.bat

# 4. 실행 테스트
Write-Host "🚀 Streamlit 실행 테스트..." -ForegroundColor Yellow
$process = Start-Process -FilePath ".venv\Scripts\python.exe" -ArgumentList "-m", "streamlit", "run", "demo.py", "--server.headless", "true" -PassThru

Start-Sleep -Seconds 5

if (-Not $process.HasExited) {
    Write-Host "✅ 설치 완료! http://localhost:8501 에서 접속 가능" -ForegroundColor Green
    Write-Host "⚠️ API Key는 웹 UI에서 설정해주세요." -ForegroundColor Yellow
} else {
    Write-Host "❌ 실행 실패" -ForegroundColor Red
    exit 1
}
```

---

## 🎯 사용자 안내 메시지 템플릿

### 설치 완료 후 사용자에게 전달할 메시지
```
🎉 PaperBanana 설치가 완료되었습니다!

📍 접속 주소: http://localhost:8501

🔐 API Key 설정 방법:
1. 브라우저에서 http://localhost:8501 접속
2. 우측 상단 "🔐 API 설정" 버튼 클릭
3. Google AI Studio (https://aistudio.google.com/app/apikey)에서 
   발급받은 API Key 입력
4. "💾 저장" 클릭

💰 비용 안내:
- Google AI Studio 물론 티어: 월 1,500 requests
- 10개 후보 생성 시 약 $0.24 (₩330)

📖 사용 방법:
- "📊 후보 생성" 탭: 논문 내용 입력 → 이미지 생성
- "✨ 이미지 개선" 탭: 이미지 업로드 → 고해상도 변환

⚠️ 주의사항:
- API Key는 개인별로 발급받아 사용하세요
- 생성된 이미지는 results/ 폴터에 자동 저장됩니다
```

---

## 🔍 디버깅 정보 수집

설치 실패 시 수집할 정보:
```bash
# 시스템 정보
cat /etc/os-release  # Linux
systeminfo  # Windows
sw_vers  # macOS

# Python 정보
python --version
which python

# 설치 로그
cat setup.log 2>/dev/null || echo "로그 파일 없음"

# 에러 메시지
docker-compose logs  # Docker
.venv/bin/python -m streamlit run demo.py 2>&1 | head -50  # 로컬
```

---

**마지막 업데이트**: 2026년 2월
**버전**: 1.0
**검증 환경**: Ubuntu 22.04, Windows 11, macOS 14
