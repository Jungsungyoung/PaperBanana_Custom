#!/bin/bash
# ============================================================================
# PaperBanana Streamlit 실행 스크립트 (Mac/Linux)
# ============================================================================
# 이 스크립트는 PaperBanana의 Streamlit 데모를 실행합니다.
# 사전 요구사항: setup.sh를 먼저 실행하여 환경을 설정해야 합니다.
#
# 실행 권한 설정:
#   chmod +x start.sh
#
# 실행 방법:
#   ./start.sh
# ============================================================================

echo ""
echo "============================================================================"
echo "PaperBanana Streamlit 데모 시작"
echo "============================================================================"
echo ""

# 가상환경 활성화
echo "[1/2] Python 가상환경 활성화 중..."
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo ""
    echo "오류: 가상환경 활성화 실패"
    echo "해결 방법: setup.sh를 먼저 실행하여 환경을 설정하세요."
    echo ""
    exit 1
fi

echo "가상환경 활성화 완료!"
echo ""

# Streamlit 실행
echo "[2/2] Streamlit 데모 실행 중..."
echo ""
echo "브라우저가 자동으로 열립니다. (기본값: http://localhost:8501)"
echo "종료하려면 Ctrl+C를 누르세요."
echo ""

streamlit run demo.py

if [ $? -ne 0 ]; then
    echo ""
    echo "오류: Streamlit 실행 실패"
    echo "해결 방법:"
    echo "  1. requirements.txt가 설치되었는지 확인하세요"
    echo "  2. setup.sh를 다시 실행해보세요"
    echo ""
    exit 1
fi
