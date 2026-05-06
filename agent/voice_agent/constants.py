from voice_agent.prompts.prompts import (
    build_mood_prompt,
    english_initial_prompt,
    french_initial_prompt,
    english_greetings,
    french_greetings,
    insufficient_info_english_end_messages,
    insufficient_info_french_end_messages,
)
from voice_agent.persona_config import (
    TIMEOUT_SECONDS,
    TIMEOUT_WARNING_TIME,
    SPEAK_DELAY,
    MAX_CALL_DURATION,
    CALL_DURATION_WARNING_TIME,
    DEFAULT_VOICE_ID as ELEVENLABS_DEFAULT_VOICE_ID,
)

mood_initial_prompts = {
    "english": english_initial_prompt,
    "french": french_initial_prompt,
}

mood_initial_greetings = {"english": english_greetings, "french": french_greetings}

mood_insufficient_info_end_messages = {
    "english": insufficient_info_english_end_messages,
    "french": insufficient_info_french_end_messages,
}
