#!/usr/bin/env python3
"""
HR Contact Discovery CLI Tool
Main controller for the application.

LEGAL & ETHICAL NOTICE:
This tool is designed for PROFESSIONAL B2B USE ONLY. Users must:
- Only use for legitimate job application follow-up purposes
- Include opt-out/unsubscribe options in all emails sent
- Comply with GDPR, CAN-SPAM, and other applicable regulations
- Avoid scraping private personal data (e.g., @gmail.com, @yahoo.com)
- Respect data subject rights and privacy

Usage:
    python -m src.main --company "Company Name" --domain company.com
    python -m src.main --company "Company Name" --domain company.com --max-results 15
    python -m src.main --company "Company Name" --domain company.com --validate-smtp
"""

import argparse
import sys
from typing import Optional
from dotenv import load_dotenv

from .search import LeadSearcher
from .email_finder import EmailFinder
from .validator import EmailValidator
from .exporter import ContactExporter

# Load environment variables
load_dotenv()


def print_banner():
    """Print application banner."""
    banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║          HR CONTACT DISCOVERY CLI TOOL v1.0                    ║
║          Professional B2B Contact Discovery                    ║
║                                                                ║
║  ⚠️  LEGAL NOTICE: For professional job application           ║
║     follow-up use only. Always include opt-out options.        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_legal_notice():
    """Print legal and ethical notice."""
    notice = """
LEGAL & ETHICAL REQUIREMENTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

By using this tool, you agree to:

✓ Use ONLY for legitimate job application follow-up
✓ Include opt-out/unsubscribe options in ALL emails
✓ Comply with GDPR, CAN-SPAM, and applicable regulations
✓ Respect data subject rights (access, correction, deletion)
✓ Only contact professional business email addresses
✓ Store data securely and delete when no longer needed

✗ Do NOT use for spam or unsolicited marketing
✗ Do NOT contact personal email addresses (@gmail, @yahoo, etc.)
✗ Do NOT share data with unauthorized third parties

Press Enter to continue or Ctrl+C to exit...
"""
    print(notice)
    try:
        input()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='HR Contact Discovery CLI Tool - Find HR contacts for job application follow-up',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --company "Acme Corp" --domain acme.com
  %(prog)s --company "Tech Startup" --domain techstartup.io --max-results 15
  %(prog)s --company "Big Company" --domain bigco.com --validate-smtp --output contacts.csv

For more information, see README.md
        """
    )

    parser.add_argument(
        '--company',
        type=str,
        required=True,
        help='Company name (e.g., "Acme Corporation")'
    )

    parser.add_argument(
        '--domain',
        type=str,
        required=True,
        help='Company domain (e.g., "acme.com")'
    )

    parser.add_argument(
        '--max-results',
        type=int,
        default=10,
        help='Maximum number of contacts to find (default: 10)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='followup_contacts.csv',
        help='Output CSV filename (default: followup_contacts.csv)'
    )

    parser.add_argument(
        '--validate-smtp',
        action='store_true',
        help='Perform SMTP validation (slower, may be blocked by some servers)'
    )

    parser.add_argument(
        '--skip-notice',
        action='store_true',
        help='Skip the legal notice prompt (use only if you have read and agreed)'
    )

    parser.add_argument(
        '--no-export',
        action='store_true',
        help='Do not export to CSV (just display results)'
    )

    return parser.parse_args()


def main():
    """Main application entry point."""
    print_banner()

    # Parse arguments
    args = parse_arguments()

    # Show legal notice unless skipped
    if not args.skip_notice:
        print_legal_notice()

    print("\n🚀 Starting HR Contact Discovery...\n")
    print(f"Target Company: {args.company}")
    print(f"Domain: {args.domain}")
    print(f"Max Results: {args.max_results}")
    print("─" * 60)

    # Initialize modules
    searcher = LeadSearcher()
    email_finder = EmailFinder()
    validator = EmailValidator()
    exporter = ContactExporter()

    # Step 1: Search for LinkedIn contacts
    print("\n[STEP 1/4] Searching for HR contacts on LinkedIn...")
    contacts = searcher.search_linkedin_contacts(
        company_name=args.company,
        domain=args.domain,
        max_results=args.max_results
    )

    if not contacts:
        print("\n❌ No contacts found. Try adjusting your search criteria.")
        sys.exit(1)

    # Step 2: Generate email addresses
    print("\n[STEP 2/4] Generating email addresses...")
    contacts = email_finder.generate_emails_for_leads(contacts, args.domain)

    # Add company domain to each contact
    for contact in contacts:
        contact['company_domain'] = args.domain

    # Display found contacts
    print("\n📋 Contacts Found:")
    print("─" * 60)
    for i, contact in enumerate(contacts, 1):
        print(f"\n{i}. {contact['name']}")
        print(f"   Title: {contact['title']}")
        print(f"   Email: {contact['email']}")
        print(f"   LinkedIn: {contact['linkedin_url']}")

    # Step 3: Validate emails
    print("\n[STEP 3/4] Validating email addresses...")
    validation_results = []

    for contact in contacts:
        print(f"   Validating: {contact['email']}...", end=' ')

        result = validator.validate_email(
            contact['email'],
            check_smtp=args.validate_smtp
        )

        validation_results.append(result)
        contact['email_valid'] = result['valid']

        if result['valid']:
            print("✓ Valid")
        else:
            print(f"✗ {result['message']}")

        # Show warnings
        if result.get('warnings'):
            for warning in result['warnings']:
                print(f"      ⚠️  {warning}")

    # Step 4: Export to CSV
    if not args.no_export:
        print("\n[STEP 4/4] Exporting to CSV...")
        output_path = exporter.export_with_validation(
            contacts,
            validation_results,
            filename=args.output
        )

        # Print summary
        exporter.print_summary(contacts)

        print(f"\n✅ SUCCESS! Contacts exported to: {output_path}\n")
    else:
        print("\n[STEP 4/4] Export skipped (--no-export flag used)")
        exporter.print_summary(contacts)

    print("\n🎉 HR Contact Discovery completed successfully!\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
