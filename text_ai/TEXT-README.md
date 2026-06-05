# Text AI Module — ReMIND

## Author
Mubashar Tanveer

## Responsibility
This module handles all text-related AI services in ReMIND, including:
- Memory reconstruction
- Retrieval-Augmented Generation (RAG)
- NLP preprocessing
- Intent classification
- Entity extraction
- Conversational memory management
- Response evaluation
- AI text generation

## Pipeline Overview
User Input → NLP Processing → Intent Detection → Entity Extraction → Context Retrieval (RAG) → Prompt Engineering → Groq LLaMA 3 → Memory Reconstruction → Evaluation → UUID Output Storage

## Technologies Used
- Groq API
- LLaMA 3
- FAISS
- Sentence Transformers
- Python
- NumPy

## How to Run
1. Activate virtual environment
2. Add API keys to `.env`
3. Run:
   python -m text_ai.pipeline.pipeline

## Output
- Generated memory reconstruction text
- Metadata JSON
- Metrics JSON
- UUID-based session outputs

## Evaluation
Latency, readability, response quality, and context usage metrics are calculated for performance validation.

## Limitations
- Depends on external LLM APIs
- Long-term memory is not persistent
- Entity extraction is rule-based
- Requires internet for Groq API

## Future Improvements
- OpenAI integration
- Persistent conversational memory
- Memory graph system
- Multimodal reasoning
- Emotion-aware memory reconstruction
- Advanced entity linking
