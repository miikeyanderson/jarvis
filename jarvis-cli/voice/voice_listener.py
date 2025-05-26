#!/usr/bin/env python3
"""Wake-word listener for J.A.R.V.I.S. voice interface."""

import os
import sys
import time
import json
import threading
import queue
import numpy as np
import pyaudio
from faster_whisper import WhisperModel
import wave


class WakeWordListener:
    """Always-on wake word detection using Whisper tiny model."""
    
    def __init__(self, wake_phrase="hey jarvis", model_size="tiny", device="cpu"):
        self.wake_phrase = wake_phrase.lower()
        self.model = WhisperModel(model_size, device=device)
        self.audio_queue = queue.Queue()
        self.running = False
        
        # Audio config
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.RECORD_SECONDS = 2  # Rolling buffer
        
        self.pa = pyaudio.PyAudio()
        
    def start_listening(self):
        """Start the wake word detection loop."""
        self.running = True
        
        # Start audio capture thread
        audio_thread = threading.Thread(target=self._audio_capture_loop)
        audio_thread.daemon = True
        audio_thread.start()
        
        print(f"Listening for wake phrase: '{self.wake_phrase}'", file=sys.stderr)
        
        # Main detection loop
        while self.running:
            try:
                audio_data = self._get_audio_window()
                if audio_data is not None:
                    transcript = self._transcribe(audio_data)
                    if transcript and self.wake_phrase in transcript.lower():
                        print(json.dumps({"event": "wake_word_detected", "transcript": transcript}))
                        sys.stdout.flush()
                        return True
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(json.dumps({"event": "error", "message": str(e)}), file=sys.stderr)
                
        return False
        
    def _audio_capture_loop(self):
        """Continuously capture audio into queue."""
        stream = self.pa.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        while self.running:
            try:
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                self.audio_queue.put(data)
            except Exception as e:
                print(json.dumps({"event": "audio_error", "message": str(e)}), file=sys.stderr)
                
        stream.stop_stream()
        stream.close()
        
    def _get_audio_window(self):
        """Get rolling audio window for analysis."""
        frames = []
        bytes_needed = int(self.RATE * self.RECORD_SECONDS * 2)  # 16-bit audio
        bytes_collected = 0
        
        while bytes_collected < bytes_needed:
            try:
                data = self.audio_queue.get(timeout=0.1)
                frames.append(data)
                bytes_collected += len(data)
            except queue.Empty:
                if not self.running:
                    return None
                    
        # Convert to numpy array
        audio_bytes = b''.join(frames)
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        return audio_np
        
    def _transcribe(self, audio_data):
        """Transcribe audio using Whisper."""
        segments, _ = self.model.transcribe(audio_data, language="en")
        transcript = " ".join([seg.text for seg in segments]).strip()
        return transcript
        
    def cleanup(self):
        """Clean up resources."""
        self.running = False
        self.pa.terminate()


def record_until_silence(duration=10, silence_threshold=1.0):
    """Record audio until silence is detected."""
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024
    )
    
    frames = []
    silent_chunks = 0
    max_silent_chunks = int(silence_threshold * 16000 / 1024)
    
    print(json.dumps({"event": "recording_started"}))
    sys.stdout.flush()
    
    for _ in range(0, int(16000 / 1024 * duration)):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)
        
        # Check for silence
        audio_chunk = np.frombuffer(data, dtype=np.int16)
        if np.abs(audio_chunk).mean() < 500:  # Silence threshold
            silent_chunks += 1
            if silent_chunks > max_silent_chunks:
                break
        else:
            silent_chunks = 0
            
    stream.stop_stream()
    stream.close()
    pa.terminate()
    
    # Save to temp file
    temp_path = "/tmp/jarvis_recording.wav"
    wf = wave.open(temp_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    print(json.dumps({"event": "recording_complete", "file": temp_path}))
    sys.stdout.flush()
    
    return temp_path


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--wake-phrase", default="hey jarvis", help="Wake phrase to detect")
    parser.add_argument("--record", action="store_true", help="Record audio after wake word")
    args = parser.parse_args()
    
    listener = WakeWordListener(wake_phrase=args.wake_phrase)
    
    try:
        if listener.start_listening():
            if args.record:
                record_until_silence()
    finally:
        listener.cleanup()