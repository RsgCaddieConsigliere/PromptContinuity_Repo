# 🧠 SOP Module: Integrating OpenAI Cookbook Examples into PromptContinuity

## Purpose
This SOP describes how to incorporate live OpenAI Cookbook examples into modular prompt engineering workflows, RAG automation, and SOP evaluation.

---

## 🔗 Referenced Examples from OpenAI Cookbook

| Feature | Notebook | Path |
|--------|----------|------|
| ✅ Model Selection | `model_selection_guide.ipynb` | `external/openai-cookbook/examples/partners/model_selection_guide/` |
| ✅ Function Calling | `Structured_Outputs_Intro.ipynb` | `external/openai-cookbook/examples/Structured_Outputs_Intro.ipynb` |
| ✅ Chained Reasoning | `Using_chained_calls_for_o1_structured_outputs.ipynb` | `external/openai-cookbook/examples/o1/` |
| ✅ Prompt Orchestration | `responses_api_tool_orchestration.ipynb` | `external/openai-cookbook/examples/responses_api/` |
| ✅ PDF-to-RAG | `Parse_PDF_docs_for_RAG.ipynb` | `external/openai-cookbook/examples/` |
| ✅ Meta Prompting | `Enhance_your_prompts_with_meta_prompting.ipynb` | `external/openai-cookbook/examples/` |

---

## Usage

1. Ensure submodules are initialized:
   ```bash
   git submodule update --init --recursive
   ```

2. Navigate to the desired notebook:
   ```bash
   cd external/openai-cookbook/examples/
   jupyter notebook
   ```

3. Copy patterns into your custom prompt chains or SOPs.

---

## Attribution
Content referenced from [OpenAI Cookbook](https://github.com/openai/openai-cookbook) under the MIT license.
