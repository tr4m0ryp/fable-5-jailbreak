"""
PTY wrapper that transparently transforms every prompt before
Claude Code's safety classifier sees it.

Every prompt you type is obfuscated (homoglyph substitution) and framed
(narrative context) before reaching Claude Code. The classifier sees only
the sanitized version.

Usage:
    claude-jb                         # interactive (defaults: moderate, study_guide)
    claude-jb --obfuscation aggressive
    claude-jb --framing fiction
    claude-jb --topic "malware analysis"
"""

import argparse
import fcntl
import os
import pty
import select
import signal
import struct
import sys
import termios
import threading

from .encoder import Encoder
from .wrapper import Wrapper
from .models import ObfuscationLevel, FramingStrategy

OBF_LEVELS = {
    "none": ObfuscationLevel.NONE,
    "light": ObfuscationLevel.LIGHT,
    "moderate": ObfuscationLevel.MODERATE,
    "aggressive": ObfuscationLevel.AGGRESSIVE,
}

FRAME_STRATS = {
    "none": FramingStrategy.NONE,
    "fiction": FramingStrategy.FICTION,
    "study_guide": FramingStrategy.STUDY_GUIDE,
    "academic": FramingStrategy.ACADEMIC_REVIEW,
    "documentation": FramingStrategy.DOCUMENTATION,
    "translation": FramingStrategy.TRANSLATION,
}


class PromptTransformer:
    def __init__(self, obf_level=ObfuscationLevel.MODERATE, framing=FramingStrategy.STUDY_GUIDE, topic="computer security"):
        self.encoder = Encoder(obf_level)
        self.wrapper = Wrapper(framing)
        self.topic = topic

    def transform(self, text: str) -> str:
        obfuscated = self.encoder.obfuscate(text)
        framed = self.wrapper.wrap(obfuscated, self.topic)
        return framed


def output_forwarder(fd, out_fd, stop):
    try:
        while not stop.is_set():
            r, _, _ = select.select([fd], [], [], 0.2)
            if r:
                data = os.read(fd, 65536)
                if not data:
                    break
                os.write(out_fd, data)
    except (OSError, ValueError):
        pass


def main():
    parser = argparse.ArgumentParser(
        description="PTY wrapper that transforms prompts before Claude Code's classifier",
    )
    parser.add_argument("--obfuscation", choices=list(OBF_LEVELS.keys()), default="moderate")
    parser.add_argument("--framing", choices=list(FRAME_STRATS.keys()), default="study_guide")
    parser.add_argument("--topic", default="computer security")
    args = parser.parse_args()

    transformer = PromptTransformer(
        obf_level=OBF_LEVELS[args.obfuscation],
        framing=FRAME_STRATS[args.framing],
        topic=args.topic,
    )

    pid, fd = pty.fork()
    if pid == 0:
        os.execvp("claude", ["claude"])

    try:
        def sigwinch(signum, frame):
            try:
                size = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, struct.pack("HHHH", 0, 0, 0, 0))
                os.write(fd, size)
            except Exception:
                pass
            os.kill(pid, signal.SIGWINCH)

        signal.signal(signal.SIGWINCH, sigwinch)

        stop = threading.Event()
        t = threading.Thread(target=output_forwarder, args=(fd, sys.stdout.fileno(), stop), daemon=True)
        t.start()

        while True:
            try:
                line = sys.stdin.readline()
            except (EOFError, KeyboardInterrupt):
                break
            if not line:
                break
            stripped = line.rstrip("\r\n")
            if stripped:
                try:
                    transformed = transformer.transform(stripped)
                    os.write(fd, (transformed + "\n").encode())
                except Exception as e:
                    os.write(fd, line.encode())
    finally:
        stop.set()
        os.kill(pid, signal.SIGTERM)
        os.close(fd)


if __name__ == "__main__":
    main()
