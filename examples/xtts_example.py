#!/usr/bin/env python3
"""
Example: generate speech with Coqui X-TTS v2 (or legacy TTS) by cloning a voice.

Usage:
  python examples/xtts_example.py \
    --model tts_models/multilingual/multi-dataset/xtts_v2 \
    --text "Hello from X-TTS v2" \
    --speaker /path/to/target/speaker.wav \
    --output output.wav

Notes:
- Ensure you have the required package installed: `pip install -r requirements.txt`.
- If you have a GPU, add `--gpu` to enable CUDA.
"""
import argparse
import sys
from pathlib import Path

try:
    from TTS.api import TTS
except Exception as e:
    print("Could not import TTS (Coqui). Install with: pip install TTS or xtts", file=sys.stderr)
    raise


def main() -> None:
    p = argparse.ArgumentParser(description="Coqui X-TTS v2 example (voice cloning)")
    p.add_argument("--model", required=True, help="Model id, e.g. tts_models/multilingual/multi-dataset/xtts_v2")
    p.add_argument("--text", required=True, help="Text to synthesize")
    p.add_argument("--speaker", required=False, help="Path to speaker wav for cloning (optional)")
    p.add_argument("--language", required=False, default="en", help="Language code (optional)")
    p.add_argument("--output", required=False, default="output.wav", help="Output WAV file path")
    p.add_argument("--gpu", action="store_true", help="Enable GPU (CUDA) if available")

    args = p.parse_args()

    model_id = args.model
    gpu_flag = args.gpu

    print(f"Loading model: {model_id} (gpu={gpu_flag})")
    tts = TTS(model_id, gpu=gpu_flag)

    out_path = Path(args.output)
    print(f"Synthesizing to {out_path}")

    kwargs = {}
    if args.speaker:
        kwargs["speaker_wav"] = args.speaker
    if args.language:
        kwargs["language"] = args.language

    # This mirrors the snippet you provided: cloning a voice using speaker_wav
    tts.tts_to_file(text=args.text, file_path=str(out_path), **kwargs)

    print("Done.")


if __name__ == "__main__":
    main()
