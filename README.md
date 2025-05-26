# J.A.R.V.I.S. CLI – Mission Control Interface

```
     _   _   ____  __     _____ ____  
    | | / \ |  _ \ \ \   / /_ _/ ___| 
 _  | |/ _ \| |_) | \ \ / / | |\___ \ 
| |_| / ___ \  _ <   \ V /  | | ___) |
 \___/_/   \_\_| \_\  \_/  |___|____/ 

Mission Control CLI – Just An Agentic, Rapidly-Verticalized Infrastructure System
```

**Welcome to J.A.R.V.I.S.** – Your AI-powered mission control interface for development operations.

## Quick Deploy

```bash
npm i -g jarvis-cli
```

![J.A.R.V.I.S. demo GIF using: jarvis "analyze system architecture"](./.github/demo.gif)

---

<details>
<summary><strong>Mission Parameters</strong></summary>

<!-- Begin ToC -->

- [System Requirements](#system-requirements)
- [Deployment](#deployment)
- [Why J.A.R.V.I.S.?](#why-jarvis)
- [Security Protocols](#security-protocols)
  - [Containment Details](#containment-details)
- [Command Interface](#command-interface)
- [Memory Core & Documentation](#memory-core--documentation)
- [Autonomous Mode](#autonomous-mode)
- [Diagnostic Logging](#diagnostic-logging)
- [Mission Recipes](#mission-recipes)
- [Configuration Matrix](#configuration-matrix)
  - [Core Parameters](#core-parameters)
  - [AI Provider Configuration](#ai-provider-configuration)
  - [History Banks](#history-banks)
  - [Configuration Examples](#configuration-examples)
  - [Full System Configuration](#full-system-configuration)
  - [Custom Directives](#custom-directives)
  - [Environment Setup](#environment-setup)
- [FAQ](#faq)
- [Zero Data Retention](#zero-data-retention)
- [Contributing to J.A.R.V.I.S.](#contributing-to-jarvis)
  - [Engineering Workflow](#engineering-workflow)
  - [Git Integration](#git-integration)
  - [Debugging Protocols](#debugging-protocols)
  - [High-Impact Modifications](#high-impact-modifications)
  - [Pull Request Protocol](#pull-request-protocol)
  - [Review Sequence](#review-sequence)
  - [Core Values](#core-values)
  - [Support Channels](#support-channels)
  - [Contributor Agreement](#contributor-agreement)
  - [Deployment Procedures](#deployment-procedures)
  - [Alternative Build Paths](#alternative-build-paths)

<!-- End ToC -->

</details>

## System Requirements

J.A.R.V.I.S. requires:
- Node.js 22+ (neural interface compatibility)
- macOS 15+, Ubuntu 22.04+, or Windows 11+ with WSL2
- 2GB RAM minimum (4GB recommended for optimal performance)

## Why J.A.R.V.I.S.?

**Mission Control at your fingertips.** J.A.R.V.I.S. transforms your terminal into an AI-powered command center:

- **Autonomous Operations**: Execute complex development tasks with natural language
- **Multi-Modal Intelligence**: Process code, images, and documentation simultaneously  
- **Secure Containment**: Sandboxed execution prevents unauthorized system access
- **Mission Memory**: Persistent context across sessions for continuous operations

## Security Protocols

J.A.R.V.I.S. operates within strict containment protocols by default:

| Protocol | Status | Override |
|----------|--------|----------|
| Network isolation | ENABLED | `--full-auto` |
| Filesystem restrictions | ENABLED | `-w /path` |
| Environment protection | ENABLED | N/A |

### Containment Details

**macOS**: Seatbelt sandbox technology
**Linux**: Landlock LSM (kernel 6.7+)
**Windows**: WSL2 isolation layer

## Command Interface

```bash
# Initialize new project architecture
jarvis "design a microservices authentication system"

# Visual analysis 
jarvis -i architecture.png "optimize this system design"

# Autonomous deployment
jarvis --full-auto "deploy to kubernetes cluster"

# Voice interface
jarvis-voice  # Start always-on voice assistant
```

Full parameter manifest: `jarvis --help`

## Memory Core & Documentation

J.A.R.V.I.S. maintains operational context through:

1. **Project Documentation** (`AGENTS.md` in project root)
2. **Global Directives** (`~/.jarvis/instructions.md`)
3. **Session Memory** (automatic context preservation)

Create `AGENTS.md` in your project:

```markdown
# Project: Quantum Authentication

Mission parameters:
- Use TypeScript with strict mode
- Implement OAuth2 + WebAuthn
- Target 99.99% uptime
```

## Autonomous Mode

Enable different automation levels:

```bash
# Manual approval required (default)
jarvis "refactor authentication"

# Auto-approve file edits only
jarvis --auto-edit "update dependencies"

# Full autonomous operation
jarvis --full-auto "run security audit and fix vulnerabilities"
```

## Voice Interface

J.A.R.V.I.S. includes a cinematic voice interface with wake-word detection:

```bash
# Start voice interface
jarvis-voice

# System will listen for "Hey Jarvis" wake phrase
# After detection, speak your command naturally
```

**Features:**
- Always-on wake word detection ("Hey Jarvis")
- Arc reactor boot sequence with system status
- Cloud voice processing (GPT-4o) with offline fallback
- Real-time command execution and status updates
- ElevenLabs voice synthesis (when configured)

**Setup:**
```bash
# Install Python dependencies
pip install pyaudio faster-whisper openai elevenlabs numpy

# Configure API keys (optional, for enhanced features)
export OPENAI_API_KEY="your-key"      # For GPT-4o voice
export ELEVEN_API_KEY="your-key"     # For ElevenLabs TTS
```

**Voice Commands:**
- "Hey Jarvis, check system status"
- "Hey Jarvis, build the authentication system"
- "Hey Jarvis, run all tests"
- "Jarvis, disengage" (exits voice mode)

## Diagnostic Logging

```bash
# Enable diagnostic mode
DEBUG=1 jarvis "analyze performance"

# Monitor operations
tail -f "$TMPDIR/jarvis/jarvis-cli-latest.log"
```

## Mission Recipes

<details>
<summary><strong>System Architecture</strong></summary>

```bash
jarvis "analyze this codebase and create an architecture diagram"
jarvis "identify performance bottlenecks and suggest optimizations"
jarvis "design a caching strategy for this API"
```
</details>

<details>
<summary><strong>Security Operations</strong></summary>

```bash
jarvis "audit dependencies for vulnerabilities"
jarvis "implement rate limiting and DDoS protection"
jarvis "add input validation to all API endpoints"
```
</details>

<details>
<summary><strong>Deployment Missions</strong></summary>

```bash
jarvis "create Docker configuration for production"
jarvis "set up GitHub Actions CI/CD pipeline"
jarvis "configure Kubernetes manifests with auto-scaling"
```
</details>

## Configuration Matrix

J.A.R.V.I.S. configuration lives in `~/.jarvis/config.yaml`:

### Core Parameters

```yaml
model: gpt-4o
provider: openai
approval_mode: suggest
memory:
  mode: hybrid
  max_messages: 40
```

### AI Provider Configuration

```yaml
providers:
  custom-llm:
    name: "Private LLM"
    baseURL: "https://llm.company.com/v1"
    envKey: "CUSTOM_API_KEY"
```

### Environment Setup

```bash
# ~/.jarvis.env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
JARVIS_QUIET_MODE=1
```

## Zero Data Retention

For classified operations, use ZDR-enabled providers:

```bash
jarvis -p openai-zdr "process confidential data"
```

## Contributing to J.A.R.V.I.S.

### Engineering Workflow

```bash
git clone https://github.com/miikeyanderson/jarvis
cd jarvis
pnpm install
pnpm build
pnpm test
```

### Core Values

- **Precision**: Clean, efficient code
- **Security**: Defense-in-depth approach
- **Innovation**: Push boundaries responsibly
- **Community**: Collaborative excellence

### Support Channels

- Issue Tracker: [github.com/miikeyanderson/jarvis/issues](https://github.com/miikeyanderson/jarvis/issues)
- Discussions: [github.com/miikeyanderson/jarvis/discussions](https://github.com/miikeyanderson/jarvis/discussions)

---

**J.A.R.V.I.S.** – Your mission begins now.