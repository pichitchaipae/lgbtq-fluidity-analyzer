# Security Policy

## 🔒 Our Commitment

We take the security and privacy of LGBTQ+ individuals seriously. This project is designed with privacy-first principles:

- ✅ **No data persistence** - All analysis happens in-memory only
- ✅ **No tracking** - No analytics or third-party tracking scripts
- ✅ **No PII collection** - We never collect personally identifiable information
- ✅ **Open source** - Complete transparency in code and data handling
- ✅ **HTTPS only** - Secure connections required in production

## 🛡️ Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## 🐛 Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

### 1. **Do Not** Open a Public Issue
Security vulnerabilities should be reported privately to protect users.

### 2. Report Privately
Email security reports to: **[jao.pichitchai@gmail.com](mailto:jao.pichitchai@gmail.com)**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. What to Expect
- **24-48 hours**: Initial acknowledgment
- **7 days**: Assessment and plan
- **30 days**: Fix and disclosure (coordinated)

### 4. Responsible Disclosure
We follow coordinated disclosure:
- We will work with you to understand and fix the issue
- We will credit you in security advisories (unless you prefer anonymity)
- We request 90 days before public disclosure

## 🔍 Security Measures

### Application Security
- ✅ Input validation on all user inputs
- ✅ XSS protection (React's built-in sanitization)
- ✅ CSRF protection on API endpoints
- ✅ Rate limiting on API routes
- ✅ Secure headers (CSP, HSTS, X-Frame-Options)

### Infrastructure Security
- ✅ Non-root containers
- ✅ Read-only filesystems where possible
- ✅ Network policies in Kubernetes
- ✅ Regular dependency updates
- ✅ Automated security scanning (Dependabot)

### Data Privacy
- ✅ No databases or persistence layers
- ✅ No session storage or cookies
- ✅ No external API calls (except CDNs)
- ✅ No logging of survey responses
- ✅ No IP address logging

## 🔐 Privacy Considerations

### What We DON'T Collect
- ❌ Personal information
- ❌ Email addresses
- ❌ IP addresses
- ❌ Browser fingerprints
- ❌ Survey responses
- ❌ Analytics data
- ❌ Cookies

### What Happens to Your Data
1. You submit survey responses
2. Analysis happens in browser and backend memory
3. Results are displayed
4. **All data is immediately discarded**

No databases. No logs. No storage. No exceptions.

## 🛠️ Security Best Practices for Deployment

### Docker Compose
```yaml
# Use official images only
# Update regularly
# Don't expose unnecessary ports
```

### Kubernetes
```yaml
# Enable network policies
# Use RBAC
# Enable pod security policies
# Regular security audits
```

### Environment Variables
```bash
# Never commit .env files
# Use secrets management
# Rotate credentials regularly
```

## 📋 Security Checklist for Contributors

Before submitting code:

- [ ] No hardcoded credentials
- [ ] Input validation added
- [ ] Output sanitization applied
- [ ] Dependencies are up-to-date
- [ ] No new security warnings in CI
- [ ] Privacy policy not violated
- [ ] No data persistence added

## 🔄 Security Updates

We release security updates:
- **Critical**: Within 24-48 hours
- **High**: Within 1 week
- **Medium**: Next minor release
- **Low**: Next major release

## 📞 Contact

For security concerns:
- Email: **[INSERT YOUR EMAIL]**
- PGP Key: **[INSERT PGP KEY ID if available]**

For general questions:
- Open a [Discussion](https://github.com/YOUR_USERNAME/lgbtq-fluidity-analyzer/discussions)

---

## 🏳️‍🌈 Privacy is a Human Right

This project exists to support LGBTQ+ individuals safely and privately. We will never compromise on security or privacy.

**Last Updated**: October 12, 2025
