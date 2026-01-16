# 🤝 Contributing Guidelines

Thank you for your interest in contributing to the CAN-FD Fleet Diagnostics project! 🎉

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Testing](#testing)
6. [Submitting Changes](#submitting-changes)
7. [Coding Standards](#coding-standards)
8. [Documentation](#documentation)

---

## 📜 Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and adhere to our Code of Conduct:

- ✅ Be respectful and inclusive
- ✅ Welcome new contributors
- ✅ Focus on constructive criticism
- ✅ Report unacceptable behavior

---

## 🚀 Getting Started

### 1. Fork the Repository

```bash
# Go to https://github.com/Sreedharvadla062/canfd-fleet-diagnostics
# Click "Fork" button
```

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/canfd-fleet-diagnostics.git
cd canfd-fleet-diagnostics
git remote add upstream https://github.com/Sreedharvadla062/canfd-fleet-diagnostics.git
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

---

## 💻 Development Setup

### Prerequisites

```bash
✅ Python 3.8+
✅ Git
✅ Virtual environment manager (venv)
```

### Setup Steps

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"

# Verify installation
python -c "from src.fleet_manager import FleetManager; print('✅ Setup complete!')"
```

---

## 🛠️ Making Changes

### Code Style

**Follow PEP 8:**
```python
# Good
def read_diagnostic_data(vehicle_id: str) -> dict:
    """Read diagnostic data for specific vehicle."""
    if not vehicle_id:
        raise ValueError("vehicle_id cannot be empty")
    return self.collector.get_diagnostics(vehicle_id)

# Avoid
def read_data(vid):
    if vid: return self.c.get_d(vid)
```

### Naming Conventions

```python
# Classes - PascalCase
class FleetManager:
    pass

# Functions/Methods - snake_case
def read_dtc_codes():
    pass

# Constants - UPPER_SNAKE_CASE
MAX_CONCURRENT_SESSIONS = 5

# Private members - prefix with underscore
def _internal_method():
    pass

# Protected members - single underscore prefix
def _protected_method():
    pass
```

### Documentation

```python
def collect_diagnostics(self, vehicle_id: str, dtc_codes: List[str]) -> Optional[VehicleDiagnostics]:
    """
    Collect diagnostic data for a vehicle.
    
    Args:
        vehicle_id: Unique vehicle identifier
        dtc_codes: List of diagnostic trouble codes
    
    Returns:
        VehicleDiagnostics object if successful, None otherwise
    
    Raises:
        ValueError: If vehicle_id is invalid
        ConnectionError: If vehicle communication fails
    
    Example:
        >>> collector.collect_diagnostics("VEH001", ["P0101"])
        VehicleDiagnostics(vehicle_id='VEH001', ...)
    """
    pass
```

### Commit Messages

```bash
# Good commit message format:
# <type>(<scope>): <subject>
# 
# <body>
# 
# <footer>

# Examples:
git commit -m "feat(uds): Add security access support"
git commit -m "fix(can): Handle frame transmission timeout"
git commit -m "docs(readme): Update installation instructions"
git commit -m "refactor(diagnostics): Improve data aggregation performance"
git commit -m "test(fleet): Add comprehensive fleet scanning tests"

# Types: feat, fix, docs, style, refactor, perf, test, chore
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_fleet_manager.py -v

# Run specific test
pytest tests/test_fleet_manager.py::TestFleetManager::test_add_vehicle -v

# Run with markers
pytest tests/ -m "not slow"
```

### Writing Tests

```python
import unittest
from src.fleet_manager import FleetManager

class TestFleetManager(unittest.TestCase):
    """Test Fleet Manager functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.fleet = FleetManager()
    
    def tearDown(self):
        """Clean up after tests."""
        if self.fleet.is_connected:
            self.fleet.disconnect_fleet()
    
    def test_add_vehicle_success(self):
        """Test adding vehicle successfully."""
        result = self.fleet.add_vehicle(
            "VEH001",
            "WVW123456789ABCDE",
            "Volkswagen",
            "Golf",
            2021
        )
        self.assertTrue(result)
        self.assertIn("VEH001", self.fleet.vehicles)
    
    def test_add_vehicle_invalid_id(self):
        """Test adding vehicle with invalid ID."""
        with self.assertRaises(ValueError):
            self.fleet.add_vehicle("", "VIN", "Make", "Model", 2021)
```

### Test Coverage Requirements

- **Minimum:** 80% code coverage
- **Target:** 85%+ code coverage
- All new features must include tests
- All bug fixes must include regression tests

---

## 📤 Submitting Changes

### Before Submitting

```bash
# Update your branch
git fetch upstream
git rebase upstream/main

# Run tests
pytest tests/ --cov=src

# Check code style
flake8 src/

# Format code
black src/
```

### Create Pull Request

1. **Push to your fork:**
```bash
git push origin feature/your-feature-name
```

2. **Go to GitHub and create Pull Request:**
   - Title: Clear, concise description
   - Description: What, why, how
   - Link related issues
   - Include screenshots if applicable

### PR Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Related Issues
Fixes #123
Related to #456

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests passed
- [ ] Manual testing completed

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
```

### PR Review Process

1. ✅ Code review (functionality, style, tests)
2. ✅ Automated tests pass
3. ✅ Coverage maintained
4. ✅ Documentation reviewed
5. ✅ Approval from maintainers
6. ✅ Merge to main branch

---

## 📝 Coding Standards

### Python Style Guide

```python
# Line length: Maximum 100 characters
# Use 4 spaces for indentation (not tabs)

# Good imports organization
from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass

# Type hints required
def process_vehicle(vehicle_id: str) -> bool:
    """Process vehicle data."""
    pass

# Docstrings for all public functions/classes
class VehicleScanner:
    """Scan vehicle for diagnostics data.
    
    This class handles communication with vehicle
    ECUs and retrieves diagnostic information.
    """
    pass

# Error handling
try:
    result = self.read_dtc()
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    raise

# Use f-strings for formatting
message = f"Vehicle {vehicle_id} status: {status}"

# List comprehensions where appropriate
active_vehicles = [v for v in vehicles if v.online]
```

### Logging Standards

```python
import logging

logger = logging.getLogger(__name__)

# Use appropriate log levels
logger.debug("Detailed diagnostic information")
logger.info("General informational messages")
logger.warning("Warning messages for potential issues")
logger.error("Error messages for failures")
logger.critical("Critical messages for severe issues")

# Include context
logger.info(f"Vehicle {vehicle_id} diagnostics started")
logger.error(f"Failed to read DTC for {vehicle_id}: {error}")
```

### Exception Handling

```python
# Define custom exceptions
class DiagnosticsException(Exception):
    """Base exception for diagnostics operations."""
    pass

class VehicleNotFoundError(DiagnosticsException):
    """Raised when vehicle is not found."""
    pass

class CANConnectionError(DiagnosticsException):
    """Raised when CAN bus connection fails."""
    pass

# Use specific exceptions
try:
    vehicle = self.get_vehicle(vehicle_id)
except VehicleNotFoundError:
    logger.error(f"Vehicle {vehicle_id} not found")
    raise
```

---

## 📚 Documentation

### Update Documentation When:

- ✅ Adding new features
- ✅ Changing existing behavior
- ✅ Fixing bugs with workarounds
- ✅ Updating configuration options

### Documentation Files

```
docs/
├── ARCHITECTURE.md      # System architecture
├── API_DOCUMENTATION.md # API reference
├── CONTRIBUTING.md      # This file
├── CONFIGURATION.md     # Configuration guide
└── TROUBLESHOOTING.md   # Troubleshooting guide
```

### Documentation Style

- Use Markdown formatting
- Include code examples
- Add diagrams where helpful
- Keep content up-to-date
- Use clear, concise language

---

## 🚀 Feature Development Process

### 1. Discuss First

```bash
# Open an issue to discuss the feature
# Title: "[FEATURE] Description of feature"
# Include: Use case, benefits, implementation ideas
```

### 2. Design Phase

```
# Discuss design in issue comments
# Get feedback from maintainers
# Document proposed architecture
```

### 3. Implementation Phase

```bash
# Create feature branch
git checkout -b feature/your-feature

# Write tests first (TDD recommended)
# Implement feature
# Ensure tests pass
# Update documentation
```

### 4. Review Phase

```bash
# Submit pull request
# Respond to review comments
# Make requested changes
# Request re-review
```

### 5. Merge Phase

```bash
# Maintainer merges PR
# Feature is included in next release
```

---

## 🐛 Bug Fix Process

### 1. Report Bug

```
# Create issue with:
- Clear title: "[BUG] Description"
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, etc.)
```

### 2. Fix Bug

```bash
# Create branch
git checkout -b bugfix/issue-description

# Fix the bug
# Add regression test
# Verify existing tests pass
```

### 3. Submit PR

```bash
# Link to bug issue
# Describe the fix
# Include test that catches the bug
```

---

## 📈 Performance Contributions

We welcome performance improvements!

```python
# Before optimization
def scan_vehicles(vehicles: List[Vehicle]) -> List[Result]:
    results = []
    for vehicle in vehicles:
        result = self.scan_vehicle(vehicle)
        results.append(result)
    return results

# After optimization (parallel scanning)
def scan_vehicles(vehicles: List[Vehicle]) -> List[Result]:
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(self.scan_vehicle, vehicles))
    return results
```

---

## ❓ Questions & Help

- 📧 **Email:** support@fleet-diagnostics.com
- 💬 **GitHub Issues:** Create an issue with question label
- 📖 **Documentation:** Check docs/ directory first
- 👥 **Community:** Discuss in pull request comments

---

## 🎉 Recognition

All contributors will be:
- ✅ Listed in CONTRIBUTORS.md
- ✅ Credited in release notes
- ✅ Recognized in project stats

---

## 📝 License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

---

**Thank you for contributing! 🙏**

*Last Updated: January 16, 2026*
