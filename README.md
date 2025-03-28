# Agentic Python Project Template

A minimal template that adds AI agent context management to your Python projects. This template provides the necessary structure for maintaining project context, memory, and workspace for AI-assisted development.

## Features

- **AI Agent Context Management**: Structured directories for maintaining project context, decisions, and workspace
- **.clinerules Configuration**: Ready-to-use configuration for AI agent interactions
- **Minimal Setup**: Only copies the essential files needed for AI-assisted development

## Adding to Your Project

### Prerequisites

- [Copier](https://copier.readthedocs.io/) 9.0 or higher

```bash
# Install Copier if you haven't already
pipx install copier
```

### Add AI Agent Support

```bash
# Add agent context to your project
copier copy gh:pypeaday/agentic-starter-kit-python .
```

This will add the following structure to your project:

```
.clinerules              # AI agent configuration
agent/                   # AI agent context management
├── context/            # Core project context (immutable)
│   ├── architecture.md    # System architecture and patterns
│   ├── constraints.md     # Project constraints and limitations
│   ├── goals.md          # Project objectives and success criteria
│   └── standards/        # Development standards and practices
├── memory/            # Persistent knowledge (append-only)
│   ├── decisions/        # Key technical decisions and rationales
│   ├── progress/         # Development progress and milestones
│   └── learnings/        # Insights and lessons learned
└── workspace/         # Active development (mutable)
    ├── current/          # Current task context and state
    ├── planning/         # Task breakdown and implementation plans
    └── validation/       # Testing and verification criteria
```

## Updating Agent Context

To update your project's agent context with the latest template changes:

```bash
copier update
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
