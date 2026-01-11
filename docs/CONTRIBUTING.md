# Contributing to Self-Healing Playwright Framework

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd self-healing-automation-framework
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install development dependencies**:
   ```bash
   make install-dev
   ```

4. **Set up pre-commit hooks** (optional):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Run tests**:
   ```bash
   make test
   ```

4. **Check code quality**:
   ```bash
   make lint
   make format
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

6. **Push and create a pull request**:
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style Guidelines

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions small and focused
- Maximum line length: 100 characters

## Testing Guidelines

- Write unit tests for all new features
- Aim for >80% code coverage
- Use descriptive test names
- Mock external dependencies (Azure OpenAI, Playwright)

## Commit Message Convention

Follow the Conventional Commits specification:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or updates
- `refactor:` - Code refactoring
- `style:` - Code style changes (formatting, etc.)
- `chore:` - Maintenance tasks

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update tests and ensure all tests pass
3. Update documentation if you're changing functionality
4. The PR will be merged once you have sign-off from maintainers

## Areas for Contribution

- Adding more self-healing methods (hover, select, etc.)
- Implementing selector caching to reduce API calls
- Adding metrics and success rate tracking
- Supporting async Playwright API
- Improving error messages and logging
- Adding more examples
- Improving documentation

## Questions?

Feel free to open an issue for any questions or concerns!
