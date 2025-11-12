# Contributing to FileSystemPro

Thank you for considering contributing to **FileSystemPro**! We appreciate your interest in improving this cross-platform file system toolkit. Whether it's fixing bugs, adding features, enhancing documentation, or refining code, your contributions help make the library more robust and user-friendly.

Before starting, please read this guide to understand our contribution process. By participating, you agree to abide by our [Code of Conduct](https://github.com/hbisneto/FileSystemPro/blob/main/CODE_OF_CONDUCT.md).

## Code of Conduct

We follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). All contributors are expected to uphold this standard. If you encounter issues, contact us at [heitor.bardemaker@live.com](mailto:heitor.bardemaker@live.com) or via GitHub issues.

## Ways to Contribute

We welcome all kinds of contributions! Here are some ideas:

- **Bug Reports**: Found an issue? [Open an issue](https://github.com/hbisneto/FileSystemPro/issues/new) with a clear description, steps to reproduce, and environment details (OS, Python version, `psutil` if used).
- **Feature Requests**: Have an idea? [Suggest it here](https://github.com/hbisneto/FileSystemPro/issues/new?template=feature_request.md). Include use cases and rationale.
- **Documentation**: Typos, clarifications, or new examples? Edit READMEs or submodule docs directly via PR.
- **Code**: Implement features, fix bugs, or refactor. See below for details.
- **Tests**: Add or improve tests in `tests/`.
- **Other**: Translations, performance benchmarks, or tooling scripts.

## Development Setup

1. **Fork and Clone**:

   ```bash
   git clone https://github.com/YOUR_USERNAME/FileSystemPro.git
   cd FileSystemPro
   git remote add upstream https://github.com/hbisneto/FileSystemPro.git
   ```

2. **Virtual Environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   # Or: .venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**:

   ```bash
   pip install -e .[dev]  # Editable install + dev extras (pytest, black, flake8)
   pip install psutil     # Optional, for device module
   ```

4. **Verify Setup**:

   ```bash
   pytest tests/          # Run tests
   black --check .        # Check formatting
   flake8 .               # Lint
   ```

## Coding Standards

- **Python Version**: Target 3.10+; test on 3.10, 3.12.
- **Style Guide**: Follow [PEP 8](https://peps.python.org/pep-0008/). Use [Black](https://black.readthedocs.io/) for formatting:
  ```bash
  black .
  ```
- **Linting**: [Flake8](https://flake8.pycqa.org/) for style checks:
  ```bash
  flake8 .
  ```
- **Type Hints**: Use [mypy](https://mypy-lang.org/) where practical (not enforced yet).
- **Docstrings**: [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for functions/classes.
- **Commit Messages**: Conventional commits (e.g., `feat: add network monitoring`).
- **Branches**: Feature branches from `main` (e.g., `feat/new-module`).

## Making a Contribution

1. **Discuss First**: For non-trivial changes, open an issue to align on scope.

2. **Branch and Commit**:

   ```bash
   git checkout -b your-branch-name
   git add .
   git commit -m "feat: brief description"
   ```

3. **Test Locally**:

   - Run `pytest` to ensure no regressions.
   - Verify with examples from submodule READMEs.
   - Check cross-platform (e.g., via GitHub Actions or local VMs).

4. **Push and PR**:

   ```bash
   git push origin your-branch-name
   ```
   - Open a Pull Request (PR) to `main`.
   - Reference related issues (e.g., "Fixes #123").
   - Include changelog entry if breaking (in `CHANGELOG.md`).

5. **Review and Merge**:

   - Expect feedback; iterate as needed.
   - Once approved, merge via squash/rebase (maintain clean history).
   - Delete branch post-merge.

## Pull Request Guidelines

- **Title**: Clear and concise (e.g., "fix: resolve path resolution on Windows").
- **Description**: 
  - What/Why: Problem solved and motivation.
  - How: Key changes.
  - Tests: New/updated tests.
  - Docs: Updated READMEs/examples.
- **Scope**: Small, focused PRs (<300 lines preferred).
- **CI Checks**: Must pass (linting, tests); re-run if needed.

## Releasing

Releases are managed by maintainers:

- Bump version in `pyproject.toml`/`setup.py`.
- Tag: `git tag vX.Y.Z`.
- Push: `git push --tags`.
- Upload to PyPI: `twine upload dist/*`.

## Questions?

- **Issues/PRs**: Use GitHub for tracking.
- **Discussions**: [Start one](https://github.com/hbisneto/FileSystemPro/discussions/new) for ideas.
- **Direct**: Email [heitor.bardemaker@live.com](mailto:heitor.bardemaker@live.com) or DM @BisnetoDev on X.

Thanks for contributing—we're excited to collaborate! 🚀