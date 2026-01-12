"""
Email Validator Module
Performs syntax validation and basic SMTP verification for email addresses.

LEGAL NOTICE: This module is for PROFESSIONAL B2B USE ONLY.
- Only validate business email addresses
- Avoid validating personal emails (@gmail.com, @yahoo.com, etc.)
- Respect GDPR and privacy regulations
"""

import re
import smtplib
import dns.resolver
import socket
from typing import Dict, Optional


class EmailValidator:
    """
    Validates email addresses using syntax checks and SMTP verification.
    """

    def __init__(self):
        """Initialize the email validator."""
        # List of personal email domains to avoid (GDPR compliance)
        self.personal_domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'aol.com', 'icloud.com', 'mail.com', 'protonmail.com',
            'yandex.com', 'zoho.com'
        ]

        # Email regex pattern (RFC 5322 simplified)
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )

    def is_personal_email(self, email: str) -> bool:
        """
        Check if email is from a personal domain (for GDPR compliance).

        Args:
            email: Email address to check

        Returns:
            True if email is from a personal domain
        """
        domain = email.split('@')[-1].lower()
        return domain in self.personal_domains

    def validate_syntax(self, email: str) -> Dict[str, any]:
        """
        Validate email address syntax.

        Args:
            email: Email address to validate

        Returns:
            Dictionary with validation results

        Example return:
            {
                'valid': True,
                'email': 'john.doe@company.com',
                'message': 'Valid syntax'
            }
        """
        result = {
            'valid': False,
            'email': email,
            'message': ''
        }

        # Check for empty or whitespace
        if not email or not email.strip():
            result['message'] = 'Email is empty'
            return result

        email = email.strip().lower()

        # Check basic format
        if not self.email_pattern.match(email):
            result['message'] = 'Invalid email format'
            return result

        # Check for personal email domains (warning, not error)
        if self.is_personal_email(email):
            result['valid'] = True
            result['message'] = 'WARNING: Personal email domain detected (potential GDPR concern)'
            result['warning'] = True
            return result

        # Check length constraints
        local_part, domain = email.split('@')
        if len(local_part) > 64 or len(domain) > 255:
            result['message'] = 'Email length exceeds limits'
            return result

        result['valid'] = True
        result['message'] = 'Valid syntax'
        return result

    def check_mx_record(self, domain: str) -> bool:
        """
        Check if domain has valid MX (Mail Exchange) records.

        Args:
            domain: Domain to check

        Returns:
            True if MX records exist
        """
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            return len(mx_records) > 0
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            return False
        except Exception:
            # If DNS check fails, assume it might be valid (network issues, etc.)
            return True

    def verify_smtp(self, email: str, timeout: int = 10) -> Dict[str, any]:
        """
        Perform lightweight SMTP verification.

        NOTE: This is a basic check and may not work with all mail servers
        due to anti-spam measures. Many servers will accept RCPT TO without
        actually verifying the mailbox exists.

        Args:
            email: Email address to verify
            timeout: Connection timeout in seconds

        Returns:
            Dictionary with verification results
        """
        result = {
            'valid': False,
            'email': email,
            'smtp_check': False,
            'message': ''
        }

        try:
            # Extract domain
            domain = email.split('@')[-1]

            # Check MX records first
            if not self.check_mx_record(domain):
                result['message'] = 'No MX records found for domain'
                return result

            # Get MX records
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_host = str(mx_records[0].exchange).rstrip('.')

            # Connect to SMTP server
            with smtplib.SMTP(timeout=timeout) as server:
                server.connect(mx_host)
                server.helo('example.com')  # Identify ourselves
                server.mail('verify@example.com')  # Sender

                # Try to verify recipient
                code, message = server.rcpt(email)

                if code == 250:
                    result['valid'] = True
                    result['smtp_check'] = True
                    result['message'] = 'SMTP verification successful'
                else:
                    result['message'] = f'SMTP returned code {code}'

        except socket.timeout:
            result['message'] = 'SMTP connection timeout'
            result['smtp_check'] = None  # Indeterminate
        except smtplib.SMTPServerDisconnected:
            result['message'] = 'SMTP server disconnected'
            result['smtp_check'] = None
        except smtplib.SMTPResponseException as e:
            result['message'] = f'SMTP error: {e.smtp_code}'
            result['smtp_check'] = None
        except Exception as e:
            result['message'] = f'Verification error: {str(e)}'
            result['smtp_check'] = None

        return result

    def validate_email(
        self,
        email: str,
        check_smtp: bool = False
    ) -> Dict[str, any]:
        """
        Comprehensive email validation.

        Args:
            email: Email address to validate
            check_smtp: Whether to perform SMTP verification (slower)

        Returns:
            Dictionary with complete validation results

        Example return:
            {
                'valid': True,
                'email': 'john.doe@company.com',
                'syntax_valid': True,
                'mx_valid': True,
                'smtp_valid': None,
                'message': 'Email appears valid',
                'warnings': []
            }
        """
        result = {
            'valid': False,
            'email': email,
            'syntax_valid': False,
            'mx_valid': False,
            'smtp_valid': None,
            'message': '',
            'warnings': []
        }

        # Step 1: Syntax validation
        syntax_check = self.validate_syntax(email)
        result['syntax_valid'] = syntax_check['valid']

        if not syntax_check['valid']:
            result['message'] = syntax_check['message']
            return result

        # Check for warnings
        if syntax_check.get('warning'):
            result['warnings'].append(syntax_check['message'])

        # Step 2: MX record check
        domain = email.split('@')[-1]
        result['mx_valid'] = self.check_mx_record(domain)

        if not result['mx_valid']:
            result['message'] = 'Domain has no valid MX records'
            return result

        # Step 3: SMTP verification (optional, as it's slow and may be blocked)
        if check_smtp:
            smtp_check = self.verify_smtp(email)
            result['smtp_valid'] = smtp_check['smtp_check']

            if smtp_check['smtp_check'] is False:
                result['message'] = smtp_check['message']
                return result

        # If we made it here, email appears valid
        result['valid'] = True
        result['message'] = 'Email appears valid'

        return result

    def validate_batch(
        self,
        emails: list,
        check_smtp: bool = False
    ) -> list:
        """
        Validate a batch of email addresses.

        Args:
            emails: List of email addresses
            check_smtp: Whether to perform SMTP verification

        Returns:
            List of validation result dictionaries
        """
        results = []

        for email in emails:
            result = self.validate_email(email, check_smtp=check_smtp)
            results.append(result)

        return results
