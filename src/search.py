"""
Lead Search Module
Uses Google search to discover LinkedIn profiles of HR/recruiting contacts.

LEGAL NOTICE: This module is for PROFESSIONAL B2B USE ONLY.
- Only search for publicly available professional information
- Respect robots.txt and terms of service
- Do not scrape private personal data
"""

import re
import time
from typing import List, Dict, Optional
from googlesearch import search


class LeadSearcher:
    """
    Search for HR and recruiting professionals on LinkedIn using Google search.
    """

    def __init__(self):
        """Initialize the lead searcher with search parameters."""
        self.hr_titles = [
            "Recruiter",
            "Talent Acquisition",
            "HR Manager",
            "Human Resources Manager",
            "Head of HR",
            "People Operations",
            "Talent Acquisition Manager",
            "Recruiting Manager",
            "Director of Talent Acquisition",
            "VP of People",
            "Chief People Officer"
        ]

    def build_search_queries(self, company_name: str, domain: str) -> List[str]:
        """
        Build Google search queries for finding HR contacts on LinkedIn.

        Args:
            company_name: Name of the company
            domain: Company domain

        Returns:
            List of search queries
        """
        queries = []

        # Search variations for better results
        search_terms = [
            f'site:linkedin.com/in "{company_name}" (Recruiter OR "Talent Acquisition")',
            f'site:linkedin.com/in "{company_name}" ("HR Manager" OR "Human Resources")',
            f'site:linkedin.com/in "{company_name}" ("Head of" OR "Director") (HR OR Recruiting)',
            f'site:linkedin.com/in "{domain}" Recruiter',
            f'site:linkedin.com/in "{domain}" "Talent Acquisition"',
        ]

        queries.extend(search_terms)
        return queries

    def extract_name_from_linkedin_url(self, url: str) -> Optional[str]:
        """
        Extract and format name from LinkedIn profile URL.

        Args:
            url: LinkedIn profile URL

        Returns:
            Formatted name or None

        Example:
            >>> extract_name_from_linkedin_url('https://www.linkedin.com/in/john-doe-12345')
            'John Doe'
        """
        # Extract the LinkedIn username from URL
        match = re.search(r'linkedin\.com/in/([^/?]+)', url)
        if not match:
            return None

        username = match.group(1)

        # Remove trailing numbers/identifiers (e.g., john-doe-12345 -> john-doe)
        username = re.sub(r'-\d+[a-z]*$', '', username)

        # Convert hyphenated name to Title Case
        name_parts = username.split('-')
        formatted_name = ' '.join(word.capitalize() for word in name_parts if word)

        # Basic validation
        if len(formatted_name) < 3 or len(formatted_name) > 50:
            return None

        return formatted_name

    def extract_title_from_snippet(self, snippet: str) -> Optional[str]:
        """
        Extract job title from search result snippet.

        Args:
            snippet: Text snippet from search result

        Returns:
            Extracted title or default title
        """
        # Common patterns in LinkedIn snippets
        title_patterns = [
            r'(Recruiter[^•|]*)',
            r'(Talent Acquisition[^•|]*)',
            r'(HR Manager[^•|]*)',
            r'(Human Resources[^•|]*)',
            r'(Head of[^•|]*)',
            r'(Director of[^•|]*)',
            r'(VP of[^•|]*)',
            r'(Chief People Officer[^•|]*)',
        ]

        for pattern in title_patterns:
            match = re.search(pattern, snippet, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Clean up the title
                title = re.sub(r'\s+', ' ', title)
                return title[:100]  # Limit length

        # Default if no specific title found
        return "HR/Recruiting Professional"

    def search_linkedin_contacts(
        self,
        company_name: str,
        domain: str,
        max_results: int = 10
    ) -> List[Dict[str, str]]:
        """
        Search for LinkedIn contacts at the specified company.

        Args:
            company_name: Name of the company
            domain: Company domain
            max_results: Maximum number of contacts to find

        Returns:
            List of contact dictionaries with name, title, and linkedin_url

        Example return:
            [
                {
                    'name': 'John Doe',
                    'title': 'Senior Recruiter',
                    'linkedin_url': 'https://linkedin.com/in/john-doe'
                }
            ]
        """
        print(f"\n🔍 Searching for HR contacts at {company_name}...")

        contacts = []
        seen_urls = set()

        queries = self.build_search_queries(company_name, domain)

        for query in queries:
            if len(contacts) >= max_results:
                break

            print(f"   Searching: {query[:80]}...")

            try:
                # Use googlesearch-python library
                # Note: Add delays to be respectful of rate limits
                results = search(query, num_results=5, sleep_interval=2, lang='en')

                for url in results:
                    if len(contacts) >= max_results:
                        break

                    # Skip if we've already seen this URL
                    if url in seen_urls:
                        continue

                    seen_urls.add(url)

                    # Extract name from LinkedIn URL
                    name = self.extract_name_from_linkedin_url(url)

                    if name:
                        contact = {
                            'name': name,
                            'title': "HR/Recruiting Professional",  # Default title
                            'linkedin_url': url
                        }
                        contacts.append(contact)
                        print(f"   ✓ Found: {name}")

                # Be respectful - add delay between queries
                time.sleep(2)

            except Exception as e:
                print(f"   ⚠️  Search error: {e}")
                continue

        print(f"\n✓ Found {len(contacts)} contacts")

        return contacts

    def enhance_contact_info(self, contacts: List[Dict]) -> List[Dict]:
        """
        Enhance contact information with additional details.

        Args:
            contacts: List of basic contact dictionaries

        Returns:
            Enhanced contact list
        """
        # This method can be extended to scrape more details if needed
        # For now, it's a placeholder for future enhancements
        return contacts

    def filter_by_title(self, contacts: List[Dict], titles: List[str]) -> List[Dict]:
        """
        Filter contacts by specific job titles.

        Args:
            contacts: List of contact dictionaries
            titles: List of titles to filter by

        Returns:
            Filtered contact list
        """
        if not titles:
            return contacts

        filtered = []
        for contact in contacts:
            for title in titles:
                if title.lower() in contact.get('title', '').lower():
                    filtered.append(contact)
                    break

        return filtered
