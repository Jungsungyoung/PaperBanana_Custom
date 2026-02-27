# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Parallel Streamlit Demo for PaperVizAgent
Accepts user text input, duplicates it 10 times, and runs parallel processing
to generate multiple diagram candidates for comparison.
"""

import streamlit as st
import asyncio
import base64
import json
from io import BytesIO
from PIL import Image
from pathlib import Path
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

print("DEBUG: Importing agents...")
try:
    from agents.planner_agent import PlannerAgent
    print("DEBUG: Imported PlannerAgent")
    from agents.visualizer_agent import VisualizerAgent
    from agents.stylist_agent import StylistAgent
    from agents.critic_agent import CriticAgent
    from agents.retriever_agent import RetrieverAgent
    from agents.vanilla_agent import VanillaAgent
    from agents.polish_agent import PolishAgent
    print("DEBUG: Imported all agents")
    from utils import config
    from utils.paperviz_processor import PaperVizProcessor
    print("DEBUG: Imported utils")

    import yaml
    config_path = Path(__file__).parent / "configs" / "model_config.yaml"
    model_config_data = {}
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            model_config_data = yaml.safe_load(f) or {}

    def get_config_val(section, key, env_var, default=""):
        val = os.getenv(env_var)
        if not val and section in model_config_data:
            val = model_config_data[section].get(key)
        return val or default

except ImportError as e:
    print(f"DEBUG: ImportError: {e}")
    import traceback
    traceback.print_exc()
    raise e
except Exception as e:
    print(f"DEBUG: Exception during import: {e}")
    import traceback
    traceback.print_exc()
    raise e

st.set_page_config(
    layout="wide",
    page_title="PaperBanana 데모",
    page_icon="🍌"
)

def init_session_state():
    """세션 상태 초기화"""
    if 'api_configured' not in st.session_state:
        st.session_state.api_configured = False
    if 'google_api_key' not in st.session_state:
        st.session_state.google_api_key = ""
    if 'model_name' not in st.session_state:
        st.session_state.model_name = ""
    if 'image_model_name' not in st.session_state:
        st.session_state.image_model_name = ""

@st.dialog("🔐 API 설정")
def render_api_settings_dialog():
    """API 설정 다이얼로그 렌더링"""
    
    # 기존 설정값 로드
    default_api_key = get_config_val("api_keys", "google_api_key", "GOOGLE_API_KEY", "")
    default_model = get_config_val("defaults", "model_name", "MODEL_NAME", "gemini-2.0-flash-exp")
    default_image_model = get_config_val("defaults", "image_model_name", "IMAGE_MODEL_NAME", "gemini-2.0-flash-exp-image-generation")
    
    # 세션 상태 초기화
    if not st.session_state.google_api_key and default_api_key:
        st.session_state.google_api_key = default_api_key
    if not st.session_state.model_name and default_model:
        st.session_state.model_name = default_model
    if not st.session_state.image_model_name and default_image_model:
        st.session_state.image_model_name = default_image_model
    
    # 설정 상태 표시
    if st.session_state.api_configured or st.session_state.google_api_key:
        st.success("✅ API 설정 완료")
    else:
        st.warning("⚠️ API Key 미설정")
    
    st.divider()
    
    # API Key 입력
    api_key = st.text_input(
        "Google API Key",
        value=st.session_state.google_api_key,
        type="password",
        help="Google AI Studio에서 발급받은 API Key를 입력하세요",
        placeholder="AIza..."
    )
    
    # 모델 설정
    col1, col2 = st.columns(2)
    with col1:
        model_name = st.text_input(
            "텍스트 모델",
            value=st.session_state.model_name or "gemini-2.0-flash-exp",
            help="텍스트 생성에 사용할 모델명"
        )
    with col2:
        image_model_name = st.text_input(
            "이미지 모델",
            value=st.session_state.image_model_name or "gemini-2.0-flash-exp-image-generation",
            help="이미지 생성에 사용할 모델명"
        )
    
    # API Key 발급 안내
    with st.expander("📖 API Key 발급 방법"):
        st.markdown("""
        ### Google API Key 발급
        
        1. [Google AI Studio](https://aistudio.google.com/app/apikey) 접속
        2. Google 계정으로 로그인
        3. "Create API Key" 클릭
        4. 새 프로젝트 선택 또는 생성
        5. API Key 복사하여 위에 입력
        
        ### 참고 모델
        - **텍스트**: `gemini-2.0-flash-exp`
        - **이미지**: `gemini-2.0-flash-exp-image-generation`
        """)
    
    st.divider()
    
    # 버튼 영역
    col1, col2 = st.columns(2)
    
    with col1:
        # 설정 저장 버튼
        if st.button("💾 저장", type="primary", use_container_width=True):
            if not api_key:
                st.error("⚠️ API Key를 입력해주세요!")
            else:
                # 세션 상태 저장
                st.session_state.google_api_key = api_key
                st.session_state.model_name = model_name
                st.session_state.image_model_name = image_model_name
                st.session_state.api_configured = True
                
                # 환경 변수 설정
                os.environ["GOOGLE_API_KEY"] = api_key
                os.environ["MODEL_NAME"] = model_name
                os.environ["IMAGE_MODEL_NAME"] = image_model_name
                
                st.success("✅ API 설정이 저장되었습니다!")
                st.rerun()
    
    with col2:
        # 설정 초기화 버튼
        if st.button("🔄 초기화", use_container_width=True):
            st.session_state.google_api_key = ""
            st.session_state.model_name = ""
            st.session_state.image_model_name = ""
            st.session_state.api_configured = False
            st.info("설정이 초기화되었습니다.")
            st.rerun()

def render_api_settings():
    """API 설정 버튼 및 상태 표시 (헤더용)"""
    # 설정 상태 확인
    is_configured = st.session_state.api_configured or st.session_state.google_api_key
    
    # 버튼 레이블 및 아이콘 설정
    if is_configured:
        button_label = "🔐 API 설정"
        button_type = "secondary"
    else:
        button_label = "⚠️ API 설정"
        button_type = "primary"
    
    # API 설정 버튼 클릭 시 다이얼로그 열기
    if st.button(button_label, type=button_type, key="api_settings_btn"):
        render_api_settings_dialog()
    
    # 현재 설정값 반환
    return (
        st.session_state.google_api_key,
        st.session_state.model_name or "gemini-2.0-flash-exp",
        st.session_state.image_model_name or "gemini-2.0-flash-exp-image-generation"
    )

def clean_text(text):
    """Clean text by removing invalid UTF-8 surrogate characters."""
    if not text:
        return text
    if isinstance(text, str):
        # Remove surrogate characters that cause UnicodeEncodeError
        return text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
    return text

def base64_to_image(b64_str):
    """Convert base64 string to PIL Image."""
    if not b64_str:
        return None
    try:
        if "," in b64_str:
            b64_str = b64_str.split(",")[1]
        image_data = base64.b64decode(b64_str)
        return Image.open(BytesIO(image_data))
    except Exception:
        return None

def create_sample_inputs(method_content, caption, diagram_type="Pipeline", aspect_ratio="16:9", num_copies=10, max_critic_rounds=3):
    """Create multiple copies of the input data for parallel processing."""
    base_input = {
        "filename": "demo_input",
        "caption": caption,
        "content": method_content,
        "visual_intent": caption,
        "additional_info": {
            "rounded_ratio": aspect_ratio
        },
        "max_critic_rounds": max_critic_rounds  # Add critic rounds control
    }
    
    # Create num_copies identical inputs, each with a unique identifier
    inputs = []
    for i in range(num_copies):
        input_copy = base_input.copy()
        input_copy["filename"] = f"demo_input_candidate_{i}"
        input_copy["candidate_id"] = i
        inputs.append(input_copy)
    
    return inputs

async def process_parallel_candidates(data_list, exp_mode="dev_planner_critic", retrieval_setting="auto", model_name=""):
    """Process multiple candidates in parallel using PaperVizProcessor."""
    # Create experiment config
    exp_config = config.ExpConfig(
        dataset_name="Demo",
        split_name="demo",
        exp_mode=exp_mode,
        retrieval_setting=retrieval_setting,
        model_name=model_name,
        work_dir=Path(__file__).parent,
    )
    
    # Initialize processor with all agents
    processor = PaperVizProcessor(
        exp_config=exp_config,
        vanilla_agent=VanillaAgent(exp_config=exp_config),
        planner_agent=PlannerAgent(exp_config=exp_config),
        visualizer_agent=VisualizerAgent(exp_config=exp_config),
        stylist_agent=StylistAgent(exp_config=exp_config),
        critic_agent=CriticAgent(exp_config=exp_config),
        retriever_agent=RetrieverAgent(exp_config=exp_config),
        polish_agent=PolishAgent(exp_config=exp_config),
    )
    
    # Process all candidates in parallel (concurrency controlled by processor)
    results = []
    concurrent_num = 10  # Process all 10 in parallel
    
    async for result_data in processor.process_queries_batch(
        data_list, max_concurrent=concurrent_num, do_eval=False
    ):
        results.append(result_data)
    
    return results

async def refine_image_with_nanoviz(image_bytes, edit_prompt, aspect_ratio="21:9", image_size="2K"):
    """
    Refine an image using an Image Editing API.
    
    Args:
        image_bytes: Image data in bytes
        edit_prompt: Text description of desired changes
        aspect_ratio: Output aspect ratio (21:9, 16:9, 3:2)
        image_size: Output resolution (2K or 4K)
    
    Returns:
        Tuple of (edited_image_bytes, success_message)
    """
    try:
        from google import genai
        from google.genai import types
        
        # Initialize client with API key (not Vertex AI)
        api_key = get_config_val("api_keys", "google_api_key", "GOOGLE_API_KEY", "")
        if not api_key:
            return None, "❌ 오류: Google API 키를 찾을 수 없습니다. configs/model_config.yaml에 설정해주세요."
        
        client = genai.Client(api_key=api_key)
        
        # Prepare content
        contents = [
            types.Part.from_text(text=edit_prompt),
            types.Part.from_bytes(
                mime_type="image/jpeg",
                data=image_bytes
            )
        ]
        
        # Configure generation
        config = types.GenerateContentConfig(
            temperature=1.0,
            max_output_tokens=8192,
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=image_size,
            ),
        )
        
        # Generate refined image
        image_model = get_config_val("defaults", "image_model_name", "IMAGE_MODEL_NAME", "")
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=image_model,
            contents=contents,
            config=config
        )
        
        # Extract image from response
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    edited_image_data = part.inline_data.data
                    
                    if isinstance(edited_image_data, bytes):
                        return edited_image_data, "✅ 이미지 개선 완료!"
                    elif isinstance(edited_image_data, str):
                        return base64.b64decode(edited_image_data), "✅ 이미지 개선 완료!"
        
        return None, "❌ 응답에서 이미지 데이터를 찾을 수 없습니다."
    
    except Exception as e:
        return None, f"❌ 오류: {str(e)}"


def get_evolution_stages(result, exp_mode):
    """Extract all evolution stages (images and descriptions) from the result."""
    task_name = "diagram"
    stages = []
    
    # Stage 1: Planner output
    planner_img_key = f"target_{task_name}_desc0_base64_jpg"
    planner_desc_key = f"target_{task_name}_desc0"
    if planner_img_key in result and result[planner_img_key]:
        stages.append({
            "name": "📋 기획자(Planner)",
            "image_key": planner_img_key,
            "desc_key": planner_desc_key,
            "description": "방법론 내용을 기반으로 한 초기 도식화 계획"
        })
    
    # Stage 2: Stylist output (only for demo_full)
    if exp_mode == "demo_full":
        stylist_img_key = f"target_{task_name}_stylist_desc0_base64_jpg"
        stylist_desc_key = f"target_{task_name}_stylist_desc0"
        if stylist_img_key in result and result[stylist_img_key]:
            stages.append({
                "name": "✨ 스타일리스트(Stylist)",
                "image_key": stylist_img_key,
                "desc_key": stylist_desc_key,
                "description": "스타일적으로 개선된 설명"
            })
    
    # Stage 3+: Critic iterations
    for round_idx in range(4):  # Check up to 4 rounds
        critic_img_key = f"target_{task_name}_critic_desc{round_idx}_base64_jpg"
        critic_desc_key = f"target_{task_name}_critic_desc{round_idx}"
        critic_sugg_key = f"target_{task_name}_critic_suggestions{round_idx}"
        
        if critic_img_key in result and result[critic_img_key]:
            stages.append({
                "name": f"🔍 평가자(Critic) 라운드 {round_idx}",
                "image_key": critic_img_key,
                "desc_key": critic_desc_key,
                "suggestions_key": critic_sugg_key,
                "description": f"평가자 피드백 후 개선 (반복 {round_idx})"
            })
    
    return stages

def display_candidate_result(result, candidate_id, exp_mode):
    """단일 후보 결과를 표시합니다."""
    task_name = "diagram"
    
    # Determine which image to show based on exp_mode
    # For demo modes, always try to find the last critic round
    final_image_key = None
    final_desc_key = None
    
    # Try to find the last critic round
    for round_idx in range(3, -1, -1):  # Check rounds 3, 2, 1, 0
        image_key = f"target_{task_name}_critic_desc{round_idx}_base64_jpg"
        if image_key in result and result[image_key]:
            final_image_key = image_key
            final_desc_key = f"target_{task_name}_critic_desc{round_idx}"
            break
    
    # Fallback if no critic rounds completed
    if not final_image_key:
        if exp_mode == "demo_full":
            # demo_full uses stylist before visualizer
            final_image_key = f"target_{task_name}_stylist_desc0_base64_jpg"
            final_desc_key = f"target_{task_name}_stylist_desc0"
        else:
            # demo_planner_critic uses planner output
            final_image_key = f"target_{task_name}_desc0_base64_jpg"
            final_desc_key = f"target_{task_name}_desc0"
    
    # Display the final image
    if final_image_key and final_image_key in result:
        img = base64_to_image(result[final_image_key])
        if img:
            st.image(img, use_container_width=True, caption=f"후보 {candidate_id} (최종)")
            
            # Add download button
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            st.download_button(
                label="⬇️ 다운로드",
                data=buffered.getvalue(),
                file_name=f"후보_{candidate_id}.png",
                mime="image/png",
                key=f"download_candidate_{candidate_id}",
                use_container_width=True
            )
        else:
            st.error(f"후보 {candidate_id}의 이미지 디코딩 실패")
    else:
        st.warning(f"후보 {candidate_id}에 대해 생성된 이미지가 없습니다.")
    
    # Show evolution timeline in an expander
    stages = get_evolution_stages(result, exp_mode)
    if len(stages) > 1:
        with st.expander(f"🔄 개선 과정 보기 ({len(stages)} 단계)", expanded=False):
            st.caption("파이프라인의 각 단계별로 도식화가 어떻게 개선되었는지 확인하세요")
            
            for idx, stage in enumerate(stages):
                st.markdown(f"### {stage['name']}")
                st.caption(stage['description'])
                
                # Display the image for this stage
                stage_img = base64_to_image(result.get(stage['image_key']))
                if stage_img:
                    st.image(stage_img, use_container_width=True)
                
                # Show description
                if stage['desc_key'] in result:
                    with st.expander(f"📝 설명", expanded=False):
                        cleaned_desc = clean_text(result[stage['desc_key']])
                        st.write(cleaned_desc)
                
                # Show critic suggestions if available
                if 'suggestions_key' in stage and stage['suggestions_key'] in result:
                    suggestions = result[stage['suggestions_key']]
                    with st.expander(f"💡 평가자 제안", expanded=False):
                        cleaned_sugg = clean_text(suggestions)
                        if cleaned_sugg.strip() == "No changes needed.":
                            st.success("✅ 변경 사항 없음 - 반복이 중지되었습니다.")
                        else:
                            st.write(cleaned_sugg)
                
                # Add separator between stages (except for the last one)
                if idx < len(stages) - 1:
                    st.divider()
    else:
        # If only one stage, show description in simpler expander
        with st.expander(f"📝 설명 보기", expanded=False):
            if final_desc_key and final_desc_key in result:
                # Clean the text to remove invalid UTF-8 characters
                cleaned_desc = clean_text(result[final_desc_key])
                st.write(cleaned_desc)
            else:
                st.info("설명이 없습니다")

def main():
    # 세션 상태 초기화
    init_session_state()
    
    # 헤더 영역: 제목과 API 설정 버튼을 나란히 배치
    header_col1, header_col2 = st.columns([6, 1])
    
    with header_col1:
        st.title("🍌 PaperBanana 데모")
        st.markdown("AI 기반 학술 도식화 자동 생성 및 개선")
    
    with header_col2:
        st.markdown("<br>", unsafe_allow_html=True)  # 버튼을 아래로 내리기 위한 여백
        # API 설정 버튼 렌더링
        api_key, model_name, image_model_name = render_api_settings()
    
    # Create tabs
    tab1, tab2 = st.tabs(["📊 후보 생성", "✨ 이미지 개선"])
    
    # ==================== TAB 1: Generate Candidates ====================
    with tab1:
        st.markdown("### 방법론 섹션과 캡션을 입력하여 여러 도식화 후보를 생성하세요")
        
        # API Key 체크
        if not st.session_state.api_configured and not get_config_val("api_keys", "google_api_key", "GOOGLE_API_KEY", ""):
            st.warning("⚠️ **API Key가 설정되지 않았습니다.** 우측 상단의 **🔐 API 설정** 버튼을 클릭하여 설정해주세요.")
            st.info("💡 API Key는 [Google AI Studio](https://aistudio.google.com/app/apikey)에서 물론 발급받을 수 있습니다.")
        
        # Sidebar configuration for Tab 1
        with st.sidebar:
            st.title("⚙️ 생성 설정")
            
            exp_mode = st.selectbox(
                "파이프라인 모드",
                ["demo_planner_critic", "demo_full"],
                index=0,
                key="tab1_exp_mode",
                help="사용할 에이전트 파이프라인을 선택하세요"
            )
            
            mode_info = {
                "demo_planner_critic": "기획자 → 시각화자 → 평가자 → 시각화자",
                "demo_full": "검색자 → 기획자 → 스타일리스트 → 시각화자 → 평가자 → 시각화자. (스타일리스트가 미적으로 더 예쁜 다이어그램을 만들지만 과도하게 단순화될 수 있으므로, 두 모드를 모두 시도하여 더 나은 것을 선택하시는 것을 권장합니다)"
            }
            st.info(f"**파이프라인:** {mode_info[exp_mode]}")
            
            retrieval_setting = st.selectbox(
                "검색 설정",
                ["auto", "manual", "random", "none"],
                index=0,
                key="tab1_retrieval_setting",
                help="참조 다이어그램을 검색하는 방법: auto (자동 선택), manual (지정된 참조 사용), random (무작위 선택), none (검색 없음)"
            )
            
            num_candidates = st.number_input(
                "후보 개수",
                min_value=1,
                max_value=20,
                value=10,
                key="tab1_num_candidates",
                help="병렬로 생성할 후보의 수"
            )
            
            aspect_ratio = st.selectbox(
                "화면 비율",
                ["21:9", "16:9", "3:2"],
                key="tab1_aspect_ratio",
                help="생성될 다이어그램의 화면 비율"
            )
            
            max_critic_rounds = st.number_input(
                "최대 평가자 라운드",
                min_value=1,
                max_value=5,
                value=3,
                key="tab1_max_critic_rounds",
                help="평가자 개선 반복의 최대 횟수"
            )
            
            default_model = get_config_val("defaults", "model_name", "MODEL_NAME", "YOUR_MODEL_NAME_HERE")
            options = ["", default_model] if default_model else ["", "YOUR_MODEL_NAME_HERE"]
            
            model_name = st.selectbox(
                "모델 이름",
                options,
                index=0,
                key="tab1_model_name",
                help="추론에 사용할 모델 이름"
            )
        
        st.divider()
        
        # Input section
        st.markdown("## 📝 입력")
        
        # Example content
        example_method = r"""## Methodology: The PaperVizAgent Framework
        
        In this section, we present the architecture of PaperVizAgent, a reference-driven agentic framework for automated academic illustration. As illustrated in Figure \ref{fig:methodology_diagram}, PaperVizAgent orchestrates a collaborative team of five specialized agents—Retriever, Planner, Stylist, Visualizer, and Critic—to transform raw scientific content into publication-quality diagrams and plots. (See Appendix \ref{app_sec:agent_prompts} for prompts)

### Retriever Agent

Given the source context $S$ and the communicative intent $C$, the Retriever Agent identifies $N$ most relevant examples $\mathcal{E} = \{E_n\}_{n=1}^{N} \subset \mathcal{R}$ from the fixed reference set $\mathcal{R}$ to guide the downstream agents. As defined in Section \ref{sec:task_formulation}, each example $E_i \in \mathcal{R}$ is a triplet $(S_i, C_i, I_i)$.
To leverage the reasoning capabilities of VLMs, we adopt a generative retrieval approach where the VLM performs selection over candidate metadata:
$$
\mathcal{E} = \text{VLM}_{\text{Ret}} \left( S, C, \{ (S_i, C_i) \}_{E_i \in \mathcal{R}} \right)
$$
Specifically, the VLM is instructed to rank candidates by matching both research domain (e.g., Agent & Reasoning) and diagram type (e.g., pipeline, architecture), with visual structure being prioritized over topic similarity. By explicitly reasoned selection of reference illustrations $I_i$ whose corresponding contexts $(S_i, C_i)$ best match the current requirements, the Retriever provides a concrete foundation for both structural logic and visual style.

### Planner Agent

The Planner Agent serves as the cognitive core of the system. It takes the source context $S$, communicative intent $C$, and retrieved examples $\mathcal{E}$ as inputs. By performing in-context learning from the demonstrations in $\mathcal{E}$, the Planner translates the unstructured or structured data in $S$ into a comprehensive and detailed textual description $P$ of the target illustration:
$$
P = \text{VLM}_{\text{plan}}(S, C, \{ (S_i, C_i, I_i) \}_{E_i \in \mathcal{E}})
$$

### Stylist Agent

To ensure the output adheres to the aesthetic standards of modern academic manuscripts, the Stylist Agent acts as a design consultant.
A primary challenge lies in defining a comprehensive “academic style,” as manual definitions are often incomplete.
To address this, the Stylist traverses the entire reference collection $\mathcal{R}$ to automatically synthesize an *Aesthetic Guideline* $\mathcal{G}$ covering key dimensions such as color palette, shapes and containers, lines and arrows, layout and composition, and typography and icons (see Appendix \ref{app_sec:auto_summarized_style_guide} for the summarized guideline and implementation details). Armed with this guideline, the Stylist refines each initial description $P$ into a stylistically optimized version $P^*$:
$$
P^* = \text{VLM}_{\text{style}}(P, \mathcal{G})
$$
This ensures that the final illustration is not only accurate but also visually professional.

### Visualizer Agent

After receiving the stylistically optimized description $P^*$, the Visualizer Agent collaborates with the Critic Agent to render academic illustrations and iteratively refine their quality. The Visualizer Agent leverages an image generation model to transform textual descriptions into visual output. In each iteration $t$, given a description $P_t$, the Visualizer generates:
$$
I_t = \text{Image-Gen}(P_t)
$$
where the initial description $P_0$ is set to $P^*$.

### Critic Agent

The Critic Agent forms a closed-loop refinement mechanism with the Visualizer by closely examining the generated image $I_t$ and providing refined description $P_{t+1}$ to the Visualizer. Upon receiving the generated image $I_t$ at iteration $t$, the Critic inspects it against the original source context $(S, C)$ to identify factual misalignments, visual glitches, or areas for improvement. It then provides targeted feedback and produces a refined description $P_{t+1}$ that addresses the identified issues:
$$
P_{t+1} = \text{VLM}_{\text{critic}}(I_t, S, C, P_t)
$$
This revised description is then fed back to the Visualizer for regeneration. The Visualizer-Critic loop iterates for $T=3$ rounds, with the final output being $I = I_T$. This iterative refinement process ensures that the final illustration meets the high standards required for academic dissemination.

### Extension to Statistical Plots

The framework extends to statistical plots by adjusting the Visualizer and Critic agents. For numerical precision, the Visualizer converts the description $P_t$ into executable Python Matplotlib code: $I_t = \text{VLM}_{\text{code}}(P_t)$. The Critic evaluates the rendered plot and generates a refined description $P_{t+1}$ addressing inaccuracies or imperfections: $P_{t+1} = \text{VLM}_{\text{critic}}(I_t, S, C, P_t)$. The same $T=3$ round iterative refinement process applies. While we prioritize this code-based approach for accuracy, we also explore direct image generation in Section \ref{sec:discussion}. See Appendix \ref{app_sec:plot_agent_prompt} for adjusted prompts."""

        example_caption = "Figure 1: Overview of our PaperVizAgent framework. Given the source context and communicative intent, we first apply a Linear Planning Phase to retrieve relevant reference examples and synthesize a stylistically optimized description. We then use an Iterative Refinement Loop (consisting of Visualizer and Critic agents) to transform the description into visual output and conduct multi-round refinements to produce the final academic illustration."
        
        col_input1, col_input2 = st.columns([3, 2])
        
        with col_input1:
            # Example selector for method content
            method_example = st.selectbox(
                "예시 불러오기 (방법론)",
                ["없음", "PaperVizAgent 프레임워크"],
                key="method_example_selector"
            )
            
            # Set value based on example selection or session state
            if method_example == "PaperVizAgent 프레임워크":
                method_value = example_method
            else:
                method_value = st.session_state.get("method_content", "")
            
            method_content = st.text_area(
                "방법론 섹션 내용 (Markdown 권장)",
                value=method_value,
                height=250,
                placeholder="방법론 섹션 내용을 여기에 붙여넣으세요...",
                help="논문의 방법론 섹션을 입력하세요. Markdown 형식을 권장합니다."
            )
        
        with col_input2:
            # Example selector for caption
            caption_example = st.selectbox(
                "예시 불러오기 (캡션)",
                ["없음", "PaperVizAgent 프레임워크"],
                key="caption_example_selector"
            )
            
            # Set value based on example selection or session state
            if caption_example == "PaperVizAgent 프레임워크":
                caption_value = example_caption
            else:
                caption_value = st.session_state.get("caption", "")
            
            caption = st.text_area(
                "그림 캡션 (Markdown 권장)",
                value=caption_value,
                height=250,
                placeholder="그림 캡션을 입력하세요...",
                help="생성할 그림의 캡션 또는 설명을 입력하세요. Markdown 형식을 권장합니다."
            )
        
        # Process button
        if st.button("🚀 후보 생성", type="primary", use_container_width=True):
            # API Key 체크
            if not st.session_state.api_configured and not get_config_val("api_keys", "google_api_key", "GOOGLE_API_KEY", ""):
                st.error("⚠️ API Key가 설정되지 않았습니다. 우측 상단의 **🔐 API 설정** 버튼을 클릭하여 설정해주세요.")
            elif not method_content or not caption:
                st.error("방법론 내용과 캡션을 모두 입력해주세요!")
            else:
                # Save to session state
                st.session_state["method_content"] = method_content
                st.session_state["caption"] = caption
                
                with st.spinner(f"{num_candidates}개 후보를 병렬로 생성 중... 몇 분 정도 소요될 수 있습니다."):
                    # Create input data list
                    input_data_list = create_sample_inputs(
                        method_content=method_content,
                        caption=caption,
                        aspect_ratio=aspect_ratio,
                        num_copies=num_candidates,
                        max_critic_rounds=max_critic_rounds
                    )
                    
                    # Process in parallel
                    try:
                        results = asyncio.run(process_parallel_candidates(
                            input_data_list, 
                            exp_mode=exp_mode, 
                            retrieval_setting=retrieval_setting,
                            model_name=model_name
                        ))
                        st.session_state["results"] = results
                        st.session_state["exp_mode"] = exp_mode
                        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state["timestamp"] = timestamp_str
                        
                        # Save results to JSON file
                        try:
                            # Create results directory if it doesn't exist
                            results_dir = Path(__file__).parent / "results" / "demo"
                            results_dir.mkdir(parents=True, exist_ok=True)
                            
                            # Generate filename with timestamp
                            json_filename = results_dir / f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                            
                            # Save to JSON with proper encoding handling (like main.py)
                            with open(json_filename, "w", encoding="utf-8", errors="surrogateescape") as f:
                                json_string = json.dumps(results, ensure_ascii=False, indent=4)
                                # Clean invalid UTF-8 characters
                                json_string = json_string.encode("utf-8", "ignore").decode("utf-8")
                                f.write(json_string)
                            
                            st.session_state["json_file"] = str(json_filename)
                            st.success(f"✅ {len(results)}개 후보 생성 완료!")
                            st.info(f"💾 결과 저장 위치: `{json_filename.name}`")
                        except Exception as e:
                            st.warning(f"⚠️ {len(results)}개 후보는 생성되었지만 JSON 저장에 실패했습니다: {e}")
                    except Exception as e:
                        st.error(f"처리 중 오류 발생: {e}")
                        import traceback
                        st.code(traceback.format_exc())
        
        # Display results
        if "results" in st.session_state and st.session_state["results"]:
            results = st.session_state["results"]
            current_mode = st.session_state.get("exp_mode", exp_mode)
            timestamp = st.session_state.get("timestamp", "N/A")
            
            st.divider()
            st.markdown("## 🎨 생성된 후보")
            st.caption(f"생성 시간: {timestamp} | 파이프라인: {mode_info.get(current_mode, current_mode)}")
            
            # Show JSON file download if available
            if "json_file" in st.session_state:
                json_file_path = Path(st.session_state["json_file"])
                if json_file_path.exists():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.info(f"📄 결과 저장 위치: `{json_file_path.relative_to(Path.cwd())}`")
                    with col2:
                        with open(json_file_path, "r", encoding="utf-8") as f:
                            json_data = f.read()
                        st.download_button(
                            label="⬇️ JSON 다운로드",
                            data=json_data,
                            file_name=json_file_path.name,
                            mime="application/json",
                            use_container_width=True
                        )
            
            # Display results in a grid (3 columns)
            num_cols = 3
            num_results = len(results)
            
            for row_start in range(0, num_results, num_cols):
                cols = st.columns(num_cols)
                for col_idx in range(num_cols):
                    result_idx = row_start + col_idx
                    if result_idx < num_results:
                        with cols[col_idx]:
                            display_candidate_result(results[result_idx], result_idx, current_mode)
            
            # Add ZIP download button
            st.divider()
            st.markdown("### 💾 일괄 다운로드")
            
            try:
                import zipfile
                
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    task_name = "diagram"
                    
                    for candidate_id, result in enumerate(results):
                        
                        # Find the final image key (same logic as display)
                        final_image_key = None
                        
                        # Try to find the last critic round
                        for round_idx in range(3, -1, -1):
                            image_key = f"target_{task_name}_critic_desc{round_idx}_base64_jpg"
                            if image_key in result and result[image_key]:
                                final_image_key = image_key
                                break
                        
                        # Fallback if no critic rounds completed
                        if not final_image_key:
                            if current_mode == "demo_full":
                                final_image_key = f"target_{task_name}_stylist_desc0_base64_jpg"
                            else:
                                final_image_key = f"target_{task_name}_desc0_base64_jpg"
                        
                        if final_image_key and final_image_key in result:
                            img = base64_to_image(result[final_image_key])
                            if img:
                                img_buffer = BytesIO()
                                img.save(img_buffer, format="PNG")
                                zip_file.writestr(
                                    f"candidate_{candidate_id}.png",
                                    img_buffer.getvalue()
                                )
                
                zip_buffer.seek(0)
                st.download_button(
                    label="⬇️ ZIP 다운로드",
                    data=zip_buffer.getvalue(),
                    file_name=f"papervizagent_candidates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip",
                    use_container_width=True
                )
                st.success("ZIP 파일 다운로드 준비 완료!")
            except Exception as e:
                st.error(f"ZIP 파일 생성 실패: {e}")
    
    # ==================== TAB 2: Refine Image ====================
    with tab2:
        st.markdown("### 다이어그램을 고해상도(2K/4K)로 개선 및 확대")
        st.caption("후보에서 이미지를 업로드하거나 다이어그램을 업로드하고, 변경 사항을 설명한 후 고해상도 버전을 생성하세요")
        
        # Sidebar for refinement settings
        with st.sidebar:
            st.title("✨ 개선 설정")
            
            refine_resolution = st.selectbox(
                "목표 해상도",
                ["2K", "4K"],
                index=0,
                key="refine_resolution",
                help="해상도가 높을수록 시간이 더 걸리지만 더 나은 품질을 제공합니다"
            )
            
            refine_aspect_ratio = st.selectbox(
                "종횡비",
                ["21:9", "16:9", "3:2"],
                index=0,
                key="refine_aspect_ratio",
                help="개선된 이미지의 종횡비"
            )
        
        st.divider()
        
        # Upload section
        st.markdown("## 📤 이미지 업로드")
        uploaded_file = st.file_uploader(
            "이미지 파일 선택",
            type=["png", "jpg", "jpeg"],
            help="개선할 다이어그램을 업로드하세요"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            uploaded_image = Image.open(uploaded_file)
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 원본 이미지")
                st.image(uploaded_image, use_container_width=True)
            
            with col2:
                st.markdown("### 편집 지침")
                edit_prompt = st.text_area(
                    "원하는 변경 사항 설명",
                    height=200,
                    placeholder="예: '색상 구성표를 학술 논문 스타일에 맞게 변경' 또는 '텍스트를 더 크고 굵게 만들기' 또는 '모든 것을 그대로 유지되 더 높은 해상도로 출력'",
                    help="변경하고 싶은 내용을 설명하거나 '모든 것을 그대로 유지'를 사용하여 확대만 하세요",
                    key="edit_prompt"
                )
                
                if st.button("✨ 이미지 개선", type="primary", use_container_width=True):
                    if not edit_prompt:
                        st.error("편집 지침을 제공해주세요!")
                    else:
                        with st.spinner(f"{refine_resolution} 해상도로 이미지를 개선 중입니다... 약 1분이 소요될 수 있습니다."):
                            try:
                                # Convert PIL image to bytes
                                img_byte_arr = BytesIO()
                                # Convert RGBA to RGB if necessary (JPEG doesn't support alpha channel)
                                if uploaded_image.mode == 'RGBA':
                                    uploaded_image = uploaded_image.convert('RGB')
                                uploaded_image.save(img_byte_arr, format='JPEG')
                                image_bytes = img_byte_arr.getvalue()
                                
                                # Call nanoviz API
                                refined_bytes, message = asyncio.run(
                                    refine_image_with_nanoviz(
                                        image_bytes=image_bytes,
                                        edit_prompt=edit_prompt,
                                        aspect_ratio=refine_aspect_ratio,
                                        image_size=refine_resolution
                                    )
                                )
                                
                                if refined_bytes:
                                    st.session_state["refined_image"] = refined_bytes
                                    st.session_state["refine_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
                            except Exception as e:
                                st.error(f"개선 중 오류 발생: {e}")
                                import traceback
                                st.code(traceback.format_exc())
            
            # Display refined result if available
            if "refined_image" in st.session_state:
                st.divider()
                st.markdown("## 🎨 개선된 결과")
                st.caption(f"생성 시간: {st.session_state.get('refine_timestamp', 'N/A')} | 해상도: {refine_resolution}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 이전")
                    st.image(uploaded_image, use_container_width=True)
                
                with col2:
                    st.markdown(f"### 이후 ({refine_resolution})")
                    refined_image = Image.open(BytesIO(st.session_state["refined_image"]))
                    st.image(refined_image, use_container_width=True)
                    
                    # Download button
                    st.download_button(
                        label=f"⬇️ {refine_resolution} 이미지 다운로드",
                        data=st.session_state["refined_image"],
                        file_name=f"refined_{refine_resolution}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png",
                        use_container_width=True
                    )

if __name__ == "__main__":
    main()
