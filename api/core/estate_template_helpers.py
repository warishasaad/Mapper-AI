# --- START OF CORRECTED FILE: api/core/estate_template_helpers.py ---

"""
Specialized Canadian Estate Template Helpers

Domain-specific formatting helpers for Canadian estate forms,
legal documents, and province-specific requirements.
"""

import re
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from decimal import Decimal
from dataclasses import dataclass

# MODIFIED: Corrected the import to be relative to the current package
from .models import ProvincialJurisdiction

@dataclass
class TemplateHelper:
    """Template helper definition"""
    name: str
    description: str
    modifiers: List[str]
    examples: List[str]
    implementation: callable

class EstateTemplateHelpers:
    """Specialized template helpers for Canadian estate processing"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.helpers = self._register_helpers()
        self.provincial_formats = self._load_provincial_formats()

        self.logger.info("Estate Template Helpers initialized")

    def _register_helpers(self) -> Dict[str, TemplateHelper]:
        """Register all estate-specific template helpers"""

        helpers = {}

        # Enhanced name helper
        helpers["estate_name"] = TemplateHelper(
            name="estate_name",
            description="Format names for estate documents with proper legal formatting",
            modifiers=["formal", "first_last", "last_first", "initials", "legal"],
            examples=[
                "{{#estate_name:formal deceased.name}}",
                "{{#estate_name:legal applicant.name}}"
            ],
            implementation=self._format_estate_name
        )

        # Canadian legal date helper
        helpers["legal_date"] = TemplateHelper(
            name="legal_date",
            description="Format dates for Canadian legal documents",
            modifiers=["long", "short", "ordinal", "written"],
            examples=[
                "{{#legal_date:long deceased.date_of_death}}",
                "{{#legal_date:written will.date_created}}"
            ],
            implementation=self._format_legal_date
        )

        # Canadian currency helper
        helpers["canadian_currency"] = TemplateHelper(
            name="canadian_currency",
            description="Format Canadian currency for legal documents",
            modifiers=["formal", "written", "short", "cents"],
            examples=[
                "{{#canadian_currency:formal estate.total_value}}",
                "{{#canadian_currency:written insurance.benefit_amount}}"
            ],
            implementation=self._format_canadian_currency
        )

        # Provincial address helper
        helpers["provincial_address"] = TemplateHelper(
            name="provincial_address",
            description="Format addresses according to provincial standards",
            modifiers=["full", "mailing", "short", "legal"],
            examples=[
                "{{#provincial_address:full deceased.home_address}}",
                "{{#provincial_address:legal applicant.address}}"
            ],
            implementation=self._format_provincial_address
        )

        # Legal relationship helper
        helpers["legal_relationship"] = TemplateHelper(
            name="legal_relationship",
            description="Format relationships for legal documents",
            modifiers=["formal", "possessive", "descriptive"],
            examples=[
                "{{#legal_relationship:formal applicant.relationship}}",
                "{{#legal_relationship:possessive spouse.relationship}}"
            ],
            implementation=self._format_legal_relationship
        )

        # Court form helper
        helpers["court_form"] = TemplateHelper(
            name="court_form",
            description="Format text for court forms and legal filings",
            modifiers=["uppercase", "formal", "sworn"],
            examples=[
                "{{#court_form:sworn declaration.text}}",
                "{{#court_form:formal estate_reps.statement}}"
            ],
            implementation=self._format_court_form
        )

        # French translation helper (Quebec)
        helpers["french_legal"] = TemplateHelper(
            name="french_legal",
            description="Format legal terms for Quebec/French documents",
            modifiers=["term", "formal", "title"],
            examples=[
                "{{#french_legal:term estate_reps.role}}",
                "{{#french_legal:formal document.title}}"
            ],
            implementation=self._format_french_legal
        )

        # Estate classification helper
        helpers["estate_classification"] = TemplateHelper(
            name="estate_classification",
            description="Classify estate for legal purposes",
            modifiers=["size", "type", "complexity"],
            examples=[
                "{{#estate_classification:size estate.total_value}}",
                "{{#estate_classification:type task_planner.estate_info}}"
            ],
            implementation=self._classify_estate
        )

        # Beneficiary designation helper
        helpers["beneficiary_designation"] = TemplateHelper(
            name="beneficiary_designation",
            description="Format beneficiary designations for legal clarity",
            modifiers=["formal", "share", "relationship"],
            examples=[
                "{{#beneficiary_designation:formal children[*].name}}",
                "{{#beneficiary_designation:share spouse.inheritance}}"
            ],
            implementation=self._format_beneficiary_designation
        )

        # Provincial filing helper
        helpers["provincial_filing"] = TemplateHelper(
            name="provincial_filing",
            description="Format information for provincial court filings",
            modifiers=["ontario", "bc", "alberta", "quebec"],
            examples=[
                "{{#provincial_filing:ontario probate.application}}",
                "{{#provincial_filing:bc administration.request}}"
            ],
            implementation=self._format_provincial_filing
        )

        return helpers

    def _transform_vin_fields(self, value: Any, form_data: Dict[str, Any]) -> str:
        """Concatenate all 17 VIN character fields into a complete VIN."""
        vin_parts = [form_data.get(f"VIN.{i}", "") for i in range(17)]
        return "".join(vin_parts)

    def _format_date_day(self, value: Any, form_data: Dict[str, Any]) -> str:
        """Extracts the day from a date string."""
        if isinstance(value, str):
            try:
                dt = datetime.strptime(value, "%Y-%m-%d")
                return str(dt.day)
            except ValueError:
                return ""
        return ""

    def _format_date_month_name(self, value: Any, form_data: Dict[str, Any]) -> str:
        """Extracts the full month name from a date string."""
        if isinstance(value, str):
            try:
                dt = datetime.strptime(value, "%Y-%m-%d")
                return dt.strftime("%B")
            except ValueError:
                return ""
        return ""

    def _format_date_year(self, value: Any, form_data: Dict[str, Any]) -> str:
        """Extracts the year from a date string."""
        if isinstance(value, str):
            try:
                dt = datetime.strptime(value, "%Y-%m-%d")
                return str(dt.year)
            except ValueError:
                return ""
        return ""

    def _load_provincial_formats(self) -> Dict[ProvincialJurisdiction, Dict[str, str]]:
        """Load province-specific formatting requirements"""

        return {
            ProvincialJurisdiction.ONTARIO: {
                "court_style": "Superior Court of Justice for Ontario",
                "filing_location": "at {city}",
                "currency_format": "CAD",
                "date_format": "%B %d, %Y",
                "address_format": "full_canadian"
            },
            ProvincialJurisdiction.BRITISH_COLUMBIA: {
                "court_style": "Supreme Court of British Columbia",
                "filing_location": "{registry} Registry",
                "currency_format": "CAD",
                "date_format": "%d %B %Y",
                "address_format": "full_canadian"
            },
            ProvincialJurisdiction.QUEBEC: {
                "court_style": "Cour supérieure du Québec",
                "filing_location": "au {district}",
                "currency_format": "CAD",
                "date_format": "%d %B %Y",
                "address_format": "quebec_style",
                "language": "french"
            },
            ProvincialJurisdiction.ALBERTA: {
                "court_style": "Court of King's Bench of Alberta",
                "filing_location": "at {city}",
                "currency_format": "CAD",
                "date_format": "%B %d, %Y",
                "address_format": "full_canadian"
            }
        }

    def _format_estate_name(self, value: str, modifier: str = "formal") -> str:
        """Format names for estate documents"""

        if not value or not value.strip():
            return ""

        name = value.strip()

        if modifier == "formal":
            return self._format_formal_name(name)
        elif modifier == "first_last":
            return self._format_first_last(name)
        elif modifier == "first_middle_initial":
            return self._format_first_middle_initial(name)
        elif modifier == "last_first":
            return self._format_last_first(name)
        elif modifier == "initials":
            return self._format_initials(name)
        elif modifier == "legal":
            return self._format_legal_name(name)
        else:
            return self._format_formal_name(name)

    def _format_formal_name(self, name: str) -> str:
        """Format name formally for legal documents"""

        parts = name.split()
        if len(parts) == 0:
            return ""
        elif len(parts) == 1:
            return parts[0].title()
        else:
            formatted_parts = []
            for part in parts:
                if part.lower() in ['jr', 'sr', 'ii', 'iii', 'iv']:
                    formatted_parts.append(part.upper())
                elif part.lower() in ['von', 'van', 'de', 'la', 'du']:
                    formatted_parts.append(part.lower())
                else:
                    formatted_parts.append(part.title())

            return ' '.join(formatted_parts)

    def _format_first_last(self, name: str) -> str:
        parts = name.split()
        if len(parts) >= 2:
            return f"{parts[0].title()} {parts[-1].title()}"
        return name.title()

    def _format_last_first(self, name: str) -> str:
        parts = name.split()
        if len(parts) >= 2:
            return f"{parts[-1].title()}, {parts[0].title()}"
        return name.title()

    def _format_initials(self, name: str) -> str:
        parts = name.split()
        initials = [part[0].upper() + '.' for part in parts if part and part[0].isalpha()]
        return ' '.join(initials)

    def _format_legal_name(self, name: str) -> str:
        return self._format_formal_name(name).upper()
    
    def _format_first_middle_initial(self, name: str) -> str:
        """Formats a full name string into 'First M.' format."""
        parts = name.split()
        if not parts:
            return ""
        first_name = parts[0].title()
        # Handle cases with middle name (e.g., John Michael Smith or John Michael)
        if len(parts) > 1:
            middle_initial = parts[1][0].upper() + "."
            return f"{first_name} {middle_initial}"
        return first_name

    def _format_legal_date(self, value: str, modifier: str = "long") -> str:
        """Format dates for Canadian legal documents"""
        if not value:
            return ""
        parsed_date = self._parse_date_flexible(value)
        if not parsed_date:
            return value
        if modifier == "long":
            day, month, year = parsed_date.day, parsed_date.strftime("%B"), parsed_date.year
            return f"the {day}{self._get_ordinal_suffix(day)} day of {month}, {year}"
        elif modifier == "short":
            return parsed_date.strftime("%B %d, %Y")
        elif modifier == "ordinal":
            day = parsed_date.day
            return f"{day}{self._get_ordinal_suffix(day)} {parsed_date.strftime('%B %Y')}"
        elif modifier == "written":
            return self._write_date_in_words(parsed_date)
        else:
            return parsed_date.strftime("%B %d, %Y")

    def _get_ordinal_suffix(self, day: int) -> str:
        if 10 <= day % 100 <= 20:
            return "th"
        return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    def _write_date_in_words(self, parsed_date: date) -> str:
        # Simplified implementation
        return f"the {parsed_date.day}{self._get_ordinal_suffix(parsed_date.day)} day of {parsed_date.strftime('%B')}, {parsed_date.year}"

    def _format_canadian_currency(self, value: str, modifier: str = "formal") -> str:
        """Format Canadian currency for legal documents"""
        if not value:
            return ""
        try:
            amount = Decimal(re.sub(r'[^\d.]', '', value))
            if modifier == "formal":
                return f"${amount:,.2f} CAD"
            elif modifier == "written":
                return self._currency_to_words(amount)
            elif modifier == "short":
                return f"${amount:,.2f}"
            else:
                return f"${amount:,.2f} CAD"
        except:
            return value

    def _currency_to_words(self, amount: Decimal) -> str:
        # Simplified placeholder
        return f"{amount:,.2f} dollars"

    def _format_provincial_address(self, value: str, modifier: str = "full", jurisdiction: Optional[ProvincialJurisdiction] = None) -> str:
        if not value:
            return ""
        if modifier == "full":
            return self._format_full_canadian_address(value, jurisdiction)
        return value

    def _format_full_canadian_address(self, address: str, jurisdiction: Optional[ProvincialJurisdiction] = None) -> str:
        return address # Placeholder

    def _format_legal_relationship(self, value: str, modifier: str = "formal") -> str:
        relationship = value.strip().lower()
        formal_terms = {"executor": "estate trustee with a will", "administrator": "estate trustee without a will"}
        return formal_terms.get(relationship, relationship.replace("_", " ").title())

    def _format_court_form(self, value: str, modifier: str = "formal") -> str:
        if not value: return ""
        if modifier == "uppercase": return value.strip().upper()
        return value.strip()

    def _format_french_legal(self, value: str, modifier: str = "term") -> str:
        french_terms = {"executor": "exécuteur testamentaire", "estate": "succession"}
        return french_terms.get(value.strip().lower(), value)

    def _classify_estate(self, value: str, modifier: str = "size") -> str:
        if modifier == "size":
            try:
                estate_value = float(re.sub(r'[^\d.]', '', value))
                if estate_value < 50000: return "small estate"
                return "large estate"
            except:
                return "undetermined value"
        return "standard estate"

    def _format_beneficiary_designation(self, value: str, modifier: str = "formal") -> str:
        return f"{value.strip()}, Beneficiary"

    def _format_provincial_filing(self, value: str, modifier: str = "ontario") -> str:
        return value # Placeholder

    def _parse_date_flexible(self, date_str: str) -> Optional[date]:
        for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y%m%d", "%B %d, %Y", "%d %B %Y"]:
            try: return datetime.strptime(date_str.strip(), fmt).date()
            except ValueError: continue
        return None

    def get_helper(self, helper_name: str) -> Optional[TemplateHelper]:
        return self.helpers.get(helper_name)

    def render_template_with_helpers(self, template: str, data: Dict[str, Any], jurisdiction: Optional[ProvincialJurisdiction] = None) -> str:
        rendered = template
        for helper_name, helper in self.helpers.items():
            pattern = r'\{\{#' + re.escape(helper_name) + r'(?::(\w+))?\s+([^}]+)\}\}'
            def replace_match(match):
                modifier = match.group(1) or "formal"
                field_path = match.group(2).strip()
                value = self._get_nested_value(data, field_path)
                return helper.implementation(str(value), modifier) if value is not None else ""
            rendered = re.sub(pattern, replace_match, rendered)
        return rendered

    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Optional[Any]:
        keys = path.split('.')
        value = data
        for key in keys:
            if isinstance(value, dict): value = value.get(key)
            else: return None
        return value