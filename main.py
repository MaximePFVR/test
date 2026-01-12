#!/usr/bin/env python3
"""
Professional Lead Discovery Tool using Hunter.io
Finds professional email contacts from a company domain for job application follow-ups.
"""

import os
import sys
import csv
import requests
from pathlib import Path
from dotenv import load_dotenv


def load_api_key():
    """Load the Hunter.io API key from .env file."""
    load_dotenv()
    api_key = os.getenv('HUNTER_API_KEY')

    if not api_key:
        print("❌ Error: HUNTER_API_KEY not found in .env file")
        print("Please add your Hunter.io API key to the .env file:")
        print("HUNTER_API_KEY=your_api_key_here")
        sys.exit(1)

    return api_key


def validate_domain(domain):
    """Basic validation for domain format."""
    domain = domain.strip().lower()
    # Remove http://, https://, and www. if present
    domain = domain.replace('http://', '').replace('https://', '').replace('www.', '')
    # Remove trailing slash
    domain = domain.rstrip('/')

    if not domain or '.' not in domain:
        return None

    return domain


def search_domain(domain, api_key, limit=10):
    """
    Search for professional contacts using Hunter.io Domain Search API.

    Args:
        domain: Company domain (e.g., apple.com)
        api_key: Hunter.io API key
        limit: Maximum number of results (default 10)

    Returns:
        dict: API response data or None if error
    """
    url = "https://api.hunter.io/v2/domain-search"
    params = {
        'domain': domain,
        'api_key': api_key,
        'limit': limit
    }

    try:
        print(f"\n🔍 Searching for professional contacts at {domain}...")
        response = requests.get(url, params=params, timeout=10)

        # Check for HTTP errors
        if response.status_code == 401:
            print("❌ Error: Invalid API key. Please check your HUNTER_API_KEY in .env")
            return None
        elif response.status_code == 429:
            print("❌ Error: Monthly credit limit reached or rate limit exceeded")
            print("Please check your Hunter.io account at https://hunter.io/users/usage")
            return None
        elif response.status_code == 400:
            data = response.json()
            error_msg = data.get('errors', [{}])[0].get('details', 'Invalid request')
            print(f"❌ Error: {error_msg}")
            return None
        elif response.status_code != 200:
            print(f"❌ Error: API request failed with status code {response.status_code}")
            return None

        data = response.json()
        return data.get('data', {})

    except requests.exceptions.Timeout:
        print("❌ Error: Request timed out. Please check your internet connection.")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to Hunter.io API. Please check your internet connection.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: Request failed - {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None


def display_results(data):
    """Display results in a clean, readable table format."""
    if not data:
        return []

    emails = data.get('emails', [])
    pattern = data.get('pattern', 'Unknown')
    organization = data.get('organization', data.get('domain', 'Unknown'))

    print("\n" + "="*80)
    print(f"🏢 Company: {organization}")
    print(f"📧 Email Pattern: {pattern}")
    print(f"👥 Contacts Found: {len(emails)}")
    print("="*80)

    if not emails:
        print("\n⚠️  No contacts found for this domain.")
        print("This could mean:")
        print("  - The domain is not in Hunter.io's database")
        print("  - The company has very limited public information")
        print("  - Try a different domain or check the spelling")
        return []

    # Display table header
    print(f"\n{'#':<4} {'Full Name':<25} {'Job Title':<30} {'Email':<35}")
    print("-" * 94)

    # Prepare contacts list for CSV export
    contacts = []

    for idx, email_data in enumerate(emails, 1):
        first_name = email_data.get('first_name', '')
        last_name = email_data.get('last_name', '')
        full_name = f"{first_name} {last_name}".strip() or "N/A"

        position = email_data.get('position', 'N/A')
        email = email_data.get('value', 'N/A')

        # Truncate long strings for display
        full_name_display = full_name[:24] if len(full_name) > 24 else full_name
        position_display = position[:29] if len(position) > 29 else position
        email_display = email[:34] if len(email) > 34 else email

        print(f"{idx:<4} {full_name_display:<25} {position_display:<30} {email_display:<35}")

        # Store full data for CSV
        contacts.append({
            'Full Name': full_name,
            'Job Title': position,
            'Email': email,
            'Company': organization,
            'Department': email_data.get('department', 'N/A'),
            'Confidence': email_data.get('confidence', 'N/A')
        })

    print("-" * 94)
    return contacts


def export_to_csv(contacts, domain):
    """Export contacts to CSV file on Desktop."""
    if not contacts:
        print("\n⚠️  No contacts to export.")
        return

    # Get Desktop path (works on macOS and Linux)
    desktop_path = Path.home() / "Desktop"

    # If Desktop doesn't exist, use home directory
    if not desktop_path.exists():
        desktop_path = Path.home()
        print(f"\n⚠️  Desktop folder not found, saving to home directory instead.")

    csv_file = desktop_path / "contacts_found.csv"

    try:
        # Check if file exists to determine if we should write headers
        file_exists = csv_file.exists()

        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            fieldnames = ['Full Name', 'Job Title', 'Email', 'Company', 'Department', 'Confidence']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            # Write header only if file is new
            if not file_exists:
                writer.writeheader()

            writer.writerows(contacts)

        print(f"\n✅ Results exported to: {csv_file}")
        print(f"   ({len(contacts)} contacts {'added' if file_exists else 'saved'})")

    except PermissionError:
        print(f"\n❌ Error: Permission denied when writing to {csv_file}")
        print("Please check file permissions and ensure the file is not open.")
    except Exception as e:
        print(f"\n❌ Error saving CSV: {str(e)}")


def display_gdpr_notice():
    """Display GDPR and professional use reminder."""
    print("\n" + "="*80)
    print("⚖️  IMPORTANT - GDPR & Professional Use Notice")
    print("="*80)
    print("""
These email addresses are intended for PROFESSIONAL B2B purposes ONLY.

Requirements:
• Only use for legitimate business purposes (job applications, B2B outreach)
• Include a clear opt-out/unsubscribe option in all communications
• Respect GDPR, CAN-SPAM, and other data protection regulations
• Do NOT use for spam, marketing without consent, or personal purposes
• Ensure your communications are relevant and professional

For more information: https://gdpr.eu/email-encryption/
""")
    print("="*80)


def main():
    """Main function to run the lead discovery tool."""
    print("\n" + "="*80)
    print("🎯 Professional Lead Discovery Tool - Hunter.io")
    print("="*80)

    # Load API key
    api_key = load_api_key()

    # Get domain from user
    print("\nEnter the company domain you want to search")
    print("Examples: apple.com, google.com, startup.fr")
    domain_input = input("\n🔎 Company domain: ").strip()

    if not domain_input:
        print("❌ Error: No domain provided")
        sys.exit(1)

    # Validate domain
    domain = validate_domain(domain_input)
    if not domain:
        print(f"❌ Error: Invalid domain format '{domain_input}'")
        print("Please enter a valid domain (e.g., company.com)")
        sys.exit(1)

    # Search for contacts
    data = search_domain(domain, api_key, limit=10)

    if data is None:
        sys.exit(1)

    # Display results
    contacts = display_results(data)

    # Export to CSV
    if contacts:
        export_to_csv(contacts, domain)

    # Display GDPR notice
    display_gdpr_notice()

    print("\n✨ Done! Thank you for using the Lead Discovery Tool.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
