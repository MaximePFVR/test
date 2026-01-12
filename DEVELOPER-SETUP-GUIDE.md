# Full Stack Developer Setup Guide

## Overview
This guide walks you through setting up a Python-based tool that integrates with the Hunter.io API for email discovery and company information retrieval. As a full stack developer, you'll learn the complete setup process from environment configuration to running the application.

---

## Prerequisites

Before starting, ensure you have:
- **Python 3.8+** installed (`python --version` to check)
- **pip** package manager
- **Git** for version control
- A text editor or IDE (VS Code, PyCharm, etc.)
- Internet connection for API requests

---

## Step-by-Step Setup

### 1. Clone and Navigate to the Project

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Dependencies

The project uses a `requirements.txt` file to manage Python dependencies.

```bash
pip install -r requirements.txt
```

**What this does:**
- Installs all required Python packages (likely including `requests`, `python-dotenv`, etc.)
- Ensures version compatibility across environments
- Creates a reproducible development environment

**Troubleshooting:**
```bash
# If you encounter permission errors, use:
pip install --user -r requirements.txt

# Or create a virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3. Obtain Hunter.io API Key

Hunter.io provides email finding and verification services through their API.

#### Steps to Get Your API Key:

1. **Sign Up:**
   - Visit https://hunter.io/
   - Click "Sign Up" or "Get Started Free"
   - Create an account using your email

2. **Navigate to API Settings:**
   - Log in to your dashboard
   - Go to **API** section (usually in top navigation)
   - Click on **API Keys** tab

3. **Generate/Copy API Key:**
   - Your API key will be displayed
   - Copy it (format: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)

#### Free Tier Limitations:
- **25-50 requests per month** (varies by account)
- Sufficient for development and testing
- Paid plans available for production use

**⚠️ Security Note:** Never commit your API key to version control!

---

### 4. Environment Configuration

The project uses a `.env` file to securely store sensitive credentials.

#### Create Your Environment File:

```bash
# Copy the example template
cp .env.example .env
```

**If .env.example doesn't exist yet**, create it manually:

```bash
# Create .env.example (template for other developers)
cat > .env.example << 'EOF'
# Hunter.io API Configuration
HUNTER_API_KEY=your_api_key_here

# Optional: Additional Configuration
COMPANY_NAME=
DOMAIN=
EOF

# Create your actual .env file
cp .env.example .env
```

#### Configure Your .env File:

Open `.env` in your text editor and add your actual API key:

```bash
# .env
HUNTER_API_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz

# Optional configurations
COMPANY_NAME=Example Corp
DOMAIN=example.com
```

**Environment Variable Best Practices:**
- ✅ Keep `.env` in `.gitignore`
- ✅ Use `.env.example` as a template (without real credentials)
- ✅ Document all required variables
- ✅ Use descriptive variable names

---

### 5. Verify .gitignore Configuration

Ensure your `.env` file is not tracked by Git:

```bash
# Check if .gitignore exists
cat .gitignore

# If it doesn't include .env, add it:
echo ".env" >> .gitignore
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
```

---

### 6. Run the Application

Execute the tool with company name and domain parameters.

#### Basic Usage:

```bash
# Method 1: Direct execution
python main.py --company "TechCorp" --domain "techcorp.com"

# Method 2: Using environment variables from .env
python main.py

# Method 3: Interactive mode (if supported)
python main.py --interactive
```

#### Expected Output:

```
Searching for emails at techcorp.com...
Found 5 email addresses:
  - john.doe@techcorp.com (CEO)
  - jane.smith@techcorp.com (CTO)
  - ...

API Requests Used: 1/50 (monthly limit)
```

---

## Project Structure (Typical Layout)

```
project-root/
├── .env                    # Your local config (not in git)
├── .env.example            # Template for other devs
├── .gitignore              # Exclude sensitive files
├── requirements.txt        # Python dependencies
├── main.py                 # Entry point
├── src/
│   ├── hunter_client.py    # Hunter.io API wrapper
│   ├── email_finder.py     # Core business logic
│   └── utils.py            # Helper functions
├── tests/
│   └── test_hunter.py      # Unit tests
└── README.md               # Project documentation
```

---

## Common Development Tasks

### Update Dependencies

```bash
# List currently installed packages
pip freeze

# Update requirements.txt after adding new packages
pip freeze > requirements.txt

# Install new package and update requirements
pip install package-name
pip freeze > requirements.txt
```

### Testing API Connection

Create a simple test script to verify your setup:

```python
# test_connection.py
import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv('HUNTER_API_KEY')
response = requests.get(
    'https://api.hunter.io/v2/account',
    params={'api_key': api_key}
)

print(f"Status: {response.status_code}")
print(f"API Calls Used: {response.json()['data']['calls']['used']}")
print(f"API Calls Available: {response.json()['data']['calls']['available']}")
```

Run it:
```bash
python test_connection.py
```

---

## Troubleshooting

### Issue: "Module not found"
**Solution:**
```bash
# Ensure you're in the correct directory
pwd

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Invalid API Key"
**Solution:**
- Verify your API key in `.env` is correct (no extra spaces)
- Check if key is activated on Hunter.io dashboard
- Ensure `.env` file is in the project root

### Issue: "Rate limit exceeded"
**Solution:**
- Check your usage on Hunter.io dashboard
- Wait until your monthly limit resets
- Consider upgrading to a paid plan

### Issue: ".env file not loaded"
**Solution:**
```python
# Ensure you're loading it in your Python code:
from dotenv import load_dotenv
load_dotenv()  # Call this before accessing os.getenv()
```

---

## API Usage Best Practices

### 1. Rate Limiting
```python
import time

def make_api_request_with_retry(url, params, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, params=params)
        if response.status_code == 429:  # Rate limited
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
            continue
        return response
    raise Exception("Max retries exceeded")
```

### 2. Error Handling
```python
try:
    response = requests.get(api_url, params={'api_key': api_key})
    response.raise_for_status()  # Raises HTTPError for bad status
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"API Error: {e}")
except ValueError:
    print("Invalid JSON response")
```

### 3. Caching Results
```python
import json
from functools import lru_cache

@lru_cache(maxsize=100)
def get_company_emails(domain):
    # This will cache results and reduce API calls
    return fetch_emails_from_hunter(domain)
```

---

## Security Considerations

### ✅ DO:
- Store API keys in `.env` files
- Use `.gitignore` to exclude `.env`
- Rotate API keys periodically
- Use environment-specific keys (dev/staging/prod)
- Validate and sanitize user inputs

### ❌ DON'T:
- Hard-code API keys in source code
- Commit `.env` files to Git
- Share API keys in chat/email
- Log API keys in application logs
- Use production keys in development

---

## Next Steps

After completing the setup:

1. **Read the API Documentation:**
   - https://hunter.io/api-documentation/v2

2. **Explore Available Endpoints:**
   - Domain Search: Find emails for a domain
   - Email Finder: Find specific person's email
   - Email Verifier: Verify email validity
   - Account Info: Check your usage

3. **Build Features:**
   - Bulk email discovery
   - CSV export functionality
   - Email validation pipeline
   - Integration with CRM systems

4. **Testing:**
   - Write unit tests for API wrapper
   - Mock API responses for testing
   - Test rate limiting behavior

5. **Deployment:**
   - Set up environment variables on server
   - Implement logging and monitoring
   - Configure production API keys

---

## Additional Resources

- **Hunter.io API Docs:** https://hunter.io/api-documentation/v2
- **Python Requests Library:** https://docs.python-requests.org/
- **Python dotenv:** https://pypi.org/project/python-dotenv/
- **API Rate Limiting Best Practices:** https://cloud.google.com/architecture/rate-limiting-strategies

---

## Quick Reference Commands

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env

# Run
python main.py --company "CompanyName" --domain "example.com"

# Test
python test_connection.py
python -m pytest tests/

# Update
pip install <package>
pip freeze > requirements.txt

# Virtual Environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
deactivate                # Exit venv
```

---

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Review Hunter.io API documentation
3. Check your API usage limits
4. Consult ERROR-TRACKING.md for known issues

---

*Last Updated: 2026-01-12*
