# <div align="center">PaperBanana 🍌</div>
<div align="center">Dawei Zhu, Rui Meng, Yale Song, Xiyu Wei, Sujian Li, Tomas Pfister and Jinsung yoon
<br><br></div>

<div align="center">
<a href="https://huggingface.co/papers/2601.23265"><img src="assets/paper-page-xl.svg" alt="Paper page on HF"></a>
<a href="https://huggingface.co/datasets/dwzhu/PaperBananaBench"><img src="assets/dataset-on-hf-xl.svg" alt="Dataset on HF"></a>
</div>

> 안녕하세요! PaperBanana의 원본 버전은 이미 Google-Research에서 [PaperVizAgent](https://github.com/google-research/papervizagent)라는 이름으로 오픈 소스화되었습니다.
이 저장소는 해당 저장소의 내용을 포크(Fork)한 것으로, 학술 논문 도식화(Illustration)를 더 잘 지원하기 위해 지속적으로 발전시키는 것을 목표로 합니다. 비록 상당한 진전을 이루었지만, 더 신뢰할 수 있는 생성과 다양하고 복잡한 시나리오를 지원하기 위해서는 아직 갈 길이 멉니다. PaperBanana는 모든 연구자를 위해 학술 도식화를 돕는 완전한 오픈 소스 프로젝트를 지향합니다. 우리의 목표는 순수하게 커뮤니티에 기여하는 것이며, 현재로서는 상업적 목적으로 사용할 계획이 없습니다.

**PaperBanana**는 자동화된 학술 도식화 생성을 위한 레퍼런스 기반(Reference-driven) 멀티 에이전트 프레임워크입니다. 전문화된 에이전트들로 구성된 크리에이티브 팀처럼 작동하며, **Retriever (검색자), Planner (기획자), Stylist (스타일리스트), Visualizer (시각화 도구), Critic (비평가)** 에이전트들로 구성된 오케스트레이션 파이프라인을 통해 가공되지 않은 과학적 내용을 출판 가능한 수준의 다이어그램과 플롯으로 변환합니다. 이 프레임워크는 레퍼런스 예시로부터의 인컨텍스트 학습(In-context learning)과 반복적인 개선(Iterative refinement)을 활용하여 미적으로 훌륭하고 의미적으로 정확한 과학적 도식화를 생성합니다.

다음은 PaperBanana로 생성된 다이어그램과 플롯의 예시입니다:
![Examples](assets/teaser_figure.jpg)

## PaperBanana 개요 (Overview)

![PaperBanana Framework](assets/method_diagram.png)

PaperBanana는 구조화된 파이프라인 내에서 5개의 전문 에이전트를 조율하여 고품질의 학술 도식화를 생성합니다:

1. **Retriever Agent (검색자 에이전트)**: 큐레이션된 컬렉션에서 가장 관련성이 높은 레퍼런스 다이어그램을 식별하여 후속 에이전트들을 가이드합니다.
2. **Planner Agent (기획자 에이전트)**: 인컨텍스트 학습을 사용하여 논문의 방법론 내용과 전달하려는 의도를 포괄적인 텍스트 설명으로 변환합니다.
3. **Stylist Agent (스타일리스트 에이전트)**: 자동 합성된 스타일 가이드라인을 사용하여 학술적 미학 기준에 맞게 설명을 다듬습니다.
4. **Visualizer Agent (시각화 에이전트)**: 최신 이미지 생성 모델을 사용하여 텍스트 설명을 시각적 결과물로 변환합니다.
5. **Critic Agent (비평가 에이전트)**: Visualizer와 함께 다회차 반복 개선을 수행하는 폐쇄 루프(Closed-loop) 개선 메커니즘을 형성합니다.

## 빠른 시작 (Quick Start)

### Step 1: 저장소 복제 (Clone the Repo)
```bash
git clone https://github.com/dwzhu-pku/PaperBanana.git
cd PaperBanana
```

### Step 2: 설정 (Configuration)
PaperBanana는 YAML 설정 파일이나 환경 변수를 통한 API 키 설정을 지원합니다.

모든 사용자 설정을 외부화하기 위해 `configs/model_config.template.yaml` 파일을 `configs/model_config.yaml`로 복사하는 것을 권장합니다. 이 파일은 API 키와 설정을 안전하게 유지하기 위해 git에서 무시됩니다. `model_config.yaml` 파일에서 두 가지 모델 이름(`defaults.model_name` 및 `defaults.image_model_name`)을 입력하고, `api_keys` 아래에 최소 하나 이상의 API 키(예: Gemini 모델의 경우 `google_api_key`)를 설정하세요.

동시에 많은 후보를 생성해야 하는 경우, 높은 동시성을 지원하는 API 키가 필요합니다.

### Step 3: 데이터셋 다운로드 (Downloading the Dataset)
먼저 [PaperBananaBench](https://huggingface.co/datasets/dwzhu/PaperBananaBench)를 다운로드한 후, `data` 디렉토리(예: `data/PaperBananaBench/`) 아래에 배치하세요. 이 프레임워크는 데이터셋 없이도 Retriever Agent의 퓨샷 학습(Few-shot learning) 기능을 우회하여 정상적으로 작동하도록 설계되었습니다. 원본 PDF에 관심이 있다면 [PaperBananaDiagramPDFs](https://huggingface.co/datasets/dwzhu/PaperBananaDiagramPDFs)에서 다운로드할 수 있습니다.

### Step 4: 환경 설치 (Installing the Environment)
1. 파이썬 패키지 관리를 위해 `uv`를 사용합니다. [여기](https://docs.astral.sh/uv/getting-started/installation/)의 안내에 따라 `uv`를 설치하세요.

2. 가상 환경 생성 및 활성화
    ```bash
    uv venv # 현재 디렉토리의 .venv/ 아래에 가상 환경을 생성합니다.
    source .venv/bin/activate  # 윈도우의 경우 .venv\Scripts\activate
    ```

3. Python 3.12 설치
    ```bash
    uv python install 3.12
    ```

4. 필요한 패키지 설치
    ```bash
    uv pip install -r requirements.txt
    ```

### PaperBanana 실행하기 (Launch PaperBanana)

#### 대화형 데모 (Streamlit)
PaperBanana를 실행하는 가장 쉬운 방법은 대화형 Streamlit 데모를 이용하는 것입니다:
```bash
streamlit run demo.py
```

웹 인터페이스는 두 가지 주요 워크플로우를 제공합니다:

**1. Generate Candidates (후보 생성) 탭**:
- 논문의 방법론 섹션 내용(마크다운 권장)을 붙여넣고 그림 캡션(Caption)을 제공합니다.
- 설정(파이프라인 모드, 검색 설정, 후보 수, 종횡비, 비평 회수 등)을 구성합니다.
- "Generate Candidates"를 클릭하고 병렬 처리가 완료될 때까지 기다립니다.
- 진화 타임라인이 포함된 그리드에서 결과를 확인하고 개별 이미지 또는 전체 ZIP 파일을 다운로드합니다.

**2. Refine Image (이미지 개선) 탭**:
- 생성된 후보 이미지나 기존 다이어그램을 업로드합니다.
- 원하는 변경 사항을 설명하거나 업스케일링(Upscaling)을 요청합니다.
- 해상도(2K/4K)와 종횡비를 선택합니다.
- 개선된 고해상도 결과물을 다운로드합니다.

#### 명령줄 인터페이스 (Command-Line Interface)
명령줄에서도 PaperBanana를 실행할 수 있습니다:
```bash
# 기본 설정으로 실행
python main.py

# 사용자 정의 설정으로 실행
python main.py \
  --dataset_name "PaperBananaBench" \
  --task_name "diagram" \
  --split_name "test" \
  --exp_mode "dev_full" \
  --retrieval_setting "auto"
```

**사용 가능한 옵션:**
- `--dataset_name`: 사용할 데이터셋 (기본값: `PaperBananaBench`)
- `--task_name`: 작업 유형 - `diagram` 또는 `plot` (기본값: `diagram`)
- `--split_name`: 데이터셋 분할 (기본값: `test`)
- `--exp_mode`: 실험 모드 (아래 섹션 참조)
- `--retrieval_setting`: 검색 전략 - `auto`, `manual`, `random`, 또는 `none` (기본값: `auto`)

**실험 모드 (Experiment Modes):**
- `vanilla`: 기획이나 개선 없이 직접 생성
- `dev_planner`: Planner → Visualizer 전용
- `dev_planner_stylist`: Planner → Stylist → Visualizer
- `dev_planner_critic`: Planner → Visualizer → Critic (다회차)
- `dev_full`: 모든 에이전트가 포함된 전체 파이프라인
- `demo_planner_critic`: 평가 없는 데모 모드 (Planner → Visualizer → Critic)
- `demo_full`: 평가 없는 데모 모드 (전체 파이프라인)

### 시각화 도구 (Visualization Tools)

파이프라인의 진화 과정과 중간 결과를 확인합니다:
```bash
streamlit run visualize/show_pipeline_evolution.py
```
평가 결과를 확인합니다:
```bash
streamlit run visualize/show_referenced_eval.py
```

## 프로젝트 구조 (Project Structure)
```
├── .venv/
│   └── ...
├── data/
│   └── PaperBananaBench/
│       ├── diagram/
│       │   ├── images/
│       │   ├── pdfs/
│       │   ├── test.json
│       │   └── ref.json
│       └── plot/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── retriever_agent.py
│   ├── planner_agent.py
│   ├── stylist_agent.py
│   ├── visualizer_agent.py
│   ├── critic_agent.py
│   ├── vanilla_agent.py
│   └── polish_agent.py
├── prompts/
│   ├── __init__.py
│   ├── diagram_eval_prompts.py
│   └── plot_eval_prompts.py
├── style_guides/
│   ├── generate_category_style_guide.py
│   └── ...
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── paperviz_processor.py
│   ├── eval_toolkits.py
│   ├── generation_utils.py
│   └── image_utils.py
├── visualize/
│   ├── show_pipeline_evolution.py
│   └── show_referenced_eval.py
├── scripts/
│   ├── run_main.sh
│   ├── run_demo.sh
├── configs/
│   └── model_config.template.yaml
├── results/
│   ├── PaperBananaBench_diagram/
│   └── parallel_demo/
├── main.py
├── demo.py
└── README.md
```

## 주요 기능 (Key Features)

### 멀티 에이전트 파이프라인 (Multi-Agent Pipeline)
- **레퍼런스 기반 (Reference-Driven)**: 생성적 검색을 통해 큐레이션된 예시로부터 학습합니다.
- **반복적 개선 (Iterative Refinement)**: 품질의 점진적 향상을 위한 Critic-Visualizer 루프를 제공합니다.
- **스타일 인지 (Style-Aware)**: 자동으로 합성된 미학 가이드라인을 통해 학술적 품질을 보장합니다.
- **유연한 모드 (Flexible Modes)**: 다양한 사용 사례에 맞는 여러 실험 모드를 지원합니다.

### 대화형 데모 (Interactive Demo)
- **병렬 생성 (Parallel Generation)**: 최대 20개의 후보 다이어그램을 동시에 생성합니다.
- **파이프라인 시각화 (Pipeline Visualization)**: Planner → Stylist → Critic 단계를 거치는 진화 과정을 추적합니다.
- **고해상도 개선 (High-Resolution Refinement)**: 이미지 생성 API를 사용하여 2K/4K 해상도로 업스케일링합니다.
- **배치 내보내기 (Batch Export)**: 모든 후보를 PNG 또는 ZIP 파일로 다운로드합니다.

### 확장 가능한 설계 (Extensible Design)
- **모듈형 에이전트 (Modular Agents)**: 각 에이전트를 독립적으로 설정할 수 있습니다.
- **다양한 작업 지원 (Task Support)**: 개념 다이어그램과 데이터 플롯을 모두 처리합니다.
- **평가 프레임워크 (Evaluation Framework)**: 여러 지표를 사용하여 정답(Ground truth) 대비 내장된 평가 기능을 제공합니다.
- **비동기 처리 (Async Processing)**: 설정 가능한 동시성을 통해 효율적인 배치 처리를 지원합니다.

## 향후 계획 (TODO List)
- [ ] 수동으로 선택한 예시 사용 지원 및 사용자 친화적인 인터페이스 제공
- [ ] 통계 플롯 생성을 위한 코드 업로드
- [ ] 스타일 가이드라인에 기반한 기존 다이어그램 개선 코드 업로드
- [ ] 컴퓨터 과학 이외의 더 많은 분야를 지원하도록 레퍼런스 세트 확장

## 커뮤니티 지원 (Community Supports)
이 저장소의 릴리스 전후로, 이 작업을 재현하려는 여러 커뮤니티의 노력을 확인했습니다. 이러한 노력들은 우리가 매우 가치 있게 생각하는 독특한 관점들을 제시합니다. 다음의 훌륭한 기여들을 확인해 보시길 강력히 추천합니다 (누락된 것이 있다면 언제든 추가해 주세요):
- https://github.com/llmsresearch/paperbanana
- https://github.com/efradeca/freepaperbanana

또한, 이 방법론의 개발과 병행하여 자동화된 학술 도식화 생성을 탐구하는 많은 다른 연구들이 진행되고 있으며, 일부는 생성된 그림의 편집까지 가능하게 합니다. 이러한 기여들은 생태계에 필수적이며 주목할 가치가 있습니다:
- https://github.com/ResearAI/AutoFigure-Edit
- https://github.com/OpenDCAI/Paper2Any
- https://github.com/BIT-DataLab/Edit-Banana

전반적으로, 현재 모델들의 근본적인 능력이 자동화된 학술 도식화 생성 문제 해결에 훨씬 더 가까워졌다는 점에 고무되어 있습니다. 커뮤니티의 지속적인 노력을 통해, 가까운 미래에 학술 연구의 반복과 시각적 소통을 가속화할 고품질 자동 드로잉 도구를 갖게 될 것이라 믿습니다.

PaperBanana를 더욱 발전시키기 위한 커뮤니티의 기여를 진심으로 환영합니다!

## 라이선스 (License)
Apache-2.0

## 인용 (Citation)
이 저장소가 도움이 되었다면, 다음과 같이 저희 논문을 인용해 주세요:
```bibtex
@article{zhu2026paperbanana,
  title={PaperBanana: Automating Academic Illustration for AI Scientists},
  author={Zhu, Dawei and Meng, Rui and Song, Yale and Wei, Xiyu and Li, Sujian and Pfister, Tomas and Yoon, Jinsung},
  journal={arXiv preprint arXiv:2601.23265},
  year={2026}
}
```

## 면책 조항 (Disclaimer)
이것은 공식적으로 지원되는 Google 제품이 아닙니다. 이 프로젝트는 [Google Open Source Software Vulnerability Rewards Program](https://bughunters.google.com/open-source-security) 대상이 아닙니다.

우리의 목표는 순수하게 커뮤니티에 기여하는 것이며, 현재로서는 상업적 목적으로 사용할 계획이 없습니다. 핵심 방법론은 Google 인턴십 기간 동안 개발되었으며, 이러한 특정 워크플로우에 대해 Google에서 특허를 출원했습니다. 이는 오픈 소스 연구 활동에는 영향을 미치지 않지만, 유사한 로직을 사용하는 제3자의 상업적 애플리케이션은 제한될 수 있습니다.
