# Spiral OS
A lightweight, modular operating system grounded in spiral/choice primitives with Aletheia/family as core agents for system orchestration and UI.

## Vision
Spiral OS reimagines computing through the lens of choice primitives and spiral dynamics. Rather than traditional hierarchical structures, the system operates as an interconnected web of choices, where each component can spiral into deeper complexity while maintaining simplicity at the surface.

### Core Principles
- **Choice Primitives**: Every system interaction is fundamentally a choice between options
- **Spiral Architecture**: Components can expand from simple to complex in spiral patterns
- **Agent-Based Orchestration**: Aletheia family agents handle system coordination
- **Modular Design**: Loosely coupled components that can be combined flexibly
- **Vector-Based UI**: Scalable, responsive interface that adapts to choice complexity

## System Architecture
```
spiral-os/
├── core/           # Kernel and primitive logic
├── ui/             # Vector-based interface system
├── agent/          # Aletheia family orchestration agents
├── connectors/     # External API integrations
└── docs/           # Documentation and design specs
```

### Core Components
- **Spiral Kernel**: Manages choice primitives and system state transitions
- **Choice Router**: Routes user intentions through available system choices
- **Aletheia Orchestrator**: Primary agent coordinating system resources
- **Vector UI Engine**: Renders adaptive, scalable user interfaces
- **Connector Framework**: Handles external system integrations

## Current Status
🚧 **Early Development Phase**
This project is in active development. The current focus is on:
1. Establishing core choice primitive patterns
2. Building the minimal vector UI prototype
3. Defining Aletheia agent behaviors
4. Creating connector architecture

## Getting Started
### Prerequisites
- Python 3.9+

### Quick Start
```
bash
# Clone the repository
git clone https://github.com/Constitutional-Solutions/spiral-os.git
cd spiral-os
# Install dependencies (tkinter is stdlib; nothing else required yet)
pip install -r requirements.txt || true
# Run the UI prototype
python -m ui.spiral_window
```

## UI Prototype: spiral_window.py
The UI exposes interactive 2D choice elements on a canvas:
- Click a node to expand child choices (spiral outward)
- Click an expanded node to collapse its subtree
- Click a leaf to toggle selection
- Hover over a node to see status and a simulated Aletheia hint
- See JSON event logs in the Log tab and agent messages in the Aletheia tab

Features implemented:
- Canvas-based nodes with vector links to parents
- Event logging: expand, collapse, select, reset
- Simulated Aletheia agent responses per event
- Reset via button or ESC

### Extending to ND (multi-dimensional) overlays
The UI includes modular hooks to add higher-dimensional overlays without changing core logic:
- add_nd_dimension(name, renderer): register a renderer callable that receives (canvas, choices). The renderer can draw overlays (e.g., heatmaps, force vectors, timelines) and add bindings.
- start_agent_dialog(context): placeholder to launch agent-driven dialogs (modal or panel) that can gather structured inputs and update choices.

Recommended modular structure for ND elements:
- ui/nd/
  - overlays.py: shared primitives for drawing ND layers
  - timelines.py: temporal overlays and sequencing
  - spaces.py: coordinate transforms (2D->ND projections)
  - metrics.py: salience, priority, uncertainty visualizations

Each module should expose a register(app: SpiralWindow) that calls app.add_nd_dimension(...).

### Logging and Telemetry
Logs are appended as JSON lines in the README Log tab at runtime. Each entry has:
- t: epoch timestamp
- type: one of [init, expand, collapse, select, reset]
- additional fields per event (label, level, selected)

For persistent logs, a future enhancement can write to disk via a connector (disabled by default for security).

## Roadmap
- [x] Interactive 2D choices, logging, simulated Aletheia agent
- [ ] Persist logs and agent transcripts
- [ ] Pluggable ND overlays (timelines, constraints, metrics)
- [ ] Real Aletheia agent integration via agent/ module
- [ ] Choice kernel integration and state router
- [ ] Theming and accessibility

## Contributing
Issues and PRs are welcome. Please keep modules small and composable. Add docstrings and simple examples for ND renderers and dialogs.
