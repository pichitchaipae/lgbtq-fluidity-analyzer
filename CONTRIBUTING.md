# Contributing to LGBTQ+ Sexual Fluidity Analysis Platform

Thank you for your interest in contributing! 🏳️‍🌈

## 🌟 Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🧪 Add tests
- 🌐 Add translations
- ♿ Improve accessibility

## 🚀 Getting Started

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/lgbtq-fluidity-analyzer.git
cd lgbtq-fluidity-analyzer
```

### 2. Set Up Development Environment

```bash
# Start services
docker-compose up -d

# Run tests
docker-compose exec backend pytest
npm test --prefix frontend

# Run E2E tests
npx cypress open
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add support for non-binary pronouns
fix: correct statistical calculation in fluidity score
docs: update deployment instructions
test: add E2E test for language switching
style: format code with prettier
refactor: simplify analyzer logic
chore: update dependencies
```

## ✅ Pull Request Process

1. **Update Documentation** - Keep README.md and docs in sync
2. **Add Tests** - Ensure coverage doesn't decrease
3. **Run Linters** - `npm run lint` and follow PEP 8
4. **Test Locally** - All tests must pass
5. **Write Clear PR Description** - Explain what and why

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Backend tests pass
- [ ] Frontend tests pass
- [ ] Cypress E2E tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🧪 Testing Requirements

### Backend Tests
```bash
cd backend
pytest --cov=app --cov-report=term-missing
# Aim for >80% coverage
```

### Frontend Tests
```bash
cd frontend
npm test -- --coverage
npm run lint
```

### E2E Tests
```bash
npx cypress run
# All 19 tests must pass
```

## 🎨 Code Style

### Python (Backend)
- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Maximum line length: 100 characters
- Use meaningful variable names

```python
# Good
def calculate_fluidity_score(responses: List[Dict]) -> float:
    """Calculate sexual fluidity score from survey responses."""
    pass

# Bad
def calc(r):
    pass
```

### JavaScript/React (Frontend)
- Use ES6+ features
- Follow [Airbnb Style Guide](https://github.com/airbnb/javascript)
- Use functional components
- PropTypes required

```javascript
// Good
const FluidityChart = ({ data, language }) => {
  return <div>{/* ... */}</div>;
};

FluidityChart.propTypes = {
  data: PropTypes.object.isRequired,
  language: PropTypes.string.isRequired
};

// Bad
function chart(props) {
  return <div>{props.d}</div>;
}
```

## 🌐 Adding Translations

We support Thai and English. To add a new language:

1. Add language file: `frontend/src/locales/[lang].json`
2. Update language selector: `frontend/src/components/LanguageSwitch.jsx`
3. Test all UI elements render correctly

## ♿ Accessibility Guidelines

- Use semantic HTML
- Include ARIA labels
- Ensure keyboard navigation works
- Test with screen readers
- Maintain color contrast ratios (WCAG AA)

## 🔒 Security & Privacy

- **No data persistence** - All processing is in-memory only
- **No tracking** - No analytics or third-party scripts
- **No PII** - Never collect personally identifiable information
- **HTTPS only** - Secure connections required
- **Input validation** - Sanitize all user inputs

## 📋 Issue Guidelines

### Bug Reports

```markdown
**Describe the bug**
Clear description of the issue

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable, add screenshots

**Environment:**
- OS: [e.g., Windows 11]
- Browser: [e.g., Chrome 120]
- Version: [e.g., v1.0.0]
```

### Feature Requests

```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution you'd like**
Clear description of what you want to happen

**Additional context**
Any other context or screenshots
```

## 🏆 Recognition

Contributors will be recognized in:
- README.md Contributors section
- Release notes
- Project documentation

## 📞 Questions?

- 💬 Open a [Discussion](https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/discussions)
- 🐛 Report a [Bug or Feature Request](https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/issues)
- 📧 Email: [jao.pichitchai@gmail.com](mailto:jao.pichitchai@gmail.com)

## 🌈 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Be respectful, inclusive, and welcoming to all contributors.

---

**Thank you for contributing to a more inclusive future!** 🏳️‍🌈✨
