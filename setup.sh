#!/bin/bash
# ============================================================================
# PaperBanana 초기 설정 스크립트 (Mac/Linux)
# ============================================================================
# 이 스크립트는 PaperBanana 실행을 위한 초기 환경을 설정합니다:
#   1. uv 설치 확인
#   2. Python 가상환경 생성
#   3. 필수 패키지 설치
#   4. 설정 파일 복사
#
# 실행 권한 설정:
#   chmod +x setup.sh
#
# 실행 방법:
#   ./setup.sh
# ============================================================================

echo ""
echo "============================================================================"
echo "PaperBanana 초기 설정 시작"
echo "============================================================================"
echo ""

# uv 설치 확인
echo "[1/4] uv 설치 확인 중..."

if ! command -v uv &> /dev/null; then
    echo ""
    echo "오류: uv가 설치되지 않았습니다."
    echo ""
    echo "해결 방법:"
    echo "  1. https://docs.astral.sh/uv/getting-started/installation/ 방문"
    echo "  2. Mac/Linux용 uv 설치 명령어 실행:"
    echo "     curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "  3. 설치 후 이 스크립트를 다시 실행하세요"
    echo ""
    exit 1
fi

echo "uv 설치 확인 완료!"
echo ""

# 가상환경 생성
echo "[2/4] Python 가상환경 생성 중..."

if [ -d ".venv" ]; then
    echo "가상환경이 이미 존재합니다. 기존 환경을 사용합니다."
else
    uv venv
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "오류: 가상환경 생성 실패"
        echo ""
        exit 1
    fi
    
    echo "가상환경 생성 완료!"
fi

echo ""

# 가상환경 활성화
echo "[3/4] 가상환경 활성화 및 패키지 설치 중..."
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo ""
    echo "오류: 가상환경 활성화 실패"
    echo ""
    exit 1
fi

# 패키지 설치
uv pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "오류: 패키지 설치 실패"
    echo ""
    echo "해결 방법:"
    echo "  1. requirements.txt 파일이 존재하는지 확인하세요"
    echo "  2. 인터넷 연결을 확인하세요"
    echo "  3. 이 스크립트를 다시 실행하세요"
    echo ""
    exit 1
fi

echo "패키지 설치 완료!"
echo ""

# 설정 파일 복사
echo "[4/4] 설정 파일 복사 중..."

if [ -f "configs/model_config.yaml" ]; then
    echo "설정 파일이 이미 존재합니다. 기존 파일을 유지합니다."
else
    if [ -f "configs/model_config.template.yaml" ]; then
        cp configs/model_config.template.yaml configs/model_config.yaml
        
        if [ $? -ne 0 ]; then
            echo ""
            echo "경고: 설정 파일 복사 실패"
            echo "수동으로 다음을 실행하세요:"
            echo "  cp configs/model_config.template.yaml configs/model_config.yaml"
            echo ""
        else
            echo "설정 파일 복사 완료!"
        fi
    else
        echo ""
        echo "경고: model_config.template.yaml 파일을 찾을 수 없습니다."
        echo ""
    fi
fi

echo ""
echo "============================================================================"
echo "초기 설정 완료!"
echo "============================================================================"
echo ""
echo "다음 단계:"
echo "  1. configs/model_config.yaml 파일을 열어 API 키를 설정하세요"
echo "     - defaults.model_name: 사용할 모델명 (예: gemini-3-pro-preview)"
echo "     - defaults.image_model_name: 이미지 생성 모델명"
echo "     - api_keys: 필요한 API 키 입력"
echo ""
echo "  2. 다음 명령어로 Streamlit 데모를 실행하세요:"
echo "     ./start.sh"
echo ""
echo "  또는 명령줄에서 직접 실행:"
echo "     streamlit run demo.py"
echo ""
