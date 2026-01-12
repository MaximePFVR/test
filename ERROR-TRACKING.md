# Error Tracking & Lessons Learned

This document serves as a centralized record of recurring errors, special cases, and lessons learned during development. Use this file to track issues and avoid repeating the same mistakes.

---

## Table of Contents
- [Git & Version Control Errors](#git--version-control-errors)
- [Build & Compilation Errors](#build--compilation-errors)
- [Runtime Errors](#runtime-errors)
- [Dependency & Package Errors](#dependency--package-errors)
- [Network & API Errors](#network--api-errors)
- [Security & Authentication Errors](#security--authentication-errors)
- [Database Errors](#database-errors)
- [Configuration Errors](#configuration-errors)
- [Special Cases & Edge Cases](#special-cases--edge-cases)
- [Best Practices & Preventive Measures](#best-practices--preventive-measures)

---

## Git & Version Control Errors

### Branch Naming Convention Failures
**Error**: `403 HTTP error when pushing to remote`
**Cause**: Branch name doesn't follow the required pattern (must start with 'claude/' and end with session ID)
**Solution**: Always use the correct branch naming convention: `claude/<description>-<SESSION_ID>`
**Date First Encountered**:
**Recurrence Count**:

### Merge Conflicts
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

---

## Build & Compilation Errors

### Type Errors
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

### Missing Dependencies
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

---

## Runtime Errors

### Null Pointer / Undefined Reference
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

### Memory Leaks
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

---

## Dependency & Package Errors

### Version Incompatibility
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

### Package Not Found
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

---

## Network & API Errors

### Timeout Errors
**Error**:
**Cause**:
**Solution**: Implement retry logic with exponential backoff (2s, 4s, 8s, 16s)
**Date First Encountered**:
**Recurrence Count**:

### Rate Limiting
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

---

## Security & Authentication Errors

### Permission Denied
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

### Token Expiration
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

---

## Database Errors

### Connection Timeout
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

### Query Performance Issues
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

---

## Configuration Errors

### Environment Variables Missing
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

### Invalid Configuration Format
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

---

## Special Cases & Edge Cases

### Edge Case 1
**Description**:
**Error**:
**Cause**:
**Solution**:
**Date First Encountered**:
**Recurrence Count**:

---

## Best Practices & Preventive Measures

### General Guidelines
1. Always read files before editing them
2. Use proper error handling at system boundaries (user input, external APIs)
3. Avoid over-engineering - keep solutions simple and focused
4. Never commit sensitive data (.env, credentials, etc.)
5. Use exponential backoff for network retry logic

### Code Review Checklist
- [ ] No security vulnerabilities (SQL injection, XSS, command injection)
- [ ] Proper error handling implemented
- [ ] No unused code or variables
- [ ] Dependencies are up to date
- [ ] Tests pass successfully
- [ ] Documentation is updated if needed

### Git Workflow Checklist
- [ ] Working on correct feature branch
- [ ] Branch follows naming convention
- [ ] Commit messages are clear and descriptive
- [ ] Changes have been tested locally
- [ ] No merge conflicts

---

## How to Use This Document

1. **When an error occurs**: Document it immediately in the appropriate section
2. **Include details**: Error message, cause, solution, and date
3. **Update recurrence count**: If the same error happens again, increment the counter
4. **Review regularly**: Read this file before starting new tasks to avoid known issues
5. **Keep it updated**: This is a living document - add new categories as needed

---

## Template for New Error Entry

```markdown
### [Error Name/Title]
**Error**: [Exact error message or description]
**Cause**: [Root cause of the error]
**Solution**: [How it was fixed]
**Prevention**: [How to avoid this in the future]
**Date First Encountered**: [YYYY-MM-DD]
**Recurrence Count**: [Number]
**Related Files**: [List of affected files]
**References**: [Links to documentation, Stack Overflow, etc.]
```

---

*Last Updated: 2026-01-12*
