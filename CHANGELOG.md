# Changelog

All notable changes to the Code Review Automation Tool are documented here.

## [1.0.0] - 2024-09-25

### Added
- ✅ **Fixed import errors and module structure**
- ✅ **Cleaned up project organization**
- ✅ **Created proper entry point (`code_review.py`)**
- ✅ **Fixed all relative imports**
- ✅ **Comprehensive testing with all output formats**

### Fixed
- Import errors with relative modules
- MIME types in email notifications
- Missing type annotations
- Entry point execution issues

### Features
- **Multi-format Output**: Terminal, JSON, Markdown
- **20+ Language Support**: Python, JavaScript, TypeScript, Go, Java, etc.
- **Security Analysis**: Detects hardcoded secrets, unsafe eval, SQL injection risks
- **Complexity Analysis**: Cyclomatic complexity, cognitive complexity, deep nesting
- **Style Checking**: Line length, naming conventions, code formatting
- **CI/CD Integration**: GitHub Actions, GitLab CI with exit codes and metrics
- **Configurable Rules**: Custom YAML configuration with team-specific standards

### Usage
```bash
# Basic file analysis
python code_review.py --files *.py --format terminal

# Git diff analysis
python code_review.py --git-diff HEAD~1..HEAD --format markdown

# Custom configuration
python code_review.py --files src/ --config .codereview.yaml --format json -o report.json
```

### Dependencies
- PyYAML >= 6.0
- GitPython >= 3.1.40
- gitignore-parser >= 0.1.0
- requests >= 2.31.0
- aiohttp >= 3.9.0

### Project Structure
```
code_reviewer/
├── code_review.py          # Main entry point
├── src/                    # Source code
│   ├── analyzers/         # Code analysis modules
│   ├── formatters/        # Output formatting
│   ├── utils/            # Utilities
│   └── config/           # Configuration handling
├── config/               # Default configurations
├── .codereview.yaml     # Main configuration file
├── .github/workflows/   # GitHub Actions
├── .gitlab-ci.yml      # GitLab CI
└── README.md
```