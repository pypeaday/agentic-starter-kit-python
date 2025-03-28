# Project Constraints

This document outlines the key limitations and requirements that must be considered during Python development.

## Technical Constraints

1. **Python Development**
   - Use Python 3.9+ for all development
   - Follow PEP 8 style guide strictly
   - Implement type hints (PEP 484)
   - Use standard library solutions when possible
   - Keep third-party dependencies minimal

2. **Development Tools**
   - Use ruff for linting and formatting
   - Manage dependencies with uv
   - Use hatch for project management
   - Configure mypy for type checking
   - Use pytest for testing

3. **Testing**
   - Write purposeful pytest-based tests
   - Focus on testing complex logic
   - Use fixtures for test setup
   - Mock external dependencies
   - Ensure cross-platform compatibility

## Process Constraints

1. **Task Management**
   - One task active at a time
   - Document key decisions
   - Track progress clearly
   - Update pyproject.toml as needed

2. **Code Changes**
   - Make incremental updates
   - Run full test suite before commits
   - Update type hints with changes
   - Keep documentation in sync
   - Run quality checks (ruff, mypy)

3. **Tools**
   - Use cross-platform compatible tools
   - Support CLI operations
   - Configure tools in pyproject.toml
   - Use virtual environments
   - Keep tool configurations minimal

## Implementation Guidelines

1. **Code**
   - Follow "Explicit is better than implicit"
   - Keep functions focused and pure
   - Use type hints consistently
   - Write clear docstrings
   - Handle errors explicitly

2. **Documentation**
   - Use Google-style docstrings
   - Keep docstrings up to date
   - Document exceptions
   - Include usage examples
   - Update README.md with changes

3. **Package Management**
   - Use `uv add` for adding requirements
   - Keep production dependencies minimal
   - Document all requirements
   - Use appropriate dependency groups

4. **Quality Standards**
   - Meaningful test coverage
   - Clear error messages
   - Documented APIs

Remember: Simple, explicit, and maintainable code over clever solutions.