# Personal AI Agent

A local-first personal desktop AI assistant built with Python, Ollama, speech recognition, computer vision, and controlled computer automation.

The project is being developed in phases, with each phase adding another capability to the assistant.

---

# Project Architecture

```text
                    Personal AI Agent
                           │
                           ▼
                    🧠 AI Brain
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       🎤 Voice         👁️ Vision        🛠️ Tools
          │                │                │
          ▼                ▼                ▼
      Speech → Text    Screen Capture   Computer Control
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                     🤖 Assistant
```

The project is designed so that individual capabilities can be developed and tested independently before being connected into one assistant.

---

# Phase 1 — AI Brain

## Goal

Build the core conversational intelligence of the assistant.

The AI Brain is responsible for receiving user input and generating a natural-language response.

## Main Technologies

* Python
* Ollama
* Local LLM
* Prompt engineering

## Main Components

```text
phase-01-ai-brain/
├── brain.py
├── configure.py
├── main.py
└── prompts.py
```

## How It Works

```text
User
 ↓
Python Application
 ↓
AIBrain
 ↓
Ollama
 ↓
Local LLM
 ↓
Response
```

The brain provides the basic conversational layer that later phases can use.

## Result

The assistant can answer normal questions using a locally running language model.

---

# Phase 2 — Voice Interface

## Goal

Give the assistant the ability to listen and speak.

Phase 2 connects speech recognition and text-to-speech with the AI Brain.

## Main Technologies

* Python
* SpeechRecognition
* Microphone input
* Whisper / speech-to-text components
* Piper TTS

## Main Components

```text
phase-02-voice/
├── interruption.py
├── microphone_test.py
├── record_audio.py
├── speech_to_text.py
├── test_interruption.py
├── test_tts.py
├── test_vad.py
├── text_cleaner.py
├── tts.py
├── voice_assistant.py
└── whisper_stt.py
```

## Speech Pipeline

```text
🎤 User Voice
      ↓
Microphone
      ↓
Speech Recognition
      ↓
Text
      ↓
🧠 AI Brain
      ↓
Response Text
      ↓
Piper TTS
      ↓
🔊 Spoken Response
```

## Result

The assistant can receive spoken requests and respond using speech instead of requiring a keyboard-only interface.

---

# Phase 3 — Vision

## Goal

Allow the assistant to understand what is currently visible on the computer screen.

## Main Technologies

* Python
* Screen capture
* Ollama vision models
* LLaVA / Moondream
* Image processing

## Main Components

```text
phase-03-vision/
├── intent_router.py
├── screen_capture.py
├── screen_context.py
└── voice_vision_assistant.py
```

Additional reusable vision tools are located in:

```text
tools/
├── vision_tools.py
└── vision_actions.py
```

## Vision Pipeline

```text
User Question
      ↓
Does the question require vision?
      ↓
     YES
      ↓
Capture Screen
      ↓
Vision Model
      ↓
Screen Information
      ↓
AI Brain
      ↓
Natural Response
```

## Example

User:

```text
What application am I using?
```

The assistant can:

1. Capture the current screen.
2. Send the image to the vision model.
3. Interpret what is visible.
4. Give the user a natural-language answer.

## Target Detection

The vision system can also be used to locate visual targets.

Example:

```text
Find VS Code
```

The vision model can return a structured result such as:

```json
{
    "found": true,
    "target": "vscode",
    "x": 500,
    "y": 400
}
```

This information can later be used by computer-control tools.

## Result

The assistant can now combine conversational AI with visual understanding of the user's desktop.

---

# Phase 4 — Tool System

## Goal

Give the AI controlled access to computer and system capabilities.

Instead of allowing the language model to directly control the computer, actions are exposed as structured tools.

## Main Tool Architecture

```text
AI Decision
     ↓
Tool Name + Arguments
     ↓
Safety Validation
     ↓
Tool Executor
     ↓
Actual Computer Action
     ↓
Result
```

## Tool Registry

The registry provides a central list of available tools.

Important file:

```text
tools/registry.py
```

It allows the system to:

* Register tools
* Find tools by name
* List available tools
* Provide tool descriptions to the AI

---

# Computer Tools

Implemented in:

```text
tools/computer_tools.py
```

Current capabilities include:

* Move mouse
* Click mouse
* Type text
* Press keyboard keys

Example:

```text
type_text("Hello")
```

or:

```text
press_key("enter")
```

---

# System Tools

Implemented in:

```text
tools/system_tools.py
```

These provide controlled system-level actions such as launching permitted applications and opening websites.

Example:

```text
launch_application("notepad")
```

---

# Vision Tools

Implemented in:

```text
tools/vision_tools.py
```

These connect screen capture with the vision model.

The assistant can ask questions about the current screen and receive visual information.

---

# Safety Layer

Implemented in:

```text
tools/safety.py
```

The safety layer is an important part of the architecture.

Every tool request must pass through validation before execution.

```text
AI
 ↓
Safety
 ↓
Allowed?
 ├── NO  → Block
 │
 └── YES → Execute
```

This prevents the AI from directly performing arbitrary unsupported actions.

---

# Tool Executor

Implemented in:

```text
tools/tool_executor.py
```

The executor is responsible for:

1. Receiving a tool name.
2. Receiving its arguments.
3. Validating the request through the safety layer.
4. Finding the corresponding tool.
5. Executing the tool.
6. Returning the result.

Example:

```text
AI
 ↓
"launch_application"
 ↓
{"application": "notepad"}
 ↓
Safety
 ↓
Executor
 ↓
Notepad
```

---

# AI Tool Router

Implemented in:

```text
tools/ai_tool_router.py
```

The router decides whether a user request needs a tool.

For example:

```text
"What is Python?"
```

returns:

```json
{
    "action": "NORMAL"
}
```

while:

```text
"What application am I using?"
```

can return:

```json
{
    "action": "TOOL",
    "tool": "inspect_screen",
    "arguments": {
        "question": "What application is currently visible?"
    }
}
```

This separates normal conversation from computer actions.

---

# Phase 4 Architecture

```text
                    USER
                      │
                      ▼
                AI Tool Router
                      │
             ┌────────┴────────┐
             │                 │
          NORMAL              TOOL
             │                 │
             ▼                 ▼
          AI Brain       Safety Layer
                               │
                               ▼
                         Tool Executor
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
        System Tools     Computer Tools     Vision Tools
             │                 │                 │
             └─────────────────┴─────────────────┘
                               │
                               ▼
                            RESULT
```

---

# Why Tools Are Kept in One Folder

The reusable implementation is kept in:

```text
tools/
```

rather than duplicating code across phase folders.

This makes the architecture easier to maintain.

The phase directories represent **development milestones**, while `tools/` contains reusable capabilities.

For example:

```text
phase-03-vision/
    Documentation + phase-specific components

tools/
    Reusable vision tools
    Computer tools
    System tools
    Safety
    Executor
    Registry
```

This prevents duplicated implementations.

---

# Current Project Progress

| Phase   | Capability        | Status         |
| ------- | ----------------- | -------------- |
| Phase 1 | AI Brain          | ✅ Complete     |
| Phase 2 | Voice             | ✅ Complete     |
| Phase 3 | Vision            | ✅ Complete     |
| Phase 4 | Tool System       | ✅ Complete     |
| Phase 5 | Fast Command Path | ✅ Complete     |
| Phase 6 | Agent Controller  | 🚧 In Progress |

---

# Current Hybrid Architecture

The project is moving toward a hybrid system.

```text
                         USER
                           │
                           ▼
                     Fast Parser
                           │
                  ┌────────┴────────┐
                  │                 │
             Recognized         Not recognized
                  │                 │
                  ▼                 ▼
              Fast Path       Agent Controller
                  │                 │
                  └────────┬────────┘
                           ▼
                     Safety Layer
                           │
                           ▼
                      Tool Executor
                           │
                           ▼
                    Computer / Web
                           │
                           ▼
                       Result
```

Simple predictable commands can use the fast path.

Complex tasks will be handled by the Agent Controller.

---

# Future Direction

The long-term goal is to create a desktop assistant capable of:

* Natural voice interaction
* Screen understanding
* Controlled computer interaction
* Web information retrieval
* Multi-step task execution
* Context-aware responses
* Safe tool execution
* Local AI processing where practical

The next major milestone is an LLM-driven Agent Controller that can dynamically choose tools, observe their results, and continue until a task is completed.

---

# Development Philosophy

The project is being developed incrementally.

Each phase is:

1. Built independently.
2. Tested separately.
3. Connected to previous phases.
4. Committed as a Git checkpoint.
5. Extended only after the previous layer works reliably.

This approach makes debugging easier and keeps the assistant's architecture understandable.

---

# Project Status

🚧 **Active Development**

Current completed foundation:

```text
🧠 AI Brain
   +
🎤 Voice
   +
👁️ Vision
   +
🛠️ Tools
   +
⚡ Fast Command Execution
```

Next:

```text
🧠 Agent Controller
   ↓
Multi-step autonomous task execution
```
