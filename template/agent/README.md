# Agent Workspace for Python Development

This directory serves as the workspace for AI agents collaborating on Python projects. It follows a simplified structure optimized for Python development while adhering to PEP standards and modern best practices.

## Directory Structure

```
agent/
├── context/     # Project context & constraints
│   ├── goals.md          # Project objectives
│   └── constraints.md    # Project limitations
├── current/     # Active task & notes
│   ├── task.md          # Current task details
│   └── notes.md         # Working notes
└── history/     # Decisions & progress
    ├── decisions/       # Key technical decisions
    └── progress.md      # Development progress
```

## Python Development Guidelines

1. **Code Standards**
   - Follow PEP 8 style guide strictly
   - Adhere to PEP 517 for build system requirements
   - Use type hints (PEP 484) for better code clarity
   - Keep line length to 88 characters (Black default)

2. **Development Tools**
   - Use ruff for fast Python linting and formatting
   - Manage dependencies with uv for optimal performance
   - Use hatch for project management and building
   - Run tests with pytest framework

3. **Testing Practices**
   - Write tests for complex logic and edge cases
   - Use pytest fixtures for test setup
   - Aim for high-value test coverage, not just metrics
   - Include doctest examples in docstrings

## Usage Guidelines

1. **Active Development**
   - Keep current task details in current/task.md
   - Use current/notes.md for temporary work
   - Clean up after task completion
   - Run ruff --fix before committing changes

2. **Context Management**
   - Review relevant files in context/
   - Reference goals.md and constraints.md
   - Keep documentation focused
   - Document dependencies in pyproject.toml

3. **Progress Tracking**
   - Document decisions in history/decisions/
   - Update progress in history/progress.md
   - Use [TODO] and [DONE] markers
   - Track test coverage changes

## Python Best Practices

1. **Code Organization**
   - One class/function per file when logical
   - Use __init__.py files purposefully
   - Keep modules focused and cohesive
   - Follow the "Flat is better than nested" principle

2. **Documentation**
   - Write clear docstrings (Google style)
   - Include type hints in signatures
   - Document exceptions and edge cases
   - Keep README.md updated with setup steps

3. **Testing**
   - Test complex logic thoroughly
   - Use parametrized tests for edge cases
   - Mock external dependencies
   - Keep tests readable and maintainable

4. **Dependency Management**
   - Use uv for fast, reliable installs
   - Pin development dependencies
   - Keep production dependencies minimal
   - Document all requirements

5. **Quality Checks**
   - Run ruff for linting and formatting
   - Use mypy for type checking
   - Maintain test coverage
   - Review security advisories

For detailed guidelines, see the project's .clinerules file and pyproject.toml configuration.