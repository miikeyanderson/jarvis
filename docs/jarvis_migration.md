# Migration Guide: Codex → J.A.R.V.I.S.

Welcome to the J.A.R.V.I.S. migration guide. This document covers the transition from the Codex CLI to J.A.R.V.I.S. (Just An Agentic, Rapidly-Verticalized Infrastructure System).

## What's Changed

### 1. Binary Name
- **Before**: `codex`
- **After**: `jarvis`

The `codex` alias remains available for backward compatibility during the transition period.

### 2. Package Name
- **Before**: `@openai/codex`
- **After**: `jarvis-cli`

Update your package.json dependencies:
```json
{
  "dependencies": {
    "jarvis-cli": "^0.1.0"
  }
}
```

### 3. Configuration Directory
- **Before**: `~/.codex/`
- **After**: `~/.jarvis/`

Configuration files have moved:
- `~/.codex/config.yaml` → `~/.jarvis/config.yaml`
- `~/.codex/instructions.md` → `~/.jarvis/instructions.md`
- `~/.codex/sessions/` → `~/.jarvis/sessions/`
- `~/.codex.env` → `~/.jarvis.env`

### 4. Environment Variables
All environment variables have been renamed:

| Before | After |
|--------|-------|
| `CODEX_RUST` | `JARVIS_RUST` |
| `CODEX_DEV` | `JARVIS_DEV` |
| `CODEX_QUIET_MODE` | `JARVIS_QUIET_MODE` |
| `CODEX_DISABLE_SANDBOX` | `JARVIS_DISABLE_SANDBOX` |
| `CODEX_DISABLE_PROJECT_DOC` | `JARVIS_DISABLE_PROJECT_DOC` |
| `CODEX_SANDBOX_NETWORK_DISABLED` | `JARVIS_SANDBOX_NETWORK_DISABLED` |
| `CODEX_UNSAFE_ALLOW_NO_SANDBOX` | `JARVIS_UNSAFE_ALLOW_NO_SANDBOX` |
| `CODEX_FPS_DEBUG` | `JARVIS_FPS_DEBUG` |

### 5. Log Files
- **Before**: `$TMPDIR/oai-codex/codex-cli-*.log`
- **After**: `$TMPDIR/jarvis/jarvis-cli-*.log`

### 6. New Features

#### Mission Console Splash
J.A.R.V.I.S. now displays a mission control splash screen on startup (disable with `JARVIS_QUIET_MODE=1`).

#### Voice Interface (Placeholder)
The `--voice` flag has been added as a placeholder for future voice integration:
```bash
jarvis --voice
# Output: 🔊 Voice interface coming soon. To enable, hook ElevenLabs into the output stream.
```

## Migration Steps

1. **Backup your configuration**:
   ```bash
   cp -r ~/.codex ~/.codex-backup
   ```

2. **Install J.A.R.V.I.S.**:
   ```bash
   npm install -g jarvis-cli
   ```

3. **Migrate configuration**:
   ```bash
   mv ~/.codex ~/.jarvis
   mv ~/.codex.env ~/.jarvis.env 2>/dev/null || true
   ```

4. **Update environment variables** in your shell profile:
   ```bash
   # Replace CODEX_ with JARVIS_ in ~/.bashrc, ~/.zshrc, etc.
   sed -i 's/CODEX_/JARVIS_/g' ~/.bashrc
   ```

5. **Update shell completions**:
   ```bash
   eval "$(jarvis completion bash)"  # or zsh/fish
   ```

## Usage Examples

### Before
```bash
codex "Write a Python script"
codex --auto-edit "fix the bug"
codex -m gpt-4 "analyze this code"
```

### After  
```bash
jarvis "deploy quantum-resistant authentication"
jarvis --auto-edit "optimize reactor core"
jarvis -m gpt-4o "analyze system architecture"
```

## Troubleshooting

- **Command not found**: Ensure `/usr/local/bin` or npm's global bin directory is in your PATH
- **Missing configuration**: J.A.R.V.I.S. will create new config files if they don't exist
- **API keys**: Your existing API keys in environment variables remain unchanged

## Support

Report issues at: https://github.com/miikeyanderson/jarvis/issues