#!/usr/bin/env python3
"""Voice chain handler for cloud vs offline ASR & TTS."""

import os
import sys
import json
import subprocess
import tempfile
from typing import Optional, Dict, Any
import openai
from faster_whisper import WhisperModel


class VoiceChain:
    """Handles voice processing chain with fallback to offline mode."""
    
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.eleven_key = os.getenv("ELEVEN_API_KEY")
        self.offline_mode = not bool(self.openai_key)
        
        if self.offline_mode:
            print(json.dumps({"event": "offline_mode", "reason": "No OPENAI_API_KEY"}), file=sys.stderr)
            self.whisper = WhisperModel("medium", device="cpu")
            
    def process_audio(self, audio_path: str) -> Dict[str, Any]:
        """Process audio file through ASR and get response."""
        if self.offline_mode:
            return self._process_offline(audio_path)
        else:
            return self._process_cloud(audio_path)
            
    def _process_cloud(self, audio_path: str) -> Dict[str, Any]:
        """Process using GPT-4o voice API."""
        try:
            client = openai.OpenAI(api_key=self.openai_key)
            
            with open(audio_path, 'rb') as audio_file:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="json"
                )
                
            transcript = response.text
            
            # Get GPT-4o response
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": transcript}
                ],
                tools=[{
                    "type": "function",
                    "function": {
                        "name": "run_jarvis_task",
                        "description": "Execute a jarvis CLI task",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task": {"type": "string", "description": "Task description to pass to jarvis run"}
                            },
                            "required": ["task"]
                        }
                    }
                }],
                stream=True
            )
            
            # Process streaming response
            response_text = ""
            tool_calls = []
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    response_text += chunk.choices[0].delta.content
                    print(json.dumps({"event": "assistant_chunk", "text": chunk.choices[0].delta.content}))
                    sys.stdout.flush()
                    
                if chunk.choices[0].delta.tool_calls:
                    for tc in chunk.choices[0].delta.tool_calls:
                        tool_calls.append(tc)
                        
            return {
                "transcript": transcript,
                "response": response_text,
                "tool_calls": tool_calls
            }
            
        except Exception as e:
            print(json.dumps({"event": "cloud_error", "message": str(e)}), file=sys.stderr)
            return self._process_offline(audio_path)
            
    def _process_offline(self, audio_path: str) -> Dict[str, Any]:
        """Process using local Whisper and fallback LLM."""
        # Transcribe with Whisper
        segments, _ = self.whisper.transcribe(audio_path)
        transcript = " ".join([seg.text for seg in segments]).strip()
        
        # Use local LLM fallback (simplified response)
        response_text = self._generate_offline_response(transcript)
        
        return {
            "transcript": transcript,
            "response": response_text,
            "tool_calls": self._parse_offline_commands(transcript)
        }
        
    def _generate_offline_response(self, transcript: str) -> str:
        """Generate simple offline response."""
        transcript_lower = transcript.lower()
        
        if "status" in transcript_lower:
            return "Checking system status offline. All systems operational."
        elif "build" in transcript_lower or "test" in transcript_lower:
            return "I'll help you with that task. Let me process your request."
        elif "goodbye" in transcript_lower or "disengage" in transcript_lower:
            return "Disengaging voice interface. Goodbye."
        else:
            return "I understand. Processing your request in offline mode."
            
    def _parse_offline_commands(self, transcript: str) -> list:
        """Parse commands from transcript in offline mode."""
        transcript_lower = transcript.lower()
        
        if "build" in transcript_lower or "create" in transcript_lower:
            # Extract task description
            task = transcript.replace("build", "").replace("create", "").strip()
            return [{
                "function": {
                    "name": "run_jarvis_task",
                    "arguments": json.dumps({"task": task})
                }
            }]
            
        return []
        
    def speak(self, text: str, voice_id: str = "jarvis"):
        """Convert text to speech using available TTS."""
        if self.eleven_key:
            self._speak_elevenlabs(text, voice_id)
        else:
            self._speak_macos(text)
            
    def _speak_elevenlabs(self, text: str, voice_id: str):
        """Use ElevenLabs TTS."""
        try:
            from elevenlabs import generate, play, voices
            
            # Try to find Jarvis voice or use default
            available_voices = voices()
            jarvis_voice = next((v for v in available_voices if "jarvis" in v.name.lower()), None)
            
            if jarvis_voice:
                voice_id = jarvis_voice.voice_id
            else:
                voice_id = available_voices[0].voice_id if available_voices else "21m00Tcm4TlvDq8ikWAM"
                
            audio = generate(
                text=text,
                voice=voice_id,
                model="eleven_monolingual_v1"
            )
            
            play(audio)
            
        except Exception as e:
            print(json.dumps({"event": "elevenlabs_error", "message": str(e)}), file=sys.stderr)
            self._speak_macos(text)
            
    def _speak_macos(self, text: str):
        """Fallback to macOS say command."""
        try:
            subprocess.run(["say", "-v", "Daniel", text], check=True)
        except Exception as e:
            print(json.dumps({"event": "tts_error", "message": str(e)}), file=sys.stderr)
            
    def _get_system_prompt(self) -> str:
        """Get system prompt for GPT-4o."""
        return """You are J.A.R.V.I.S., an AI assistant for software development.

When the user asks you to perform tasks, you should:
1. Acknowledge their request professionally
2. Use the run_jarvis_task function to execute development tasks
3. Keep responses concise and action-oriented

Available commands:
- Building features
- Running tests  
- Checking system status
- Managing development workflow

Respond in character as a helpful AI assistant."""


def get_system_status() -> Dict[str, Any]:
    """Get current system status from jarvis CLI."""
    try:
        result = subprocess.run(
            ["node", "bin/jarvis", "status", "--json"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"error": "Failed to get status", "stderr": result.stderr}
            
    except Exception as e:
        return {"error": str(e)}
        

def play_boot_sound():
    """Play arc reactor startup sound."""
    sound_path = os.path.join(os.path.dirname(__file__), "assets", "arc_reactor_start.wav")
    
    if os.path.exists(sound_path):
        try:
            subprocess.run(["afplay", sound_path], check=True)
        except:
            pass  # Silently fail if audio playback not available
            

if __name__ == "__main__":
    # Test voice chain
    chain = VoiceChain()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test-tts":
        chain.speak("Systems online. All tests passing. Awaiting command.")
    else:
        print(json.dumps({"ready": True, "offline_mode": chain.offline_mode}))