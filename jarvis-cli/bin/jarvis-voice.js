#!/usr/bin/env node

/**
 * J.A.R.V.I.S. Voice Interface
 * Cinematic wake-up experience with continuous voice loop
 */

const { spawn } = require('child_process');
const path = require('path');
const readline = require('readline');
require('dotenv').config();

class JarvisVoice {
  constructor() {
    this.pythonPath = process.env.PYTHON_PATH || 'python3';
    this.voiceDir = path.join(__dirname, '..', 'voice');
    this.isRunning = false;
    this.currentProcess = null;
  }

  async start() {
    console.log('🎯 J.A.R.V.I.S. Voice Interface Starting...');
    
    // Check Python dependencies
    const depsCheck = await this.checkDependencies();
    if (!depsCheck) {
      console.error('❌ Missing Python dependencies. Please run:');
      console.error('   pip install pyaudio faster-whisper openai elevenlabs numpy');
      process.exit(1);
    }

    // Start wake word listener
    this.isRunning = true;
    await this.runWakeWordLoop();
  }

  async checkDependencies() {
    try {
      const checkScript = `
import sys
try:
    import pyaudio
    import faster_whisper
    import numpy
    print("OK")
except ImportError as e:
    print(f"MISSING: {e}", file=sys.stderr)
    sys.exit(1)
`;
      
      const result = await this.runPython(['-c', checkScript]);
      return result.stdout.trim() === 'OK';
    } catch {
      return false;
    }
  }

  async runWakeWordLoop() {
    while (this.isRunning) {
      try {
        // Listen for wake word
        console.log('👂 Listening for "Hey Jarvis"...');
        
        const listener = spawn(this.pythonPath, [
          path.join(this.voiceDir, 'voice_listener.py'),
          '--wake-phrase', 'hey jarvis'
        ]);
        
        this.currentProcess = listener;
        
        const wakeDetected = await new Promise((resolve) => {
          listener.stdout.on('data', (data) => {
            const output = data.toString();
            try {
              const event = JSON.parse(output);
              if (event.event === 'wake_word_detected') {
                console.log('✨ Wake word detected!');
                resolve(true);
              }
            } catch (e) {
              // Not JSON, ignore
            }
          });
          
          listener.stderr.on('data', (data) => {
            const output = data.toString();
            if (output.includes('Listening for wake phrase')) {
              // Expected output
            } else {
              console.error('Error:', output);
            }
          });
          
          listener.on('close', (code) => {
            if (code !== 0) {
              console.error(`Wake word listener exited with code ${code}`);
            }
            resolve(false);
          });
          
          // Handle Ctrl+C
          process.on('SIGINT', () => {
            this.cleanup();
            resolve(false);
          });
        });
        
        if (wakeDetected && this.isRunning) {
          await this.handleWakeWord();
        }
        
      } catch (error) {
        console.error('Error in wake word loop:', error);
        await this.sleep(1000);
      }
    }
  }

  async handleWakeWord() {
    try {
      // Play boot sound and get status
      const bootSequence = spawn(this.pythonPath, ['-c', `
import sys
import json
sys.path.insert(0, '${this.voiceDir}')
from voice_chain import play_boot_sound, get_system_status, VoiceChain

# Play boot sound
play_boot_sound()

# Get system status
status = get_system_status()

# Initialize voice chain
chain = VoiceChain()

# Generate and speak boot message
if 'error' not in status:
    message = "Systems online. All tests passing. Dev agent idle, growth agent idle. Awaiting command."
else:
    message = "Systems online. Awaiting command."
    
chain.speak(message)
print(json.dumps({"event": "boot_complete"}))
`]);

      await this.waitForProcess(bootSequence);
      
      // Start conversation loop
      await this.conversationLoop();
      
    } catch (error) {
      console.error('Error in wake word handler:', error);
    }
  }

  async conversationLoop() {
    console.log('🎤 Recording your command...');
    
    // Record user audio
    const recorder = spawn(this.pythonPath, [
      path.join(this.voiceDir, 'voice_listener.py'),
      '--record'
    ]);
    
    const audioFile = await new Promise((resolve) => {
      recorder.stdout.on('data', (data) => {
        try {
          const event = JSON.parse(data.toString());
          if (event.event === 'recording_complete') {
            resolve(event.file);
          }
        } catch (e) {
          // Ignore non-JSON
        }
      });
      
      recorder.on('close', () => resolve(null));
    });
    
    if (!audioFile) {
      console.error('Failed to record audio');
      return;
    }
    
    // Process audio through voice chain
    console.log('🤖 Processing your request...');
    
    const processor = spawn(this.pythonPath, ['-c', `
import sys
import json
sys.path.insert(0, '${this.voiceDir}')
from voice_chain import VoiceChain

chain = VoiceChain()
result = chain.process_audio('${audioFile}')

print(json.dumps({"event": "transcript", "text": result['transcript']}))

# Speak response
if result['response']:
    chain.speak(result['response'])
    
# Handle tool calls
if result.get('tool_calls'):
    for tc in result['tool_calls']:
        print(json.dumps({"event": "tool_call", "call": tc}))
        
# Check for goodbye intent
if 'goodbye' in result['transcript'].lower() or 'disengage' in result['transcript'].lower():
    print(json.dumps({"event": "goodbye"}))
`]);

    let shouldExit = false;
    const toolCalls = [];
    
    processor.stdout.on('data', (data) => {
      const lines = data.toString().split('\n').filter(l => l.trim());
      for (const line of lines) {
        try {
          const event = JSON.parse(line);
          
          if (event.event === 'transcript') {
            console.log(`📝 You said: "${event.text}"`);
          } else if (event.event === 'tool_call') {
            toolCalls.push(event.call);
          } else if (event.event === 'goodbye') {
            shouldExit = true;
          }
        } catch (e) {
          // Ignore non-JSON
        }
      }
    });
    
    await this.waitForProcess(processor);
    
    // Execute any tool calls
    for (const toolCall of toolCalls) {
      await this.executeToolCall(toolCall);
    }
    
    if (shouldExit) {
      console.log('👋 J.A.R.V.I.S. disengaging. Goodbye!');
      this.isRunning = false;
    }
  }

  async executeToolCall(toolCall) {
    try {
      const func = toolCall.function;
      if (func.name === 'run_jarvis_task') {
        const args = JSON.parse(func.arguments);
        console.log(`🚀 Executing task: ${args.task}`);
        
        // Run jarvis CLI command
        const jarvisCmd = spawn('node', [
          path.join(__dirname, 'jarvis'),
          'run',
          '--task', args.task
        ], {
          stdio: 'inherit'
        });
        
        await this.waitForProcess(jarvisCmd);
      }
    } catch (error) {
      console.error('Error executing tool call:', error);
    }
  }

  runPython(args) {
    return new Promise((resolve, reject) => {
      const proc = spawn(this.pythonPath, args);
      let stdout = '';
      let stderr = '';
      
      proc.stdout.on('data', (data) => { stdout += data.toString(); });
      proc.stderr.on('data', (data) => { stderr += data.toString(); });
      
      proc.on('close', (code) => {
        if (code === 0) {
          resolve({ stdout, stderr });
        } else {
          reject(new Error(`Python process exited with code ${code}: ${stderr}`));
        }
      });
    });
  }

  waitForProcess(proc) {
    return new Promise((resolve) => {
      proc.on('close', resolve);
    });
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  cleanup() {
    this.isRunning = false;
    if (this.currentProcess) {
      this.currentProcess.kill();
    }
  }
}

// Main execution
const jarvis = new JarvisVoice();

process.on('SIGINT', () => {
  console.log('\n⚡ Shutting down J.A.R.V.I.S. voice interface...');
  jarvis.cleanup();
  process.exit(0);
});

jarvis.start().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});