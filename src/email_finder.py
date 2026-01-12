"""
Email Finder Module
Integrates with Hunter.io API to discover email patterns and generate professional emails.

LEGAL NOTICE: This module is for PROFESSIONAL B2B USE ONLY.
Always respect privacy laws (GDPR, CAN-SPAM) and include opt-out options in communications.
"""

import os
import requests
from typing import Dict, Optional, List
from dotenv import load_dotenv

load_dotenv()


class EmailFinder:
    """
    Hunter.io API integration for email pattern discovery and email generation.
    """

    def __init__(self):
        """Initialize EmailFinder with Hunter.io API key from environment."""
        self.api_key = os.getenv('HUNTER_API_KEY')
        self.base_url = "https://api.hunter.io/v2"

        if not self.api_key:
            print("⚠️  WARNING: HUNTER_API_KEY not found in environment variables.")
            print("   Email pattern discovery will not work without a valid API key.")

    def get_email_pattern(self, domain: str) -> Optional[Dict]:
        """
        Retrieve the email pattern for a given domain from Hunter.io.

        Args:
            domain: Company domain (e.g., "company.com")

        Returns:
            Dictionary containing email pattern and other domain info, or None if not found.

        Example return:
            {
                'pattern': '{first}.{last}@company.com',
                'organization': 'Company Name',
                'emails': 50
            }
        """
        if not self.api_key:
            print("❌ Cannot retrieve email pattern: API key not configured.")
            return None

        try:
            url = f"{self.base_url}/domain-search"
            params = {
                'domain': domain,
                'api_key': self.api_key,
                'limit': 1  # We only need the pattern, not actual emails
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get('data'):
                pattern = data['data'].get('pattern')
                organization = data['data'].get('organization')
                emails = data['data'].get('emails', 0)

                if pattern:
                    print(f"✓ Found email pattern for {domain}: {pattern}")
                    return {
                        'pattern': pattern,
                        'organization': organization,
                        'emails': emails,
                        'domain': domain
                    }
                else:
                    print(f"⚠️  No email pattern found for {domain}")
                    return None
            else:
                print(f"⚠️  No data available for domain: {domain}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"❌ Error retrieving email pattern: {e}")
            return None

    def generate_email(self, first_name: str, last_name: str, domain: str, pattern: str) -> str:
        """
        Generate a professional email address based on the company's email pattern.

        Args:
            first_name: Contact's first name
            last_name: Contact's last name
            domain: Company domain
            pattern: Email pattern (e.g., '{first}.{last}@{domain}')

        Returns:
            Generated email address

        Example:
            >>> generate_email('John', 'Doe', 'company.com', '{first}.{last}@{domain}')
            'john.doe@company.com'
        """
        # Clean and normalize names
        first = first_name.lower().strip().replace(' ', '')
        last = last_name.lower().strip().replace(' ', '')

        # Common pattern variations
        pattern_map = {
            '{first}': first,
            '{last}': last,
            '{f}': first[0] if first else '',
            '{l}': last[0] if last else '',
            '{domain}': domain
        }

        # Replace pattern placeholders
        email = pattern
        for placeholder, value in pattern_map.items():
            email = email.replace(placeholder, value)

        # Ensure proper format
        if '@' not in email:
            email = f"{email}@{domain}"

        return email

    def generate_emails_for_leads(self, leads: List[Dict], domain: str) -> List[Dict]:
        """
        Generate email addresses for a list of leads.

        Args:
            leads: List of lead dictionaries with 'name' and 'title' fields
            domain: Company domain

        Returns:
            Updated leads list with 'email' field added
        """
        pattern_info = self.get_email_pattern(domain)

        if not pattern_info or not pattern_info.get('pattern'):
            # Fallback to common pattern if Hunter.io doesn't return one
            print(f"⚠️  Using fallback email pattern: {{first}}.{{last}}@{domain}")
            pattern = f"{{first}}.{{last}}@{{domain}}"
        else:
            pattern = pattern_info['pattern']

        for lead in leads:
            # Parse name (assuming format "First Last" or "First Middle Last")
            name_parts = lead['name'].strip().split()

            if len(name_parts) >= 2:
                first_name = name_parts[0]
                last_name = name_parts[-1]
            elif len(name_parts) == 1:
                first_name = name_parts[0]
                last_name = name_parts[0]
            else:
                print(f"⚠️  Unable to parse name: {lead['name']}")
                lead['email'] = f"unknown@{domain}"
                continue

            lead['email'] = self.generate_email(first_name, last_name, domain, pattern)

        return leads

    def verify_email(self, email: str) -> Optional[Dict]:
        """
        Verify an email address using Hunter.io email verifier.

        Args:
            email: Email address to verify

        Returns:
            Dictionary with verification results or None

        Example return:
            {
                'status': 'valid',
                'score': 95,
                'result': 'deliverable'
            }
        """
        if not self.api_key:
            return None

        try:
            url = f"{self.base_url}/email-verifier"
            params = {
                'email': email,
                'api_key': self.api_key
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get('data'):
                return {
                    'status': data['data'].get('status'),
                    'score': data['data'].get('score'),
                    'result': data['data'].get('result')
                }

            return None

        except requests.exceptions.RequestException as e:
            print(f"⚠️  Email verification error: {e}")
            return None
