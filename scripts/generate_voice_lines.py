#!/usr/bin/env python3
"""
Voice Line Generator for Bennie Game
Uses ElevenLabs API to generate all 69 voice lines per playbook specification.

Requirements:
- pip install elevenlabs
- Set ELEVENLABS_API_KEY environment variable

Usage:
    python generate_voice_lines.py
    python generate_voice_lines.py --narrator-only
    python generate_voice_lines.py --bennie-only
    python generate_voice_lines.py --effects-only
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from elevenlabs.client import ElevenLabs
except ImportError:
    print("ERROR: elevenlabs package not installed.")
    print("Run: pip install elevenlabs")
    sys.exit(1)

# Configuration
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "BennieGame" / "BennieGame" / "Resources" / "Audio"

# Voice settings per playbook (85% speed = stability/similarity adjustments)
# Using dict format for new API
NARRATOR_SETTINGS = {
    "stability": 0.70,
    "similarity_boost": 0.75,
    "style": 0.0,
    "speed": 0.85  # 85% speaking rate per playbook
}

BENNIE_SETTINGS = {
    "stability": 0.65,
    "similarity_boost": 0.80,
    "style": 0.2,  # Slightly more expressive for character
    "speed": 0.85  # 85% speaking rate per playbook
}

# =============================================================================
# VOICE LINE DEFINITIONS (Per Playbook docs/playbook/03-voice-script.md)
# =============================================================================

NARRATOR_LINES = {
    # Loading Screen
    "narrator_loading_complete": "Wir sind gleich bereit zum Spielen.",

    # Player Selection
    "narrator_player_question": "Wie heißt du? Alexander oder Oliver?",
    "narrator_hello_alexander": "Hallo Alexander! Los geht's!",
    "narrator_hello_oliver": "Hallo Oliver! Los geht's!",

    # Home Screen
    "narrator_home_question": "Was möchtest du spielen?",

    # Activities
    "narrator_puzzle_start": "Mach das Muster nach!",
    "narrator_labyrinth_start": "Hilf Bennie den Weg finden!",
    "narrator_dice_start": "Wirf den Würfel!",

    # Number prompts (Würfel)
    "narrator_show_number_1": "Zeig mir die eins!",
    "narrator_show_number_2": "Zeig mir die zwei!",
    "narrator_show_number_3": "Zeig mir die drei!",
    "narrator_show_number_4": "Zeig mir die vier!",
    "narrator_show_number_5": "Zeig mir die fünf!",
    "narrator_show_number_6": "Zeig mir die sechs!",

    # Number prompts (Wähle die Zahl) - 1-10
    "narrator_choose_number_1": "Zeig mir die eins!",
    "narrator_choose_number_2": "Zeig mir die zwei!",
    "narrator_choose_number_3": "Zeig mir die drei!",
    "narrator_choose_number_4": "Zeig mir die vier!",
    "narrator_choose_number_5": "Zeig mir die fünf!",
    "narrator_choose_number_6": "Zeig mir die sechs!",
    "narrator_choose_number_7": "Zeig mir die sieben!",
    "narrator_choose_number_8": "Zeig mir die acht!",
    "narrator_choose_number_9": "Zeig mir die neun!",
    "narrator_choose_number_10": "Zeig mir die zehn!",

    # Treasure/YouTube
    "narrator_film_ab": "Film ab!",
}

BENNIE_LINES = {
    # Home Screen - First Visit
    "bennie_greeting_alexander": "Hi Alexander, ich bin Bennie!",
    "bennie_greeting_oliver": "Hi Oliver, ich bin Bennie!",
    "bennie_greeting_part2": "Wir lösen Aktivitäten um YouTube zu schauen.",

    # Home Screen - Return
    "bennie_return_part1": "Lösen wir noch mehr Aktivitäten.",
    "bennie_return_part2": "Dann können wir mehr YouTube schauen!",

    # Locked Activity
    "bennie_locked": "Das ist noch gesperrt.",

    # Puzzle Activity
    "bennie_puzzle_start": "Das packen wir!",
    "bennie_puzzle_hint_10s": "Wir können das, YouTube kommt bald.",
    "bennie_puzzle_hint_20s": "Welche Farbe fehlt noch?",

    # Labyrinth Activity
    "bennie_labyrinth_start": "Wie fange ich die Lemminge?",
    "bennie_labyrinth_wrong": "Da komme ich nicht durch.",
    "bennie_labyrinth_hint": "Wo ist der Anfang?",

    # Würfel Activity - Wrong answers
    "bennie_wrong_number_1": "Das ist die eins. Probier nochmal!",
    "bennie_wrong_number_2": "Das ist die zwei. Probier nochmal!",
    "bennie_wrong_number_3": "Das ist die drei. Probier nochmal!",
    "bennie_wrong_number_4": "Das ist die vier. Probier nochmal!",
    "bennie_wrong_number_5": "Das ist die fünf. Probier nochmal!",
    "bennie_wrong_number_6": "Das ist die sechs. Probier nochmal!",

    # Würfel Hints
    "bennie_dice_hint_10s": "Zähle die Punkte.",
    "bennie_dice_hint_20s": "Schau auf den Würfel.",
    "bennie_dice_hint_30s": "Wo ist die Zahl?",

    # Wähle Zahl Hints
    "bennie_choose_hint_10s": "Der Erzähler hat es gesagt.",
    "bennie_choose_hint_20s": "Wo ist die Zahl?",

    # Celebrations (every 5 coins)
    "bennie_celebration_5": "Wir haben schon fünf Goldmünzen!",
    "bennie_celebration_10": "Zehn Goldmünzen! Du kannst jetzt YouTube schauen.",
    "bennie_celebration_15": "Fünfzehn! Weiter so!",
    "bennie_celebration_20": "Zwanzig Münzen! Du bekommst Bonuszeit!",
    "bennie_celebration_25": "Fünfundzwanzig! Super!",
    "bennie_celebration_30": "Dreißig Münzen! Toll gemacht!",

    # Treasure Screen
    "bennie_treasure_under10": "Wir brauchen noch mehr Münzen.",
    "bennie_treasure_10to19": "Wir können fünf Minuten schauen!",
    "bennie_treasure_over20": "Wir können zwölf Minuten schauen!",

    # Video Player
    "bennie_video_1min_warning": "Noch eine Minute.",
    "bennie_video_time_up": "Die Zeit ist um. Lass uns spielen!",
}

SUCCESS_PHRASES = {
    "success_super": "Super!",
    "success_toll_gemacht": "Toll gemacht!",
    "success_wunderbar": "Wunderbar!",
    "success_ja_genau": "Ja, genau!",
    "success_das_hast_du": "Das hast du super gemacht!",
    "success_perfekt": "Perfekt!",
    "success_bravo": "Bravo!",
}

# =============================================================================
# GENERATION FUNCTIONS
# =============================================================================

def get_client():
    """Initialize ElevenLabs client."""
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY environment variable not set.")
        print("Set it with: export ELEVENLABS_API_KEY='your-api-key'")
        sys.exit(1)
    return ElevenLabs(api_key=api_key)


def list_voices(client):
    """List available voices to help select narrator and Bennie voices."""
    print("\nAvailable voices:")
    print("-" * 60)
    response = client.voices.get_all()
    for voice in response.voices:
        print(f"  {voice.name}: {voice.voice_id}")
        if voice.labels:
            print(f"    Labels: {voice.labels}")
    print("-" * 60)


def generate_audio(client, text, voice_id, settings, output_path):
    """Generate a single audio file using ElevenLabs text_to_speech API."""
    print(f"  Generating: {output_path.name}")
    print(f"    Text: \"{text}\"")

    try:
        # Use new API: client.text_to_speech.convert()
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",  # Best for German
            output_format="mp3_44100_128",
            voice_settings={
                "stability": settings["stability"],
                "similarity_boost": settings["similarity_boost"],
                "style": settings.get("style", 0.0),
                "speed": settings.get("speed", 1.0)
            }
        )

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save audio - audio is now a generator, write bytes directly
        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        print(f"    ✓ Saved: {output_path}")
        return True

    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False


def generate_narrator_lines(client, voice_id):
    """Generate all narrator voice lines."""
    print("\n" + "=" * 60)
    print("GENERATING NARRATOR LINES")
    print("=" * 60)

    output_base = OUTPUT_DIR / "Voice" / "Narrator"
    success_count = 0

    for filename, text in NARRATOR_LINES.items():
        output_path = output_base / f"{filename}.mp3"
        if generate_audio(client, text, voice_id, NARRATOR_SETTINGS, output_path):
            success_count += 1

    print(f"\nNarrator: {success_count}/{len(NARRATOR_LINES)} generated")
    return success_count


def generate_bennie_lines(client, voice_id):
    """Generate all Bennie voice lines."""
    print("\n" + "=" * 60)
    print("GENERATING BENNIE LINES")
    print("=" * 60)

    output_base = OUTPUT_DIR / "Voice" / "Bennie"
    success_count = 0

    for filename, text in BENNIE_LINES.items():
        output_path = output_base / f"{filename}.mp3"
        if generate_audio(client, text, voice_id, BENNIE_SETTINGS, output_path):
            success_count += 1

    print(f"\nBennie: {success_count}/{len(BENNIE_LINES)} generated")
    return success_count


def generate_success_phrases(client, voice_id):
    """Generate success phrases (can use either narrator or Bennie voice)."""
    print("\n" + "=" * 60)
    print("GENERATING SUCCESS PHRASES")
    print("=" * 60)

    output_base = OUTPUT_DIR / "Voice" / "Success"
    success_count = 0

    for filename, text in SUCCESS_PHRASES.items():
        output_path = output_base / f"{filename}.mp3"
        if generate_audio(client, text, voice_id, BENNIE_SETTINGS, output_path):
            success_count += 1

    print(f"\nSuccess phrases: {success_count}/{len(SUCCESS_PHRASES)} generated")
    return success_count


def main():
    parser = argparse.ArgumentParser(description="Generate voice lines for Bennie Game")
    parser.add_argument("--list-voices", action="store_true", help="List available voices")
    parser.add_argument("--narrator-voice", type=str, help="Voice ID for narrator")
    parser.add_argument("--bennie-voice", type=str, help="Voice ID for Bennie")
    parser.add_argument("--narrator-only", action="store_true", help="Generate narrator lines only")
    parser.add_argument("--bennie-only", action="store_true", help="Generate Bennie lines only")
    parser.add_argument("--success-only", action="store_true", help="Generate success phrases only")

    args = parser.parse_args()

    client = get_client()

    if args.list_voices:
        list_voices(client)
        return

    # Default voice IDs - UPDATE THESE after running --list-voices
    # Choose warm German voices from ElevenLabs
    narrator_voice = args.narrator_voice or os.environ.get("NARRATOR_VOICE_ID", "")
    bennie_voice = args.bennie_voice or os.environ.get("BENNIE_VOICE_ID", "")

    if not narrator_voice or not bennie_voice:
        print("ERROR: Voice IDs not configured.")
        print("\nSteps to configure:")
        print("1. Run: python generate_voice_lines.py --list-voices")
        print("2. Choose appropriate German voices")
        print("3. Set environment variables:")
        print("   export NARRATOR_VOICE_ID='voice-id-here'")
        print("   export BENNIE_VOICE_ID='voice-id-here'")
        print("\nOr pass them as arguments:")
        print("   --narrator-voice 'voice-id' --bennie-voice 'voice-id'")
        sys.exit(1)

    print("=" * 60)
    print("Bennie Game Voice Line Generator")
    print("=" * 60)
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Narrator voice: {narrator_voice}")
    print(f"Bennie voice: {bennie_voice}")

    total_success = 0
    total_lines = 0

    if args.narrator_only:
        total_success += generate_narrator_lines(client, narrator_voice)
        total_lines += len(NARRATOR_LINES)
    elif args.bennie_only:
        total_success += generate_bennie_lines(client, bennie_voice)
        total_lines += len(BENNIE_LINES)
    elif args.success_only:
        total_success += generate_success_phrases(client, bennie_voice)
        total_lines += len(SUCCESS_PHRASES)
    else:
        # Generate all
        total_success += generate_narrator_lines(client, narrator_voice)
        total_lines += len(NARRATOR_LINES)

        total_success += generate_bennie_lines(client, bennie_voice)
        total_lines += len(BENNIE_LINES)

        total_success += generate_success_phrases(client, bennie_voice)
        total_lines += len(SUCCESS_PHRASES)

    print("\n" + "=" * 60)
    print(f"COMPLETE: {total_success}/{total_lines} voice lines generated")
    print("=" * 60)

    if total_success < total_lines:
        print("\nSome files failed. Check errors above and retry.")
        sys.exit(1)


if __name__ == "__main__":
    main()
