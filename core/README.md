# Core - Kernel and Primitive Logic

This directory contains the core kernel components and choice primitive logic for Spiral OS.

## Overview

The core system implements the fundamental abstractions that make Spiral OS unique:
- **Choice Primitives**: Base-level constructs representing discrete choices
- **Spiral Kernel**: Manages state transitions and choice composition
- **Process Coordination**: Multi-agent process management
- **Resource Management**: System resource allocation and scheduling

## Architecture

```
core/
├── primitives/      # Choice primitive implementations
├── kernel/          # Core kernel logic
├── process/         # Process management
├── memory/          # Memory management
├── scheduler/       # Task scheduler
└── syscalls/        # System call interface
```

## Key Components

### Choice Primitives

Choice primitives are the atomic units of computation in Spiral OS. Every system operation can be decomposed into a series of choices.

**Properties:**
- Immutable once created
- Composable into complex choice trees
- Reversible for debugging and undo operations
- Type-safe with compile-time verification

**Example Structure:**
```python
class ChoicePrimitive:
    def __init__(self, options, context):
        self.options = options
        self.context = context
        self.selected = None
        
    def select(self, option):
        """Make a choice from available options."""
        if option in self.options:
            self.selected = option
            return self.apply_choice()
        raise InvalidChoiceError(option)
```

### Spiral Kernel

The kernel manages the lifecycle of choice primitives and coordinates between system components.

**Responsibilities:**
- Initialize choice primitive environment
- Route choices to appropriate handlers
- Maintain system state consistency
- Coordinate with Aletheia agents
- Handle system calls

### Process Model

Unlike traditional process models, Spiral OS processes are defined by their choice trees:
- Each process is a root choice that spirals into sub-choices
- Processes communicate through shared choice contexts
- Agent orchestration replaces traditional IPC

## Development Status

🚧 **Under Active Development**

Current focus:
- [ ] Define choice primitive API
- [ ] Implement basic kernel bootstrap
- [ ] Create process abstraction
- [ ] Design memory management for choice trees
- [ ] Build scheduler for choice resolution

## Design Questions

### 1. Choice Resolution Strategy
**Question**: Should choices be resolved eagerly or lazily?
- **Eager**: Resolve all choices immediately when presented
- **Lazy**: Defer resolution until choice result is needed
- **Hybrid**: Context-dependent resolution strategy

**Considerations**: Performance vs. resource usage

### 2. State Persistence
**Question**: How should choice history be persisted?
- **Full history**: Store complete choice tree (enables full undo)
- **Checkpointing**: Periodic snapshots with delta compression
- **Minimal**: Only current state, no history

**Considerations**: Storage vs. debugging capability

### 3. Concurrency Model
**Question**: How do concurrent choices interact?
- **Isolated**: Each choice tree is independent
- **Coordinated**: Choices can observe and influence each other
- **Transactional**: ACID guarantees for choice sequences

**Considerations**: Simplicity vs. expressiveness

## Getting Started

### Prerequisites
- Rust or Python 3.9+ (language decision pending)
- Understanding of operating system concepts
- Familiarity with choice theory

### Building (Placeholder)
```bash
# Future build instructions
make kernel
make test
```

## Contributing

Contributions to the core kernel are highly valued. Areas of focus:
- Choice primitive design and implementation
- Kernel architecture
- Performance optimization
- Formal verification

## References

- [Choice Primitives Specification](../docs/choice-primitives.md)
- [Kernel Architecture](../docs/kernel-arch.md)
- [System Calls](../docs/syscalls.md)

---

**Note**: This is foundational work. Design decisions made here will influence the entire system architecture.
