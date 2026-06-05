import os
from voice_ai.preprocessing.format_converter import convert_to_wav
from voice_ai.preprocessing.audio_cleaner import clean_audio
from voice_ai.preprocessing.silence_trimmer import trim_silence
from voice_ai.transcription.elevenlabs_stt import transcribe_audio
from voice_ai.analysis.emotion_detector import detect_emotion
from voice_ai.analysis.tone_classifier import classify_tone
from voice_ai.evaluation.accuracy_evaluator import evaluate_transcription_quality
from voice_ai.evaluation.cost_tracker import estimate_audio_duration, estimate_stt_cost
from voice_ai.evaluation.latency_tracker import LatencyTracker
from voice_ai.utils.logger import get_logger

logger = get_logger("VoicePipeline")


def run_voice_pipeline(
    input_audio_path: str,
    response_text: str = None,
    force_refresh: bool = False,
    output_dir: str = None,
):

    logger.info("Starting voice preprocessing pipeline")

    # output directory
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(input_audio_path), "processed_audio")
    os.makedirs(output_dir, exist_ok=True)
    formatted_audio = os.path.join(output_dir, "formatted.wav")
    cleaned_audio = os.path.join(output_dir, "cleaned.wav")
    final_audio = os.path.join(output_dir, "Output.wav")

    # preprocessing
    convert_to_wav(input_audio_path, formatted_audio)
    clean_audio(formatted_audio, cleaned_audio)
    trim_silence(cleaned_audio, final_audio)
    logger.info("Preprocessing complete. Starting transcription")
    logger.info(f"Force refresh: {force_refresh}")

    # latency

    latency = LatencyTracker()
    latency.start()

    # STT
    stt_result = transcribe_audio(final_audio)
    transcript = stt_result["transcript"]
    print("TRANSCRIPT:", transcript)

    # emotion detection
    emotion_result = detect_emotion(transcript)

    # tone analysis
    tone_result = classify_tone(transcript)

    # quality metrics
    quality_metrics = evaluate_transcription_quality(transcript)

    latency.stop()

    # audio matrics
    duration = estimate_audio_duration(final_audio)
    estimated_cost = estimate_stt_cost(duration)

    # final response
    metadata = {
        "transcript": transcript,
        "language": (stt_result["language"]),
        "confidence": (stt_result["confidence"]),
        "spelling_accuracy": (stt_result["spelling_accuracy"]),
        "emotion": (emotion_result["emotion"]),
        "emotion_confidence": (emotion_result["emotion_confidence"]),
        "tones": (tone_result["tones"]),
        "tone_strength": (tone_result["tone_strength"]),
        "latency_sec": (latency.get_latency()),
        "audio_duration_sec": (duration),
        "estimated_cost_usd": (estimated_cost),
        "quality_metrics": (quality_metrics),
        "audio_path": (final_audio),
    }

    logger.info("Voice pipeline completed successfully")

    print(
        "Audio → STT → Emotion → Tone → Evaluation complete. Pipeline stable and working."
    )
    return metadata
