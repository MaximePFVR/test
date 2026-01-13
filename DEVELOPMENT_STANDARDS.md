# Development Standards & Architecture Guide

**Project**: Python-based HR Discovery Tool
**Purpose**: This document serves as the authoritative reference for all development work in this project. All code must comply with these standards to ensure maintainability, security, and professional quality.

---

## 1. Project Architecture

All project files must follow this standardized folder structure:

```
project_root/
├── src/                    # All application logic and modules
│   ├── __init__.py
│   ├── core/              # Core business logic
│   ├── utils/             # Helper functions and utilities
│   ├── scrapers/          # Data collection modules
│   └── validators/        # Input validation logic
├── tests/                 # All test files (mirrors src/ structure)
│   ├── __init__.py
│   ├── test_core/
│   └── test_utils/
├── data/                  # Output files, logs, and generated data
│   ├── outputs/           # CSV, JSON, or other export files
│   └── logs/              # Application log files
├── config/                # Configuration files
│   └── .env.example       # Template for environment variables
├── docs/                  # Additional documentation
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (NEVER commit to git)
├── .gitignore            # Git ignore rules
└── README.md             # Project overview and setup instructions
```

**Key Principles**:
- Keep source code separate from output data
- Mirror test structure to match source code organization
- Never commit sensitive data or credentials to version control

---

## 2. Coding Standards

### 2.1 Import Standards

**MANDATORY: Use Absolute Imports Only**

All imports must be absolute to prevent `ImportError` issues when running scripts from different directories.

**Correct**:
```python
from src.core.scraper import fetch_data
from src.utils.validators import validate_email
```

**Incorrect (Never Use)**:
```python
from ..core.scraper import fetch_data  # Relative import - DO NOT USE
from .validators import validate_email  # Relative import - DO NOT USE
```

### 2.2 PEP 8 Style Guidelines

Follow [PEP 8](https://pep8.org/) standards for all Python code:

- **Variable Names**: Use descriptive, lowercase names with underscores (`company_name`, not `cn` or `CompanyName`)
- **Function Names**: Use lowercase with underscores (`fetch_company_data`, not `fetchCompanyData`)
- **Class Names**: Use PascalCase (`DataScraper`, not `data_scraper`)
- **Constants**: Use uppercase with underscores (`MAX_RETRIES`, `API_BASE_URL`)
- **Indentation**: Use 4 spaces (never tabs)
- **Line Length**: Maximum 100 characters per line
- **Blank Lines**: Two blank lines between top-level functions and classes

### 2.3 Environment Variables & Secrets Management

**MANDATORY: Use python-dotenv for All Credentials**

Never hardcode API keys, passwords, or sensitive data in source code.

**Setup**:
```python
# At the top of every file that needs environment variables
import os
from dotenv import load_dotenv

load_dotenv()

# Access credentials
API_KEY = os.getenv('API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
```

**.env file structure**:
```
# API Credentials
API_KEY=your_api_key_here
API_SECRET=your_secret_here

# Database
DATABASE_URL=postgresql://localhost/dbname

# Application Settings
DEBUG_MODE=false
MAX_RETRIES=3
```

**Important**:
- Always create a `.env.example` file with placeholder values
- Add `.env` to `.gitignore` to prevent accidental commits
- Document all required environment variables in README.md

---

## 3. Error Handling & Logging

### 3.1 Mandatory Try/Except Blocks

**Every function must include error handling** to prevent unexpected crashes and provide clear feedback.

**Standard Pattern**:
```python
import logging

def fetch_company_data(company_url):
    """
    Fetches company information from a given URL.

    Args:
        company_url (str): The URL of the company website

    Returns:
        dict: Company data including name, industry, and size
        None: If the fetch operation fails
    """
    try:
        # Main logic here
        response = requests.get(company_url, timeout=10)
        response.raise_for_status()
        return parse_response(response)

    except requests.exceptions.Timeout:
        logging.error(f"Request timed out while fetching {company_url}. "
                     f"The server took too long to respond. Try again later.")
        return None

    except requests.exceptions.ConnectionError:
        logging.error(f"Failed to connect to {company_url}. "
                     f"Check your internet connection or verify the URL is correct.")
        return None

    except Exception as e:
        logging.error(f"Unexpected error fetching data from {company_url}: {str(e)}")
        return None
```

### 3.2 Beginner-Friendly Error Messages

Error messages must:
- **Explain what went wrong** in plain language
- **Suggest why it happened** (e.g., "The server took too long to respond")
- **Provide actionable next steps** (e.g., "Check your internet connection")

**Bad**: `Error: 404`
**Good**: `Failed to find the company page at {url}. The page may have been moved or deleted. Verify the URL is correct.`

### 3.3 Logging Configuration

Every application entry point should configure logging:

```python
import logging

# Configure at application start
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/app.log'),
        logging.StreamHandler()  # Also print to console
    ]
)
```

---

## 4. Documentation Requirements

### 4.1 File Headers

**Every Python file must start with a header** that includes:
- Purpose of the file
- Legal and ethical warnings (when applicable)
- Author information (optional)
- Last updated date

**Template**:
```python
"""
===============================================================================
MODULE: Company Data Scraper
PURPOSE: Fetches publicly available company information from business websites
         for recruitment research purposes only.

LEGAL NOTICE:
- This tool is designed for legitimate recruitment research only
- Users must comply with website Terms of Service and robots.txt
- Do not use this tool to scrape personal data or violate privacy laws
- Respect rate limits and do not overload target servers

ETHICAL GUIDELINES:
- Only collect publicly available business information
- Never scrape or store personal email addresses (e.g., @gmail.com)
- Obtain proper authorization before collecting data at scale

Last Updated: 2026-01-13
===============================================================================
"""
```

### 4.2 Function Docstrings

**Every function must have a docstring** following this format:

```python
def process_company_list(csv_file, output_format='json'):
    """
    Processes a list of companies from a CSV file and exports results.

    This function reads company names from a CSV file, fetches additional
    data about each company, and exports the enriched data in the specified
    format.

    Args:
        csv_file (str): Path to the input CSV file containing company names
        output_format (str, optional): Export format ('json' or 'csv').
                                      Defaults to 'json'.

    Returns:
        bool: True if processing completed successfully, False otherwise

    Raises:
        FileNotFoundError: If the input CSV file doesn't exist
        ValueError: If output_format is not 'json' or 'csv'

    Example:
        >>> process_company_list('data/companies.csv', output_format='json')
        True
    """
    # Function implementation
```

**Required Sections**:
1. **Summary**: One-line description of what the function does
2. **Detailed Description**: Explain the logic and workflow (if complex)
3. **Args**: List each parameter with type and description
4. **Returns**: Describe what the function returns and the data type
5. **Raises** (if applicable): Document exceptions that may be raised
6. **Example** (for complex functions): Show usage example

---

## 5. Legal & Ethical Guardrails

### 5.1 Personal Data Protection

**HARDCODED REQUIREMENT**: The application must never scrape or store personal email addresses.

**Implementation**:
```python
import re

def is_personal_email(email):
    """
    Checks if an email address is a personal email (not business).

    Args:
        email (str): Email address to validate

    Returns:
        bool: True if personal email, False if business email
    """
    personal_domains = [
        '@gmail.com', '@yahoo.com', '@hotmail.com', '@outlook.com',
        '@aol.com', '@icloud.com', '@protonmail.com', '@mail.com'
    ]
    return any(email.lower().endswith(domain) for domain in personal_domains)

def validate_and_filter_emails(email_list):
    """
    Filters out personal emails from a list of email addresses.

    Args:
        email_list (list): List of email addresses

    Returns:
        list: Filtered list containing only business emails
    """
    business_emails = []
    for email in email_list:
        if is_personal_email(email):
            logging.warning(f"Rejected personal email: {email}. "
                          f"Only business emails are allowed.")
        else:
            business_emails.append(email)
    return business_emails
```

### 5.2 Legal Notice Requirement

**All CLI tools must display a legal notice** when executed:

```python
def display_legal_notice():
    """Displays legal and ethical usage notice to the user."""
    notice = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                     LEGAL NOTICE                               ║
    ╔════════════════════════════════════════════════════════════════╝
    ║
    ║  This tool is designed for legitimate business research only.
    ║
    ║  By using this tool, you agree to:
    ║  • Comply with all applicable laws and website Terms of Service
    ║  • Respect robots.txt and rate limiting
    ║  • Only collect publicly available business information
    ║  • Never scrape or misuse personal data
    ║
    ║  Unauthorized use may result in legal consequences.
    ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    print(notice)

    # Require acknowledgment for CLI tools
    response = input("\nDo you agree to these terms? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("You must agree to the terms to use this tool. Exiting.")
        exit(0)

# Call at the start of main()
if __name__ == "__main__":
    display_legal_notice()
    main()
```

---

## 6. Workflow for New Features

Follow this standardized workflow when implementing new features:

### Step 1: Plan & Design
- Document the feature requirements
- Identify which modules need to be created or modified
- Determine what new dependencies are needed
- Consider edge cases and error scenarios

### Step 2: Update Dependencies
```bash
# Add new packages to requirements.txt
pip install new-package
pip freeze > requirements.txt
```

### Step 3: Build the Module
- Create the new file in the appropriate `src/` subdirectory
- Add file header with purpose and legal warnings
- Implement functions with docstrings
- Include try/except blocks for all operations
- Use absolute imports only
- Load environment variables with python-dotenv if needed

### Step 4: Test the Module
- Create corresponding test file in `tests/` directory
- Write unit tests for all functions
- Test error handling paths
- Verify edge cases

```python
# Example test structure
import pytest
from src.core.scraper import fetch_company_data

def test_fetch_company_data_success():
    """Test successful data fetch."""
    result = fetch_company_data("https://example.com")
    assert result is not None
    assert 'company_name' in result

def test_fetch_company_data_invalid_url():
    """Test handling of invalid URL."""
    result = fetch_company_data("invalid-url")
    assert result is None
```

### Step 5: Integration
- Update main application to use the new feature
- Update README.md with usage examples
- Test the complete workflow end-to-end

### Step 6: Documentation
- Update this DEVELOPMENT_STANDARDS.md if new patterns emerge
- Add feature documentation to `docs/` if complex
- Update .env.example if new environment variables are needed

---

## 7. Code Review Checklist

Before considering any code complete, verify:

- [ ] File has a proper header with purpose and legal warnings
- [ ] All functions have complete docstrings (what, args, returns)
- [ ] All imports are absolute (no relative imports)
- [ ] Every function has try/except error handling
- [ ] Error messages are beginner-friendly and descriptive
- [ ] No hardcoded credentials (all use python-dotenv)
- [ ] No personal email scraping or storage
- [ ] CLI tools display legal notice
- [ ] Code follows PEP 8 style guidelines
- [ ] Tests exist for new functionality
- [ ] requirements.txt is updated with new dependencies

---

## 8. Common Pitfalls to Avoid

1. **Relative Imports**: Always use absolute imports from project root
2. **Missing Error Handling**: Every external operation can fail
3. **Hardcoded Secrets**: Use environment variables for all credentials
4. **Vague Error Messages**: Explain what happened and why
5. **Missing Documentation**: Future you (and others) need context
6. **Personal Data Collection**: Violates privacy and legal standards
7. **Skipping Tests**: Untested code will break in production
8. **Inconsistent Structure**: Follow the defined folder architecture

---

## 9. Quick Reference

**Starting a new module?**
1. Create file in appropriate `src/` subdirectory
2. Add file header with legal warnings
3. Import with absolute paths
4. Load environment variables if needed
5. Add try/except to all functions
6. Write docstrings for everything

**Adding a new dependency?**
```bash
pip install package-name
pip freeze > requirements.txt
```

**Running tests?**
```bash
pytest tests/
```

**Need help?** Refer to this document first. All code in this project must comply with these standards.

---

**Document Version**: 1.0
**Last Updated**: 2026-01-13
**Status**: Active - This is the authoritative reference for all development work
