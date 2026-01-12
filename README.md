# HR Contact Discovery CLI Tool

A professional Python-based command-line tool for discovering HR contacts and facilitating job application follow-up. This tool helps job seekers identify the right contacts (Recruiters, HR Managers, Department Heads) within a company after submitting an application.

## ⚠️ Legal & Ethical Notice

**THIS TOOL IS FOR PROFESSIONAL B2B USE ONLY**

By using this tool, you agree to:

✅ **DO:**
- Only use for legitimate job application follow-up purposes
- Include opt-out/unsubscribe options in ALL emails sent
- Comply with GDPR, CAN-SPAM Act, and other applicable regulations
- Respect data subject rights (access, correction, deletion)
- Only contact professional business email addresses
- Store data securely and delete when no longer needed

❌ **DO NOT:**
- Use for spam or unsolicited marketing
- Contact personal email addresses (@gmail.com, @yahoo.com, etc.)
- Share data with unauthorized third parties
- Ignore opt-out requests
- Violate privacy laws and regulations

## Features

### Core Functionality (MVP)

1. **Lead Discovery**: Search for HR/recruiting professionals on LinkedIn using Google search
2. **Email Pattern Detection**: Integrate with Hunter.io API to discover company email patterns
3. **Email Generation**: Generate probable professional email addresses based on detected patterns
4. **Email Validation**: Perform syntax checks and optional SMTP validation
5. **CSV Export**: Save findings (Name, Title, Email, LinkedIn URL) to a local CSV file

### Technical Features

- **Modular Architecture**: Separate modules for search, email finding, validation, and export
- **API Integration**: Hunter.io for email pattern discovery (Apollo.io can be integrated)
- **GDPR Compliance**: Warnings for personal email domains, ethical use reminders
- **Secure Configuration**: Environment variables for API key management
- **Python 3.10+**: Modern Python with type hints and best practices

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Hunter.io API key (free tier available)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd test
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Hunter.io API key:
   ```bash
   nano .env  # or use your preferred editor
   ```

3. Add your API key:
   ```
   HUNTER_API_KEY=your_actual_api_key_here
   ```

### Step 5: Get Your Hunter.io API Key

1. Visit [Hunter.io](https://hunter.io/)
2. Sign up for a free account
3. Navigate to API section in your dashboard
4. Copy your API key
5. Paste it in your `.env` file

**Free Tier Limits:**
- 25 requests per month (free plan)
- 50 requests per month (upgraded free trial)

## Usage

### Basic Usage

```bash
python -m src.main --company "Company Name" --domain company.com
```

### Advanced Usage Examples

#### Find up to 15 contacts

```bash
python -m src.main --company "Tech Startup" --domain techstartup.io --max-results 15
```

#### Perform SMTP validation (slower but more accurate)

```bash
python -m src.main --company "Acme Corp" --domain acme.com --validate-smtp
```

#### Custom output filename

```bash
python -m src.main --company "Big Company" --domain bigco.com --output custom_contacts.csv
```

#### Skip legal notice (after you've read and agreed)

```bash
python -m src.main --company "Company" --domain company.com --skip-notice
```

#### Display results without exporting

```bash
python -m src.main --company "Company" --domain company.com --no-export
```

### Command-Line Options

```
Options:
  --company TEXT          Company name (required)
  --domain TEXT           Company domain, e.g., "acme.com" (required)
  --max-results INTEGER   Maximum number of contacts to find (default: 10)
  --output TEXT           Output CSV filename (default: followup_contacts.csv)
  --validate-smtp         Perform SMTP validation (slower)
  --skip-notice           Skip the legal notice prompt
  --no-export             Display results without exporting to CSV
  -h, --help             Show help message
```

## Project Structure

```
test/
├── src/
│   ├── __init__.py          # Package initialization with legal notice
│   ├── main.py              # Main CLI controller
│   ├── search.py            # LinkedIn lead discovery module
│   ├── email_finder.py      # Hunter.io integration for email patterns
│   ├── validator.py         # Email validation (syntax + SMTP)
│   └── exporter.py          # CSV export functionality
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment variables
├── .env                     # Your API keys (not in git)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Module Documentation

### search.py - Lead Discovery

Searches for HR/recruiting professionals on LinkedIn using Google search.

**Key Features:**
- Multiple search query variations for better results
- Extracts names from LinkedIn URLs
- Customizable job title filters
- Rate limiting to respect search APIs

### email_finder.py - Email Pattern Detection

Integrates with Hunter.io API to discover and apply email patterns.

**Key Features:**
- Retrieves company email patterns from Hunter.io
- Generates emails based on detected patterns
- Fallback to common patterns if API fails
- Optional email verification via Hunter.io

### validator.py - Email Validation

Performs comprehensive email validation.

**Key Features:**
- Syntax validation (RFC 5322 compliant)
- MX record verification
- Optional SMTP verification
- GDPR compliance checks (warns about personal domains)

### exporter.py - CSV Export

Exports contact data to CSV with legal notices.

**Key Features:**
- Formatted CSV output with proper columns
- Embedded legal/ethical notices in CSV
- Export summary statistics
- Validation results included

## Output Format

The tool generates a CSV file (`followup_contacts.csv` by default) with the following columns:

| Column          | Description                                    |
|-----------------|------------------------------------------------|
| name            | Contact's full name                            |
| title           | Job title (e.g., "Senior Recruiter")          |
| email           | Generated email address                        |
| linkedin_url    | LinkedIn profile URL                           |
| email_valid     | Email validation status (True/False)           |
| company_domain  | Company domain                                 |
| export_date     | Timestamp of export                            |

## API Rate Limits

### Hunter.io (Free Tier)
- 25-50 requests per month
- 1 request for email pattern per domain
- Optional: 1 request per email for verification

**Tips to Conserve API Calls:**
- Use the same domain for multiple searches
- Skip SMTP validation unless necessary
- The tool caches patterns during the same run

## Troubleshooting

### "HUNTER_API_KEY not found"

**Solution:** Make sure you have:
1. Created a `.env` file in the project root
2. Added `HUNTER_API_KEY=your_key` to the file
3. No spaces around the `=` sign

### "No contacts found"

**Possible causes:**
- Company name or domain might be incorrect
- Limited public LinkedIn profiles
- Search API rate limiting

**Solutions:**
- Try different company name variations
- Increase `--max-results`
- Wait a few minutes and try again

### "Email validation failed"

**Possible causes:**
- Domain has no MX records
- SMTP server blocking verification attempts
- Network/firewall issues

**Solutions:**
- Don't use `--validate-smtp` flag
- Check if the domain is correct
- Manual verification might be needed

### ImportError or ModuleNotFoundError

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

## Best Practices for Using the Tool

### 1. Research First
- Verify the company domain is correct
- Check the company's LinkedIn page
- Understand the company structure

### 2. Professional Outreach
- Personalize every email
- Be concise and respectful
- Include your application details
- **Always include an opt-out option**

### 3. Email Template Example

```
Subject: Following up on [Position] Application - [Your Name]

Hi [Contact Name],

I recently applied for the [Position Title] role at [Company Name] and wanted
to reach out directly to express my strong interest.

[Brief 2-3 sentences about why you're a good fit]

I would appreciate the opportunity to discuss how my experience aligns with
your team's needs. Would you be open to a brief conversation?

Thank you for your time and consideration.

Best regards,
[Your Name]
[Your Contact Info]

---
If you'd prefer not to receive follow-up messages, please reply with
"unsubscribe" and I'll remove you from my outreach list.
```

### 4. Respect Privacy
- Delete data when no longer needed
- Honor all opt-out requests immediately
- Don't share data with third parties
- Follow GDPR and local privacy laws

### 5. Track Your Outreach
- Keep records of who you contacted
- Note responses and opt-outs
- Don't contact the same person multiple times
- Respect "no response" as a boundary

## Contributing

Contributions are welcome! Please ensure any contributions:
- Maintain GDPR/privacy compliance
- Include appropriate error handling
- Follow PEP 8 style guidelines
- Add tests for new functionality

## Limitations

- **Search Accuracy**: Results depend on publicly available LinkedIn data
- **Email Accuracy**: Generated emails are probabilistic, not guaranteed
- **API Dependencies**: Requires Hunter.io API for best results
- **Rate Limits**: Free tier has monthly request limits
- **SMTP Validation**: May be blocked by some mail servers

## Future Enhancements

Potential features for future versions:
- Apollo.io integration as an alternative to Hunter.io
- LinkedIn API integration (requires paid LinkedIn access)
- Bulk company processing
- Response tracking system
- Email template management
- CRM integration

## License

This tool is provided for educational and professional use. Users are solely responsible for ensuring their use complies with all applicable laws and regulations including GDPR, CAN-SPAM Act, and other privacy legislation.

## Disclaimer

This tool is provided "as is" without warranty of any kind. The authors and contributors are not responsible for:
- Misuse of the tool
- Privacy violations
- Regulatory non-compliance
- Generated email accuracy
- Any damages resulting from use

Users must ensure their use complies with all applicable laws and regulations.

## Support

For issues, questions, or contributions:
1. Check the Troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed information

## Acknowledgments

- Hunter.io for email discovery API
- googlesearch-python for search functionality
- The Python community for excellent libraries

---

**Remember: Professional, respectful, compliant outreach is not just legally required—it's the right thing to do.**