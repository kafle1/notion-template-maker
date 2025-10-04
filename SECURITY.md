# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | ✅                 |
| < 2.0   | ❌                 |

## Reporting a Vulnerability

**Please do not open public issues for security vulnerabilities.**

Email: security@notiontemplate.com

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (optional)

We aim to respond within 48 hours.

## Security Best Practices

### For Users
- Never commit API keys to version control
- Use strong passwords and 2FA
- Keep application updated
- Use HTTPS in production

### For Developers
- Use environment variables for secrets
- Validate and sanitize all inputs
- Keep dependencies updated
- Run security audits regularly

## Known Considerations

- API keys stored in session storage (encrypted in transit)
- Notion tokens stored as environment variables only
- Rate limiting on all endpoints
- No sensitive data logged

## Updates

Security updates announced via:
- GitHub Security Advisories
- Release notes

For critical issues, registered users are notified by email.
