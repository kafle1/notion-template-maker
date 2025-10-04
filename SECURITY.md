# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Reporting a Vulnerability

We take the security of Notion Template Maker seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please Do Not

- Open a public GitHub issue for security vulnerabilities
- Publicly disclose the vulnerability before we've had a chance to address it

### Please Do

1. **Email us directly**: security@notiontemplate.com
2. **Provide details**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
3. **Allow us time**: We aim to respond within 48 hours

### What to Expect

1. **Acknowledgment**: We'll confirm receipt within 48 hours
2. **Assessment**: We'll investigate and assess severity
3. **Fix**: We'll develop and test a fix
4. **Disclosure**: We'll coordinate public disclosure with you
5. **Credit**: We'll credit you in our security advisories (if desired)

## Security Best Practices

### For Users

- Keep your API keys secure and never commit them to version control
- Use strong, unique passwords for all accounts
- Enable two-factor authentication where available
- Keep the application updated to the latest version
- Use HTTPS in production environments
- Regularly review access logs

### For Developers

- Never hardcode API keys or secrets
- Use environment variables for all sensitive data
- Validate and sanitize all user inputs
- Implement rate limiting on all API endpoints
- Use parameterized queries to prevent SQL injection
- Keep dependencies up to date
- Run security audits regularly

## Known Security Considerations

### API Keys

API keys are stored temporarily in session storage. They are:
- Encrypted in transit (HTTPS)
- Never logged or persisted to disk
- Cleared on session end
- Not shared between users

### Notion Integration Secret

Notion Internal Integration tokens are:
- Stored as environment variables (never in code)
- Used only for server-side API calls
- Never exposed to frontend
- Scoped with minimum required permissions
- Rotated regularly for security

### Rate Limiting

All API endpoints should implement rate limiting:
- Authentication: 5 requests/minute
- Template generation: 10 requests/minute
- Notion import: 20 requests/minute

## Security Updates

We release security updates as soon as possible after discovering vulnerabilities. Updates are announced:
- GitHub Security Advisories
- Release notes
- Email to registered users (for critical issues)

## Compliance

This project aims to comply with:
- OWASP Top 10 security practices
- GDPR data protection requirements (for EU users)
- API security best practices

## Bug Bounty

We currently do not offer a bug bounty program, but we greatly appreciate responsible disclosure and will credit researchers in our acknowledgments.

## Contact

- **Security Issues**: security@notiontemplate.com
- **General Contact**: support@notiontemplate.com
- **PGP Key**: Available on request

## Acknowledgments

We'd like to thank the following researchers for responsibly disclosing security issues:

<!-- Security researchers will be listed here -->

---

Last Updated: January 2025
