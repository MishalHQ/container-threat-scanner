# Contributing to Container Image Threat Scanner

Thank you for your interest in contributing to this project! This is an educational DevSecOps project, and we welcome contributions from the community.

## 🚀 Getting Started

1. **Fork the repository**
   - Click the "Fork" button at the top right of the repository page

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/container-threat-scanner.git
   cd container-threat-scanner
   ```

3. **Set up development environment**
   ```bash
   # Install required tools
   # - Docker Desktop
   # - Syft
   # - Trivy
   # - Python 3.10+
   
   # Verify installation
   python main.py --image nginx:latest
   ```

## 🔧 Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

### Testing

Before submitting a pull request:

1. **Test with multiple images**
   ```bash
   python main.py --image nginx:latest
   python main.py --image ubuntu:22.04
   python main.py --image alpine:3.18
   ```

2. **Test verbose mode**
   ```bash
   python main.py --image nginx:latest --verbose
   ```

3. **Verify cross-platform compatibility**
   - Test on both Windows and macOS if possible
   - Ensure no hardcoded OS-specific paths

### Commit Messages

Use clear, descriptive commit messages:

```
✅ Good:
- "Add support for custom output directory"
- "Fix layer classification for Alpine images"
- "Improve remediation suggestions for base images"

❌ Bad:
- "Update code"
- "Fix bug"
- "Changes"
```

## 📝 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Test thoroughly
   - Update README if needed

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your feature branch
   - Provide a clear description of your changes

## 🎯 Areas for Contribution

### High Priority
- [ ] Add support for additional container registries
- [ ] Implement caching for faster repeated scans
- [ ] Add HTML/PDF report generation
- [ ] Improve layer-to-package mapping accuracy

### Medium Priority
- [ ] Add support for scanning container images from tar files
- [ ] Implement parallel scanning for multiple images
- [ ] Add configuration file support (YAML/JSON)
- [ ] Create interactive CLI mode

### Low Priority
- [ ] Add support for custom vulnerability databases
- [ ] Implement plugin system for custom analyzers
- [ ] Add web UI dashboard
- [ ] Create Docker container for the scanner itself

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details**
   - OS (Windows/macOS/Linux)
   - Python version
   - Docker version
   - Syft version
   - Trivy version

2. **Steps to reproduce**
   - Exact command used
   - Image being scanned
   - Expected vs actual behavior

3. **Logs**
   - Include relevant error messages
   - Attach `scanner.log` if available

## 💡 Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists or is planned
2. Describe the use case clearly
3. Explain how it aligns with the project goals
4. Provide examples if possible

## 📚 Documentation

Help improve documentation:

- Fix typos or unclear explanations
- Add examples and use cases
- Improve installation instructions
- Create tutorials or guides

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on what's best for the project

## 📧 Questions?

If you have questions:

1. Check the README.md
2. Search existing issues
3. Create a new issue with the "question" label

## 🙏 Thank You!

Your contributions make this project better for everyone. Whether it's code, documentation, bug reports, or feature ideas - every contribution is valued!

---

**Happy Contributing! 🎉**