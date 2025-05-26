import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

describe('J.A.R.V.I.S. Voice Interface', () => {
  let mockPython;
  
  beforeEach(() => {
    // Mock environment
    process.env.OPENAI_API_KEY = 'test-key';
    process.env.ELEVEN_API_KEY = 'test-eleven-key';
  });
  
  afterEach(() => {
    delete process.env.OPENAI_API_KEY;
    delete process.env.ELEVEN_API_KEY;
  });
  
  it('should detect wake word and trigger boot sequence', async () => {
    // Mock Python script that simulates wake word detection
    const mockScript = `
import json
import sys
import time

# Simulate wake word detection
time.sleep(0.1)
print(json.dumps({"event": "wake_word_detected", "transcript": "hey jarvis"}))
sys.stdout.flush()
`;
    
    const voiceScriptPath = path.join(__dirname, '..', 'bin', 'jarvis-voice.js');
    
    // Create a promise to capture output
    const output = await new Promise((resolve, reject) => {
      const outputs = [];
      const proc = spawn('node', [voiceScriptPath], {
        env: {
          ...process.env,
          PYTHON_MOCK_SCRIPT: mockScript
        }
      });
      
      proc.stdout.on('data', (data) => {
        outputs.push(data.toString());
      });
      
      proc.stderr.on('data', (data) => {
        const text = data.toString();
        if (text.includes('Wake word detected')) {
          proc.kill();
          resolve(outputs.join(''));
        }
      });
      
      // Timeout after 5 seconds
      setTimeout(() => {
        proc.kill();
        reject(new Error('Test timeout'));
      }, 5000);
    });
    
    expect(output).toContain('J.A.R.V.I.S. Voice Interface Starting');
  }, 10000);
  
  it('should handle missing Python dependencies gracefully', async () => {
    // Test with a Python environment that lacks dependencies
    const mockScript = `
import sys
sys.stderr.write("MISSING: No module named 'pyaudio'\\n")
sys.exit(1)
`;
    
    const voiceScriptPath = path.join(__dirname, '..', 'bin', 'jarvis-voice.js');
    
    const output = await new Promise((resolve) => {
      const outputs = [];
      const proc = spawn('node', [voiceScriptPath], {
        env: {
          ...process.env,
          PYTHON_MOCK_SCRIPT: mockScript
        }
      });
      
      proc.stderr.on('data', (data) => {
        outputs.push(data.toString());
      });
      
      proc.on('close', (code) => {
        resolve({
          code,
          output: outputs.join('')
        });
      });
    });
    
    expect(output.code).toBe(1);
    expect(output.output).toContain('Missing Python dependencies');
    expect(output.output).toContain('pip install');
  });
  
  it('should handle offline mode when no API keys present', async () => {
    delete process.env.OPENAI_API_KEY;
    
    const mockScript = `
import json
print(json.dumps({"ready": true, "offline_mode": true}))
`;
    
    // Just verify that the voice chain initializes in offline mode
    const voiceChainPath = path.join(__dirname, '..', 'voice', 'voice_chain.py');
    
    const output = await new Promise((resolve) => {
      const proc = spawn('python3', [voiceChainPath], {
        env: {
          ...process.env
        }
      });
      
      let output = '';
      proc.stdout.on('data', (data) => {
        output += data.toString();
      });
      
      proc.on('close', () => {
        resolve(output);
      });
    });
    
    const result = JSON.parse(output.trim());
    expect(result.offline_mode).toBe(true);
  });
});