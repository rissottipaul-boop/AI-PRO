# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this project, please report it by emailing rissottipaul@gmail.com. Please do not create public GitHub issues for security vulnerabilities.

## Security Measures

### Automated Security Scanning

This project uses multiple layers of security scanning:

1. **CodeQL** - Advanced semantic code analysis for finding security vulnerabilities
   - Runs on every push and pull request
   - Also runs weekly on a schedule
   - Scans for common vulnerability patterns

2. **Bandit** - Python security linter
   - Identifies common security issues in Python code
   - Runs in CI pipeline on every build
   - Part of the security job in CI workflow

3. **pip-audit** - Dependency vulnerability scanner
   - Checks for known vulnerabilities in Python dependencies
   - Fails CI if HIGH severity vulnerabilities are found
   - Runs in CI pipeline

4. **Gitleaks** - Secret detection tool
   - Prevents committing secrets, API keys, tokens, and private keys
   - Runs as a pre-commit hook
   - Also runs in CI pipeline

5. **Dependabot** - Automated dependency updates
   - Weekly checks for dependency updates
   - Automatically creates PRs for security updates

### Secret Management

**NEVER commit sensitive information to the repository:**

- Private keys (SSH, PGP, etc.)
- API keys and tokens
- Passwords or credentials
- Environment files with secrets (.env files)
- SSL/TLS certificates

The `.gitignore` file is configured to exclude common secret file patterns:
- `*.pem`, `*.key`, `*.pub`
- SSH key files (`id_rsa`, `id_ed25519`, etc.)
- `.env.local`, `.env.*.local`
- `secrets.yml`, `secrets.yaml`
- `*.secret`, `*.secrets`

### Pre-commit Hooks

Before committing code, pre-commit hooks automatically run:
- Code formatting (ruff, black)
- Type checking (mypy)
- Secret scanning (gitleaks)

To install pre-commit hooks:
```bash
pre-commit install
```

To run manually:
```bash
pre-commit run --all-files
```

### CI/CD Security

All CI/CD pipelines:
- Run with minimal permissions
- Use pinned action versions (e.g., `@v4`, `@v5`)
- Separate security job from build/test jobs
- Upload security reports to appropriate services

### Best Practices

1. **Keep dependencies up to date** - Dependabot will create PRs automatically
2. **Review security alerts** - Check GitHub Security tab regularly
3. **Use environment variables** - For configuration and secrets in runtime
4. **Rotate secrets** - If a secret is exposed, rotate it immediately
5. **Enable 2FA** - All contributors should use two-factor authentication

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < main  | :x:                |

We only support the latest version on the main branch.

## Known Security Considerations

### Past Issues

- **SSH Keys Committed** (Resolved) - Private SSH keys were accidentally committed to the repository. These have been removed and `.gitignore` has been updated to prevent future occurrences. If you pulled these commits, please:
  1. Consider the exposed SSH keys as compromised
  2. Generate new SSH keys
  3. Update authorized keys on all systems
  4. Remove old keys from GitHub/GitLab accounts

## Security Checklist for Contributors

Before submitting a PR:
- [ ] No hardcoded secrets or credentials
- [ ] All dependencies are up to date
- [ ] Pre-commit hooks pass (including gitleaks)
- [ ] No new security warnings from linters
- [ ] Sensitive data uses environment variables
- [ ] New code follows secure coding practices

## References

- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Python Security Best Practices](https://snyk.io/learn/python-security-best-practices/)
