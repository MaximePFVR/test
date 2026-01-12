"""
CSV Exporter Module
Exports contact data to CSV format for easy follow-up.

LEGAL NOTICE: This module is for PROFESSIONAL B2B USE ONLY.
Users MUST include opt-out/unsubscribe options in all communications
sent to contacts exported by this tool.
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict
import os


class ContactExporter:
    """
    Exports contact information to CSV format with proper formatting and metadata.
    """

    def __init__(self, output_dir: str = '.'):
        """
        Initialize the exporter.

        Args:
            output_dir: Directory to save CSV files (default: current directory)
        """
        self.output_dir = output_dir

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

    def format_contacts_dataframe(self, contacts: List[Dict]) -> pd.DataFrame:
        """
        Format contacts list into a pandas DataFrame with proper columns.

        Args:
            contacts: List of contact dictionaries

        Returns:
            Formatted pandas DataFrame
        """
        # Define column order
        columns = [
            'name',
            'title',
            'email',
            'linkedin_url',
            'email_valid',
            'company_domain',
            'export_date'
        ]

        # Add export timestamp
        for contact in contacts:
            contact['export_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create DataFrame
        df = pd.DataFrame(contacts)

        # Ensure all columns exist
        for col in columns:
            if col not in df.columns:
                df[col] = ''

        # Reorder columns
        df = df[columns]

        return df

    def export_to_csv(
        self,
        contacts: List[Dict],
        filename: str = 'followup_contacts.csv',
        include_header_note: bool = True
    ) -> str:
        """
        Export contacts to CSV file.

        Args:
            contacts: List of contact dictionaries
            filename: Output filename
            include_header_note: Whether to include legal/ethical note

        Returns:
            Full path to the exported CSV file
        """
        if not contacts:
            print("⚠️  No contacts to export")
            return None

        # Format as DataFrame
        df = self.format_contacts_dataframe(contacts)

        # Full output path
        output_path = os.path.join(self.output_dir, filename)

        # Export to CSV
        df.to_csv(output_path, index=False, encoding='utf-8')

        # Add legal/ethical notice as a comment at the top if requested
        if include_header_note:
            self._add_csv_header_note(output_path)

        print(f"\n✓ Exported {len(contacts)} contacts to: {output_path}")

        return output_path

    def _add_csv_header_note(self, csv_path: str):
        """
        Add legal and ethical notice to the top of the CSV file.

        Args:
            csv_path: Path to the CSV file
        """
        notice = """# HR CONTACT DISCOVERY TOOL - LEGAL & ETHICAL NOTICE
#
# This file contains contact information for PROFESSIONAL B2B USE ONLY.
#
# REQUIREMENTS FOR USE:
# 1. Only use for legitimate job application follow-up purposes
# 2. MUST include an opt-out/unsubscribe option in ALL emails sent
# 3. Comply with GDPR, CAN-SPAM Act, and other applicable regulations
# 4. Respect data subject rights (access, correction, deletion)
# 5. Do NOT use for spam, marketing, or unsolicited communications
# 6. Obtain explicit consent where required by law
#
# PRIVACY NOTICE:
# - This data should be stored securely and deleted when no longer needed
# - Do not share this data with third parties without proper authorization
# - Personal email addresses (@gmail, @yahoo, etc.) should NOT be used
#
# By using this data, you agree to comply with all applicable laws and regulations.
#
"""

        # Read existing content
        with open(csv_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Write notice + content
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(notice)
            f.write(content)

    def export_summary(self, contacts: List[Dict]) -> Dict:
        """
        Generate a summary of the exported contacts.

        Args:
            contacts: List of contact dictionaries

        Returns:
            Summary dictionary with statistics
        """
        summary = {
            'total_contacts': len(contacts),
            'valid_emails': sum(1 for c in contacts if c.get('email_valid')),
            'with_linkedin': sum(1 for c in contacts if c.get('linkedin_url')),
            'unique_companies': len(set(c.get('company_domain', '') for c in contacts))
        }

        return summary

    def print_summary(self, contacts: List[Dict]):
        """
        Print a formatted summary of the export.

        Args:
            contacts: List of contact dictionaries
        """
        summary = self.export_summary(contacts)

        print("\n" + "="*60)
        print("EXPORT SUMMARY")
        print("="*60)
        print(f"Total Contacts:      {summary['total_contacts']}")
        print(f"Valid Emails:        {summary['valid_emails']}")
        print(f"LinkedIn Profiles:   {summary['with_linkedin']}")
        print(f"Unique Companies:    {summary['unique_companies']}")
        print("="*60)

        print("\n📋 NEXT STEPS:")
        print("1. Review the contacts in the CSV file")
        print("2. Personalize your outreach emails")
        print("3. IMPORTANT: Include an opt-out/unsubscribe option")
        print("4. Follow up professionally and respectfully")
        print("5. Track responses and respect opt-out requests")
        print("\n⚠️  REMEMBER: This tool is for professional B2B use only.")
        print("   Always comply with GDPR, CAN-SPAM, and privacy regulations.\n")

    def export_with_validation(
        self,
        contacts: List[Dict],
        validation_results: List[Dict],
        filename: str = 'followup_contacts.csv'
    ) -> str:
        """
        Export contacts with validation results included.

        Args:
            contacts: List of contact dictionaries
            validation_results: List of validation result dictionaries
            filename: Output filename

        Returns:
            Full path to the exported CSV file
        """
        # Merge validation results into contacts
        for i, contact in enumerate(contacts):
            if i < len(validation_results):
                val_result = validation_results[i]
                contact['email_valid'] = val_result.get('valid', False)
                contact['validation_message'] = val_result.get('message', '')
                contact['mx_valid'] = val_result.get('mx_valid', False)

        return self.export_to_csv(contacts, filename)
