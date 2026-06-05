"""
input_merger.py

Build unified multimodal memory context.
"""


def build_memory_context(
    user_input: str,
    audio_context=None,
    image_context=None,
    profile_context=None,
    retrieved_memories=None,
):
    context_parts = []

    # user input

    if user_input:
        context_parts.append(user_input)

    # audio context

    if audio_context and isinstance(audio_context, dict):
        transcript = audio_context.get("transcript", "")
        emotion = audio_context.get("emotion", "")
        tones = audio_context.get("tones", [])

        if transcript:
            context_parts.append(f"The uploaded audio mentions: {transcript}")
        if emotion:
            context_parts.append(f"The emotional tone appears to be {emotion}.")
        if tones:
            context_parts.append(
                f"The conversation style suggests: {', '.join(tones)}."
            )

    # image context

    if image_context and isinstance(image_context, dict):
        caption = image_context.get("caption", "")
        if caption:
            context_parts.append(f"Visual clues suggest: {caption}")
    # profile context

    if profile_context and isinstance(profile_context, dict):
        profile_text = " ".join(
            [f"{key}: {value}" for key, value in profile_context.items()]
        )
        context_parts.append(profile_text)

    # memory context

    if retrieved_memories and isinstance(retrieved_memories, list):
        memory_text = " ".join([str(memory) for memory in retrieved_memories])
        context_parts.append(f"Relevant memory clues: {memory_text}")

    # final merged context
    return "\n".join(context_parts)
