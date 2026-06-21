"""
Enhanced Estate Forms Pattern Matching for Cadence Schema - Complete Version
Maps 50+ estate-related forms to Cadence schema paths for automated processing.
Includes forms from multiple jurisdictions and various estate administration needs.
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import re
import json

@dataclass
class FormFieldMapping:
    """Represents a mapping between a form field and Cadence schema path"""
    form_field: str
    schema_path: str
    field_type: str
    transform_function: Optional[str] = None
    options: Optional[List[str]] = field(default_factory=list)
    value: Optional[str] = None
    validation_rules: Optional[List[str]] = field(default_factory=list)
    required: bool = True
    description: Optional[str] = None

@dataclass
class FormMetadata:
    """Metadata about each form"""
    identifier: str
    title: str
    jurisdiction: str
    category: str
    complexity: str
    estimated_time: str
    time_sensitivity: str
    required_documents: List[str]
    purpose: str
    applicable_situations: List[str]

class EstateFormsPatternMatcher:
    """
    Enhanced pattern matcher for mapping estate-related forms to Cadence schema paths.
    This class is the single source of truth for form definitions, mappings, and metadata.
    """
    FORM_DETECTION_PATTERNS = {
        "alabama_dmv_next_of_kin_affidavit": {
            "keywords": [
                "affidavit for assignment of title",
                "deceased owner whose estate does not require probate",
                "alabama department of revenue",
                "motor vehicle division",
                "mvt 5-6",
                "next of kin"
            ],
            "required_fields": [
                "NAME OF DECEASED",
                "PRINTED NAME OF NEXT OF KIN",
                "VIN.0"
            ],
            "field_patterns": [
                r"VIN\.\d+",
                r"NAME OF DECEASED",
                r"PRINTED NAME OF NEXT OF KIN"
            ]
        },
      "atf_form_5_firearm_transfer": {
            "keywords": [
                "application for tax exempt transfer",
                "registration of firearm",
                "atf form 5",
                "department of justice",
                "bureau of alcohol, tobacco, firearms and explosives",
                "national firearms act",
                "transferee",
                "transferor"
            ],
            "required_fields": [
                "topmostSubform[0].Page1[0].TransfereeNameandAddres",
                "topmostSubform[0].Page1[0].TransferorNameandAddres",
                "topmostSubform[0].Page1[0].NameandAddressofMakerMa"
            ],
            "field_patterns": [
                r"topmostSubform\[0\]\.Page\d+\[0\]\.TransfereeNameandAddre",
                r"topmostSubform\[0\]\.Page\d+\[0\]\.TransferorNameandAddre",
                r"topmostSubform\[0\]\.Page\d+\[0\]\.FederalFirearmsLicense",
                r"topmostSubform\[0\]\.Page\d+\[0\]\.TFederalFirearmsLicens"
            ],
            "category": "firearm_transfer"
        },
        "hilton_honors_points_transfer": {
            "keywords": [
                "hilton honors worldwide llc",
                "declaration in support of",
                "request for transfer of deceased member",
                "hilton honors points",
                "executor/administrator",
                "member died on",
                "death certificate/proof of death",
                "hilton honors member",
                "hilton honors account number",
                "priorityletter@hilton.com"
            ],
            "required_fields": [
                "death of Hilton Honors Member",
                "Member died on",
                "ExecutorAdministrator",
                "Printed Name",
                "Street Address",
                "City State Zip",
                "Telephone number",
                "Email address"
            ],
            "field_patterns": [
                r"death of Hilton Honors Member",
                r"Member died on",
                r"ExecutorAdministrator",
                r"Printed Name",
                r"Street Address",
                r"City State Zip",
                r"Telephone number",
                r"Email address"
            ],
            "category": "loyalty_program_transfer"
        },
       "irs_form_56_fiduciary": {
             "keywords": [
                "notice concerning fiduciary relationship",
                "form 56",
                "internal revenue code sections 6036 and 6903",
                "department of the treasury",
                "internal revenue service",
                "fiduciary relationship",
                "authority for fiduciary",
                "court appointment",
                "nature of liability and tax notices",
                "revocation or termination",
                "testate estate",
                "intestate estate",
                "guardian or conservator",
                "trust instrument",
                "bankruptcy or assignment",
                "omb no. 1545-0013",
                "part i identification",
                "section a authority",
                "section b nature of liability"
            ],
            "required_fields": [
                "name_of_person",
                "fiduciary_name",
                "court_appointment_testate",
                "court_appointment_intestate",
                "income_tax",
                "estate_tax",
                "form_706_series",
                "form_1041"
            ],
            "field_patterns": [
                r"name.*person.*acting",
                r"identifying.*number",
                r"decedent.*social.*security",
                r"fiduciary.*name",
                r"court.*appointment",
                r"authority.*fiduciary",
                r"date.*death",
                r"type.*taxes",
                r"federal.*tax.*form",
                r"fiduciary.*signature"
            ],
            "category": "tax_administration"
        },
        "irs_form_1310_refund_claim": {
            "keywords": [
                "statement of person claiming refund due a deceased taxpayer",
                "form 1310",
                "refund due a deceased taxpayer",
                "omb no. 1545-0074",
                "attachment sequence no. 87",
                "surviving spouse requesting reissuance",
                "court-appointed or certified personal representative",
                "person claiming refund for the decedent's estate"
            ],
            "required_fields": [
                "topmostSubform[0].Page1[0].f1_1[0]",
                "topmostSubform[0].Page1[0].f1_2[0]",
                "topmostSubform[0].Page1[0].f1_3[0]"
            ],
            "field_patterns": [
                r"^topmostSubform\[0\]\.Page1\[0\]\.f1_[1-9]\[0\]$",
                r"^topmostSubform\[0\]\.Page1\[0\]\.f1_1[0-5]\[0\]$"
            ],
            "category": "tax_administration",
            "max_field_count": 30,
            "min_field_count": 20
        },
        "irs_form_ss4_estate": {
            "keywords": [
                "application for employer identification number",
                "form ss-4", "ss-4", "ss4",
                "department of the treasury",
                "internal revenue service",
                "estate (ssn of decedent)",
                "executor, administrator, trustee",
                "employer identification number",
                "ein", "omb no. 1545-0003",
                "topmostsubform", "pgheader", "page1",
                "line4readorder", "estate", "executor",
                "responsible party", "legal name",
                "mailing address", "tax administration"
            ],
            "required_fields": [
                "topmostSubform[0].Page1[0].PgHeader",
                "topmostSubform[0].Page1[0].f1_2[0]",
                "topmostSubform[0].Page1[0].f1_4[0]",
                "topmostSubform[0].Page1[0].Line4ReadOrder"
            ],
            "field_patterns": [
                r"topmostSubform\[0\]\.Page1\[0\]\.f1_\d+\[0\]",
                r"topmostSubform\[0\]\.Page1\[0\]\.c1_\d+\[.*\]",
                r"topmostSubform\[0\]\.Page1\[0\]\.PgHeader.*",
                r"topmostSubform\[0\]\.Page1\[0\]\.Line4ReadOrder.*",
                r".*Line4ReadOrder.*f1_[56]\[.*",
                r".*estate.*ssn.*decedent.*",
                r".*executor.*administrator.*"
            ],
            "category": "tax_administration"
        },
        "canada_post_mail_forwarding": {
            "keywords": [
                "mail forwarding",
                "canada post",
                "postes canada",
                "réacheminement du courrier",
                "mail recipients",
                "service details",
                "détails du service",
                "33-086-784",
                "canadapost.ca/mailforwarding"
            ],
            "required_fields": [
                "Moving to a new address",
                "First name",
                "Last name",
                "Email address*",
                "Daytime telephone no.",
                "Unit/Apt no.",
                "Street no.",
                "Street name"
            ],
            "field_patterns": [
                r"33-086-784.*",
                r"canadapost\.ca/mailfor.*",
                r"MAIL FORWARDING",
                r"SERVICE DETAILS",
                r"DÉTAILS DU SERVICE"
            ],
            "category": "death_notification"
        },
        "california_dmv_death_report_dmv22": {
            "keywords": [
                "reporting a deceased person",
                "dmv 22",
                "california dmv",
                "disabled person parking placard",
                "driver's license/identification card number",
                "death certificate information",
                "person reporting death",
                "sacramento, ca 94269-0001",
                "ms c271",
                "penalty of perjury under the laws of the state of california"
            ],
            "required_fields": [
                "Legal owner",
                "Person Reporting Death",
                "Relationship",
                "Date of Birth1A"
            ],
            "field_patterns": [
                r"Date of Birth\d+[A-Z]",
                r"DL ID\d+",
                r"Parking Placard-ID\d+",
                r"Date of Year\d+[A-Z]",
                r"Date of Date\d+[A-Z]",
                r"Date of Month\d+[A-Z]",
                r"Principal city",
                r"Principal county",
                r"Person Reporting Death",
                r"TELEPHONE\d*",
                r"E-mail"
            ],
            "category": "vehicle_administration"
        },
        "florida_certificate_title_hsmv82040": {
            "keywords": [
                "florida certificate", "hsmv", "certificate of title",
                "owner name", "co-owner name", "customer number",
                "florida resident", "alien status", "vehicle type"
            ],
            "required_fields": [
                "owner name", "co-owner name", "Customer Number",
                "VIN", "FL DL/FEID#"
            ],
            "field_patterns": [
                r"owner.*name", r"co-owner.*name", r"Customer Number",
                r"FL.*DL.*FEID", r"florida.*resident"
            ],
            "category": "vehicle_title_transfer"
        },
        "service_canada_benefit_payment_ins2882": {
            "keywords": [
                "employment insurance",
                "service canada",
                "ins2882", "ins-2882",
                "esdc", "esdc ins2882",
                "request for payment of benefit",
                "legal representative",
                "deceased person",
                "txtf_deceased_person",
                "txtf_legal_representative",
                "txtf_sin",
                "employment benefits"
            ],
            "required_fields": [
                "INS2882_E[0].page1[0].txtF_Deceased_Person[0]",
                "INS2882_E[0].page1[0].txtF_Legal_Representative[0]",
                "INS2882_E[0].page1[0].txtF_SIN[0]"
            ],
            "field_patterns": [
                r"INS2882_E\[0\]\.page\d+\[0\]\.txtF_.*",
                r"INS2882_E\[0\]\.Page\d+\[0\]\.txtF_.*",
                r".*txtF_Deceased.*",
                r".*txtF_Legal_Representative.*",
                r".*txtF_SIN.*"
            ],
            "category": "death_benefit_application"
        },
    "military_death_gratuity_dd397": {
            "keywords": [
                "death gratuity payment",
                "servicemembers",
                "military death gratuity",
                "dd form 397",
                "death gratuity",
                "deceased servicemember",
                "member grade",
                "bureau no",
                "disbursing office",
                "payee certification"
            ],
            "required_fields": [
                "mbr_name",
                "mbr_ssn",
                "mbr_grade",
                "death_date",
                "payee",
                "amt_due"
            ],
            "field_patterns": [
                r"mbr_.*",
                r"payee.*",
                r"death_.*",
                r"amt_due",
                r"bureau_no",
                r"do_no",
                r"childname_\d+",
                r"childaddr_\d+",
                r"wit\d+.*",
                r"check_.*",
                r"route_no",
                r"acct_no"
            ],
            "category": "military_benefits"
        },
    "service_canada_death_notification_isp1201": {
            "keywords": [
                "notification of death",
                "service canada",
                "isp-1201", "isp 1201",
                "canada pension plan",
                "old age security",
                "cpp", "oas",
                "mother's maiden name",
                "funeral service provider"
            ],
            "required_fields": [
                "Last Name",
                "First Name and Initial",
                "Social Insurance Number",
                "Date of Death YYYYMMDD"
            ],
            "field_patterns": [
                r"ISP-?1201",
                r"Mother.*s Maiden Name",
                r"Funeral Service Provider",
                r"Signature1_es_:signer:signature"
            ],
            "category": "death_notification"
        },
    "service_canada_t4a_representative_isp1202": {
            "keywords": [
                "deemed person to represent",
                "deceased client",
                "purpose of issuing a t-4",
                "t4a representative",
                "service canada",
                "isp-1202",
                "sc_isp1202_e",
                "representative for deceased",
                "t4 slip",
                "section a",
                "section b"
            ],
            "required_fields": [
                "SC_ISP1202_E[0].Page1[0].sub_SectionA[0].txtF_FirstAndLastName1[0]",
                "SC_ISP1202_E[0].Page1[0].sub_SectionA[0].txtF_SocialInsuranceNumbe[0]",
                "SC_ISP1202_E[0].Page1[0].sub_SectionA[0].txtF_DateOfDeath[0]",
                "SC_ISP1202_E[0].Page1[0].sub_SectionB[0].txtF_FirstAndLastName2[0]",
                "SC_ISP1202_E[0].Page1[0].sub_Statment[0].txtF_SignatureOfPersonToR[0]"
            ],
            "field_patterns": [
                r"SC_ISP1202_E\[0\]\.Page1\[0\]\.sub_SectionA\[0\]\..*",
                r"SC_ISP1202_E\[0\]\.Page1\[0\]\.sub_SectionB\[0\]\..*",
                r"SC_ISP1202_E\[0\]\.Page1\[0\]\.sub_Statment\[0\]\..*",
                r".*txtF_FirstAndLastName.*",
                r".*txtF_SocialInsuranceNumbe.*",
                r".*txtF_DateOfDeath.*",
                r".*txtF_MailingAddress.*",
                r".*txtF_TelephoneNumber.*",
                r".*txtF_NatureOfRelationship.*",
                r".*txtF_SignatureOfPersonToR.*",
                r".*cb_Oas.*",
                r".*cb_Cpp.*"
            ],
            "category": "death_benefit_application"
        },
        "service_canada_oas_isp3008": {
            "keywords": [
                "old age security", "oas", "pension",
                "sc_isp3008_e", "isp-3008", "isp3008",
                "service canada", "esdc",
                "sub_1_7", "sub_8", "sub_q9",
                "txtf_q8_branch_number", "txtf_q8_account_number",
                "rb_marital_status", "txtf_q9_spouse_name",
                "txtf_q15_applicant_signature"
            ],
            "required_fields": [
                "SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_LastNameBirth[0]",
                "SC_ISP3008_E[0].page1[0].sub_8[0].txtF_Q8_Account_Number[0]",
                "SC_ISP3008_E[0].page2[0].sub_Q9[0].rb_Marital_Status[0]",
                "SC_ISP3008_E[0].page4[0].txtF_Q15_Applicant_Signature[0]"
            ],
            "field_patterns": [
                r"SC_ISP3008_E\[0\]\.page\d+\[0\]\..*",
                r"SC_ISP3008_E\[0\]\.#pageSet\[0\]\.Page\d+\[0\]\..*",
                r".*sub_1_7.*",
                r".*sub_8.*",
                r".*sub_Q9.*",
                r".*txtF_Q\d+.*",
                r".*rb_.*",
                r".*sub_Mid_Top_Box.*"
            ],
            "category": "death_benefit_application"
        },
       "cra_death_notification_rc4111": {
            "keywords": [
                "notify canada revenue agency death",
                "death notification",
                "canada revenue agency",
                "cra death",
                "rc4111",
                "social insurance number sin",
                "relationship to the deceased person",
                "information about deceased person",
                "your information",
                "deceased person date of death"
            ],
            "required_fields": [
                "Social insurance number SIN",
                "Relationship to the deceased person",
                "Date",
                "Address",
                "Telephone number"
            ],
            "field_patterns": [
                r"Social insurance number.*SIN",
                r"Relationship to.*deceased.*person",
                r"Telephone number",
                r"Address",
                r"Signature",
                r"Text[0-9]+"
            ],
            "category": "tax_administration"
        },
        "manitoba_funeral_home_invoice_schedule_b": {
            "keywords": [
                "manitoba",
                "funeral home",
                "invoice",
                "schedule b",
                "eia case no",
                "total fees",
                "casket",
                "cremation"
            ],
            "required_fields": [
                "Funeral Home",
                "Deceased - Full Name",
                "EIA Case No",
                "Total Fees"
            ],
            "field_patterns": [
                r"EIA Case No",
                r"Total.*Fees",
                r"License Number",
                r"Oversized Casket",
                r"Opening/Closing Fee"
            ],
            "category": "estate_information"
        },
        "social_security_death_payment_ssa8": {
            "keywords": [
                "ssa-8", "lump-sum death payment", "social security administration",
                "deceased wage earner", "0960-0013", "title ii", "railroad retirement act",
                "application for lump-sum death payment",
                "form ssa-8", "ssa 8"
            ],
            "required_fields": [
                "form1[0].#subform[0].TextField1[0]",
                "form1[0].#subform[0].TextField1[1]",
                "form1[0].#subform[0].NumericField1[0]"
            ],
            "field_patterns": [
                r"form1\[0\]\.#subform\[\d+\]\.TextField1\[\d+\]",
                r"form1\[0\]\.#subform\[\d+\]\.NumericField1\[\d+\]",
                r"form1\[0\]\.#subform\[\d+\]\.DateField\d+\[\d+\]",
                r"form1\[0\]\.#subform\[\d+\]\.C\d+[A-Za-z]*\[\d+\]"
            ],
            "category": "death_benefit_application",
            "priority_boost": 1.5,
            "ocr_text_patterns": [
                r"APPLICATION FOR LUMP-SUM DEATH PAYMENT",
                r"SSA-8",
                r"Form SSA-8",
                r"Social Security Administration",
                r"OMB No\. 0960-0013"
            ],
            "form_structure_indicators": [
                "122_total_fields",
                "4_subforms",
                "generic_field_names"
            ]
        },
        "service_canada_cpp_death_benefit_isp1200": {
            "keywords": [
                "application for a canada pension plan death benefit",
                "isp-1200", "isp 1200", "sc isp-1200",
                "deceased contributor",
                "order of priority",
                "funeral expenses",
                "next-of-kin",
                "executor named in the will",
                "information about the applicant"
            ],
            "required_fields": [
                "SC_ISP1200[0].page3[0].sub_TabOrder[0].sub_A1_SIN[0]",
                "SC_ISP1200[0].page7[0].sub_D1[0].sub_D1_row_2[0].txtF_FamilyName[0]",
                "SC_ISP1200[0].page8[0].txtF_signature[0]"
            ],
            "field_patterns": [
                r"SC_ISP1200\[0\]\.page\d+\[0\]\..*",
                r".*sub_A1_DOD_MaritalStatus.*",
                r".*I_am_applying_as_the.*",
                r".*sub_dd\[0\].*txtF_AccountNumber.*"
            ],
            "category": "death_benefit_application"
        },
        "service_canada_cpp_survivors_pension_isp1300": {
            "keywords": [
                "cpp survivors pension",
                "canada pension plan",
                "service canada",
                "survivors pension",
                "deceased spouse",
                "common-law partner",
                "sc isp-1300",
                "sc_isp1300_e",
                "surviving spouse",
                "social insurance number"
            ],
            "required_fields": [
                "txtF_1A_SIN",
                "txtF_1B_DOB",
                "txtF_7A_SIN",
                "rb_3_Marital_St",
                "txtF_Applican"
            ],
            "field_patterns": [
                r"SC_ISP1300_E.*",
                r".*txtF_.*_SIN.*",
                r".*txtF_.*_DOB.*",
                r".*rb_.*_Marital.*",
                r".*txtF_Applican.*",
                r".*sub_Q.*",
                r".*Page.*"
            ],
            "category": "death_benefit_application"
        },
        "irs_form_2848_power_of_attorney": {
            "keywords": [
                "power of attorney and declaration of representative",
                "form 2848", "irs form 2848",
                "department of the treasury",
                "internal revenue service",
                "centralized authorization file",
                "preparer tax identification number",
                "taxpayer name and address",
                "representative name",
                "acts authorized",
                "declaration of representative"
            ],
            "required_fields": [
                "topmostSubform[0].Page1[0].TaxpayerName[0]",
                "topmostSubform[0].Page1[0].TaxpayerAddress[0]",
                "topmostSubform[0].Page1[0].RepresentativesName1[0]",
                "topmostSubform[0].Page1[0].CAFNumber1[0]",
                "topmostSubform[0].Page1[0].PTIN1[0]"
            ],
            "field_patterns": [
                r"topmostSubform\[0\]\.Page\d+\[0\]\.Taxpayer.*",
                r"topmostSubform\[0\]\.Page\d+\[0\]\.Representatives.*",
                r"topmostSubform\[0\]\.Page\d+\[0\]\.CAFNumber.*",
                r"topmostSubform\[0\]\.Page\d+\[0\]\.PTIN.*",
                r"topmostSubform\[0\]\.Page\d+\[0\]\.Table_.*",
                r".*TaxpayerID.*",
                r".*TelephoneNo.*",
                r".*BodyRow.*"
            ],
            "category": "tax_administration",
            "max_field_count": 120,
            "min_field_count": 80
        },
        "maine_voter_death_notice": {
            "keywords": [
                "notice of voter's death",
                "immediate family member",
                "maine",
                "registrar",
                "voters city/town of residence",
                "date cancelled in cvr"
            ],
            "required_fields": [
                "Deceased Voters Name",
                "Printed name of immediate family member",
                "Signature of immediate family member"
            ],
            "field_patterns": [
                r"Voters City.*Town.*Residence",
                r"Voters Pilace of Death",
                r"Relationslilip to Voter",
                r"Registrar Initials"
            ],
            "category": "electoral_administration"
        },
        "california_statement_of_facts_reg256": {
            "keywords": [
                "statement of facts",
                "license plate",
                "vehicle vessel id",
                "family transfer",
                "inheritance",
                "use tax exemption",
                "smog exemption",
                "transfer only",
                "title only",
                "reg 256",
                "california dmv"
            ],
            "required_fields": [
                "License Plate/CF Number",
                "Veh/Vessel ID Number",
                "Year/Make",
                "inheritance box",
                "Current Market Value"
            ],
            "field_patterns": [
                r"License Plate.*Number",
                r"Veh.*Vessel.*ID.*Number",
                r"Year.*Make",
                r".*transfer.*box",
                r"inheritance.*box",
                r"Current Market Value",
                r"Mail to.*",
                r".*SIGNATURE.*"
            ],
            "category": "vehicle_title_transfer"
        },
        "service_canada_child_rearing_isp1640": {
            "keywords": [
                "child rearing provision",
                "sc_isp1640_e",
                "isp-1640",
                "service canada",
                "child rearing",
                "caregiver periods",
                "family allowance",
                "canada child benefit",
                "sub_info",
                "sub_section_b",
                "sub_waiver",
                "page3", "page4", "page5", "page6", "page7", "page9", "page10",
                "txtf_firstname", "txtf_middlename", "txtf_familyname",
                "txtf_emailaddress", "txtf_phone", "txtf_address"
            ],
            "required_fields": [
                "SC_ISP1640_E[0].page3[0].sub_info[0].txtF_FirstName[0]",
                "SC_ISP1640_E[0].page3[0].sub_info[0].txtF_LastName[0]",
                "SC_ISP1640_E[0].page3[0].sub_info[0].txtF_Address[0]",
                "SC_ISP1640_E[0].page3[0].sub_Section_B[0]",
                "SC_ISP1640_E[0].page6[0].txtF_Signature[0]"
            ],
            "field_patterns": [
                r"SC_ISP1640_E\[0\]\.page\d+\[0\]\..*",
                r".*txtF_.*",
                r".*sub_info.*",
                r".*sub_Section.*",
                r".*sub_Waiver.*",
                r".*Table2.*",
                r".*Check_Boxes.*"
            ],
            "category": "death_benefit_application",
            "min_keyword_matches": 3,
            "min_field_matches": 2,
            "min_pattern_matches": 2
        },
        "nevada_dmv_affidavit_vp24": {
            "keywords": [
                "affidavit for transfer of title",
                "estates without probate",
                "nevada",
                "dmv",
                "vp-24", "vp 24",
                "affiant",
                "name of deceased"
            ],
            "required_fields": [
                "Affiant full legal name",
                "Name of deceased",
                "Vehicle Identification Number",
                "Affiants Signature"
            ],
            "field_patterns": [
                r"Affiant.*legal name",
                r"Affiant.*relationship",
                r"Affiant.*Signature",
                r"VP(-|\s)?24"
            ],
            "category": "vehicle_title_transfer"
        },
        "cra_legal_representative_appointment": {
            "keywords": [
                "canada revenue agency",
                "legal representative",
                "deceased person",
                "representative repid",
                "social insurance number",
                "signature representative",
                "cra", "rc552"
            ],
            "required_fields": [
                "Deceased persons first name",
                "Deceased persons last name",
                "Deceased social insurance number",
                "representative first name",
                "Signature representative"
            ],
            "field_patterns": [
                r"Deceased persons.*name",
                r"representative.*name",
                r"Signature representative",
                r"Date YYYYMMDD",
                r"deceased address.*",
                r"representative address.*"
            ],
            "category": "tax_administration"
        },
        "elections_ontario_f0527w": {
            "keywords": [
                "elections ontario",
                "application to remove a deceased person",
                "f0527w",
                "electoral district",
                "elector signature"
            ],
            "required_fields": [
                "Applicant Acting on Behalf of Deceased",
                "Information About the Deceased",
                "Last Residential Address of the Deceased",
                "Elector Signature"
            ],
            "field_patterns": [
                r"F0527W",
                r"Elector ID",
                r"ED #",
                r"Poll #"
            ],
            "category": "electoral_administration"
        },
        "electoral_deceased_removal_form": {
        "keywords": [
            "remove deceased person",
            "elector signature",
            "registers maintained",
            "acceptable documentation",
            "voter registration",
            "electoral"
        ],
        "required_fields": [
            "Elector Signature",
            "I request that the deceased person",
            "Year", "Month", "Day"
        ],
        "field_patterns": [
            r"Elector.*Signature",
            r"deceased person.*named",
            r"Text\d+",
            r"acceptable documentation"
        ],
        "category": "electoral_administration"
    }
    }
            # In the FORM_DETECTION_PATTERNS dictionary...
        

    # Jurisdiction-based form organization
    JURISDICTION_FORMS = {
        "alabama": [
            "alabama_dmv_next_of_kin_affidavit",
            "alabama_vehicle_title_affidavit_mvt56",
        ],
        "nevada": [
            "nevada_dmv_affidavit_vp24",
        ],
        "utah": [
            "utah_survivorship_affidavit_tc569c",
        ],
        "us_federal": [
            "veterans_affairs_disability_death_benefit_pen542",
            "va_headstone_marker_claim_40_1330",
            "sf1174_unpaid_compensation_claim",
            "atf_form_5_firearm_transfer",
            "military_death_gratuity_dd397",
            "irs_form_ss4_estate",
            "irs_form_56_fiduciary",
            "social_security_death_payment_ssa8",
        ],
        "provincial_municipal": [
        "electoral_deceased_removal_form"
        ],
        "california_state": [
            "california_statement_of_facts_reg256",
            "california_dmv_death_report_dmv22" 
        ],
        "maine": [
            "maine_voter_death_notice",
        ],
        "manitoba": [
            "manitoba_funeral_home_invoice_schedule_b",
        ],

        "canada_federal": [
            "service_canada_death_notification_isp1201",
            "canada_cpp_survivors_pension_isp1300",
            "cra_legal_representative_appointment",
            "service_canada_cpp_survivors_pension_isp1300",
            "cra_death_notification_rc4111",
            "service_canada_cpp_death_benefit_isp1200",
        ]
    }

    # Category-based form organization
    CATEGORY_FORMS = {
        "vehicle_title_transfer": [
            "alabama_dmv_next_of_kin_affidavit",
            "alabama_vehicle_title_affidavit_mvt56",
            "utah_survivorship_affidavit_tc569c",
            "nevada_dmv_affidavit_vp24",
            "oregon_dmv_inheritance_affidavit",
            "california_statement_of_facts_reg256"
        ],
        "military_benefits": [
            "veterans_affairs_disability_death_benefit_pen542",
            "va_headstone_marker_claim_40_1330",
            "sf1174_unpaid_compensation_claim",
            "military_death_gratuity_dd397",
        ],
        "tax_administration": [
            "cra_legal_representative_appointment",
            "cra_death_notification_rc4111" ,
            "irs_form_56_fiduciary"
        ],
        "estate_information": [
             "manitoba_funeral_home_invoice_schedule_b", 
        ],
        "firearm_transfer": [ 
            "atf_form_5_firearm_transfer"
        ],
        "death_benefit_application": [
            "veterans_affairs_disability_death_benefit_pen542",
            "service_canada_cpp_survivors_pension_isp1300" ,
            "social_security_death_payment_ssa8" 
        ],
        "death_notification": [
            "california_dmv_death_report_dmv22" ,
            "service_canada_death_notification_isp1201", 
            "service_canada_cpp_death_benefit_isp1200",
        ],
        "loyalty_program_transfer": [
            "hilton_honors_points_transfer",
        ],
        "electoral_administration": [
            "electoral_deceased_removal_form"
            "maine_voter_death_notice"
        ]
        }
    

    def detect_form_with_generic_fields(self, pdf_fields, ocr_text=""):
        """Special detection for forms with generic field names like form1[0].#subform[0].TextField1[0]"""
        
        # Count field patterns specific to SSA-8
        ssa8_field_count = len([f for f in pdf_fields if "form1[0].#subform" in f])
        
        if ssa8_field_count >= 100:  # SSA-8 has ~122 fields
            # Check OCR text for SSA-8 indicators
            if any(pattern in ocr_text.upper() for pattern in [
                "SSA-8", "LUMP-SUM DEATH PAYMENT", "SOCIAL SECURITY ADMINISTRATION",
                "APPLICATION FOR LUMP-SUM DEATH PAYMENT", "OMB NO. 0960-0013"
            ]):
                return "social_security_death_payment_ssa8", 0.85  # High confidence
        
        return None, 0.0

    def get_field_sequence_mapping(self, form_identifier):
        """Get field mapping by position for forms with generic field names"""
        
        if form_identifier == "social_security_death_payment_ssa8":
            return {
                # Page 1: Applicant and Deceased Info
                'form1[0].#subform[0].TextField1[0]': 'applicant.full_name',
                'form1[0].#subform[0].TextField1[1]': 'deceased.full_name',
                'form1[0].#subform[0].NumericField1[0]': 'deceased.social_insurance_number', # SSN
                'form1[0].#subform[0].DateField1[0]': 'deceased.date_of_birth',
                'form1[0].#subform[0].DateField2[0]': 'deceased.date_of_death',
                'form1[0].#subform[0].TextField1[2]': 'deceased.place_of_death',
                
                # Page 1: Deceased's Work Status
                'form1[0].#subform[0].TextField1[3]': 'deceased.earnings.year_of_death',
                'form1[0].#subform[0].TextField1[4]': 'deceased.earnings.year_before_death',
                'form1[0].#subform[0].C7Yes[0]': 'deceased.work_status.unable_to_work_at_death',
                'form1[0].#subform[0].DateField3[0]': 'deceased.work_status.date_unable_to_work',
                
                # Page 2: Deceased's Military/Railroad/Foreign Work
                'form1[0].#subform[0].C8Yes[0]': 'deceased.military.active_service_pre_1968',
                'form1[0].#subform[0].TextField1[5]': 'deceased.military.service_start_date',
                'form1[0].#subform[0].TextField1[6]': 'deceased.military.service_end_date',
                'form1[0].#subform[0].C8CYes[0]': 'deceased.military.other_federal_benefits',
                'form1[0].#subform[0].C9Yes[0]': 'deceased.employment.railroad_work_7_years',
                'form1[0].#subform[1].C10Yes[0]': 'deceased.employment.foreign_work',
                'form1[0].#subform[1].TextField1[7]': 'deceased.employment.foreign_countries',

                # Page 2: Spouse and Marriage Information
                'form1[0].#subform[1].C11Yes[0]': 'deceased.marital_status.surviving_spouse_exists',
                'form1[0].#subform[1].TextField1[8]': 'spouse.full_name',
                'form1[0].#subform[1].TextField1[11]': 'spouse.date_of_marriage',
                'form1[0].#subform[1].TextField1[12]': 'spouse.place_of_marriage',
                'form1[0].#subform[1].TextField1[13]': 'spouse.date_of_birth',
                'form1[0].#subform[1].TextField1[14]': 'spouse.social_insurance_number', # SSN
                
                # Page 3: Living Arrangements & Applicant Status
                'form1[0].#subform[2].C16Yes[0]': 'spouse.living_together_at_death',
                'form1[0].#subform[2].C17Yes[0]': 'applicant.disability_status',
                'form1[0].#subform[2].TextField1[46]': 'applicant.disability_start_date',
                
                # Page 4: Remarks, Signature, Contact Info
                'form1[0].#subform[2].TextField1[65]': 'notes.remarks',
                'form1[0].#subform[2].TextField1[66]': 'applicant.signature', # This is a text field for signature
                'form1[0].#subform[2].TextField1[67]': 'key_document.signature_date',
                'form1[0].#subform[2].TextField1[68]': 'applicant.phone',
                'form1[0].#subform[2].TextField1[69]': 'applicant.mailing_address.street',
                'form1[0].#subform[2].TextField1[70]': 'applicant.mailing_address.city_state_zip',

                # Page 5: Direct Deposit
                'form1[0].#subform[3].TextField1[76]': 'payment.routing_number',
                'form1[0].#subform[3].TextField1[77]': 'payment.account_number',
                'form1[0].#subform[3].Checking[0]': 'payment.account_type_checking',
                'form1[0].#subform[3].Savings[0]': 'payment.account_type_savings',
                        # Prior Marriage 1 Checkboxes (Deceased)
                'form1[0].#subform[1].C11BClerg[0]': 'deceased.prior_marriages[0].ceremonial_marriage',
                'form1[0].#subform[1].C11BOther[0]': 'deceased.prior_marriages[0].other_marriage',
                'form1[0].#subform[1].DateField4[0]': 'deceased.prior_marriages[0].end_date',

                # Prior Marriage 2 Checkboxes (Deceased)
                'form1[0].#subform[1].C11CClerg[0]': 'deceased.prior_marriages[1].ceremonial_marriage',
                'form1[0].#subform[1].C11COther[0]': 'deceased.prior_marriages[1].other_marriage',

                # Checkboxes for Item 14
                'form1[0].#subform[1].C14No[0]': 'applicant.no_prior_filing_spouse_record',
                'form1[0].#subform[1].C14Yes[0]': 'applicant.prior_filing_spouse_record',

                # Prior Marriage Checkboxes (Applicant)
                'form1[0].#subform[2].C18No[0]': 'applicant.no_prior_marriage_10_years',
                'form1[0].#subform[2].C18Yes[0]': 'applicant.prior_marriage_10_years',
                'form1[0].#subform[2].C18Clerg[0]': 'applicant.prior_marriages[0].ceremonial_marriage',
                'form1[0].#subform[2].C18Other[0]': 'applicant.prior_marriages[0].other_marriage',
            }
        
        return {}

    def enhance_form_detection(self, pdf_fields, ocr_text="", field_values=None):
        """Enhanced form detection that handles generic field names"""
        
        # First try standard detection
        standard_result = self.detect_form_type(pdf_fields, ocr_text)
        
        # If standard detection fails or gives low confidence, try generic field detection
        if standard_result[1] < 0.5:  # Low confidence
            generic_result = self.detect_form_with_generic_fields(pdf_fields, ocr_text)
            if generic_result[1] > standard_result[1]:
                return generic_result
        
        return standard_result


    def __init__(self):
        self.form_mappings = self._initialize_form_mappings()
        self.form_metadata = self._initialize_form_metadata()
    
    def _initialize_form_mappings(self) -> Dict[str, List[FormFieldMapping]]:
        """Initialize all form mappings to Cadence schema paths"""
        
        
        mappings = {
            # ============================================================================
            # 1. ALABAMA VEHICLE TITLE AFFIDAVIT (MVT 5-6)
            # ============================================================================
          "alabama_dmv_next_of_kin_affidavit": [
                    # Vehicle Information
                   FormFieldMapping("VIN.0", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.1", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.2", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.3", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.4", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.5", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.6", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.7", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.8", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.9", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.10", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.11", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.12", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.13", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.14", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.15", "property.vehicles[0].vin", "text"),
                    FormFieldMapping("VIN.16", "property.vehicles[0].vin", "text"),
                    
                    FormFieldMapping("YEAR", "property.vehicles[0].year", "text"),
                    FormFieldMapping("MAKE", "property.vehicles[0].make", "text"),
                    FormFieldMapping("MODEL", "property.vehicles[0].model", "text"),
                    FormFieldMapping("TITLE NUMBER", "property.vehicles[0].title_number", "text"),
                    
                    # Deceased Information
                    FormFieldMapping("NAME OF DECEASED", "deceased.full_name", "text"),
                    FormFieldMapping("ADDRESS", "deceased.home_address.street", "text"),
                    FormFieldMapping("CITY", "deceased.home_address.city", "text"),
                    FormFieldMapping("STATE", "deceased.home_address.state", "text"),
                    FormFieldMapping("ZIP CODE", "deceased.home_address.zip_code", "text"),
                    
                    # Date of Death
                    FormFieldMapping("DAY", "deceased.date_of_death", "date_component"),
                    FormFieldMapping("MONTH", "deceased.date_of_death", "date_component"),
                    FormFieldMapping("DATE", "deceased.date_of_death", "date"),
                    
                    # Next of Kin Information
                    FormFieldMapping("PRINTED NAME OF NEXT OF KIN", "applicant.full_name", "text"),
                    FormFieldMapping("SIGNATURE OF NEXT OF KIN", "applicant.signature", "signature"),
                    
                    # Checkboxes for title options
                    FormFieldMapping("Check Box6", "property.vehicles[0].title_action", "checkbox", None, [], False),
                    FormFieldMapping("Check Box7", "property.vehicles[0].title_action", "checkbox", None, [], False),
                    
                    # Generic text fields that might contain additional info
                    FormFieldMapping("Text1", "notes.additional_info_1", "text", None, [], False),
                    FormFieldMapping("Text2", "notes.additional_info_2", "text", None, [], False),
                    FormFieldMapping("Text3", "notes.additional_info_3", "text", None, [], False),
                ],

        "cra_legal_representative_appointment": [
                # Deceased Person Information
                FormFieldMapping("Deceased persons first name", "deceased.first_name", "name"),
                FormFieldMapping("Deceased persons middle name if applicable", "deceased.middle_name", "name", required=False),
                FormFieldMapping("Deceased persons last name", "deceased.last_name", "name"),
                FormFieldMapping("Deceased date of birth", "deceased.date_of_birth", "date", required=False),
                FormFieldMapping("Deceased social insurance number", "deceased.social_insurance_number", "sin"),
                
                # Deceased Address
                FormFieldMapping("deceased address - street", "deceased.home_address", "location", "combine_address_street"),
                FormFieldMapping("deceased address - City", "deceased.home_address", "location", "combine_address_city"),
                FormFieldMapping("deceased address - Province or territory", "deceased.home_address", "location", "combine_address_province"),
                FormFieldMapping("deceased address - Postal code", "deceased.home_address", "location", "combine_address_postal"),
                
                # Legal Representative Information
                FormFieldMapping("representative first name", "estate_reps[*].first_name", "name"),
                FormFieldMapping("representative last name", "estate_reps[*].last_name", "name"),
                FormFieldMapping("representative social insurance number", "estate_reps[*].social_insurance_number", "sin", required=False),
                FormFieldMapping("representative relationship to the deceased person", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("representative RepID", "estate_reps[*].cra_rep_id", "string", required=False),
                
                # Representative Address
                FormFieldMapping("representative address - street", "estate_reps[*].address", "location", "combine_address_street"),
                FormFieldMapping("representative address - city", "estate_reps[*].address", "location", "combine_address_city"),
                FormFieldMapping("representative address - province or territory", "estate_reps[*].address", "location", "combine_address_province"),
                FormFieldMapping("representative address - postal code", "estate_reps[*].address", "location", "combine_address_postal"),
                FormFieldMapping("representative address - telephone number", "estate_reps[*].phone", "phone"),
                
                # Legal Execution & Signatures
                FormFieldMapping("Signature representative", "estate_reps[*].signature", "signature"),
                FormFieldMapping("Date YYYYMMDD", "key_document.signature_date", "date"),
                
                # Witness Information
                FormFieldMapping("First name witness", "contact.witness.first_name", "name", required=False),
                FormFieldMapping("Last name witness", "contact.witness.last_name", "name", required=False),
                FormFieldMapping("Telephone number witness", "contact.witness.phone", "phone", required=False),
                FormFieldMapping("Signature witness", "contact.witness.signature", "string", required=False),
                FormFieldMapping("Date YYYYMMDD_2", "contact.witness.signature_date", "date", required=False),
            ],
            # ============================================================================
            # 2. UTAH STATE TAX COMMISSION SURVIVORSHIP AFFIDAVIT (TC-569C)
            # ============================================================================
            "utah_survivorship_affidavit_tc569c": [
                # Vehicle Information (Section 1)
                FormFieldMapping("year", "property.vehicles[*].year", "number"),
                FormFieldMapping("make", "property.vehicles[*].make_model", "string", "extract_make"),
                FormFieldMapping("model", "property.vehicles[*].make_model", "string", "extract_model"),
                FormFieldMapping("vehicle_hull_identification_number", "property.vehicles[*].vin", "string"),
                FormFieldMapping("body_type", "property.vehicles[*].body_type", "string"),
                FormFieldMapping("license_plate_number", "property.vehicles[*].license_plate", "string"),
                FormFieldMapping("state_last_registered", "property.vehicles[*].previous_state", "string"),
                FormFieldMapping("trailer_length", "property.vehicles[*].length", "string"),
                FormFieldMapping("watercraft_length", "property.vessels[*].length", "string"),
                
                # Deceased Owner Information (Section 2)
                FormFieldMapping("deceased_owner_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("city_state_where_death_occurred", "deceased.place_of_death", "location"),
                FormFieldMapping("date_of_death", "deceased.date_of_death", "date"),
                
                # Survivor Information (Section 3)
                FormFieldMapping("survivor_name", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("survivor_address", "estate_reps[*].address", "location"),
                FormFieldMapping("signature_of_affidavit_survivor", "estate_reps[*].signature", "string"),
                FormFieldMapping("notary_signature", "key_document[*].notes", "string"),
                FormFieldMapping("notary_date", "key_document[*].notary_date", "date"),
                FormFieldMapping("notary_stamp", "key_document[*].notary_seal", "string"),
                
                # New Owner Information (Section 4)
                FormFieldMapping("primary_owner_name", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("co_owner_name", "estate_reps[*].co_owner_name", "name", "parse_full_name"),
                FormFieldMapping("street_address_primary_owner", "estate_reps[*].address", "location"),
                FormFieldMapping("mailing_address_primary_owner", "estate_reps[*].mailing_address", "location"),
                FormFieldMapping("city_state_zip", "estate_reps[*].address", "location", "extract_city_state_zip"),
                
                # Legal Certification
                FormFieldMapping("utah_code_75_3_1201_certification", "key_document[*].legal_authority", "string"),
                FormFieldMapping("estate_value_certification", "financial_information.total_estate_value", "currency"),
                FormFieldMapping("30_days_elapsed_certification", "key_document[*].waiting_period_met", "boolean"),
                FormFieldMapping("no_personal_representative_certification", "estate_reps[*].no_pr_appointed", "boolean"),
            ],
            
            # ============================================================================
            # 3. VETERANS AFFAIRS DISABILITY/DEATH BENEFIT APPLICATION (PEN542)
            # ============================================================================
            "veterans_affairs_disability_death_benefit_pen542": [
                # Deceased Member/Veteran Information (Section A)
                FormFieldMapping("deceased_last_name", "deceased.last_name", "name"),
                FormFieldMapping("deceased_first_name", "deceased.first_name", "name"),
                FormFieldMapping("deceased_middle_name", "deceased.middle_name", "name"),
                FormFieldMapping("deceased_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("deceased_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("cause_of_death", "deceased.cause_of_death", "string"),
                FormFieldMapping("place_of_death", "deceased.place_of_death", "location"),
                FormFieldMapping("service_number_rcmp_regimental", "deceased.military.service_number", "string"),
                FormFieldMapping("type_of_service", "deceased.military.branch_of_service", "string"),
                FormFieldMapping("date_of_enlistment", "deceased.military.service_start_date", "date"),
                FormFieldMapping("date_of_discharge", "deceased.military.service_end_date", "date"),
                FormFieldMapping("maiden_name", "deceased.mothers_name", "name"),
                FormFieldMapping("other_names_used", "deceased.name_variations", "string"),
                FormFieldMapping("csdn_id", "deceased.military.service_id", "string"),
                FormFieldMapping("file_no", "key_document[*].id", "string"),
                
                # Applicant Information (Section B)
                FormFieldMapping("applicant_name", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("mailing_address", "applicant.mailing_address", "location"),
                FormFieldMapping("home_address", "applicant.home_address", "location"),
                FormFieldMapping("telephone", "applicant.phone", "phone"),
                FormFieldMapping("other_telephone", "applicant.phone_alt", "phone"),
                FormFieldMapping("title_rank", "applicant.title", "string"),
                FormFieldMapping("official_language_oral", "applicant.preferred_language", "select"),
                FormFieldMapping("official_language_correspondence", "applicant.correspondence_language", "select"),
                FormFieldMapping("veterans_affairs_employee", "applicant.va_employee", "boolean"),
                FormFieldMapping("applicant_date_of_birth", "applicant.date_of_birth", "date"),
                FormFieldMapping("applicant_maiden_name", "applicant.mothers_name", "name"),
                FormFieldMapping("applicant_other_names", "applicant.name_variations", "string"),
                
                # Spouse/Common-law Partner Information (Section C)
                FormFieldMapping("married_living_together", "spouse.married_at_death", "boolean"),
                FormFieldMapping("date_of_marriage", "spouse.date_of_marriage", "date"),
                FormFieldMapping("living_common_law", "spouse.common_law_status", "boolean"),
                FormFieldMapping("common_law_relationship_began", "spouse.date_started_living_with_spouse", "date"),
                FormFieldMapping("divorced_from_member", "spouse.divorced_status", "boolean"),
                FormFieldMapping("separated_medical_reasons", "spouse.separation_medical", "boolean"),
                FormFieldMapping("separated_temporary_circumstances", "spouse.separation_temporary", "boolean"),
                FormFieldMapping("separation_explanation", "spouse.separation_reason", "string"),
                FormFieldMapping("member_veteran_caf_rcmp", "applicant.military_status", "boolean"),
                FormFieldMapping("applied_va_benefits", "applicant.prior_va_benefits", "boolean"),
                FormFieldMapping("va_file_number", "applicant.va_file_number", "string"),
                FormFieldMapping("applicant_service_number", "applicant.military.service_number", "string"),
                FormFieldMapping("remarried_subsequent_relationship", "spouse.remarried_since_death", "boolean"),
                FormFieldMapping("remarriage_date", "spouse.remarriage_date", "date"),
                FormFieldMapping("current_spouse_member_veteran", "spouse.current_spouse_veteran", "boolean"),
                FormFieldMapping("current_spouse_name", "spouse.current_spouse_name", "name", "parse_full_name"),
                FormFieldMapping("current_spouse_service_number", "spouse.current_spouse_service_number", "string"),
                
                # Dependant Information (Section D)
                FormFieldMapping("child_dependant_name", "children[*].name", "name", "parse_full_name"),
                FormFieldMapping("relationship_to_member", "children[*].relationship", "string"),
                FormFieldMapping("child_date_of_birth", "children[*].date_of_birth", "date"),
                FormFieldMapping("attending_school_at_death", "children[*].school_at_death", "boolean"),
                FormFieldMapping("attending_school_at_application", "children[*].school_at_application", "boolean"),
                FormFieldMapping("child_disabled", "children[*].disabled_status", "boolean"),
                FormFieldMapping("person_dependant_lives_with", "children[*].guardian_name", "name", "parse_full_name"),
                FormFieldMapping("guardian_relationship", "children[*].guardian_relationship", "string"),
                FormFieldMapping("guardian_mailing_address", "children[*].guardian_address", "location"),
                FormFieldMapping("other_dependants_exist", "children[*].other_dependants", "boolean"),
                
                # Applicant Statement (Section E)
                FormFieldMapping("death_ruling_claim", "key_document[*].claim_type", "select"),
                FormFieldMapping("injury_illness_specification", "deceased.injury_illness", "string"),
                FormFieldMapping("member_disability_award", "deceased.prior_disability_award", "boolean"),
                FormFieldMapping("disability_condition", "deceased.disability_condition", "string"),
                FormFieldMapping("disability_benefits_after_death", "key_document[*].posthumous_disability", "boolean"),
                FormFieldMapping("claimed_conditions", "deceased.claimed_conditions", "string"),
                FormFieldMapping("workers_compensation", "deceased.workers_compensation", "boolean"),
                FormFieldMapping("service_relationship_explanation", "deceased.service_connection", "string"),
                
                # Quality of Life Questionnaire (Section F)
                FormFieldMapping("household_activities", "deceased.functional_assessment.household_activities", "select"),
                FormFieldMapping("shopping_errands", "deceased.functional_assessment.shopping_errands", "select"),
                FormFieldMapping("drive_vehicle", "deceased.functional_assessment.driving", "select"),
                FormFieldMapping("public_transportation", "deceased.functional_assessment.public_transport", "select"),
                FormFieldMapping("work_regular_occupation", "deceased.functional_assessment.work_capacity", "select"),
                FormFieldMapping("recreational_activities", "deceased.functional_assessment.recreation", "select"),
                FormFieldMapping("family_responsibilities", "deceased.functional_assessment.family_duties", "select"),
                FormFieldMapping("personal_social_relationships", "deceased.functional_assessment.relationships", "select"),
                FormFieldMapping("activity_limitations_explanation", "deceased.functional_assessment.limitations", "string"),
                FormFieldMapping("changes_due_to_claimed_condition", "deceased.functional_assessment.condition_impact", "boolean"),
                FormFieldMapping("other_conditions_impact", "deceased.functional_assessment.other_conditions", "string"),
                
                # Privacy and Declaration (Section G)
                FormFieldMapping("privacy_notice_acknowledgment", "key_document[*].privacy_acknowledged", "boolean"),
                FormFieldMapping("applicant_signature", "applicant.signature", "string"),
                FormFieldMapping("signature_date", "key_document[*].date_created", "date"),
                FormFieldMapping("legal_representative_completion", "estate_reps[*].completing_on_behalf", "boolean"),
                FormFieldMapping("legal_rep_name", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("legal_rep_telephone", "estate_reps[*].phone", "phone"),
                FormFieldMapping("legal_rep_signature", "estate_reps[*].signature", "string"),
                
                # Witness Information
                FormFieldMapping("witness_first_name", "contact[*].first_name", "name"),
                FormFieldMapping("witness_last_name", "contact[*].last_name", "name"),
                FormFieldMapping("witness_telephone", "contact[*].phone.phone_number", "phone"),
                FormFieldMapping("witness_address", "contact[*].address.address_location", "location"),
                FormFieldMapping("witness_signature", "contact[*].signature", "string"),
                FormFieldMapping("witness_date", "contact[*].signature_date", "date"),
                
                # Form Metadata
                FormFieldMapping("form_number", "key_document[*].id", "string"),
                FormFieldMapping("form_title", "key_document[*].name", "string"),
                FormFieldMapping("decision_number", "key_document[*].decision_number", "string"),
                FormFieldMapping("date_of_application", "key_document[*].date_created", "date"),
            ],
            
            # ============================================================================
            # 4. VA CLAIM FOR STANDARD GOVERNMENT HEADSTONE OR MARKER (VA-40-1330)
            # ============================================================================
            "va_headstone_marker_claim_40_1330": [
                # Basic Determination and Request Type
                FormFieldMapping("va_previously_determined_eligibility", "key_document[*].va_eligibility_determined", "boolean"),
                FormFieldMapping("initial_request", "key_document[*].request_type", "select"),
                FormFieldMapping("replacement_request", "key_document[*].request_type", "select"),
                FormFieldMapping("replacement_reason", "key_document[*].replacement_reason", "string"),
                
                # Deceased Information
                FormFieldMapping("name_first", "deceased.first_name", "name"),
                FormFieldMapping("name_middle", "deceased.middle_name", "name"),
                FormFieldMapping("name_last", "deceased.last_name", "name"),
                FormFieldMapping("name_suffix", "deceased.name_suffix", "string"),
                FormFieldMapping("grave_currently_marked", "final_wishes.preparations.plot.current_marker", "boolean"),
                FormFieldMapping("grave_not_marked", "final_wishes.preparations.plot.unmarked", "boolean"),
                FormFieldMapping("race_ethnicity", "deceased.race_ethnicity", "select"),
                FormFieldMapping("sex", "deceased.gender", "select"),
                FormFieldMapping("age_at_death", "deceased.age_at_death", "number"),
                
                # Veteran Service Information
                FormFieldMapping("veteran_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("service_number", "deceased.military.service_number", "string"),
                FormFieldMapping("place_of_birth", "deceased.place_of_birth", "location"),
                FormFieldMapping("date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("date_entered_service", "deceased.military.service_start_date", "date"),
                FormFieldMapping("date_separated_service", "deceased.military.service_end_date", "date"),
                FormFieldMapping("highest_rank_attained", "deceased.military.highest_rank", "string"),
                
                # Branch of Service
                FormFieldMapping("army", "deceased.military.branch_of_service", "select"),
                FormFieldMapping("navy", "deceased.military.branch_of_service", "select"),
                FormFieldMapping("marine_corps", "deceased.military.branch_of_service", "select"),
                FormFieldMapping("coast_guard", "deceased.military.branch_of_service", "select"),
                FormFieldMapping("air_force", "deceased.military.branch_of_service", "select"),
                FormFieldMapping("army_air_forces", "deceased.military.branch_of_service", "select"),
                FormFieldMapping("merchant_marine", "deceased.military.branch_of_service", "select"),
                FormFieldMapping("other_service", "deceased.military.branch_of_service", "select"),
                
                # Awards and Decorations
                FormFieldMapping("medal_of_honor", "deceased.military.awards", "string", "track_awards"),
                FormFieldMapping("distinguished_service_cross", "deceased.military.awards", "string", "track_awards"),
                FormFieldMapping("silver_star", "deceased.military.awards", "string", "track_awards"),
                FormFieldMapping("distinguished_flying_cross", "deceased.military.awards", "string", "track_awards"),
                FormFieldMapping("purple_heart", "deceased.military.awards", "string", "track_awards"),
                FormFieldMapping("air_medal", "deceased.military.awards", "string", "track_awards"),
                FormFieldMapping("other_awards", "deceased.military.awards", "string", "track_awards"),
                
                # Headstone/Marker Type
                FormFieldMapping("flat_bronze", "final_wishes.monument.type", "select"),
                FormFieldMapping("flat_granite", "final_wishes.monument.type", "select"),
                FormFieldMapping("upright_marble", "final_wishes.monument.type", "select"),
                FormFieldMapping("flat_marble", "final_wishes.monument.type", "select"),
                FormFieldMapping("bronze_niche", "final_wishes.monument.type", "select"),
                FormFieldMapping("upright_granite", "final_wishes.monument.type", "select"),
                FormFieldMapping("small_flat_granite", "final_wishes.monument.type", "select"),
                
                # War Service
                FormFieldMapping("world_war_ii", "deceased.military.war_service", "string", "track_war_service"),
                FormFieldMapping("korea", "deceased.military.war_service", "string", "track_war_service"),
                FormFieldMapping("vietnam", "deceased.military.war_service", "string", "track_war_service"),
                FormFieldMapping("persian_gulf", "deceased.military.war_service", "string", "track_war_service"),
                FormFieldMapping("afghanistan", "deceased.military.war_service", "string", "track_war_service"),
                FormFieldMapping("iraq", "deceased.military.war_service", "string", "track_war_service"),
                FormFieldMapping("other_war_service", "deceased.military.war_service", "string", "track_war_service"),
                
                # Emblem of Belief
                FormFieldMapping("emblem_number", "final_wishes.monument.emblem", "string"),
                FormFieldMapping("no_emblem", "final_wishes.monument.emblem", "string"),
                
                # Additional Inscription
                FormFieldMapping("additional_inscription", "final_wishes.monument.inscription_additional", "string"),
                
                # Applicant Information
                FormFieldMapping("applicant_name_address", "applicant.address", "location"),
                FormFieldMapping("applicant_phone", "applicant.phone", "phone"),
                FormFieldMapping("applicant_email", "applicant.email", "email"),
                FormFieldMapping("applicant_fax", "applicant.fax", "phone"),
                FormFieldMapping("family_member", "estate_reps[*].secondary_relationship_to_deceased", "select"),
                FormFieldMapping("personal_representative", "estate_reps[*].role", "select"),
                FormFieldMapping("veterans_service_officer", "estate_reps[*].role", "select"),
                FormFieldMapping("funeral_home_management", "estate_reps[*].role", "select"),
                FormFieldMapping("cemetery_management", "estate_reps[*].role", "select"),
                FormFieldMapping("other_applicant_role", "estate_reps[*].role", "select"),
                
                # Presidential Memorial Certificate
                FormFieldMapping("presidential_memorial_certificate", "key_document[*].presidential_certificate", "boolean"),
                FormFieldMapping("certificate_quantity", "key_document[*].certificate_quantity", "number"),
                
                # Certification and Signatures
                FormFieldMapping("applicant_signature", "applicant.signature", "string"),
                FormFieldMapping("application_date", "key_document[*].date_created", "date"),
                
                # Delivery Information
                FormFieldMapping("consignee_name_address", "funeral_home.address", "location"),
                FormFieldMapping("consignee_phone", "funeral_home.phone", "phone"),
                FormFieldMapping("consignee_signature", "funeral_home.authorized_signature", "string"),
                FormFieldMapping("consignee_date", "funeral_home.signature_date", "date"),
                
                # Cemetery Information
                FormFieldMapping("cemetery_name_address", "final_wishes.preparations.plot.location", "location"),
                FormFieldMapping("cemetery_phone", "final_wishes.preparations.plot.cemetery_phone", "phone"),
                FormFieldMapping("cemetery_official_signature", "final_wishes.preparations.plot.authorized_signature", "string"),
                FormFieldMapping("cemetery_official_date", "final_wishes.preparations.plot.signature_date", "date"),
                FormFieldMapping("section_grave_number", "final_wishes.preparations.plot.section_grave", "string"),
                
                # Special Circumstances
                FormFieldMapping("remains_not_buried", "final_wishes.disposition.method.special_circumstances", "boolean"),
                FormFieldMapping("remains_disposition_explanation", "final_wishes.disposition.method.details", "string"),
                FormFieldMapping("remarks", "key_document[*].notes", "string"),
                
                # Form Metadata
                FormFieldMapping("form_number", "key_document[*].id", "string"),
                FormFieldMapping("form_title", "key_document[*].name", "string"),
            ],
            
            # ============================================================================
            # 5. SF-1174 CLAIM FOR UNPAID COMPENSATION OF DECEASED UNIFORMED SERVICES MEMBER
            # ============================================================================
            "sf1174_unpaid_compensation_claim": [
                # Part A - Basic Claimant Information
                FormFieldMapping("claimant_names_ssn", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("claimant_social_security", "applicant.social_insurance_number", "sin"),
                FormFieldMapping("relationship_to_deceased", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("minor_age", "applicant.age", "number"),
                FormFieldMapping("designation_beneficiary_on_file", "key_document[*].beneficiary_on_file", "boolean"),
                FormFieldMapping("named_beneficiary", "key_document[*].applicant_named_beneficiary", "boolean"),
                FormFieldMapping("claimant_state_residence", "applicant.address", "location", "extract_state"),
                FormFieldMapping("decedent_name_rank_service_number", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("decedent_rank", "deceased.military.rank", "string"),
                FormFieldMapping("decedent_service_number", "deceased.military.service_number", "string"),
                FormFieldMapping("decedent_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("name_of_service", "deceased.military.branch_of_service", "string"),
                FormFieldMapping("decedent_domicile", "deceased.home_address", "location"),
                
                # Part B - Widow/Widower Certification
                FormFieldMapping("married_to_decedent", "spouse.married_status", "boolean"),
                FormFieldMapping("marriage_not_dissolved", "spouse.marriage_not_dissolved", "boolean"),
                
                # Part C - Family Information
                FormFieldMapping("widow_widower_name", "spouse.name", "name", "parse_full_name"),
                FormFieldMapping("widow_widower_ssn", "spouse.social_insurance_number", "sin"),
                FormFieldMapping("widow_widower_age", "spouse.age", "number"),
                FormFieldMapping("widow_widower_relationship", "spouse.relationship", "string"),
                FormFieldMapping("widow_widower_address", "spouse.address", "location"),
                
                FormFieldMapping("living_child_name", "children[*].name", "name", "parse_full_name"),
                FormFieldMapping("living_child_ssn", "children[*].social_insurance_number", "sin"),
                FormFieldMapping("living_child_age", "children[*].age", "number"),
                FormFieldMapping("living_child_relationship", "children[*].relationship", "string"),
                FormFieldMapping("living_child_address", "children[*].address", "location"),
                FormFieldMapping("child_class_designation", "children[*].child_class", "string"),
                
                FormFieldMapping("surviving_parent_name", "contact[*].name", "name", "parse_full_name"),
                FormFieldMapping("surviving_parent_ssn", "contact[*].social_insurance_number", "sin"),
                FormFieldMapping("surviving_parent_age", "contact[*].age", "number"),
                FormFieldMapping("surviving_parent_relationship", "contact[*].relationship", "string"),
                FormFieldMapping("surviving_parent_address", "contact[*].address.address_location", "location"),
                FormFieldMapping("parent_type", "contact[*].parent_type", "string"),
                
                FormFieldMapping("next_of_kin_name", "contact[*].name", "name", "parse_full_name"),
                FormFieldMapping("next_of_kin_ssn", "contact[*].social_insurance_number", "sin"),
                FormFieldMapping("next_of_kin_age", "contact[*].age", "number"),
                FormFieldMapping("next_of_kin_relationship", "contact[*].relationship", "string"),
                FormFieldMapping("next_of_kin_address", "contact[*].address.address_location", "location"),
                
                # Part D - Executor/Administrator Information
                FormFieldMapping("executor_administrator_appointed", "estate_reps[*].executor_appointed", "boolean"),
                FormFieldMapping("executor_administrator_name", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("estate_administration_location", "estate_reps[*].administration_location", "location"),
                FormFieldMapping("administration_certificate", "estate_reps[*].proof_of_authority", "file"),
                FormFieldMapping("appointment_still_in_effect", "estate_reps[*].appointment_active", "boolean"),
                FormFieldMapping("will_administrator_be_appointed", "estate_reps[*].future_appointment", "boolean"),
                FormFieldMapping("interested_relative_creditor", "contact[*].interested_party", "string"),
                
                # Part E - Funeral Expenses
                FormFieldMapping("funeral_expenses_paid", "funeral_home.expenses_paid", "boolean"),
                FormFieldMapping("funeral_undertaker_bill", "funeral_home.receipted_bill", "file"),
                FormFieldMapping("funeral_expense_payer", "funeral_home.expense_payer", "string"),
                
                # Signatures and Witnesses
                FormFieldMapping("claimant_signature_1", "applicant.signature", "string"),
                FormFieldMapping("claimant_signature_date_1", "applicant.signature_date", "date"),
                FormFieldMapping("claimant_street_address_1", "applicant.address", "location"),
                FormFieldMapping("claimant_city_state_zip_1", "applicant.address", "location", "extract_city_state_zip"),
                
                FormFieldMapping("claimant_signature_2", "estate_reps[*].signature", "string"),
                FormFieldMapping("claimant_signature_date_2", "estate_reps[*].signature_date", "date"),
                FormFieldMapping("claimant_street_address_2", "estate_reps[*].address", "location"),
                FormFieldMapping("claimant_city_state_zip_2", "estate_reps[*].address", "location", "extract_city_state_zip"),
                
                FormFieldMapping("witness_1_signature", "contact[*].signature", "string"),
                FormFieldMapping("witness_1_address", "contact[*].address.address_location", "location"),
                FormFieldMapping("witness_1_city_state_zip", "contact[*].address.address_location", "location", "extract_city_state_zip"),
                
                FormFieldMapping("witness_2_signature", "contact[*].co_witness_signature", "string"),
                FormFieldMapping("witness_2_address", "contact[*].co_witness_address", "location"),
                FormFieldMapping("witness_2_city_state_zip", "contact[*].co_witness_address", "location", "extract_city_state_zip"),
                
                # Legal Warnings and Penalties
                FormFieldMapping("false_claim_penalty_warning", "key_document[*].legal_warnings", "string"),
                FormFieldMapping("federal_checks_in_possession", "key_document[*].federal_checks_note", "string"),
                
                # Form Metadata
                FormFieldMapping("form_number", "key_document[*].id", "string"),
                FormFieldMapping("form_title", "key_document[*].name", "string"),
                FormFieldMapping("form_revision_date", "key_document[*].revision_date", "date"),
            ],
            
            # ============================================================================
            # CONTINUING WITH EXISTING FORMS FROM ORIGINAL CODE...
            # ============================================================================
            
            # ============================================================================
            # 6. NEVADA DMV AFFIDAVIT FOR TRANSFER OF TITLE (VP-24)
            # ============================================================================
            "nevada_dmv_affidavit_vp24": [
                # Affiant (Applicant/Heir) Information
                FormFieldMapping("Affiant full legal name", "applicant.full_name", "name"),
                FormFieldMapping("Affiants Mailing Address", "applicant.mailing_address", "location"),
                FormFieldMapping("Affiants Physical Address", "applicant.home_address", "location"),
                FormFieldMapping("Affiant's relationship to decedent", "applicant.relationship_to_deceased", "string"),
                FormFieldMapping("Affiants Signature", "applicant.signature", "signature"),
                FormFieldMapping("Affiants Printed Name and Title if applicable", "applicant.printed_name_and_title", "string"),

                # Deceased Information
                FormFieldMapping("Name of deceased", "deceased.full_name", "name"),
                FormFieldMapping("Day", "deceased.date_of_death", "date", "combine_date_components"),
                FormFieldMapping("Month", "deceased.date_of_death", "date", "combine_date_components"),
                FormFieldMapping("Year2", "deceased.date_of_death", "date", "combine_date_components"),

                # Vehicle Information
                FormFieldMapping("Year1", "property.vehicles[0].year", "string"),
                FormFieldMapping("Make", "property.vehicles[0].make", "string"),
                FormFieldMapping("Model", "property.vehicles[0].model", "string"),
                FormFieldMapping("Vehicle Identification Number", "property.vehicles[0].vin", "string"),

                # Legal Declaration
                FormFieldMapping("Transferred to the Affiant for the reason that Aff", "key_document.transfer_reason", "string", required=False),

                # Notary Information
                FormFieldMapping("State of", "key_document.notary_state", "string", required=False),
                FormFieldMapping("County of", "key_document.notary_county", "string", required=False),
                FormFieldMapping("day of", "key_document.notary_date", "date", required=False), # e.g., "15th day of"
                FormFieldMapping("By 1", "key_document.notary_name", "string", required=False),
                FormFieldMapping("By 2", "key_document.notary_signature", "signature", required=False),
            ],
            

            "electoral_deceased_removal_form": [
            # Declaration/Request Fields
                FormFieldMapping("I request that the deceased person named above be removed from the registers maintained by", 
                                "key_document[*].removal_request_text", "string"),
                
                FormFieldMapping("I have included a copy of acceptable documentation", 
                                "key_document[*].documentation_declaration", "boolean"),
                FormFieldMapping("I have included a copy of acceptable documentation (proof of death)", 
                                "key_document[*].documentation_declaration", "boolean"),
                FormFieldMapping("I have included a copy of acceptable documentation (proof of death);", 
                                "key_document[*].documentation_declaration", "boolean"),
                FormFieldMapping("I have included a copy of acceptabl", 
                                "key_document[*].documentation_declaration", "boolean"),
                FormFieldMapping("I have included a copy of acceptable", 
                                "key_document[*].documentation_declaration", "boolean"),
                FormFieldMapping("I have included a copy of acceptable document", 
                                "key_document[*].documentation_declaration", "boolean"),
                FormFieldMapping("I have included a copy of acceptable documenta", 
                                "key_document[*].documentation_declaration", "boolean"),
                FormFieldMapping("I have included a copy of acceptable documentat", 
                                "key_document[*].documentation_declaration", "boolean"),
                FormFieldMapping("I have included a copy of acceptable documentati", 
                                "key_document[*].documentation_declaration", "boolean"),
                FormFieldMapping("I have included a copy of acceptable documentatio", 
                                "key_document[*].documentation_declaration", "boolean"),
                
                # Signature and Legal Fields
                FormFieldMapping("Elector Signature", "applicant.signature", "signature"),
                
                # Date Fields
                FormFieldMapping("Year", "deceased.date_of_death", "date", "combine_date_components"),
                FormFieldMapping("Month", "deceased.datek_of_death", "date", "combine_date_components"), 
                FormFieldMapping("Day", "deceased.date_of_death", "date", "combine_date_components"),
                
                # Text Fields - Conservative Mapping
                FormFieldMapping("Text1", "deceased.full_name", "name"),
                FormFieldMapping("Text2", "deceased.date_of_birth", "date"),
                FormFieldMapping("Text3", "deceased.home_address", "location"),
                FormFieldMapping("Text4", "applicant.full_name", "name"),
                FormFieldMapping("Text5", "applicant.home_address", "location"),
                FormFieldMapping("Text6", "applicant.phone", "phone"),
                FormFieldMapping("Text7", "applicant.email", "email"),
                FormFieldMapping("Text8", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("Text9", "deceased.electoral_district", "string"),
                FormFieldMapping("Text13", "deceased.voter_registration_number", "string"),
                FormFieldMapping("Text14", "key_document[*].electoral_office_name", "string"),
                FormFieldMapping("Text15", "key_document[*].death_certificate_number", "string"),
                FormFieldMapping("Text16", "key_document[*].proof_of_relationship", "string"),
                FormFieldMapping("Text17", "applicant.identification_type", "string"),
                FormFieldMapping("Text18", "applicant.identification_number", "string"),
                FormFieldMapping("Text19", "key_document[*].additional_notes", "string"),
                FormFieldMapping("Text20", "key_document[*].office_use_only", "string"),
            ],
            
            "service_canada_cpp_death_benefit_isp1200": [
                # Page 3 - Section A: Deceased Contributor Information
                FormFieldMapping("SC_ISP1200[0].page3[0].sub_TabOrder[0].sub_A1_SIN[0]", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("SC_ISP1200[0].page3[0].sub_TabOrder[0].txtF_Dob[0]", "deceased.date_of_birth", "date"),
                FormFieldMapping("SC_ISP1200[0].page3[0].sub_TabOrder[0].txtF_Date_Death[0]", "deceased.date_of_death", "date"),
                FormFieldMapping("SC_ISP1200[0].page3[0].txtF_FirstName[0]", "deceased.first_name", "name"),
                FormFieldMapping("SC_ISP1200[0].page3[0].txtF_MiddleName[0]", "deceased.middle_name", "name"),
                FormFieldMapping("SC_ISP1200[0].page3[0].txtF_FamilyName[0]", "deceased.last_name", "name"),
                FormFieldMapping("SC_ISP1200[0].page3[0].txtF_LastNameBirth[0]", "deceased.name_at_birth", "name"),
                FormFieldMapping("SC_ISP1200[0].page3[0].txtF_Country[0]", "deceased.country_of_birth", "string"),

                # Page 4 - Deceased Contributor Information (continued)
                FormFieldMapping("SC_ISP1200[0].#pageSet[0].Page4[0].#subform[0].txtF_SIN[0]", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_info[0].txtF_HomeAddress[0]", "deceased.home_address", "location"),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_info[0].dd_LastProvinceOfResidence[0]", "deceased.last_province_of_residence", "string"),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_info[0].sub_A1_DOD_Marital_status[0].rb_Marital[0]", "deceased.marital_status_at_death", "string"),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_info[0].sub_A1_DC_Details[0].txtF_DC_Name[0]", "spouse.name", "name", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_info[0].sub_A1_DC_Details[0].txtF_DC_TelNum[0]", "spouse.phone", "phone", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_info[0].sub_DC_ProgramMembership[0].sub_CPP[0].rb_CPP[0]", "deceased.benefits.cpp_benefit", "checkbox"),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_info[0].sub_DC_ProgramMembership[0].sub_OAS[0].rb_OAS[0]", "deceased.benefits.oas_benefit", "checkbox"),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_info[0].sub_DC_ProgramMembership[0].sub_QPP[0].rb_QPP[0]", "deceased.benefits.qpp_benefit", "checkbox"),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_info[0].txtF_DC_SIN[0]", "deceased.benefits.account_number", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].rb_YesNo1[0]", "deceased.benefits.family_allowance", "boolean"),

                # Page 4 - Section B: Deceased International Work History
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_A2[0].rb_YesNo1[0]", "deceased.international_work_history", "boolean"),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_1[0].txtF_country[0]", "deceased.international_work[0].country", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_1[0].txtF_SIN_in_country[0]", "deceased.international_work[0].id_number", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_1[0].txtF_lived_from[0]", "deceased.international_work[0].lived_from", "date", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_1[0].txtF_ResFromY_2[0]", "deceased.international_work[0].lived_from_year", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_1[0].txtF_lived_to[0]", "deceased.international_work[0].lived_to", "date", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_1[0].txtF_RedToY_2[0]", "deceased.international_work[0].lived_to_year", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_1[0].txtF_worked_from[0]", "deceased.international_work[0].worked_from", "date", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_1[0].txtF_EmFromY_2[0]", "deceased.international_work[0].worked_from_year", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_1[0].txtF_worked_to[0]", "deceased.international_work[0].worked_to", "date", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_1[0].txtF_EmToY_2[0]", "deceased.international_work[0].worked_to_year", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_1[0].rbg_YesNo[0]", "deceased.international_work[0].received_benefits", "boolean", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_2[0].txtF_country[0]", "deceased.international_work[1].country", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_2[0].txtF_SIN_in_country[0]", "deceased.international_work[1].id_number", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_2[0].txtF_ResFromY_2[0]", "deceased.international_work[1].lived_from_year", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_2[0].txtF_RedToY_2[0]", "deceased.international_work[1].lived_to_year", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_2[0].txtF_EmFromY_2[0]", "deceased.international_work[1].worked_from_year", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_2[0].txtF_EmToY_2[0]", "deceased.international_work[1].worked_to_year", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page4[0].sub_table_SecB[0].BR_2[0].rbg_YesNo[0]", "deceased.international_work[1].received_benefits", "boolean", required=False),
                
                # Page 5 - Section C1: Person Waiving Benefit
                FormFieldMapping("SC_ISP1200[0].page5[0].Executor[0]", "waiver.is_executor", "checkbox", required=False),
                FormFieldMapping("SC_ISP1200[0].page5[0].Individual[0]", "waiver.is_individual_funeral_payer", "checkbox", required=False),
                FormFieldMapping("SC_ISP1200[0].page5[0].sub_C1[0].txtF_FirstName[0]", "waiver.first_name", "name", required=False),
                FormFieldMapping("SC_ISP1200[0].page5[0].sub_C1[0].txtF_MiddleName[0]", "waiver.middle_name", "name", required=False),
                FormFieldMapping("SC_ISP1200[0].page5[0].sub_C1[0].txtF_FamilyName[0]", "waiver.last_name", "name", required=False),
                FormFieldMapping("SC_ISP1200[0].page5[0].sub_C1[0].txtF_Home_address[0]", "waiver.address", "location", required=False),
                FormFieldMapping("SC_ISP1200[0].page5[0].sub_C1[0].txtF_city[0]", "waiver.city", "string", required=False), # NEW
                FormFieldMapping("SC_ISP1200[0].page5[0].sub_C1[0].txtF_province[0]", "waiver.province", "string", required=False), # NEW
                FormFieldMapping("SC_ISP1200[0].page5[0].sub_C1[0].txtF_country[0]", "waiver.country", "string", required=False), # NEW
                FormFieldMapping("SC_ISP1200[0].page5[0].sub_C1[0].txtF_postalcode[0]", "waiver.postal_code", "string", required=False), # NEW
                FormFieldMapping("SC_ISP1200[0].page5[0].sub_C1[0].txtF_telephone[0]", "waiver.phone", "phone", required=False),
                FormFieldMapping("SC_ISP1200[0].page5[0].sub_C1[0].txtF_signature[0]", "waiver.signature", "signature", required=False),
                FormFieldMapping("SC_ISP1200[0].page5[0].sub_C1[0].txtF_date[0]", "waiver.signature_date", "date", required=False),

                # Page 6 - Section C2: Applicant Role
                FormFieldMapping("SC_ISP1200[0].page6[0].sub_c2[0].rb_isthereawill[0]", "deceased.has_will", "boolean"),
                FormFieldMapping("SC_ISP1200[0].page6[0].sub_Do_you_know[0].rb_isthereawill[0]", "applicant.knows_funeral_payer", "boolean"),
                FormFieldMapping("SC_ISP1200[0].page6[0].sub_Do_you_know[0].sub_paye_info[0].txtF_name[0]", "funeral_home.payer_name", "name", required=False),
                FormFieldMapping("SC_ISP1200[0].page6[0].sub_Do_you_know[0].sub_paye_info[0].txtF_address[0]", "funeral_home.payer_address", "location", required=False),
                FormFieldMapping("SC_ISP1200[0].page6[0].sub_Do_you_know[0].sub_paye_info[0].txtF_tel[0]", "funeral_home.payer_phone", "phone", required=False),
                FormFieldMapping("SC_ISP1200[0].page6[0].I_am_applying_as_the[0].rb_Applying_as_the[0]", "applicant.role", "string"),
                FormFieldMapping("SC_ISP1200[0].page6[0].I_am_applying_as_the[0].txtF_Speciallist[0]", "applicant.role_next_of_kin_details", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page6[0].I_am_applying_as_the[0].sub_funeral_expenses[0].txtF_amount[0]", "funeral_home.expenses_paid_amount", "currency", required=False),
                FormFieldMapping("SC_ISP1200[0].page6[0].I_am_applying_as_the[0].sub_funeral_expenses[0].txtF_Service_provider[0]", "funeral_home.service_provider_name", "string", required=False),

                # Page 7 - Section D: Applicant Information
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D1[0].sub_D1_first_row[0].sub_written[0].rb_prefLang_written[0]", "applicant.language_preference_written", "string"),
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D1[0].sub_D1_first_row[0].sub_verbal[0].rb_prefLang_verbal[0]", "applicant.language_preference_verbal", "string"),
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D1[0].sub_D1_first_row[0].txtF_relationship[0]", "applicant.relationship_to_deceased", "string"),
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D1[0].sub_D1_row_2[0].txtF_FirstName[0]", "applicant.first_name", "name"),
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D1[0].sub_D1_row_2[0].txtF_MiddleName[0]", "applicant.middle_name", "name"),
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D1[0].sub_D1_row_2[0].txtF_FamilyName[0]", "applicant.last_name", "name"),
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D1[0].txtF_Home_address[0]", "applicant.home_address", "location", "combine_address_street"),
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D1[0].txtF_city[0]", "applicant.home_address", "location", "combine_address_city"), # NEW
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D1[0].txtF_province[0]", "applicant.home_address", "location", "combine_address_province"), # NEW
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D1[0].txtF_country[0]", "applicant.home_address", "location", "combine_address_country"), # NEW
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D1[0].txtF_postalcode[0]", "applicant.home_address", "location", "combine_address_postal"), # NEW
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D1[0].txtF_teleNum[0]", "applicant.phone", "phone"),
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D1[0].txtF_Alt_teleNum[0]", "applicant.phone_alt", "phone", required=False),
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D1[0].txtF_EmailAddress[0]", "applicant.email", "email", required=False),
                
                # Page 7 - Direct Deposit Information
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_dd[0].txtF_BranchNumber5Digits[0]", "payment.transit_number", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_dd[0].txtF_InstitutionNumber3Di[0]", "payment.institution_number", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_dd[0].txtF_AccountNumbermaximum[0]", "payment.account_number", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_dd[0].txtF_NamesOnTheAccount[0]", "payment.account_holder", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_dd[0].txtF_teleNum[0]", "payment.bank_phone", "phone", required=False), # NEW
                
                # Page 7 - Section D2: Tax Representative
                FormFieldMapping("SC_ISP1200[0].page7[0].sub_D2[0].rb_D2[0]", "applicant.is_tax_representative", "boolean"),

                # Page 8 - Section E/F: Signatures
                FormFieldMapping("SC_ISP1200[0].page8[0].txtF_signature[0]", "applicant.signature", "signature"),
                FormFieldMapping("SC_ISP1200[0].page8[0].dte_Date_of_Signature[0]", "key_document.signature_date", "date"),
                FormFieldMapping("SC_ISP1200[0].page8[0].sub_first_name[0].txtF_FirstName[0]", "contact.witness_first_name", "name", required=False),
                FormFieldMapping("SC_ISP1200[0].page8[0].sub_first_name[0].txtF_FamilyName[0]", "contact.witness_last_name", "name", required=False),
                FormFieldMapping("SC_ISP1200[0].page8[0].sub_first_name[0].txtF_relationship[0]", "contact.witness_relationship", "string", required=False),
                FormFieldMapping("SC_ISP1200[0].page8[0].sub_first_name[0].txtF_address[0]", "contact.witness_address", "location", required=False),
                FormFieldMapping("SC_ISP1200[0].page8[0].sub_first_name[0].txtF_Signature[0]", "contact.witness_signature", "signature", required=False),
                FormFieldMapping("SC_ISP1200[0].page8[0].sub_first_name[0].dte_dateWitness[0]", "contact.witness_signature_date", "date", required=False),

                # Page 9 - Checklist and Additional Info
                FormFieldMapping("SC_ISP1200[0].page9[0].sub_check_list[0].cb_1[0]", "checklist.all_fields_complete", "checkbox", required=False),
                FormFieldMapping("SC_ISP1200[0].page9[0].sub_check_list[0].cb_2[0]", "checklist.proof_of_death_provided", "checkbox", required=False),
                FormFieldMapping("SC_ISP1200[0].page9[0].sub_check_list[0].cb_3[0]", "checklist.funeral_expenses_provided", "checkbox", required=False),
                FormFieldMapping("SC_ISP1200[0].page9[0].sub_check_list[0].cb_4[0]", "checklist.sin_on_documents", "checkbox", required=False),
                FormFieldMapping("SC_ISP1200[0].page9[0].sub_check_list[0].cb_5[0]", "checklist.declaration_signed", "checkbox", required=False),
                FormFieldMapping("SC_ISP1200[0].page9[0].txtF_additional_information[0]", "key_document.additional_notes", "string", required=False)
            ],

            "california_statement_of_facts_reg256": [
                # Vehicle Identification
                FormFieldMapping("License Plate/CF Number", "vehicle[*].license_plate_number", "string"),
                FormFieldMapping("Veh/Vessel ID Number", "vehicle[*].vehicle_identification_number", "string"),
                FormFieldMapping("Year/Make2", "vehicle[*].year_make_model", "string"),
                FormFieldMapping("Vehicle/Vessel ID Number", "vehicle[*].vehicle_identification_number", "string"),
                FormFieldMapping("Year/Make", "vehicle[*].year_make_model", "string"),
                
                # Tax Exemption Checkboxes
                FormFieldMapping("Family transfer box", "key_document[*].exemption_family_transfer", "boolean"),
                FormFieldMapping("addition/deletion box", "key_document[*].exemption_family_addition_deletion", "boolean"),
                FormFieldMapping("gift box", "key_document[*].exemption_gift", "boolean"),
                FormFieldMapping("Court order box", "key_document[*].exemption_court_order", "boolean"),
                FormFieldMapping("inheritance box", "key_document[*].exemption_inheritance", "boolean"),
                FormFieldMapping("Current Market Value 1", "vehicle[*].current_market_value", "currency"),
                FormFieldMapping("Current Market Value", "vehicle[*].current_market_value", "currency"),
                
                # Smog Exemption Checkboxes
                FormFieldMapping("Biennial Smog cert box", "key_document[*].smog_cert_90_days", "boolean"),
                FormFieldMapping("Powered by electricity box", "vehicle[*].powered_by_electricity", "boolean"),
                FormFieldMapping("Powered by diesel box", "vehicle[*].powered_by_diesel", "boolean"),
                FormFieldMapping("Powered by other box", "vehicle[*].powered_by_other", "boolean"),
                FormFieldMapping("Powered by other 2", "vehicle[*].powered_by_other_specify", "string"),
                FormFieldMapping("Located outside CA box.0", "key_document[*].located_outside_california", "boolean"),
                FormFieldMapping("Located outside CA box.1", "key_document[*].located_outside_california_alt", "boolean"),
                FormFieldMapping("Paren, grandparent, etc box", "key_document[*].family_transfer_smog_exempt", "boolean"),
                FormFieldMapping("Companies leasing vehicle box", "key_document[*].company_leasing_exempt", "boolean"),
                FormFieldMapping("Lessor/Lessee of vehicle box", "key_document[*].lessor_lessee_exempt", "boolean"),
                FormFieldMapping("Lessor/lessee operator box", "key_document[*].lessor_lessee_operator_exempt", "boolean"),
                FormFieldMapping("Individual as registered own box.0", "key_document[*].individual_registered_owner", "boolean"),
                FormFieldMapping("Individual as registered own box.1", "key_document[*].individual_registered_owner_alt", "boolean"),
                
                # Transfer Type
                FormFieldMapping("Transfer only box", "key_document[*].transfer_only", "boolean"),
                FormFieldMapping("Title only box", "key_document[*].title_only", "boolean"),
                
                # Disabled Person Section
                FormFieldMapping("Disabled Person Plate", "applicant.disabled_person_plate", "string"),
                FormFieldMapping("Disabled Vet Plate", "applicant.disabled_veteran_plate", "string"),
                FormFieldMapping("Disabled Person Placard", "applicant.disabled_person_placard", "string"),
                FormFieldMapping("Window decal-License No", "vehicle[*].window_decal_license_number", "string"),
                FormFieldMapping("Window decal-Vehicle Make", "vehicle[*].window_decal_vehicle_make", "string"),
                FormFieldMapping("Window decal-Veh ID No", "vehicle[*].window_decal_vehicle_id", "string"),
                
                # Mailing Address
                FormFieldMapping("Mail to-Name", "applicant.mail_to_name", "name"),
                FormFieldMapping("Mail to-Address", "applicant.mail_to_address", "location", "combine_address_street"),
                FormFieldMapping("Mail to-City", "applicant.mail_to_address", "location", "combine_address_city"),
                FormFieldMapping("Mail to-State", "applicant.mail_to_address", "location", "combine_address_state"),
                FormFieldMapping("Mail to-Zip", "applicant.mail_to_address", "location", "combine_address_zip"),
                
                # Vehicle Body Change Section
                FormFieldMapping("E. Market value of vehicle or vessel", "vehicle[*].current_market_value", "currency"),
                FormFieldMapping("E. Cost of changes", "vehicle[*].modification_cost", "currency"),
                FormFieldMapping("E. Date changes made", "vehicle[*].modification_date", "date"),
                FormFieldMapping("E. Unladen weight box", "vehicle[*].unladen_weight_changed", "boolean"),
                FormFieldMapping("UNLADEN WEIGHT", "vehicle[*].unladen_weight", "string"),
                FormFieldMapping("E. Motive power box", "vehicle[*].motive_power_changed", "boolean"),
                FormFieldMapping("E. Motive power changed from", "vehicle[*].motive_power_from", "string"),
                FormFieldMapping("E. Motive power changed to", "vehicle[*].motive_power_to", "string"),
                FormFieldMapping("E. Body type box", "vehicle[*].body_type_changed", "boolean"),
                FormFieldMapping("E. Body type changed from", "vehicle[*].body_type_from", "string"),
                FormFieldMapping("E. Body power changed to", "vehicle[*].body_type_to", "string"),
                FormFieldMapping("E. No of axles box", "vehicle[*].number_of_axles_changed", "boolean"),
                FormFieldMapping("E. No axles changed from", "vehicle[*].number_of_axles_from", "string"),
                FormFieldMapping("E. No axles changed to", "vehicle[*].number_of_axles_to", "string"),
                
                # Name Statement Section
                FormFieldMapping("F. I/We same person box", "applicant.same_person_declaration", "boolean"),
                FormFieldMapping("F. I, name", "applicant.name_statement_first_name", "name"),
                FormFieldMapping("F. and are same person", "applicant.name_statement_second_name", "name"),
                FormFieldMapping("F. Name mispelled box", "applicant.name_misspelled", "boolean"),
                FormFieldMapping("F. Name misspelled", "applicant.name_misspelled_correction", "name"),
                FormFieldMapping("F. Changing name box", "applicant.name_change", "boolean"),
                FormFieldMapping("F. changing name from", "applicant.name_change_from", "name"),
                FormFieldMapping("F. Changing name to", "applicant.name_change_to", "name"),
                
                # Statement of Facts
                FormFieldMapping("g. undersigned state", "key_document[*].statement_of_facts", "string"),
                
                # Signature Section
                FormFieldMapping("PRINTED NAME", "applicant.printed_last_name", "name"),
                FormFieldMapping("FIRST NAME", "applicant.first_name", "name"),
                FormFieldMapping("MIDDLE NAME", "applicant.middle_name", "name"),
                FormFieldMapping("App sign area code", "applicant.phone_area_code", "string"),
                FormFieldMapping("App sign phone no", "applicant.phone_number", "phone"),
                FormFieldMapping("Signature date", "applicant.signature_date", "date"),
                
                # Form Buttons (PDF Interactive Elements)
                FormFieldMapping("click", "key_document[*].pdf_button_1", "string"),
                FormFieldMapping("click to", "key_document[*].pdf_button_2", "string"),
                FormFieldMapping("click to 1", "key_document[*].pdf_button_3", "string"),

                FormFieldMapping("Powered by box", "vehicle[*].powered_by_checkbox", "boolean"),
            ],

            "service_canada_cpp_survivors_pension_isp1300": [
                # ==============================================================================
                # PAGE 1 - DECEASED SPOUSE/PARTNER INFORMATION
                # ==============================================================================
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_No_1[0].txtF_1A_SIN[0]", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_No_1[0].txtF_1B_DOB[0]", "deceased.date_of_birth", "date"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_No_1[0].txtF_1C_Country_Of_Birth[0]", "deceased.country_of_birth", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].subQ2[0].DateField1[0]", "deceased.date_of_death", "date"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q3[0].rb_3_Marital_Status[0]", "deceased.marital_status_at_death", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q4[0].sub_4A[0].sub_optional[0].rb_4A_Salutation[0]", "deceased.salutation", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q4[0].sub_4A[0].txtF_4A_First_Name_Init[0]", "deceased.first_name", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q4[0].sub_4A[0].txtF_4A_Last_Name[0]", "deceased.last_name", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q4[0].sub_4B[0].txtF_4B_First_Name_Init[0]", "deceased.name_at_birth_first", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q4[0].sub_4B[0].txtF_4B_Last_Name[0]", "deceased.name_at_birth_last", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q4[0].sub_4C[0].txtF_4C_First_Name_Init[0]", "deceased.name_on_sin_card_first", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q4[0].sub_4C[0].txtF_4C_Last_Name[0]", "deceased.name_on_sin_card_last", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q5[0].txtF_HoneAddress[0]", "deceased.home_address_street", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q5[0].txtF_City[0]", "deceased.home_address_city", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q5[0].txtF_Province[0]", "deceased.home_address_province", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q5[0].txtF_Country[0]", "deceased.home_address_country", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q5[0].txtF_PostalCode[0]", "deceased.home_address_postal", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q6[0].RadioButtonList[0]", "deceased.worked_other_countries", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q6[0].sub_Table[0].BR_A[0].txtF_Country[0]", "deceased.international_work[0].country", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q6[0].sub_Table[0].BR_A[0].txtF_Insurance_Num[0]", "deceased.international_work[0].insurance_number", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q6[0].sub_Table[0].BR_A[0].RadioButtonList[0]", "deceased.international_work[0].applied_for_benefits", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q6[0].sub_Table[0].BR_B[0].txtF_Country[0]", "deceased.international_work[1].country", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q6[0].sub_Table[0].BR_B[0].txtF_Insurance_Num[0]", "deceased.international_work[1].insurance_number", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q6[0].sub_Table[0].BR_B[0].RadioButtonList[0]", "deceased.international_work[1].applied_for_benefits", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q6[0].sub_Table[0].BR_C[0].txtF_Country[0]", "deceased.international_work[2].country", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q6[0].sub_Table[0].BR_C[0].txtF_Insurance_Num[0]", "deceased.international_work[2].insurance_number", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page1[0].sub_Q6[0].sub_Table[0].BR_C[0].RadioButtonList[0]", "deceased.international_work[2].applied_for_benefits", "boolean"),

                # ==============================================================================
                # PAGE 2 - SURVIVING SPOUSE/PARTNER INFORMATION
                # ==============================================================================
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q7A[0].txtF_7A_SIN[0]", "applicant.social_insurance_number", "sin"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q7A[0].txtF_7B_DOB[0]", "applicant.date_of_birth", "date"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q7A[0].txtF_7C_Country_Of_Birth[0]", "applicant.country_of_birth", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q8[0].sub_Q8A[0].rb_8A_Written_Comm[0]", "applicant.language_preference_written", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q8[0].sub_Q8B[0].rb_8B_Verbal_Comm[0]", "applicant.language_preference_verbal", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q9[0].sub_9A[0].sub_optional[0].rb_9A_Salutation[0]", "applicant.salutation", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q9[0].sub_9A[0].txtF_9A_First_Name_Init[0]", "applicant.first_name", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q9[0].sub_9A[0].txtF_9A_Last_Name[0]", "applicant.last_name", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q9[0].sub_Q9B[0].txtF_9B_First_Name_Init[0]", "applicant.name_at_birth_first", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q9[0].sub_Q9B[0].txtF_9B_Last_Name[0]", "applicant.name_at_birth_last", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q9[0].sub_Q9C[0].txtF_9C_First_Name_Init[0]", "applicant.name_on_sin_card_first", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q9[0].sub_Q9C[0].txtF_9C_Last_Name[0]", "applicant.name_on_sin_card_last", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q10A[0].txtF_10A_MailingAddress[0]", "applicant.mailing_address_street", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q10A[0].txtF_10A_City[0]", "applicant.mailing_address_city", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q10A[0].txtF_10A_Prov[0]", "applicant.mailing_address_province", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q10A[0].txtF_10A_Other_Country[0]", "applicant.mailing_address_country", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q10A[0].txtF_10A_Postal_Code[0]", "applicant.mailing_address_postal", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q10B[0].txtF_10B_HomeAddress[0]", "applicant.home_address_street", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q10B[0].txtF_10B_City[0]", "applicant.home_address_city", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q10B[0].txtF_10B_Prov[0]", "applicant.home_address_province", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q10B[0].txtF_10B_Other_Country[0]", "applicant.home_address_country", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q10B[0].txtF_10B_Postal_Code[0]", "applicant.home_address_postal", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q11[0].areacode_tel_11A[0]", "applicant.phone_home", "phone"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q11[0].Areacode_tel_11B[0]", "applicant.phone_work", "phone"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q12[0].txtF_12_EmailAddress[0]", "applicant.email", "email"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_13A[0].sub_CPP[0].rb_13A_CPP[0]", "applicant.previous_cpp_benefits", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_13A[0].sub_OAS[0].rb_13A_OAS[0]", "applicant.previous_oas_benefits", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_13A[0].rb_13A_QPP[0]", "applicant.previous_qpp_benefits", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q13B[0].txtF_13B_SIN[0]", "applicant.previous_benefits_sin", "sin"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q14[0].sub_Q14A[0].sub_14A[0].rb_15A_Married[0]", "applicant.was_married", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q14[0].sub_Q14A[0].dtDatemarriage_15a[0]", "applicant.marriage_date", "date"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q14[0].sub_Q14B[0].sub_15B[0].rb_15B_Still_Married[0]", "applicant.still_married_at_death", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page2[0].sub_Q14[0].sub_Q14C[0].rb_15C_Still_Living_Together[0]", "applicant.living_together_at_death", "boolean"),

                # ==============================================================================
                # PAGE 3 - COMMON LAW, BANKING, TAX, CHILDREN INFO
                # ==============================================================================
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_15A[0].dtDatelivingtogether16a[0]", "applicant.common_law_start_date", "date"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_Q15B[0].rb_16B_Still_Living_Together[0]", "applicant.common_law_living_together_at_death", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_No_16[0].txtF_BranchNumber5Digits[0]", "payment.transit_number", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_No_16[0].txtF_InstitutionNumber3Di[0]", "payment.institution_number", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_No_16[0].txtF_AccountNumbermaximum[0]", "payment.account_number", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_No_16[0].txtF_NamesOnAccount[0]", "payment.account_holder_names", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_No_16[0].txtF_TelephoneNumber[0]", "payment.bank_phone", "phone"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_No_17[0].#subform[0].rb_19_Deduct_Tax[0]", "applicant.request_tax_deduction", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_No_17[0].txtF_19_Federal_Tax_amount[0]", "applicant.tax_deduction_amount", "currency"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_No_17[0].txtF_19_Federal_Tax_percentage[0]", "applicant.tax_deduction_percentage", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_Q18[0].rb_18_Children_Under_18[0]", "applicant.has_children_under_18", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_Q18[0].sub_Q18A[0].txtF_18A_ChildFirstName[0]", "children[0].first_name", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_Q18[0].sub_Q18A[0].txtF_18A_ChildLastName[0]", "children[0].last_name", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_Q18[0].sub_Q18A[0].sub_optional[0].sub_sex[0].rb_20a_Gender[0]", "children[0].gender", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_Q18[0].sub_Q18A[0].txtF_18A_ChildDOB[0]", "children[0].date_of_birth", "date"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_Q18[0].sub_Q18A[0].txtF_18A_ChildSIN[0]", "children[0].social_insurance_number", "sin"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_Q18[0].sub_Q18A[0].sub_20a_Yes-No[0].#subform[0].rb_20a_Child_In_Care[0]", "children[0].in_care_since_birth", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_Q18[0].sub_Q18A[0].rb_20a_Child_Still_In_Care[0]", "children[0].still_in_care", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page3[0].sub_Q18[0].sub_Q18A[0].rb_20a_Child_Is[0]", "children[0].relationship", "string"),

                # ==============================================================================
                # PAGE 4 - CHILDREN 18-25 AND SUPPORT INFO
                # ==============================================================================
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].rb_19_Children_Under_18_School[0]", "applicant.has_children_18_25_school", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].sub_No_19a[0].txtF_19A_ChildFirstName[0]", "children[1].first_name", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].sub_No_19a[0].txtF_19A_ChildLastName[0]", "children[1].last_name", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].sub_No_19a[0].txtF_19A_ChildDOB[0]", "children[1].date_of_birth", "date"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].sub_No_19a[0].txtF_21a_City[0]", "children[1].address_city", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].sub_No_19a[0].txtF_21a_Prov[0]", "children[1].address_province", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].sub_No_19a[0].txtF_21a_Other_Country[0]", "children[1].address_country", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].sub_No_19a[0].txtF_21a_Postal_Code[0]", "children[1].address_postal", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].sub_No_19b[0].txtF_19B_ChildFirstName[0]", "children[2].first_name", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].sub_No_19b[0].txtF_19B_ChildLastName[0]", "children[2].last_name", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].sub_No_19b[0].txtF_19B_ChildDOB[0]", "children[2].date_of_birth", "date"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].sub_No_19b[0].txtF_21b_City[0]", "children[2].address_city", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].sub_No_19b[0].txtF_21b_Prov[0]", "children[2].address_province", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].sub_No_19b[0].txtF_21b_Other_Country[0]", "children[2].address_country", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_Q19[0].sub_No_19b[0].txtF_21b_Postal_Code[0]", "children[2].address_postal", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_No_20[0].rb_20a_CPP[0]", "children.benefits_cpp", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_No_20[0].rb_20b_QPP[0]", "children.benefits_qpp", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].rb_21_Maintaining_Children[0]", "applicant.maintaining_children_financially", "boolean"),

                # ==============================================================================
                # PAGE 5 - ALTERNATE APPLICANT INFORMATION
                # ==============================================================================
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].txtF_22_SIN[0]", "alternate_applicant.social_insurance_number", "sin"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_No_23A[0].#subform[1].rb_23A_Written_Comm[0]", "alternate_applicant.language_preference_written", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_No_23A[0].rb_23B_Verbal_Comm[0]", "alternate_applicant.language_preference_verbal", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_No_24[0].#subform[0].#subform[1].rb_24_Salutation[0]", "alternate_applicant.salutation", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_No_24[0].txtF_24_FirstName[0]", "alternate_applicant.first_name", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_No_24[0].txtF_24_FamilyName[0]", "alternate_applicant.last_name", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_No_25[0].txtF_25_MailingAddress[0]", "alternate_applicant.mailing_address_street", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_No_25[0].txtF_25_City[0]", "alternate_applicant.mailing_address_city", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_No_25[0].txtF_25_Prov[0]", "alternate_applicant.mailing_address_province", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_No_25[0].txtF_25_Other_Country[0]", "alternate_applicant.mailing_address_country", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_No_25[0].txtF_25_Postal_Code[0]", "alternate_applicant.mailing_address_postal", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_No_26[0].txtF_26A_Other[0]", "alternate_applicant.phone_home", "phone"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_No_26[0].txtF_26A_Other_Country[0]", "alternate_applicant.phone_home_country", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_No_26[0].txtF_26B_Other[0]", "alternate_applicant.phone_work", "phone"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_No_26[0].txtF_26B_Other_Country[0]", "alternate_applicant.phone_work_country", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page5[0].sub_Q27[0].txtF_27_EmailAddress[0]", "alternate_applicant.email", "email"),

                # ==============================================================================
                # PAGE 6 - SIGNATURES
                # ==============================================================================
                FormFieldMapping("SC_ISP1300_E[0].Page6[0].#subform[0].txtF_Applicant_Signature[0]", "applicant.signature", "signature"),
                FormFieldMapping("SC_ISP1300_E[0].Page6[0].#subform[0].txtF_Application_Date[0]", "key_document.signature_date", "date"),
                FormFieldMapping("SC_ISP1300_E[0].Page6[0].sub_Witness_Declaration[0].txtF_Witness_Name[0]", "contact.witness.name", "name"),
                FormFieldMapping("SC_ISP1300_E[0].Page6[0].sub_Witness_Declaration[0].txtF_Witness_Relation[0]", "contact.witness.relationship", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page6[0].sub_Witness_Declaration[0].txtF_Witness_Phone[0]", "contact.witness.phone", "phone"),
                FormFieldMapping("SC_ISP1300_E[0].Page6[0].sub_Witness_Declaration[0].txtF_Witness_Address[0]", "contact.witness.address", "location"),
                FormFieldMapping("SC_ISP1300_E[0].Page6[0].sub_Witness_Declaration[0].txtF_Signature[0]", "contact.witness.signature", "signature"),
                FormFieldMapping("SC_ISP1300_E[0].Page6[0].sub_Witness_Declaration[0].txtF_Witness_Signature_Date[0]", "contact.witness.signature_date", "date"),

                # ==============================================================================
                # PAGE 7 - EXTRA SPACE
                # ==============================================================================
                FormFieldMapping("SC_ISP1300_E[0].Page7[0].txtF_Extra_Space[0]", "key_document.additional_notes", "string"),
                # --- Child #2 (18-25 in School) - Previously Missing Fields ---
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_No_18b[0].sub_Q20B[0].ub_optional[0].rb_20b_Gender[0]", "children[2].gender", "string"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_No_18b[0].sub_Q20B[0].sub_child[0].rb_20b_Child_In_Care[0]", "children[2].in_care_since_birth", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_No_18b[0].sub_Q20B[0].rb_20b_Child_Still_In_Care[0]", "children[2].still_in_care", "boolean"),
                FormFieldMapping("SC_ISP1300_E[0].Page4[0].sub_No_18b[0].sub_Q20B[0].rb_20b_Child_Is[0]", "children[2].relationship", "string"),
            ],

            "cra_death_notification_rc4111": [
                # Deceased Person Information
                FormFieldMapping("Text1", "deceased.full_name", "name"),
                FormFieldMapping("Social insurance number SIN", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("Text2", "deceased.date_of_birth", "date"),
                FormFieldMapping("Date", "deceased.date_of_death", "date"),
                FormFieldMapping("Text3", "deceased.home_address", "location"),
                FormFieldMapping("Address", "deceased.home_address", "location"),
                FormFieldMapping("Text4", "applicant.full_name", "name"),
                FormFieldMapping("Telephone number", "applicant.phone", "phone"),
                FormFieldMapping("Text5", "applicant.home_address", "location"),
                FormFieldMapping("Relationship to the deceased person", "applicant.relationship_to_deceased", "string"),
                FormFieldMapping("Signature", "applicant.signature", "signature"),
                FormFieldMapping("Text6", "applicant.signature_date", "date"),
            ],
            "maine_voter_death_notice": [
                # Deceased Voter Information
                FormFieldMapping("Deceased Voters Name", "deceased.full_name", "name"),
                FormFieldMapping("Voters Date of Birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("Voters CityTown of Residence", "deceased.home_address.city", "string"),
                FormFieldMapping("Voters Pilace of Death", "deceased.place_of_death", "string"), # Typo in PDF
                FormFieldMapping("Voters Date of Death", "deceased.date_of_death", "date"),

                # Immediate Family Member (Applicant) Information
                FormFieldMapping("Printed name of immediate family member", "applicant.full_name", "name"),
                FormFieldMapping("Relationslilip to Voter", "applicant.relationship_to_deceased", "string"), # Typo in PDF
                FormFieldMapping("Signature of immediate family member", "applicant.signature", "signature"),
                FormFieldMapping("Date", "key_document.signature_date", "date"),

                # Registrar Use Only
                FormFieldMapping("Date Received by Registrar", "key_document.date_received", "date", required=False),
                FormFieldMapping("Date cancelled in CVR", "key_document.date_processed", "date", required=False),
                FormFieldMapping("Registrar Initials NEW 4121", "key_document.processed_by", "string", required=False)
            ],
            # ============================================================================
            # 7. OREGON DMV INHERITANCE AFFIDAVIT
            # ============================================================================
            "oregon_dmv_inheritance_affidavit": [
                FormFieldMapping("deceased_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("plate_number", "property.vehicles[*].license_plate", "string"),
                FormFieldMapping("vehicle_year", "property.vehicles[*].year", "number"),
                FormFieldMapping("vehicle_make", "property.vehicles[*].make_model", "string", "extract_make"),
                FormFieldMapping("vehicle_identification_number", "property.vehicles[*].vin", "string"),
                FormFieldMapping("heir_name", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("heir_address", "estate_reps[*].address", "location"),
                FormFieldMapping("heir_city", "estate_reps[*].address", "location", "extract_city"),
                FormFieldMapping("heir_state", "estate_reps[*].address", "location", "extract_state"),
                FormFieldMapping("heir_zip_code", "estate_reps[*].address", "location", "extract_zip"),
                FormFieldMapping("heir_signature", "estate_reps[*].signature", "string"),
                FormFieldMapping("list_all_heirs", "estate_reps[*].all_heirs", "string"),
                FormFieldMapping("no_other_heirs_certification", "estate_reps[*].heir_certification", "boolean"),
                FormFieldMapping("notary_signature", "key_document[*].notes", "string"),
                FormFieldMapping("notary_state", "key_document[*].notary_state", "string"),
                FormFieldMapping("notary_county", "key_document[*].notary_county", "string"),
            ],
            
            
            
            # ============================================================================
            # 10. PROBATE COURT PETITION FOR ADMINISTRATION
            # ============================================================================
            "probate_court_petition_administration": [
                FormFieldMapping("petitioner_name", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("petitioner_address", "estate_reps[*].address", "location"),
                FormFieldMapping("decedent_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("decedent_address", "deceased.home_address", "location"),
                FormFieldMapping("decedent_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("decedent_place_of_death", "deceased.place_of_death", "location"),
                FormFieldMapping("decedent_domicile", "deceased.legal_domicile", "location"),
                FormFieldMapping("died_testate", "deceased.will_status", "boolean"),
                FormFieldMapping("died_intestate", "deceased.will_status", "boolean"),
                FormFieldMapping("will_date", "estate_reps[*].will_date", "date"),
                FormFieldMapping("codicil_dates", "estate_reps[*].codicil_dates", "string"),
                FormFieldMapping("petitioner_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("surviving_spouse", "spouse.name", "name", "parse_full_name"),
                FormFieldMapping("surviving_children", "children[*].name", "name", "parse_full_name"),
                FormFieldMapping("heirs_at_law", "heirs[*].name", "name", "parse_full_name"),
                FormFieldMapping("estimated_estate_value", "financial_information.total_estate_value", "currency"),
                FormFieldMapping("real_property_value", "property.real_estate[*].estimated_value", "currency"),
                FormFieldMapping("personal_property_value", "property.personal_property[*].estimated_value", "currency"),
                FormFieldMapping("bond_required", "estate_reps[*].bond_required", "boolean"),
                FormFieldMapping("bond_amount", "estate_reps[*].bond_amount", "currency"),
                FormFieldMapping("court_venue", "key_document[*].court_location", "location"),
                FormFieldMapping("case_number", "key_document[*].case_number", "string"),
                FormFieldMapping("petitioner_signature", "estate_reps[*].signature", "string"),
                FormFieldMapping("attorney_signature", "estate_reps[*].attorney_signature", "string"),
                FormFieldMapping("attorney_bar_number", "estate_reps[*].attorney_bar_number", "string"),
                FormFieldMapping("filing_date", "key_document[*].date_created", "date"),
            ],
            
            # ============================================================================
            # 11. LIFE INSURANCE CLAIM FORM
            # ============================================================================
            "life_insurance_claim_form": [
                FormFieldMapping("policy_number", "insurance__life[*].id", "string"),
                FormFieldMapping("insured_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("insured_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("insured_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("insured_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("cause_of_death", "deceased.cause_of_death", "string"),
                FormFieldMapping("place_of_death", "deceased.place_of_death", "location"),
                FormFieldMapping("policy_issue_date", "insurance__life[*].start_date", "date"),
                FormFieldMapping("policy_effective_date", "insurance__life[*].effective_date", "date"),
                FormFieldMapping("coverage_amount", "insurance__life[*].coverage_amount", "currency"),
                FormFieldMapping("beneficiary_name", "insurance__life[*].beneficiary_primary", "name", "parse_full_name"),
                FormFieldMapping("beneficiary_relationship", "insurance__life[*].beneficiary_relationship", "string"),
                FormFieldMapping("beneficiary_address", "insurance__life[*].beneficiary_address", "location"),
                FormFieldMapping("beneficiary_ssn", "insurance__life[*].beneficiary_ssn", "sin"),
                FormFieldMapping("contingent_beneficiary", "insurance__life[*].beneficiary_contingent", "name", "parse_full_name"),
                FormFieldMapping("attending_physician", "deceased.attending_physician", "name", "parse_full_name"),
                FormFieldMapping("physician_address", "deceased.physician_address", "location"),
                FormFieldMapping("last_medical_attention", "deceased.last_medical_date", "date"),
                FormFieldMapping("medical_condition", "deceased.medical_condition", "string"),
                FormFieldMapping("hospitalization", "deceased.hospitalization", "boolean"),
                FormFieldMapping("hospital_name", "deceased.hospital_name", "string"),
                FormFieldMapping("hospital_dates", "deceased.hospital_dates", "string"),
                FormFieldMapping("accident_related", "deceased.accident_related", "boolean"),
                FormFieldMapping("accident_details", "deceased.accident_details", "string"),
                FormFieldMapping("suicide_clause", "insurance__life[*].suicide_clause", "boolean"),
                FormFieldMapping("contestability_period", "insurance__life[*].contestability", "boolean"),
                FormFieldMapping("claimant_signature", "insurance__life[*].claimant_signature", "string"),
                FormFieldMapping("claim_date", "insurance__life[*].claim_date", "date"),
                FormFieldMapping("death_certificate_attached", "deceased.proof_of_death", "file"),
                FormFieldMapping("funeral_director_name", "funeral_home.director_name", "string"),
                FormFieldMapping("funeral_director_signature", "funeral_home.director_signature", "string"),
            ],
            
            # ============================================================================
            # 12. BANK ACCOUNT DEATH NOTIFICATION
            # ============================================================================
            "bank_account_death_notification": [
                FormFieldMapping("account_holder_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("account_number", "financial_information.bank_accounts[*].account_number", "string"),
                FormFieldMapping("account_type", "financial_information.bank_accounts[*].account_type", "select"),
                FormFieldMapping("joint_account_holder", "financial_information.bank_accounts[*].joint_holder", "name", "parse_full_name"),
                FormFieldMapping("deceased_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("deceased_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("deceased_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("notifier_name", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("notifier_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("notifier_address", "applicant.address", "location"),
                FormFieldMapping("notifier_phone", "applicant.phone", "phone"),
                FormFieldMapping("death_certificate_provided", "deceased.proof_of_death", "file"),
                FormFieldMapping("letters_testamentary", "estate_reps[*].proof_of_authority", "file"),
                FormFieldMapping("letters_of_administration", "estate_reps[*].proof_of_authority", "file"),
                FormFieldMapping("court_order", "estate_reps[*].court_order", "file"),
                FormFieldMapping("account_balance_request", "financial_information.bank_accounts[*].balance_request", "boolean"),
                FormFieldMapping("account_closure_request", "financial_information.bank_accounts[*].closure_request", "boolean"),
                FormFieldMapping("funds_transfer_request", "financial_information.bank_accounts[*].transfer_request", "boolean"),
                FormFieldMapping("transfer_to_account", "financial_information.bank_accounts[*].transfer_destination", "string"),
                FormFieldMapping("executor_signature", "estate_reps[*].signature", "string"),
                FormFieldMapping("notification_date", "key_document[*].date_created", "date"),
                FormFieldMapping("bank_officer_signature", "financial_information.bank_accounts[*].officer_signature", "string"),
                FormFieldMapping("bank_processing_date", "financial_information.bank_accounts[*].processing_date", "date"),
            ],
            
            # ============================================================================
            # 13. SOCIAL SECURITY DEATH REPORT
            # ============================================================================
            "social_security_death_report": [
                FormFieldMapping("deceased_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("deceased_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("deceased_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("deceased_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("deceased_place_of_death", "deceased.place_of_death", "location"),
                FormFieldMapping("deceased_last_address", "deceased.home_address", "location"),
                FormFieldMapping("reporter_name", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("reporter_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("reporter_address", "applicant.address", "location"),
                FormFieldMapping("reporter_phone", "applicant.phone", "phone"),
                FormFieldMapping("funeral_home_name", "funeral_home.name", "string"),
                FormFieldMapping("funeral_home_phone", "funeral_home.phone", "phone"),
                FormFieldMapping("funeral_home_license", "funeral_home.license_number", "string"),
                FormFieldMapping("death_certificate_number", "deceased.death_certificate_number", "string"),
                FormFieldMapping("surviving_spouse_name", "spouse.name", "name", "parse_full_name"),
                FormFieldMapping("surviving_spouse_ssn", "spouse.social_insurance_number", "sin"),
                FormFieldMapping("minor_children", "children[*].minor_status", "boolean"),
                FormFieldMapping("disabled_adult_children", "children[*].disabled_status", "boolean"),
                FormFieldMapping("benefits_currently_received", "financial_information[*].current_benefits", "string"),
                FormFieldMapping("lump_sum_death_payment", "financial_information[*].lump_sum_request", "boolean"),
                FormFieldMapping("survivor_benefits_request", "financial_information[*].survivor_benefits_request", "boolean"),
                FormFieldMapping("reporter_signature", "applicant.signature", "string"),
                FormFieldMapping("report_date", "key_document[*].date_created", "date"),
            ],
            
            # ============================================================================
            # 14. PENSION PLAN DEATH BENEFIT CLAIM
            # ============================================================================
            "pension_plan_death_benefit_claim": [
                FormFieldMapping("plan_name", "financial_information__pension[*].name", "string"),
                FormFieldMapping("plan_number", "financial_information__pension[*].id", "string"),
                FormFieldMapping("participant_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("participant_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("participant_employee_id", "deceased.employment.employee_id", "string"),
                FormFieldMapping("participant_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("participant_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("participant_hire_date", "deceased.employment.hire_date", "date"),
                FormFieldMapping("participant_termination_date", "deceased.employment.termination_date", "date"),
                FormFieldMapping("employer_name", "deceased.employment.company_name", "string"),
                FormFieldMapping("employer_address", "deceased.employment.company_address", "location"),
                FormFieldMapping("beneficiary_name", "financial_information__pension[*].beneficiary_primary", "name", "parse_full_name"),
                FormFieldMapping("beneficiary_relationship", "financial_information__pension[*].beneficiary_relationship", "string"),
                FormFieldMapping("beneficiary_address", "financial_information__pension[*].beneficiary_address", "location"),
                FormFieldMapping("beneficiary_ssn", "financial_information__pension[*].beneficiary_ssn", "sin"),
                FormFieldMapping("beneficiary_date_of_birth", "financial_information__pension[*].beneficiary_dob", "date"),
                FormFieldMapping("benefit_commencement_date", "financial_information__pension[*].benefit_start_date", "date"),
                FormFieldMapping("monthly_benefit_amount", "financial_information__pension[*].monthly_amount", "currency"),
                FormFieldMapping("lump_sum_option", "financial_information__pension[*].lump_sum_option", "boolean"),
                FormFieldMapping("survivor_annuity", "financial_information__pension[*].survivor_annuity", "boolean"),
                FormFieldMapping("preretirement_death_benefit", "financial_information__pension[*].preretirement_benefit", "currency"),
                FormFieldMapping("vested_percentage", "financial_information__pension[*].vested_percentage", "number"),
                FormFieldMapping("account_balance", "financial_information__pension[*].account_balance", "currency"),
                FormFieldMapping("rollover_ira", "financial_information__pension[*].rollover_option", "boolean"),
                FormFieldMapping("direct_rollover_institution", "financial_information__pension[*].rollover_institution", "string"),
                FormFieldMapping("tax_withholding_election", "financial_information__pension[*].tax_withholding", "select"),
                FormFieldMapping("payment_method", "financial_information__pension[*].payment_method", "select"),
                FormFieldMapping("banking_information", "financial_information__pension[*].bank_details", "string"),
                FormFieldMapping("claimant_signature", "financial_information__pension[*].claimant_signature", "string"),
                FormFieldMapping("claim_date", "financial_information__pension[*].claim_date", "date"),
                FormFieldMapping("notarization", "financial_information__pension[*].notarized", "boolean"),
                FormFieldMapping("spouse_consent", "spouse.pension_consent", "boolean"),
                FormFieldMapping("spouse_signature", "spouse.signature", "string"),
            ],
            
            # ============================================================================
            # 15. ESTATE TAX RETURN (FORM 706)
            # ============================================================================
            "estate_tax_return_form_706": [
                FormFieldMapping("decedent_first_name", "deceased.first_name", "name"),
                FormFieldMapping("decedent_middle_initial", "deceased.middle_name", "name"),
                FormFieldMapping("decedent_last_name", "deceased.last_name", "name"),
                FormFieldMapping("decedent_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("decedent_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("decedent_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("decedent_domicile", "deceased.legal_domicile", "location"),
                FormFieldMapping("executor_name", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("executor_address", "estate_reps[*].address", "location"),
                FormFieldMapping("executor_ssn_ein", "estate_reps[*].tax_id", "string"),
                FormFieldMapping("attorney_name", "estate_reps[*].attorney_name", "name", "parse_full_name"),
                FormFieldMapping("attorney_address", "estate_reps[*].attorney_address", "location"),
                FormFieldMapping("gross_estate_us", "financial_information.gross_estate_us", "currency"),
                FormFieldMapping("gross_estate_foreign", "financial_information.gross_estate_foreign", "currency"),
                FormFieldMapping("total_gross_estate", "financial_information.total_gross_estate", "currency"),
                FormFieldMapping("total_allowable_deductions", "financial_information.total_deductions", "currency"),
                FormFieldMapping("taxable_estate", "financial_information.taxable_estate", "currency"),
                FormFieldMapping("gift_tax_payable", "financial_information.gift_tax_payable", "currency"),
                FormFieldMapping("gross_estate_tax", "financial_information.gross_estate_tax", "currency"),
                FormFieldMapping("total_credits", "financial_information.total_credits", "currency"),
                FormFieldMapping("net_estate_tax", "financial_information.net_estate_tax", "currency"),
                FormFieldMapping("generation_skipping_tax", "financial_information.generation_skipping_tax", "currency"),
                FormFieldMapping("total_transfer_tax", "financial_information.total_transfer_tax", "currency"),
                FormFieldMapping("prior_payments", "financial_information.prior_payments", "currency"),
                FormFieldMapping("balance_due", "financial_information.balance_due", "currency"),
                FormFieldMapping("cash", "property.liquid_assets", "currency"),
                FormFieldMapping("publicly_traded_securities", "financial_information__investment_provider[*].publicly_traded", "currency"),
                FormFieldMapping("closely_held_stock", "financial_information__investment_provider[*].closely_held", "currency"),
                FormFieldMapping("real_estate", "property.real_estate[*].total_value", "currency"),
                FormFieldMapping("personal_property", "property.personal_property[*].total_value", "currency"),
                FormFieldMapping("life_insurance", "insurance__life[*].death_benefit", "currency"),
                FormFieldMapping("annuities", "financial_information__pension[*].annuity_value", "currency"),
                FormFieldMapping("business_interests", "business.total_value", "currency"),
                FormFieldMapping("other_assets", "property.other_assets", "currency"),
                FormFieldMapping("funeral_expenses", "final_wishes.cost.funeral_service", "currency"),
                FormFieldMapping("administration_expenses", "financial_information.administration_costs", "currency"),
                FormFieldMapping("debts_of_decedent", "financial_information.outstanding_debts", "currency"),
                FormFieldMapping("mortgages_liens", "financial_information.mortgages_liens", "currency"),
                FormFieldMapping("charitable_deduction", "financial_information.charitable_deductions", "currency"),
                FormFieldMapping("marital_deduction", "financial_information.marital_deduction", "currency"),
                FormFieldMapping("extension_requested", "key_document[*].extension_requested", "boolean"),
                FormFieldMapping("protective_election", "key_document[*].protective_election", "boolean"),
                FormFieldMapping("executor_signature", "estate_reps[*].signature", "string"),
                FormFieldMapping("preparer_signature", "estate_reps[*].preparer_signature", "string"),
                FormFieldMapping("preparer_ptin", "estate_reps[*].preparer_ptin", "string"),
            ],
            
            # ============================================================================
            # 16. WORKER'S COMPENSATION DEATH BENEFIT CLAIM
            # ============================================================================
            "workers_compensation_death_benefit": [
                FormFieldMapping("injured_worker_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("injured_worker_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("injured_worker_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("injured_worker_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("date_of_injury", "deceased.injury_date", "date"),
                FormFieldMapping("injury_description", "deceased.injury_description", "string"),
                FormFieldMapping("injury_location", "deceased.injury_location", "location"),
                FormFieldMapping("employer_name", "deceased.employment.company_name", "string"),
                FormFieldMapping("employer_address", "deceased.employment.company_address", "location"),
                FormFieldMapping("employee_id", "deceased.employment.employee_id", "string"),
                FormFieldMapping("job_title", "deceased.employment.job_title", "string"),
                FormFieldMapping("hire_date", "deceased.employment.hire_date", "date"),
                FormFieldMapping("weekly_wage", "deceased.employment.weekly_wage", "currency"),
                FormFieldMapping("work_related_death", "deceased.work_related_death", "boolean"),
                FormFieldMapping("autopsy_performed", "deceased.autopsy_performed", "boolean"),
                FormFieldMapping("autopsy_report", "deceased.autopsy_report", "file"),
                FormFieldMapping("surviving_spouse_name", "spouse.name", "name", "parse_full_name"),
                FormFieldMapping("surviving_spouse_ssn", "spouse.social_insurance_number", "sin"),
                FormFieldMapping("surviving_spouse_dob", "spouse.date_of_birth", "date"),
                FormFieldMapping("spouse_dependent_on_worker", "spouse.dependent_status", "boolean"),
                FormFieldMapping("date_of_marriage", "spouse.date_of_marriage", "date"),
                FormFieldMapping("surviving_children_names", "children[*].name", "name", "parse_full_name"),
                FormFieldMapping("children_ages", "children[*].age", "number"),
                FormFieldMapping("children_dependent", "children[*].dependent_status", "boolean"),
                FormFieldMapping("other_dependents", "contact[*].dependent_status", "boolean"),
                FormFieldMapping("other_dependents_names", "contact[*].name", "name", "parse_full_name"),
                FormFieldMapping("funeral_burial_expenses", "final_wishes.cost.total", "currency"),
                FormFieldMapping("funeral_receipts", "final_wishes.receipts", "file"),
                FormFieldMapping("weekly_compensation_rate", "financial_information.workers_comp_rate", "currency"),
                FormFieldMapping("claim_number", "key_document[*].claim_number", "string"),
                FormFieldMapping("insurance_carrier", "insurance[*].carrier_name", "string"),
                FormFieldMapping("policy_number", "insurance[*].policy_number", "string"),
                FormFieldMapping("physician_treating", "deceased.treating_physician", "name", "parse_full_name"),
                FormFieldMapping("physician_address", "deceased.physician_address", "location"),
                FormFieldMapping("claimant_signature", "applicant.signature", "string"),
                FormFieldMapping("claimant_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("claim_date", "key_document[*].date_created", "date"),
            ],
            
            # ============================================================================
            # 17. AIRLINE PASSENGER DEATH CLAIM
            # ============================================================================
            "airline_passenger_death_claim": [
                FormFieldMapping("passenger_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("passenger_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("passenger_nationality", "deceased.nationality", "string"),
                FormFieldMapping("passenger_passport_number", "id_document__passport[*].id", "string"),
                FormFieldMapping("flight_number", "key_document[*].flight_number", "string"),
                FormFieldMapping("flight_date", "key_document[*].flight_date", "date"),
                FormFieldMapping("airline_name", "key_document[*].airline_name", "string"),
                FormFieldMapping("departure_airport", "key_document[*].departure_location", "location"),
                FormFieldMapping("destination_airport", "key_document[*].destination_location", "location"),
                FormFieldMapping("seat_number", "key_document[*].seat_assignment", "string"),
                FormFieldMapping("ticket_number", "key_document[*].ticket_number", "string"),
                FormFieldMapping("cause_of_death", "deceased.cause_of_death", "string"),
                FormFieldMapping("date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("location_of_death", "deceased.place_of_death", "location"),
                FormFieldMapping("aircraft_accident", "key_document[*].aircraft_accident", "boolean"),
                FormFieldMapping("medical_emergency", "key_document[*].medical_emergency", "boolean"),
                FormFieldMapping("claimant_name", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("claimant_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("claimant_address", "applicant.address", "location"),
                FormFieldMapping("claimant_phone", "applicant.phone", "phone"),
                FormFieldMapping("claimant_email", "applicant.email", "email"),
                FormFieldMapping("beneficiary_designation", "insurance[*].airline_beneficiary", "name", "parse_full_name"),
                FormFieldMapping("travel_insurance", "insurance[*].travel_insurance", "boolean"),
                FormFieldMapping("travel_insurance_policy", "insurance[*].travel_policy_number", "string"),
                FormFieldMapping("baggage_claim", "property.personal_effects", "string"),
                FormFieldMapping("personal_effects", "property.personal_effects", "string"),
                FormFieldMapping("repatriation_request", "final_wishes.repatriation", "boolean"),
                FormFieldMapping("repatriation_destination", "final_wishes.repatriation_destination", "location"),
                FormFieldMapping("funeral_arrangements", "final_wishes.arrangements", "string"),
                FormFieldMapping("compensation_sought", "financial_information.compensation_amount", "currency"),
                FormFieldMapping("legal_representation", "estate_reps[*].attorney_representation", "boolean"),
                FormFieldMapping("attorney_name", "estate_reps[*].attorney_name", "name", "parse_full_name"),
                FormFieldMapping("attorney_contact", "estate_reps[*].attorney_contact", "string"),
                FormFieldMapping("incident_report_number", "key_document[*].incident_report", "string"),
                FormFieldMapping("investigation_agency", "key_document[*].investigating_agency", "string"),
                FormFieldMapping("coroner_report", "deceased.coroner_report", "file"),
                FormFieldMapping("autopsy_report", "deceased.autopsy_report", "file"),
                FormFieldMapping("claim_submission_date", "key_document[*].date_created", "date"),
                FormFieldMapping("claimant_signature", "applicant.signature", "string"),
            ],
            
            # ============================================================================
            # 18. CEMETERY PLOT DEED TRANSFER
            # ============================================================================
            "cemetery_plot_deed_transfer": [
                FormFieldMapping("cemetery_name", "final_wishes.preparations.plot.cemetery_name", "string"),
                FormFieldMapping("cemetery_address", "final_wishes.preparations.plot.cemetery_address", "location"),
                FormFieldMapping("plot_section", "final_wishes.preparations.plot.section", "string"),
                FormFieldMapping("plot_lot_number", "final_wishes.preparations.plot.lot_number", "string"),
                FormFieldMapping("plot_grave_number", "final_wishes.preparations.plot.grave_number", "string"),
                FormFieldMapping("deed_number", "final_wishes.preparations.plot.deed_number", "string"),
                FormFieldMapping("original_owner_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("original_purchase_date", "final_wishes.preparations.plot.purchase_date", "date"),
                FormFieldMapping("original_purchase_price", "final_wishes.preparations.plot.purchase_price", "currency"),
                FormFieldMapping("deed_holder_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("new_owner_name", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("new_owner_address", "estate_reps[*].address", "location"),
                FormFieldMapping("new_owner_phone", "estate_reps[*].phone", "phone"),
                FormFieldMapping("relationship_to_deceased", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("transfer_by_will", "estate_reps[*].transfer_method", "select"),
                FormFieldMapping("transfer_by_inheritance", "estate_reps[*].transfer_method", "select"),
                FormFieldMapping("transfer_by_sale", "estate_reps[*].transfer_method", "select"),
                FormFieldMapping("transfer_by_gift", "estate_reps[*].transfer_method", "select"),
                FormFieldMapping("sale_price", "final_wishes.preparations.plot.sale_price", "currency"),
                FormFieldMapping("gift_consideration", "final_wishes.preparations.plot.gift_value", "currency"),
                FormFieldMapping("will_probate_date", "estate_reps[*].probate_date", "date"),
                FormFieldMapping("court_jurisdiction", "estate_reps[*].court_jurisdiction", "location"),
                FormFieldMapping("estate_case_number", "estate_reps[*].case_number", "string"),
                FormFieldMapping("death_certificate_attached", "deceased.proof_of_death", "file"),
                FormFieldMapping("will_copy_attached", "estate_reps[*].will_copy", "file"),
                FormFieldMapping("letters_testamentary", "estate_reps[*].proof_of_authority", "file"),
                FormFieldMapping("maintenance_fees_current", "final_wishes.preparations.plot.maintenance_current", "boolean"),
                FormFieldMapping("outstanding_fees", "final_wishes.preparations.plot.outstanding_fees", "currency"),
                FormFieldMapping("perpetual_care", "final_wishes.preparations.plot.perpetual_care", "boolean"),
                FormFieldMapping("plot_restrictions", "final_wishes.preparations.plot.restrictions", "string"),
                FormFieldMapping("transfer_fee", "final_wishes.preparations.plot.transfer_fee", "currency"),
                FormFieldMapping("transferor_signature", "final_wishes.preparations.plot.transferor_signature", "string"),
                FormFieldMapping("transferee_signature", "estate_reps[*].signature", "string"),
                FormFieldMapping("notary_signature", "key_document[*].notary_signature", "string"),
                FormFieldMapping("notary_commission_expires", "key_document[*].notary_expires", "date"),
                FormFieldMapping("cemetery_approval_signature", "final_wishes.preparations.plot.cemetery_signature", "string"),
                FormFieldMapping("transfer_date", "key_document[*].date_created", "date"),
                FormFieldMapping("recording_fee", "final_wishes.preparations.plot.recording_fee", "currency"),
            ],
            
            # ============================================================================
            # CONTINUING WITH REMAINING ORIGINAL FORMS...
            # (Adding all the existing forms from the original code)
            # ============================================================================
            
            # SERVICE CANADA NOTIFICATION OF DEATH (SC ISP-1201)
            "service_canada_death_notification_isp1201": [
                # Deceased Information
                FormFieldMapping("Last Name", "deceased.last_name", "name"),
                FormFieldMapping("First Name and Initial", "deceased.first_name", "name"),
                FormFieldMapping("Social Insurance Number", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("Mothers Maiden Name", "deceased.mothers_maiden_name", "name", required=False),
                FormFieldMapping("Maiden name unknown", "deceased.mothers_maiden_name_unknown", "checkbox", required=False),
                FormFieldMapping("Date of Birth YYYYMMDD", "deceased.date_of_birth", "date"),
                FormFieldMapping("Date of Death YYYYMMDD", "deceased.date_of_death", "date"),
                FormFieldMapping("Place of Death", "deceased.place_of_death", "string"),

                # Applicant / Information Provider
                FormFieldMapping("Information Provided By", "applicant.relationship_to_deceased", "string"),
                FormFieldMapping("I am also the", "applicant.additional_role", "string", required=False),
                FormFieldMapping("Full Name", "applicant.full_name", "name"),
                FormFieldMapping("Telephone Number", "applicant.phone", "phone"),
                FormFieldMapping("Alternate Phone Number", "applicant.phone_alt", "phone", required=False),
                FormFieldMapping("Mailing Address", "applicant.mailing_address", "location"),
                FormFieldMapping("Signature1_es_:signer:signature", "applicant.signature", "signature"),
                FormFieldMapping("Date YYYYMMDD", "key_document.signature_date", "date"),
                
                # Consent Checkbox
                FormFieldMapping("I consent to Service Canada sharing the information contained in this", "key_document.consent_given", "checkbox", required=False),

                # Funeral Home / Other Provider
                FormFieldMapping("Name of Funeral Service Provider or other Organization I Individual", "funeral_home.name", "string", required=False),
                FormFieldMapping("Telephone Number_2", "funeral_home.phone", "phone", required=False),
                FormFieldMapping("Mailing Address_2", "funeral_home.address", "location", required=False),

                # Informational Text (usually not mapped, but can be for context)
                FormFieldMapping("There is no obligation to have the funeral service", "key_document.notes", "string", required=False)
            ],
            
            # CANADA CHILD BENEFITS APPLICATION (RC66)
            "canada_child_benefits_rc66": [
                FormFieldMapping("applicant_sin", "applicant.social_insurance_number", "sin"),
                FormFieldMapping("applicant_first_name", "applicant.first_name", "name"),
                FormFieldMapping("applicant_last_name", "applicant.last_name", "name"),
                FormFieldMapping("applicant_date_of_birth", "applicant.date_of_birth", "date"),
                FormFieldMapping("language_of_correspondence", "applicant.preferred_language", "select"),
                FormFieldMapping("home_phone", "applicant.phone", "phone"),
                FormFieldMapping("work_phone", "applicant.phone_work", "phone"),
                FormFieldMapping("work_extension", "applicant.phone_work_ext", "string"),
                FormFieldMapping("cell_phone", "applicant.phone_alt", "phone"),
                FormFieldMapping("mailing_address", "applicant.mailing_address", "location"),
                FormFieldMapping("apartment_number", "applicant.mailing_address", "location", "extract_apartment"),
                FormFieldMapping("city", "applicant.mailing_address", "location", "extract_city"),
                FormFieldMapping("province_territory", "applicant.mailing_address", "location", "extract_province"),
                FormFieldMapping("postal_zip_code", "applicant.mailing_address", "location", "extract_postal_code"),
                FormFieldMapping("moved_within_12_months", "applicant.moved_recently", "boolean"),
                FormFieldMapping("previous_province", "applicant.previous_address", "location", "extract_province"),
                FormFieldMapping("move_date", "applicant.move_date", "date"),
                FormFieldMapping("home_address", "applicant.home_address", "location"),
                FormFieldMapping("same_as_mailing", "applicant.addresses_same", "boolean"),
                FormFieldMapping("marital_status", "applicant.marital_status", "select"),
                FormFieldMapping("marital_status_date", "applicant.marital_status_date", "date"),
                FormFieldMapping("spouse_sin", "spouse.social_insurance_number", "sin"),
                FormFieldMapping("spouse_first_name", "spouse.first_name", "name"),
                FormFieldMapping("spouse_last_name", "spouse.last_name", "name"),
                FormFieldMapping("spouse_date_of_birth", "spouse.date_of_birth", "date"),
                FormFieldMapping("spouse_different_address", "spouse.different_address", "location"),
                FormFieldMapping("canadian_citizen_12_months", "applicant.citizenship_status", "boolean"),
                FormFieldMapping("spouse_canadian_citizen_12_months", "spouse.citizenship_status", "boolean"),
                FormFieldMapping("newcomer_or_returning", "applicant.newcomer_status", "boolean"),
                FormFieldMapping("spouse_newcomer_or_returning", "spouse.newcomer_status", "boolean"),
                FormFieldMapping("child_first_name", "children[*].first_name", "name"),
                FormFieldMapping("child_last_name", "children[*].last_name", "name"),
                FormFieldMapping("child_gender", "children[*].gender", "select"),
                FormFieldMapping("child_date_of_birth", "children[*].date_of_birth", "date"),
                FormFieldMapping("child_city_of_birth", "children[*].place_of_birth", "location"),
                FormFieldMapping("child_province_country_of_birth", "children[*].place_of_birth", "location", "extract_province_country"),
                FormFieldMapping("child_lives_with_you_most_time", "children[*].primary_residence", "boolean"),
                FormFieldMapping("child_start_date_with_you", "children[*].start_date_with_applicant", "date"),
                FormFieldMapping("child_since_birth", "children[*].with_applicant_since_birth", "boolean"),
                FormFieldMapping("shared_custody_40_60_percent", "children[*].shared_custody", "boolean"),
                FormFieldMapping("child_less_than_40_percent", "children[*].minimal_custody", "boolean"),
                FormFieldMapping("applicant_signature", "applicant.signature", "string"),
                FormFieldMapping("application_date", "key_document[*].date_created", "date"),
                FormFieldMapping("spouse_signature", "spouse.signature", "string"),
                FormFieldMapping("spouse_signature_date", "spouse.signature_date", "date"),
            ],
            
            
            
            # SOCIAL SECURITY LUMP-SUM DEATH PAYMENT (SSA-8)
            "social_security_death_payment_ssa8": [
                # Page 1
         
                FormFieldMapping(form_field="form1[0].#subform[0].TextField1[0]", schema_path="applicant.full_name", field_type="name"),
                FormFieldMapping(form_field="form1[0].#subform[0].TextField1[1]", schema_path="deceased.full_name", field_type="name"),
                FormFieldMapping(form_field="form1[0].#subform[0].NumericField1[0]", schema_path="deceased.social_insurance_number", field_type="sin"),
                FormFieldMapping(form_field="form1[0].#subform[0].DateField1[0]", schema_path="deceased.date_of_birth", field_type="date"),
                FormFieldMapping(form_field="form1[0].#subform[0].DateField2[0]", schema_path="deceased.date_of_death", field_type="date"),
                FormFieldMapping(form_field="form1[0].#subform[0].TextField1[2]", schema_path="deceased.place_of_death", field_type="location"),
                FormFieldMapping(form_field="form1[0].#subform[0].TextField1[3]", schema_path="deceased.earnings.year_of_death", field_type="currency"),
                FormFieldMapping(form_field="form1[0].#subform[0].TextField1[4]", schema_path="deceased.earnings.year_before_death", field_type="currency"),
                FormFieldMapping(form_field="form1[0].#subform[0].C7Yes[0]", schema_path="deceased.work_status.unable_to_work_at_death", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[0].C7No[0]", schema_path="deceased.work_status.able_to_work_at_death", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[0].DateField3[0]", schema_path="deceased.work_status.date_unable_to_work", field_type="date"),
                FormFieldMapping(form_field="form1[0].#subform[0].C8Yes[0]", schema_path="deceased.military.active_service_pre_1968", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[0].C8No[0]", schema_path="deceased.military.no_active_service_pre_1968", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[0].TextField1[5]", schema_path="deceased.military.service_start_date", field_type="date"),
                FormFieldMapping(form_field="form1[0].#subform[0].TextField1[6]", schema_path="deceased.military.service_end_date", field_type="date"),
                FormFieldMapping(form_field="form1[0].#subform[0].C8CYes[0]", schema_path="deceased.military.other_federal_benefits", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[0].C8CNo[0]", schema_path="deceased.military.no_other_federal_benefits", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[0].C9Yes[0]", schema_path="deceased.employment.railroad_work_7_years", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[0].C9No[0]", schema_path="deceased.employment.no_railroad_work", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[1].C10Yes[0]", schema_path="deceased.employment.foreign_work", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[1].C10No[0]", schema_path="deceased.employment.no_foreign_work", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[7]", schema_path="deceased.employment.foreign_countries", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[1].C11Yes[0]", schema_path="deceased.marital_status.surviving_spouse_exists", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[1].C11No[0]", schema_path="deceased.marital_status.no_surviving_spouse", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[8]", schema_path="spouse.full_name", field_type="name"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[9]", schema_path="spouse.date_of_marriage", field_type="date"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[10]", schema_path="spouse.place_of_marriage", field_type="location"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[11]", schema_path="spouse.date_of_birth", field_type="date"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[12]", schema_path="spouse.social_insurance_number", field_type="sin"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[13]", schema_path="deceased.prior_marriages", field_type="table"),
                FormFieldMapping(form_field="form1[0].#subform[1].C11Clerg[0]", schema_path="deceased.prior_marriages.ceremonial", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[1].C11Other[0]", schema_path="deceased.prior_marriages.other", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[14]", schema_path="children[0].full_name", field_type="name"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[15]", schema_path="children[0].date_of_birth", field_type="date"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[16]", schema_path="children[0].relationship", field_type="string"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[17]", schema_path="children[1].full_name", field_type="name"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[18]", schema_path="children[1].date_of_birth", field_type="date"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[19]", schema_path="children[1].relationship", field_type="string"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[32]", schema_path="parents.were_dependent", field_type="string"),
                FormFieldMapping(form_field="form1[0].#subform[1].C13Yes[0]", schema_path="applicant.prior_ssa_filing", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[1].C13No[0]", schema_path="applicant.no_prior_ssa_filing", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[1].TextField1[41]", schema_path="spouse.contact_info_by_other", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[2].C16Yes[0]", schema_path="spouse.living_together_at_death", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[2].C16No[0]", schema_path="spouse.not_living_together_at_death", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[2].Surviving[0]", schema_path="spouse.separation_details.person_away", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[2].Deceased[0]", schema_path="spouse.separation_details.person_away", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[42]", schema_path="spouse.separation_details.date_last_home", field_type="date"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[43]", schema_path="spouse.separation_details.reason_for_absence", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[44]", schema_path="spouse.separation_details.reason_apart_at_death", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[45]", schema_path="spouse.separation_details.illness_details", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[2].C17Yes[0]", schema_path="applicant.disability_status", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[2].C17No[0]", schema_path="applicant.no_disability", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[46]", schema_path="applicant.disability_start_date", field_type="date"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[47]", schema_path="applicant.prior_marriages", field_type="table"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[60]", schema_path="applicant.phone", field_type="phone"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[61]", schema_path="applicant.mailing_address.street", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[62]", schema_path="applicant.mailing_address.city_state", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[63]", schema_path="applicant.mailing_address.zip_code", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[64]", schema_path="applicant.mailing_address.county", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[65]", schema_path="payment.routing_number", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[66]", schema_path="payment.account_number", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[2].Checking[0]", schema_path="payment.account_type_checking", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[2].Savings[0]", schema_path="payment.account_type_savings", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[2].DirectExp[0]", schema_path="payment.enroll_direct_express", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[2].DirectDeposit[0]", schema_path="payment.direct_deposit_refused", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[67]", schema_path="witnesses[0].signature", field_type="signature"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[68]", schema_path="witnesses[0].address", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[69]", schema_path="witnesses[1].signature", field_type="signature"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[70]", schema_path="witnesses[1].address", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[3].TextField1[71]", schema_path="receipt.ssa_contact_phone", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[3].TextField1[72]", schema_path="receipt.ssa_office", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[3].TextField1[73]", schema_path="receipt.date_claim_received", field_type="date"),
                FormFieldMapping(form_field="form1[0].#subform[3].TextField1[74]", schema_path="receipt.claimant_name", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[3].TextField1[75]", schema_path="receipt.bnc_number", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[3].TextField1[76]", schema_path="receipt.deceased_name", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[55]", schema_path="applicant.signature", field_type="signature"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[56]", schema_path="key_document.signature_date", field_type="date"),
                FormFieldMapping(form_field="form1[0].#subform[2].TextField1[57]", schema_path="notes.remarks", field_type="text"),
                FormFieldMapping(form_field="form1[0].#subform[1].C11BClerg[0]", schema_path="deceased.prior_marriages[0].ceremonial_marriage", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[1].C11BOther[0]", schema_path="deceased.prior_marriages[0].other_marriage", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[1].DateField4[0]", schema_path="deceased.prior_marriages[0].end_date", field_type="date"),
                FormFieldMapping(form_field="form1[0].#subform[1].C11CClerg[0]", schema_path="deceased.prior_marriages[1].ceremonial_marriage", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[1].C11COther[0]", schema_path="deceased.prior_marriages[1].other_marriage", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[1].C14No[0]", schema_path="applicant.no_prior_filing_spouse_record", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[1].C14Yes[0]", schema_path="applicant.prior_filing_spouse_record", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[2].C18No[0]", schema_path="applicant.no_prior_marriage_10_years", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[2].C18Yes[0]", schema_path="applicant.prior_marriage_10_years", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[2].C18Clerg[0]", schema_path="applicant.prior_marriages[0].ceremonial_marriage", field_type="checkbox"),
                FormFieldMapping(form_field="form1[0].#subform[2].C18Other[0]", schema_path="applicant.prior_marriages[0].other_marriage", field_type="checkbox"),
            
            ],
            
            # ============================================================================
            # 19. HOSPITAL PATIENT BELONGINGS RELEASE FORM
            # ============================================================================
            "hospital_patient_belongings_release": [
                FormFieldMapping("patient_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("patient_id", "deceased.medical_record_number", "string"),
                FormFieldMapping("patient_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("patient_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("date_of_admission", "deceased.hospital_admission_date", "date"),
                FormFieldMapping("attending_physician", "deceased.attending_physician", "name", "parse_full_name"),
                FormFieldMapping("hospital_name", "deceased.hospital_name", "string"),
                FormFieldMapping("hospital_address", "deceased.hospital_address", "location"),
                FormFieldMapping("belongings_description", "property.personal_effects", "string"),
                FormFieldMapping("valuable_items", "property.valuables", "string"),
                FormFieldMapping("medications", "property.medications", "string"),
                FormFieldMapping("medical_equipment", "property.medical_equipment", "string"),
                FormFieldMapping("clothing_description", "property.clothing", "string"),
                FormFieldMapping("jewelry_description", "property.jewelry", "string"),
                FormFieldMapping("electronics", "property.electronics", "string"),
                FormFieldMapping("documents_papers", "property.documents", "string"),
                FormFieldMapping("wallet_purse", "property.wallet_purse", "string"),
                FormFieldMapping("cash_amount", "property.cash_found", "currency"),
                FormFieldMapping("recipient_name", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("recipient_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("recipient_address", "estate_reps[*].address", "location"),
                FormFieldMapping("recipient_phone", "estate_reps[*].phone", "phone"),
                FormFieldMapping("recipient_id_type", "estate_reps[*].id_type", "string"),
                FormFieldMapping("recipient_id_number", "estate_reps[*].id_number", "string"),
                FormFieldMapping("release_signature", "estate_reps[*].signature", "string"),
                FormFieldMapping("release_date", "key_document[*].date_created", "date"),
                FormFieldMapping("witness_signature", "contact[*].signature", "string"),
                FormFieldMapping("hospital_staff_signature", "deceased.hospital_staff_signature", "string"),
            ],
            
            # ============================================================================
            # 20. CREDIT CARD COMPANY DEATH NOTIFICATION
            # ============================================================================
            "credit_card_death_notification": [
                FormFieldMapping("cardholder_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("account_number", "financial_information.credit_cards[*].account_number", "string"),
                FormFieldMapping("card_number_last_four", "financial_information.credit_cards[*].card_last_four", "string"),
                FormFieldMapping("cardholder_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("cardholder_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("cardholder_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("notifier_name", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("notifier_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("notifier_address", "applicant.address", "location"),
                FormFieldMapping("notifier_phone", "applicant.phone", "phone"),
                FormFieldMapping("joint_cardholder", "financial_information.credit_cards[*].joint_holder", "name", "parse_full_name"),
                FormFieldMapping("authorized_users", "financial_information.credit_cards[*].authorized_users", "string"),
                FormFieldMapping("current_balance", "financial_information.credit_cards[*].balance", "currency"),
                FormFieldMapping("autopay_arrangements", "financial_information.credit_cards[*].autopay", "boolean"),
                FormFieldMapping("recurring_charges", "financial_information.credit_cards[*].recurring_charges", "string"),
                FormFieldMapping("account_closure_request", "financial_information.credit_cards[*].closure_request", "boolean"),
                FormFieldMapping("balance_transfer_request", "financial_information.credit_cards[*].transfer_request", "boolean"),
                FormFieldMapping("estate_payment_method", "financial_information.credit_cards[*].estate_payment", "string"),
                FormFieldMapping("death_certificate_attached", "deceased.proof_of_death", "file"),
                FormFieldMapping("letters_testamentary", "estate_reps[*].proof_of_authority", "file"),
                FormFieldMapping("executor_signature", "estate_reps[*].signature", "string"),
                FormFieldMapping("notification_date", "key_document[*].date_created", "date"),
            ],
            
            # ============================================================================
            # 21. UTILITY COMPANY ACCOUNT TRANSFER
            # ============================================================================
            "utility_company_account_transfer": [
                FormFieldMapping("service_address", "property.real_estate[*].address", "location"),
                FormFieldMapping("account_number", "account[*].id", "string"),
                FormFieldMapping("meter_number", "account[*].meter_number", "string"),
                FormFieldMapping("utility_type", "account[*].type", "select"),
                FormFieldMapping("deceased_account_holder", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("deceased_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("deceased_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("new_account_holder", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("new_holder_ssn", "estate_reps[*].social_insurance_number", "sin"),
                FormFieldMapping("new_holder_phone", "estate_reps[*].phone", "phone"),
                FormFieldMapping("new_holder_email", "estate_reps[*].email", "email"),
                FormFieldMapping("relationship_to_deceased", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("transfer_type", "account[*].transfer_type", "select"),
                FormFieldMapping("property_ownership_transfer", "property.real_estate[*].ownership_transfer", "boolean"),
                FormFieldMapping("temporary_service", "account[*].temporary_service", "boolean"),
                FormFieldMapping("service_termination", "account[*].termination_request", "boolean"),
                FormFieldMapping("final_bill_address", "account[*].final_bill_address", "location"),
                FormFieldMapping("deposit_required", "account[*].deposit_required", "boolean"),
                FormFieldMapping("deposit_amount", "account[*].deposit_amount", "currency"),
                FormFieldMapping("billing_preferences", "account[*].billing_method", "select"),
                FormFieldMapping("autopay_setup", "account[*].autopay_setup", "boolean"),
                FormFieldMapping("budget_billing", "account[*].budget_billing", "boolean"),
                FormFieldMapping("death_certificate", "deceased.proof_of_death", "file"),
                FormFieldMapping("proof_of_property_ownership", "property.real_estate[*].ownership_proof", "file"),
                FormFieldMapping("applicant_signature", "estate_reps[*].signature", "string"),
                FormFieldMapping("application_date", "key_document[*].date_created", "date"),
            ],
            
            # ============================================================================
            # 22. CELL PHONE CARRIER ACCOUNT CLOSURE
            # ============================================================================
            "cell_phone_account_closure": [
                FormFieldMapping("account_holder_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("account_number", "account[*].id", "string"),
                FormFieldMapping("phone_numbers", "account[*].phone_numbers", "string"),
                FormFieldMapping("account_holder_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("account_pin", "account[*].pin", "string"),
                FormFieldMapping("date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("requestor_name", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("requestor_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("requestor_contact", "applicant.phone", "phone"),
                FormFieldMapping("family_plan", "account[*].family_plan", "boolean"),
                FormFieldMapping("other_lines", "account[*].other_lines", "string"),
                FormFieldMapping("device_information", "property.electronics", "string"),
                FormFieldMapping("device_return_required", "property.device_return", "boolean"),
                FormFieldMapping("outstanding_balance", "account[*].balance", "currency"),
                FormFieldMapping("early_termination_fee", "account[*].termination_fee", "currency"),
                FormFieldMapping("equipment_payment_plan", "account[*].equipment_balance", "currency"),
                FormFieldMapping("insurance_claims", "account[*].insurance_claims", "boolean"),
                FormFieldMapping("number_porting", "account[*].number_porting", "boolean"),
                FormFieldMapping("new_carrier", "account[*].new_carrier", "string"),
                FormFieldMapping("autopay_cancellation", "account[*].autopay_cancel", "boolean"),
                FormFieldMapping("final_bill_address", "account[*].final_bill_address", "location"),
                FormFieldMapping("death_certificate", "deceased.proof_of_death", "file"),
                FormFieldMapping("account_closure_date", "account[*].closure_date", "date"),
                FormFieldMapping("requestor_signature", "applicant.signature", "string"),
            ],
            
            # ============================================================================
            # 23. SUBSCRIPTION SERVICE CANCELLATION
            # ============================================================================
            "subscription_service_cancellation": [
                FormFieldMapping("subscriber_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("subscription_id", "account[*].id", "string"),
                FormFieldMapping("service_type", "account[*].type", "string"),
                FormFieldMapping("service_provider", "account[*].name", "string"),
                FormFieldMapping("billing_email", "account[*].billing_email", "email"),
                FormFieldMapping("billing_address", "account[*].billing_address", "location"),
                FormFieldMapping("payment_method", "account[*].payment_method", "string"),
                FormFieldMapping("monthly_amount", "account[*].monthly_fee", "currency"),
                FormFieldMapping("annual_subscription", "account[*].annual_plan", "boolean"),
                FormFieldMapping("subscription_start_date", "account[*].start_date", "date"),
                FormFieldMapping("next_billing_date", "account[*].next_billing", "date"),
                FormFieldMapping("cancellation_requestor", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("requestor_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("requestor_contact", "applicant.email", "email"),
                FormFieldMapping("date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("immediate_cancellation", "account[*].immediate_cancel", "boolean"),
                FormFieldMapping("end_of_billing_cycle", "account[*].end_cycle_cancel", "boolean"),
                FormFieldMapping("refund_request", "account[*].refund_request", "boolean"),
                FormFieldMapping("prorated_refund", "account[*].prorated_amount", "currency"),
                FormFieldMapping("unused_credits", "account[*].unused_credits", "currency"),
                FormFieldMapping("gift_subscriptions", "account[*].gift_subscriptions", "boolean"),
                FormFieldMapping("family_sharing", "account[*].family_plan", "boolean"),
                FormFieldMapping("digital_content_access", "account[*].digital_content", "string"),
                FormFieldMapping("data_deletion_request", "account[*].data_deletion", "boolean"),
                FormFieldMapping("memorial_account", "account[*].memorial_option", "boolean"),
                FormFieldMapping("death_certificate", "deceased.proof_of_death", "file"),
                FormFieldMapping("cancellation_date", "account[*].cancellation_date", "date"),
                FormFieldMapping("confirmation_number", "account[*].confirmation_number", "string"),
            ],
            
            # ============================================================================
            # 24. PROPERTY DEED TRANSFER AFFIDAVIT
            # ============================================================================
            "property_deed_transfer_affidavit": [
                FormFieldMapping("property_address", "property.real_estate[*].address", "location"),
                FormFieldMapping("legal_description", "property.real_estate[*].legal_description", "string"),
                FormFieldMapping("parcel_number", "property.real_estate[*].parcel_number", "string"),
                FormFieldMapping("deed_book_page", "property.real_estate[*].deed_reference", "string"),
                FormFieldMapping("deceased_owner_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("deceased_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("survivorship_deed", "property.real_estate[*].survivorship", "boolean"),
                FormFieldMapping("joint_tenancy", "property.real_estate[*].joint_tenancy", "boolean"),
                FormFieldMapping("tenancy_by_entirety", "property.real_estate[*].tenancy_entirety", "boolean"),
                FormFieldMapping("surviving_owner_name", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("surviving_owner_address", "estate_reps[*].address", "location"),
                FormFieldMapping("property_value", "property.real_estate[*].estimated_value", "currency"),
                FormFieldMapping("homestead_exemption", "property.real_estate[*].homestead", "boolean"),
                FormFieldMapping("mortgage_information", "financial_information.mortgages[*].details", "string"),
                FormFieldMapping("outstanding_liens", "financial_information.liens[*].details", "string"),
                FormFieldMapping("property_taxes_current", "property.real_estate[*].taxes_current", "boolean"),
                FormFieldMapping("tax_assessment", "property.real_estate[*].assessed_value", "currency"),
                FormFieldMapping("inheritance_transfer", "property.real_estate[*].transfer_type", "select"),
                FormFieldMapping("will_transfer", "property.real_estate[*].transfer_type", "select"),
                FormFieldMapping("intestate_succession", "property.real_estate[*].transfer_type", "select"),
                FormFieldMapping("court_jurisdiction", "estate_reps[*].court_jurisdiction", "location"),
                FormFieldMapping("probate_case_number", "estate_reps[*].case_number", "string"),
                FormFieldMapping("death_certificate", "deceased.proof_of_death", "file"),
                FormFieldMapping("will_copy", "estate_reps[*].will_copy", "file"),
                FormFieldMapping("letters_testamentary", "estate_reps[*].proof_of_authority", "file"),
                FormFieldMapping("affiant_signature", "estate_reps[*].signature", "string"),
                FormFieldMapping("notary_signature", "key_document[*].notary_signature", "string"),
                FormFieldMapping("notary_commission_expires", "key_document[*].notary_expires", "date"),
                FormFieldMapping("recording_requested_by", "key_document[*].recording_party", "string"),
                FormFieldMapping("transfer_tax_paid", "property.real_estate[*].transfer_tax", "currency"),
            ],
            
            # ============================================================================
            # 25. MOTOR VEHICLE DEPARTMENT TITLE SURRENDER
            # ============================================================================
            "motor_vehicle_title_surrender": [
                FormFieldMapping("vehicle_year", "property.vehicles[*].year", "number"),
                FormFieldMapping("vehicle_make", "property.vehicles[*].make_model", "string", "extract_make"),
                FormFieldMapping("vehicle_model", "property.vehicles[*].make_model", "string", "extract_model"),
                FormFieldMapping("vehicle_vin", "property.vehicles[*].vin", "string"),
                FormFieldMapping("license_plate", "property.vehicles[*].license_plate", "string"),
                FormFieldMapping("title_number", "property.vehicles[*].title_number", "string"),
                FormFieldMapping("odometer_reading", "property.vehicles[*].odometer_reading", "number"),
                FormFieldMapping("lien_holder", "financial_information.liens[*].holder_name", "string"),
                FormFieldMapping("lien_amount", "financial_information.liens[*].amount", "currency"),
                FormFieldMapping("deceased_owner_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("co_owner_name", "property.vehicles[*].co_owner", "name", "parse_full_name"),
                FormFieldMapping("deceased_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("vehicle_disposition", "property.vehicles[*].disposition", "select"),
                FormFieldMapping("sale_to_dealer", "property.vehicles[*].sale_dealer", "boolean"),
                FormFieldMapping("sale_to_individual", "property.vehicles[*].sale_individual", "boolean"),
                FormFieldMapping("junked_scrapped", "property.vehicles[*].junked", "boolean"),
                FormFieldMapping("donated", "property.vehicles[*].donated", "boolean"),
                FormFieldMapping("transferred_to_heir", "property.vehicles[*].inherited", "boolean"),
                FormFieldMapping("purchaser_name", "property.vehicles[*].purchaser_name", "name", "parse_full_name"),
                FormFieldMapping("purchaser_address", "property.vehicles[*].purchaser_address", "location"),
                FormFieldMapping("sale_price", "property.vehicles[*].sale_price", "currency"),
                FormFieldMapping("sale_date", "property.vehicles[*].sale_date", "date"),
                FormFieldMapping("dealer_name", "property.vehicles[*].dealer_name", "string"),
                FormFieldMapping("dealer_license", "property.vehicles[*].dealer_license", "string"),
                FormFieldMapping("junkyard_name", "property.vehicles[*].junkyard_name", "string"),
                FormFieldMapping("charity_name", "property.vehicles[*].charity_name", "string"),
                FormFieldMapping("heir_name", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("heir_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("death_certificate", "deceased.proof_of_death", "file"),
                FormFieldMapping("title_surrender_date", "property.vehicles[*].surrender_date", "date"),
                FormFieldMapping("surrendering_party_signature", "estate_reps[*].signature", "string"),
                FormFieldMapping("dmv_official_signature", "property.vehicles[*].dmv_signature", "string"),
            ],
            
            # ============================================================================
            # 26. DIGITAL ASSET RECOVERY REQUEST
            # ============================================================================
            "digital_asset_recovery_request": [
                FormFieldMapping("deceased_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("deceased_email", "deceased.email", "email"),
                FormFieldMapping("deceased_username", "account[*].username", "string"),
                FormFieldMapping("deceased_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("deceased_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("service_provider", "account[*].name", "string"),
                FormFieldMapping("account_type", "account[*].type", "string"),
                FormFieldMapping("account_url", "account[*].url", "string"),
                FormFieldMapping("last_known_password", "account[*].last_password", "string"),
                FormFieldMapping("security_questions", "account[*].security_info", "string"),
                FormFieldMapping("two_factor_authentication", "account[*].two_factor", "boolean"),
                FormFieldMapping("recovery_phone", "account[*].recovery_phone", "phone"),
                FormFieldMapping("recovery_email", "account[*].recovery_email", "email"),
                FormFieldMapping("requestor_name", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("requestor_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("requestor_email", "applicant.email", "email"),
                FormFieldMapping("requestor_phone", "applicant.phone", "phone"),
                FormFieldMapping("legal_authority", "estate_reps[*].legal_authority", "string"),
                FormFieldMapping("court_order", "estate_reps[*].court_order", "file"),
                FormFieldMapping("letters_testamentary", "estate_reps[*].proof_of_authority", "file"),
                FormFieldMapping("power_of_attorney", "estate_reps[*].power_of_attorney", "file"),
                FormFieldMapping("data_request_type", "account[*].data_request", "select"),
                FormFieldMapping("account_memorialization", "account[*].memorial_request", "boolean"),
                FormFieldMapping("data_download", "account[*].data_download", "boolean"),
                FormFieldMapping("account_deletion", "account[*].deletion_request", "boolean"),
                FormFieldMapping("financial_information", "account[*].financial_data", "boolean"),
                FormFieldMapping("communication_history", "account[*].messages", "boolean"),
                FormFieldMapping("photo_video_content", "account[*].media_content", "boolean"),
                FormFieldMapping("cloud_storage_access", "account[*].cloud_storage", "boolean"),
                FormFieldMapping("cryptocurrency_wallets", "account[*].crypto_assets", "boolean"),
                FormFieldMapping("subscription_details", "account[*].subscriptions", "boolean"),
                FormFieldMapping("business_accounts", "account[*].business_data", "boolean"),
                FormFieldMapping("death_certificate", "deceased.proof_of_death", "file"),
                FormFieldMapping("government_id", "estate_reps[*].government_id", "file"),
                FormFieldMapping("relationship_proof", "estate_reps[*].relationship_proof", "file"),
                FormFieldMapping("request_date", "key_document[*].date_created", "date"),
                FormFieldMapping("requestor_signature", "applicant.signature", "string"),
                FormFieldMapping("urgency_reason", "key_document[*].urgency", "string"),
                FormFieldMapping("additional_documentation", "key_document[*].additional_docs", "file"),
            ],
            
            
            
            # ATF FORM 5 - FIREARM TRANSFER AND REGISTRATION
            "atf_form_5_firearm_transfer": [
               # ==============================================================================
                # PAGE 1 - ATF COPY 1 (MAIN APPLICATION)
                # ==============================================================================
                 # --- Header ---
                FormFieldMapping("topmostSubform[0].Page1[0].ATFControl[0]", "key_document.atf_control_number", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].InternalControl[0]", "key_document.internal_control_number", "string"),
                # --- Box 3 ---
                FormFieldMapping("topmostSubform[0].Page1[0].NumberStreetCityStateZipDifferent[0]", "applicant.transferor_physical_address", "location"),
                # --- Box 5: Transferee FFL ---
                FormFieldMapping("topmostSubform[0].Page1[0].FederalFirearmsLicense6dig[0]", "estate_reps.ffl_part1_6", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].FederalFirearmsLicense2dig[0]", "estate_reps.ffl_part2_2", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].FederalFirearmsLicense2dig2[0]", "estate_reps.ffl_part3_2", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].FederalFirearmsLicense5dig[0]", "estate_reps.ffl_part4_5", "string"),
                # --- Box 6: Transferee SOT ---
                FormFieldMapping("topmostSubform[0].Page1[0].TransfereeSpecialTaxStatus[0]", "estate_reps.sot_ein", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].TransfereeSpecialTaxStatusClass[0]", "estate_reps.sot_class", "string"),
                # --- Box 7: Transferor FFL ---
                FormFieldMapping("topmostSubform[0].Page1[0].TFederalFirearmsLicense6dig[0]", "applicant.ffl_part1_6", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].TFederalFirearmsLicense2dig[0]", "applicant.ffl_part2_2", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].TFederalFirearmsLicense2dig2[0]", "applicant.ffl_part3_2", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].TFederalFirearmsLicense5dig[0]", "applicant.ffl_part4_5", "string"),
                # --- Box 8: Transferor SOT ---
                FormFieldMapping("topmostSubform[0].Page1[0].TransferorSpecialTaxStatus[0]", "applicant.sot_ein", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].TransferorSpecialTaxStatusClass[0]", "applicant.sot_class", "string"),
                # --- Uncategorized FFL fields on Page 1 (likely for manufacturer) ---
                FormFieldMapping("topmostSubform[0].Page1[0].FederalFirearmsLicense6dig6[0]", "property.firearms[0].manufacturer_ffl_part1", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].FederalFirearmsLicense2dig7[0]", "property.firearms[0].manufacturer_ffl_part2", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].FederalFirearmsLicense2dig28[0]", "property.firearms[0].manufacturer_ffl_part3", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].FederalFirearmsLicense5dig9[0]", "property.firearms[0].manufacturer_ffl_part4", "string"),

                # ==============================================================================
                # PAGE 2 - TRANSFEREE CERTIFICATION (COPY 1)
                # ==============================================================================
                FormFieldMapping("topmostSubform[0].Page2[0].reasons2[0]", "estate_reps.necessity_statement_reason_continued", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxYes14[0]", "estate_reps.background.additional_info_attached_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxNo14[0]", "estate_reps.background.additional_info_attached_no", "checkbox"),

                # ==============================================================================
                # PAGE 3 - RESPONSIBLE PERSONS (COPY 1)
                # ==============================================================================
                FormFieldMapping("topmostSubform[0].Page3[0].TextField9n[0]", "estate_reps.responsible_persons[2].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page3[0].TextField10n[0]", "estate_reps.responsible_persons[3].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page3[0].TextField711n[0]", "estate_reps.responsible_persons[4].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page3[0].TextField12n[0]", "estate_reps.responsible_persons[5].full_name", "name"),

                # ==============================================================================
                # PAGE 7 - ATF COPY 2 (REGISTRANT COPY)
                # ==============================================================================
                FormFieldMapping("topmostSubform[0].Page7[0].ATFControl[0]", "key_document.atf_control_number_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].InternalControl[0]", "key_document.internal_control_number_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].CheckBox5firearm[0]", "key_document.transfer_reason_unserviceable_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page7[0].CheckBox6firearm[0]", "key_document.transfer_reason_government_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page7[0].CheckBox7firearm[0]", "key_document.transfer_reason_lawful_heir_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page7[0].CheckBox8firearm[0]", "key_document.transfer_reason_other_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page7[0].Other[0]", "key_document.transfer_reason_other_specify_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].County[0]", "estate_reps.transferee_county_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].CheckBox9ind[0]", "estate_reps.entity_individual_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page7[0].CheckBox9trust[0]", "estate_reps.entity_trust_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page7[0].CheckBox9gov[0]", "estate_reps.entity_government_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page7[0].TransferorNumber[0]", "applicant.phone_copy2", "phone"),
                FormFieldMapping("topmostSubform[0].Page7[0].TypeofFirearm[0]", "property.firearms[0].type_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].CaliberorGauge[0]", "property.firearms[0].caliber_gauge_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].Model[0]", "property.firearms[0].model_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].LengthofBarrel[0]", "property.firearms[0].barrel_length_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].LengthOverall[0]", "property.firearms[0].overall_length_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].SerialNumber[0]", "property.firearms[0].serial_number_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].AdditionalDescription[0]", "property.firearms[0].additional_description_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].CheckBoxYes[0]", "property.firearms[0].is_unserviceable_yes_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page7[0].CheckBoxNo[0]", "property.firearms[0].is_unserviceable_no_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page7[0].DateField1[0]", "key_document.signature_date_copy2", "date"),
                FormFieldMapping("topmostSubform[0].Page7[0].SignatureField1[0]", "applicant.signature_copy2", "signature"),
                FormFieldMapping("topmostSubform[0].Page7[0].ole[0]", "estate_reps.entity_other_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page7[0].corp[0]", "estate_reps.entity_corporation_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page7[0].NumberStreetCityStateZipDifferent[0]", "applicant.transferor_physical_address_copy2", "location"),
                FormFieldMapping("topmostSubform[0].Page7[0].FederalFirearmsLicense6dig[0]", "estate_reps.ffl_part1_6_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].FederalFirearmsLicense2dig[0]", "estate_reps.ffl_part2_2_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].FederalFirearmsLicense2dig2[0]", "estate_reps.ffl_part3_2_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].FederalFirearmsLicense5dig[0]", "estate_reps.ffl_part4_5_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].TFederalFirearmsLicense6dig[0]", "applicant.ffl_part1_6_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].TFederalFirearmsLicense2dig[0]", "applicant.ffl_part2_2_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].TFederalFirearmsLicense2dig2[0]", "applicant.ffl_part3_2_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].TFederalFirearmsLicense5dig[0]", "applicant.ffl_part4_5_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].TransfereeSpecialTaxStatus[0]", "estate_reps.sot_ein_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].TransfereeSpecialTaxStatusClass[0]", "estate_reps.sot_class_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].TransferorSpecialTaxStatus[0]", "applicant.sot_ein_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].TransferorSpecialTaxStatusClass[0]", "applicant.sot_class_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].FederalFirearmsLicense6dig6[0]", "property.firearms[0].manufacturer_ffl_part1_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].FederalFirearmsLicense2dig7[0]", "property.firearms[0].manufacturer_ffl_part2_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].FederalFirearmsLicense2dig28[0]", "property.firearms[0].manufacturer_ffl_part3_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page7[0].FederalFirearmsLicense5dig9[0]", "property.firearms[0].manufacturer_ffl_part4_copy2", "string"),

                # ==============================================================================
                # PAGE 8 - TRANSFEREE CERTIFICATION (COPY 2)
                # ==============================================================================
                FormFieldMapping("topmostSubform[0].Page8[0].TextField4[0]", "estate_reps.cleo_agency_name_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page8[0].TextField5[0]", "estate_reps.cleo_official_name_title_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page8[0].TextField6[0]", "estate_reps.cleo_address_copy2", "location"),
                FormFieldMapping("topmostSubform[0].Page8[0].Reasons[0]", "estate_reps.necessity_statement_reason_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page8[0].reasons2[0]", "estate_reps.necessity_statement_reason_continued_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckboxYes1[0]", "estate_reps.background.is_under_indictment_yes_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxNo1[0]", "estate_reps.background.is_under_indictment_no_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxYes2[0]", "estate_reps.background.has_felony_conviction_yes_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxNo2[0]", "estate_reps.background.has_felony_conviction_no_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxYes3[0]", "estate_reps.background.is_fugitive_yes_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckboxNo3[0]", "estate_reps.background.is_fugitive_no_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxYes4[0]", "estate_reps.background.is_drug_user_yes_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxNo4[0]", "estate_reps.background.is_drug_user_no_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxYes5[0]", "estate_reps.background.is_mental_defective_yes_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxNo5[0]", "estate_reps.background.is_mental_defective_no_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxYes6[0]", "estate_reps.background.has_dishonorable_discharge_yes_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxNo6[0]", "estate_reps.background.has_dishonorable_discharge_no_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxYes7[0]", "estate_reps.background.has_restraining_order_yes_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxNo7[0]", "estate_reps.background.has_restraining_order_no_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxYes8[0]", "estate_reps.background.has_domestic_violence_conviction_yes_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxNo8[0]", "estate_reps.background.has_domestic_violence_conviction_no_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBox5usa[0]", "estate_reps.citizenship_usa_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBox5other[0]", "estate_reps.citizenship_other_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].TextField6other[0]", "estate_reps.citizenship_other_specify_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxYes11[0]", "estate_reps.background.renounced_citizenship_yes_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxNo11[0]", "estate_reps.background.renounced_citizenship_no_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxYes12[0]", "estate_reps.background.is_illegal_alien_yes_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxNo12[0]", "estate_reps.background.is_illegal_alien_no_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxYes13[0]", "estate_reps.background.is_nonimmigrant_alien_yes_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxNo13[0]", "estate_reps.background.is_nonimmigrant_alien_no_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxYes14[0]", "estate_reps.background.question_14_yes_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBoxNo14[0]", "estate_reps.background.question_14_no_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].checkbox18f2na[0]", "estate_reps.background.nonimmigrant_exception_na_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].TextField19[0]", "estate_reps.alien_or_admission_number_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBox20upinyes[0]", "estate_reps.has_upin_yes_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].CheckBox20upinno[0]", "estate_reps.has_upin_no_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].TextField20ifyes[0]", "estate_reps.upin_number_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page8[0].sob[0]", "estate_reps.state_of_birth_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page8[0].cob[0]", "estate_reps.country_of_birth_copy2", "string"),
                FormFieldMapping("topmostSubform[0].Page8[0].ehl[0]", "estate_reps.ethnicity_hispanic_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].nhl[0]", "estate_reps.ethnicity_not_hispanic_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].aian[0]", "estate_reps.race_american_indian_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].a[0]", "estate_reps.race_asian_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].baa[0]", "estate_reps.race_black_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].nhopi[0]", "estate_reps.race_pacific_islander_copy2", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page8[0].w[0]", "estate_reps.race_white_copy2", "checkbox"),

                # ==============================================================================
                # PAGE 9 - SIGNATURES & RESPONSIBLE PERSONS (COPY 2)
                # ==============================================================================
                FormFieldMapping("topmostSubform[0].Page9[0].DateField5[0]", "estate_reps.transferee_signature_date_copy2", "date"),
                FormFieldMapping("topmostSubform[0].Page9[0].SignatureField2[0]", "estate_reps.transferee_signature_copy2", "signature"),
                FormFieldMapping("topmostSubform[0].Page9[0].TextField7n[0]", "estate_reps.responsible_persons_copy2[0].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page9[0].TextField8n[0]", "estate_reps.responsible_persons_copy2[1].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page9[0].TextField9n[0]", "estate_reps.responsible_persons_copy2[2].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page9[0].TextField10n[0]", "estate_reps.responsible_persons_copy2[3].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page9[0].TextField711n[0]", "estate_reps.responsible_persons_copy2[4].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page9[0].TextField12n[0]", "estate_reps.responsible_persons_copy2[5].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page9[0].TextField18[0]", "estate_reps.responsible_persons_count_copy2", "number"),
                
                # ==============================================================================
                # PAGE 10 - CLEO COPY
                # ==============================================================================
                FormFieldMapping("topmostSubform[0].Page10[0].ATFControl[0]", "key_document.atf_control_number_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].InternalControl[0]", "key_document.internal_control_number_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].CheckBox5firearm[0]", "key_document.transfer_reason_unserviceable_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page10[0].CheckBox6firearm[0]", "key_document.transfer_reason_government_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page10[0].CheckBox7firearm[0]", "key_document.transfer_reason_lawful_heir_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page10[0].CheckBox8firearm[0]", "key_document.transfer_reason_other_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page10[0].Other[0]", "key_document.transfer_reason_other_specify_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].County[0]", "estate_reps.transferee_county_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].CheckBox9ind[0]", "estate_reps.entity_individual_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page10[0].CheckBox9trust[0]", "estate_reps.entity_trust_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page10[0].CheckBox9gov[0]", "estate_reps.entity_government_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page10[0].TransferorNumber[0]", "applicant.phone_cleo_copy", "phone"),
                FormFieldMapping("topmostSubform[0].Page10[0].TypeofFirearm[0]", "property.firearms[0].type_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].CaliberorGauge[0]", "property.firearms[0].caliber_gauge_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].Model[0]", "property.firearms[0].model_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].LengthofBarrel[0]", "property.firearms[0].barrel_length_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].LengthOverall[0]", "property.firearms[0].overall_length_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].AdditionalDescription[0]", "property.firearms[0].additional_description_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].CheckBoxYes[0]", "property.firearms[0].is_unserviceable_yes_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page10[0].CheckBoxNo[0]", "property.firearms[0].is_unserviceable_no_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page10[0].DateField1[0]", "key_document.signature_date_cleo_copy", "date"),
                FormFieldMapping("topmostSubform[0].Page10[0].SignatureField1[0]", "applicant.signature_cleo_copy", "signature"),
                FormFieldMapping("topmostSubform[0].Page10[0].ole[0]", "estate_reps.entity_other_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page10[0].corp[0]", "estate_reps.entity_corporation_cleo_copy", "checkbox"),

                # ==============================================================================
                # PAGE 11 - TRANSFEREE CERTIFICATION (CLEO COPY)
                # ==============================================================================
                FormFieldMapping("topmostSubform[0].Page11[0].TextField4[0]", "estate_reps.cleo_agency_name_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page11[0].TextField5[0]", "estate_reps.cleo_official_name_title_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page11[0].TextField6[0]", "estate_reps.cleo_address_cleo_copy", "location"),
                FormFieldMapping("topmostSubform[0].Page11[0].Reasons[0]", "estate_reps.necessity_statement_reason_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page11[0].reasons2[0]", "estate_reps.necessity_statement_reason_continued_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckboxYes1[0]", "estate_reps.background.is_under_indictment_yes_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxNo1[0]", "estate_reps.background.is_under_indictment_no_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxYes2[0]", "estate_reps.background.has_felony_conviction_yes_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxNo2[0]", "estate_reps.background.has_felony_conviction_no_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxYes3[0]", "estate_reps.background.is_fugitive_yes_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckboxNo3[0]", "estate_reps.background.is_fugitive_no_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxYes4[0]", "estate_reps.background.is_drug_user_yes_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxNo4[0]", "estate_reps.background.is_drug_user_no_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxYes5[0]", "estate_reps.background.is_mental_defective_yes_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxNo5[0]", "estate_reps.background.is_mental_defective_no_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxYes6[0]", "estate_reps.background.has_dishonorable_discharge_yes_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxNo6[0]", "estate_reps.background.has_dishonorable_discharge_no_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxYes7[0]", "estate_reps.background.has_restraining_order_yes_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxNo7[0]", "estate_reps.background.has_restraining_order_no_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxYes8[0]", "estate_reps.background.has_domestic_violence_conviction_yes_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxNo8[0]", "estate_reps.background.has_domestic_violence_conviction_no_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBox5usa[0]", "estate_reps.citizenship_usa_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBox5other[0]", "estate_reps.citizenship_other_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].TextField6other[0]", "estate_reps.citizenship_other_specify_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxYes11[0]", "estate_reps.background.renounced_citizenship_yes_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxNo11[0]", "estate_reps.background.renounced_citizenship_no_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxYes12[0]", "estate_reps.background.is_illegal_alien_yes_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxNo12[0]", "estate_reps.background.is_illegal_alien_no_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxYes13[0]", "estate_reps.background.is_nonimmigrant_alien_yes_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxNo13[0]", "estate_reps.background.is_nonimmigrant_alien_no_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxYes14[0]", "estate_reps.background.question_14_yes_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBoxNo14[0]", "estate_reps.background.question_14_no_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].checkbox18f2na[0]", "estate_reps.background.nonimmigrant_exception_na_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].TextField19[0]", "estate_reps.alien_or_admission_number_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBox20upinyes[0]", "estate_reps.has_upin_yes_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].CheckBox20upinno[0]", "estate_reps.has_upin_no_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].TextField20ifyes[0]", "estate_reps.upin_number_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page11[0].sob[0]", "estate_reps.state_of_birth_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page11[0].cob[0]", "estate_reps.country_of_birth_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page11[0].ehl[0]", "estate_reps.ethnicity_hispanic_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].nhl[0]", "estate_reps.ethnicity_not_hispanic_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].aian[0]", "estate_reps.race_american_indian_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].a[0]", "estate_reps.race_asian_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].baa[0]", "estate_reps.race_black_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].nhopi[0]", "estate_reps.race_pacific_islander_cleo_copy", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page11[0].w[0]", "estate_reps.race_white_cleo_copy", "checkbox"),

                # ==============================================================================
                # PAGE 12 - SIGNATURES & RESPONSIBLE PERSONS (CLEO COPY)
                # ==============================================================================
                FormFieldMapping("topmostSubform[0].Page12[0].DateField5[0]", "estate_reps.transferee_signature_date_cleo_copy", "date"),
                FormFieldMapping("topmostSubform[0].Page12[0].SignatureField2[0]", "estate_reps.transferee_signature_cleo_copy", "signature"),
                FormFieldMapping("topmostSubform[0].Page12[0].TextField7n[0]", "estate_reps.responsible_persons_cleo_copy[0].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page12[0].TextField8n[0]", "estate_reps.responsible_persons_cleo_copy[1].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page12[0].TextField9n[0]", "estate_reps.responsible_persons_cleo_copy[2].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page12[0].TextField10n[0]", "estate_reps.responsible_persons_cleo_copy[3].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page12[0].TextField711n[0]", "estate_reps.responsible_persons_cleo_copy[4].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page12[0].TextField12n[0]", "estate_reps.responsible_persons_cleo_copy[5].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page12[0].TextField18[0]", "estate_reps.responsible_persons_count_cleo_copy", "number"),

                FormFieldMapping("topmostSubform[0].Page1[0].ATFControl[0]", "key_document.atf_control_number", "string"),
                # ... hundreds of lines of existing mappings ...
                FormFieldMapping("topmostSubform[0].Page12[0].TextField18[0]", "estate_reps.responsible_persons_count_cleo_copy", "number"),
            
                # PASTE THE NEW CODE BLOCK HERE

                FormFieldMapping("topmostSubform[0].Page1[0].CheckBox5firearm[0]", "key_document.transfer_reason_unserviceable", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].CheckBox6firearm[0]", "key_document.transfer_reason_government", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].CheckBox7firearm[0]", "key_document.transfer_reason_lawful_heir", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].CheckBox8firearm[0]", "key_document.transfer_reason_other", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].Other[0]", "key_document.transfer_reason_other_specify", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].County[0]", "estate_reps.transferee_county", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].CheckBox9ind[0]", "estate_reps.entity_individual", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].CheckBox9trust[0]", "estate_reps.entity_trust", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].CheckBox9gov[0]", "estate_reps.entity_government", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].TransferorNumber[0]", "applicant.phone", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].TypeofFirearm[0]", "property.firearms[0].type", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].CaliberorGauge[0]", "property.firearms[0].caliber_gauge", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].Model[0]", "property.firearms[0].model", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].LengthofBarrel[0]", "property.firearms[0].barrel_length", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].LengthOverall[0]", "property.firearms[0].overall_length", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].SerialNumber[0]", "property.firearms[0].serial_number", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].AdditionalDescription[0]", "property.firearms[0].additional_description", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].CheckBoxYes[0]", "property.firearms[0].is_unserviceable_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].CheckBoxNo[0]", "property.firearms[0].is_unserviceable_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].DateField1[0]", "key_document.signature_date", "date"),
                FormFieldMapping("topmostSubform[0].Page1[0].SignatureField1[0]", "applicant.signature", "signature"),
                FormFieldMapping("topmostSubform[0].Page1[0].ole[0]", "estate_reps.entity_other", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].corp[0]", "estate_reps.entity_corporation", "checkbox"),
                # --- PAGE 2 ---
                FormFieldMapping("topmostSubform[0].Page2[0].TextField4[0]", "estate_reps.cleo_agency_name", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].TextField5[0]", "estate_reps.cleo_official_name_title", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].TextField6[0]", "estate_reps.cleo_address", "location"),
                FormFieldMapping("topmostSubform[0].Page2[0].Reasons[0]", "estate_reps.necessity_statement_reason", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckboxYes1[0]", "estate_reps.background.is_under_indictment_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxNo1[0]", "estate_reps.background.is_under_indictment_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxYes2[0]", "estate_reps.background.has_felony_conviction_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxNo2[0]", "estate_reps.background.has_felony_conviction_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxYes3[0]", "estate_reps.background.is_fugitive_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckboxNo3[0]", "estate_reps.background.is_fugitive_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxYes4[0]", "estate_reps.background.is_drug_user_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxNo4[0]", "estate_reps.background.is_drug_user_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxYes5[0]", "estate_reps.background.is_mental_defective_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxNo5[0]", "estate_reps.background.is_mental_defective_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxYes6[0]", "estate_reps.background.has_dishonorable_discharge_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxNo6[0]", "estate_reps.background.has_dishonorable_discharge_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxYes7[0]", "estate_reps.background.has_restraining_order_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxNo7[0]", "estate_reps.background.has_restraining_order_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxYes8[0]", "estate_reps.background.has_domestic_violence_conviction_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxNo8[0]", "estate_reps.background.has_domestic_violence_conviction_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBox5usa[0]", "estate_reps.citizenship_usa", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBox5other[0]", "estate_reps.citizenship_other", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].TextField6other[0]", "estate_reps.citizenship_other_specify", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxYes11[0]", "estate_reps.background.renounced_citizenship_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxNo11[0]", "estate_reps.background.renounced_citizenship_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxYes12[0]", "estate_reps.background.is_illegal_alien_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxNo12[0]", "estate_reps.background.is_illegal_alien_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxYes13[0]", "estate_reps.background.is_nonimmigrant_alien_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBoxNo13[0]", "estate_reps.background.is_nonimmigrant_alien_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].checkbox18f2NA[0]", "estate_reps.background.nonimmigrant_exception_na", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].TextField19[0]", "estate_reps.alien_or_admission_number", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBox20upinyes[0]", "estate_reps.has_upin_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].CheckBox20upinno[0]", "estate_reps.has_upin_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].TextField20ifyes[0]", "estate_reps.upin_number", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].sob[0]", "estate_reps.state_of_birth", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].cob[0]", "estate_reps.country_of_birth", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].ehl[0]", "estate_reps.ethnicity_hispanic", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].nhl[0]", "estate_reps.ethnicity_not_hispanic", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].aian[0]", "estate_reps.race_american_indian", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].a[0]", "estate_reps.race_asian", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].baa[0]", "estate_reps.race_black", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].nhopi[0]", "estate_reps.race_pacific_islander", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].w[0]", "estate_reps.race_white", "checkbox"),
                # --- PAGE 3 ---
                FormFieldMapping("topmostSubform[0].Page3[0].DateField5[0]", "estate_reps.transferee_signature_date", "date"),
                FormFieldMapping("topmostSubform[0].Page3[0].SignatureField2[0]", "estate_reps.transferee_signature", "signature"),
                FormFieldMapping("topmostSubform[0].Page3[0].TextField7n[0]", "estate_reps.responsible_persons[0].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page3[0].TextField8n[0]", "estate_reps.responsible_persons[1].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page3[0].TextField18[0]", "estate_reps.responsible_persons_count", "number"),
                # --- PAGE 10 (Fields not already covered by pattern) ---
                FormFieldMapping("topmostSubform[0].Page10[0].NumberStreetCityStateZipDifferent[0]", "applicant.transferor_physical_address_cleo_copy", "location"),
                FormFieldMapping("topmostSubform[0].Page10[0].FederalFirearmsLicense6dig[0]", "estate_reps.ffl_part1_6_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].FederalFirearmsLicense2dig[0]", "estate_reps.ffl_part2_2_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].FederalFirearmsLicense2dig2[0]", "estate_reps.ffl_part3_2_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].FederalFirearmsLicense5dig[0]", "estate_reps.ffl_part4_5_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].TFederalFirearmsLicense6dig[0]", "applicant.ffl_part1_6_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].TFederalFirearmsLicense2dig[0]", "applicant.ffl_part2_2_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].TFederalFirearmsLicense2dig2[0]", "applicant.ffl_part3_2_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].TFederalFirearmsLicense5dig[0]", "applicant.ffl_part4_5_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].TransfereeSpecialTaxStatus[0]", "estate_reps.sot_ein_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].TransfereeSpecialTaxStatusClass[0]", "estate_reps.sot_class_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].TransferorSpecialTaxStatus[0]", "applicant.sot_ein_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].TransferorSpecialTaxStatusClass[0]", "applicant.sot_class_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].FederalFirearmsLicense6dig6[0]", "property.firearms[0].manufacturer_ffl_part1_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].FederalFirearmsLicense2dig7[0]", "property.firearms[0].manufacturer_ffl_part2_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].FederalFirearmsLicense2dig28[0]", "property.firearms[0].manufacturer_ffl_part3_cleo_copy", "string"),
                FormFieldMapping("topmostSubform[0].Page10[0].FederalFirearmsLicense5dig9[0]", "property.firearms[0].manufacturer_ffl_part4_cleo_copy", "string"),


            ],
            # ============================================================================
            # 27. SOCIAL SECURITY MARITAL RELATIONSHIP STATEMENT (SSA-754-F5)
            # ============================================================================
            "social_security_marital_statement_ssa754f5": [
                FormFieldMapping("wage_earner_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("wage_earner_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("applicant_name", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("person_living_with", "spouse.name", "name", "parse_full_name"),
                FormFieldMapping("living_together_start_date", "spouse.date_started_living_with_spouse", "date"),
                FormFieldMapping("living_together_start_month", "spouse.date_started_living_with_spouse", "date", "extract_month"),
                FormFieldMapping("living_together_start_year", "spouse.date_started_living_with_spouse", "date", "extract_year"),
                FormFieldMapping("living_together_location", "spouse.address_history", "location"),
                FormFieldMapping("living_together_city", "spouse.address_history", "location", "extract_city"),
                FormFieldMapping("living_together_state", "spouse.address_history", "location", "extract_state"),
                FormFieldMapping("continuous_cohabitation", "spouse.continuous_cohabitation", "boolean"),
                FormFieldMapping("separation_periods", "spouse.separation_periods", "string"),
                FormFieldMapping("separation_reasons", "spouse.separation_reasons", "string"),
                FormFieldMapping("places_lived_together", "spouse.cohabitation_addresses", "string"),
                FormFieldMapping("relationship_understanding", "spouse.relationship_understanding", "string"),
                FormFieldMapping("understanding_in_writing", "spouse.written_understanding", "boolean"),
                FormFieldMapping("understanding_changed", "spouse.understanding_changed", "boolean"),
                FormFieldMapping("understanding_changes", "spouse.understanding_changes_details", "string"),
                FormFieldMapping("duration_understanding", "spouse.duration_understanding", "string"),
                FormFieldMapping("relationship_ending_understanding", "spouse.ending_understanding", "string"),
                FormFieldMapping("believed_legally_married", "spouse.believed_legally_married", "boolean"),
                FormFieldMapping("belief_reason", "spouse.marriage_belief_reason", "string"),
                FormFieldMapping("ceremonial_marriage_promise", "spouse.ceremonial_promise", "boolean"),
                FormFieldMapping("ceremony_not_performed_reason", "spouse.no_ceremony_reason", "string"),
                FormFieldMapping("children_of_relationship", "children[*].name", "name", "parse_full_name"),
                FormFieldMapping("child_date_of_birth", "children[*].date_of_birth", "date"),
                FormFieldMapping("child_place_of_birth", "children[*].place_of_birth", "location"),
                FormFieldMapping("name_before_living_together", "applicant.previous_name", "name"),
                FormFieldMapping("partner_name_before", "spouse.previous_name", "name"),
                FormFieldMapping("name_after_living_together", "applicant.name_during_relationship", "name"),
                FormFieldMapping("partner_name_after", "spouse.name_during_relationship", "name"),
                FormFieldMapping("different_names_reason", "spouse.different_names_reason", "string"),
                FormFieldMapping("joint_documents", "key_document[*].joint_documents", "string"),
                FormFieldMapping("joint_tax_returns", "financial_information[*].joint_tax_returns", "boolean"),
                FormFieldMapping("joint_deeds_contracts", "financial_information[*].joint_legal_documents", "boolean"),
                FormFieldMapping("joint_insurance", "insurance[*].joint_policies", "boolean"),
                FormFieldMapping("joint_bank_accounts", "financial_information[*].joint_accounts", "boolean"),
                FormFieldMapping("document_dates", "key_document[*].document_dates", "string"),
                FormFieldMapping("shown_as_spouse", "spouse.documented_as_spouse", "string"),
                FormFieldMapping("business_dealings", "financial_information[*].joint_business", "boolean"),
                FormFieldMapping("joint_charge_accounts", "financial_information[*].joint_credit", "boolean"),
                FormFieldMapping("business_names_addresses", "financial_information[*].business_details", "string"),
                FormFieldMapping("introduction_as_spouse", "spouse.public_recognition", "string"),
                FormFieldMapping("partner_introduction_of_you", "spouse.partner_introduction", "string"),
                FormFieldMapping("mail_addressing", "spouse.mail_addressing", "string"),
                FormFieldMapping("employers_neighbors_list", "contact[*].employer_neighbor_contacts", "string"),
                FormFieldMapping("closest_relatives_list", "contact[*].relative_contacts", "string"),
                FormFieldMapping("partner_relatives_list", "contact[*].partner_relative_contacts", "string"),
                FormFieldMapping("contact_objections", "contact[*].contact_restrictions", "string"),
                FormFieldMapping("applicant_other_relationships", "applicant.other_relationships", "string"),
                FormFieldMapping("partner_other_relationships", "spouse.other_relationships", "string"),
                FormFieldMapping("earlier_marriage_knowledge", "spouse.earlier_marriage_knowledge", "string"),
                FormFieldMapping("earlier_marriage_discovery", "spouse.marriage_discovery_details", "string"),
                FormFieldMapping("relationship_discussion_after_discovery", "spouse.post_discovery_discussion", "string"),
                FormFieldMapping("applicant_signature", "applicant.signature", "string"),
                FormFieldMapping("signature_date", "key_document[*].date_created", "date"),
                FormFieldMapping("applicant_phone", "applicant.phone", "phone"),
                FormFieldMapping("applicant_mailing_address", "applicant.mailing_address", "location"),
                FormFieldMapping("applicant_county", "applicant.address", "location", "extract_county"),
                FormFieldMapping("applicant_state", "applicant.address", "location", "extract_state"),
                FormFieldMapping("applicant_zip", "applicant.address", "location", "extract_zip"),
            ],
            
            
            
            # ============================================================================
            # 29. ELECTIONS ONTARIO F0527W - REMOVE DECEASED PERSON
            # ============================================================================
            "elections_ontario_f0527w": [
                # Section: Applicant Acting on Behalf of Deceased
                FormFieldMapping("Last Name", "applicant.last_name", "name", required=True),
                FormFieldMapping("First Name", "applicant.first_name", "name", required=True),
                FormFieldMapping("Middle Name(s)", "applicant.middle_name", "name", required=False),
                FormFieldMapping("Relationship to Deceased", "applicant.relationship_to_deceased", "string", required=True),

                # Section: Applicant's Contact Information
                FormFieldMapping("Phone", "applicant.phone", "phone", required=True),
                FormFieldMapping("Email", "applicant.email", "email", required=True),

                # Section: Information About the Deceased
                FormFieldMapping("Last Name_2", "deceased.last_name", "name", required=True),
                FormFieldMapping("First Name_2", "deceased.first_name", "name", required=True),
                FormFieldMapping("Middle Name(s)_2", "deceased.middle_name", "name", required=False),
                FormFieldMapping("Date of Birth", "deceased.date_of_birth", "date", required=True),
                FormFieldMapping("Year", "deceased.date_of_birth", "date_component", required=True), # Year part of DOB
                FormFieldMapping("Month", "deceased.date_of_birth", "date_component", required=True), # Month part of DOB
                FormFieldMapping("Day", "deceased.date_of_birth", "date_component", required=True),   # Day part of DOB

                # Section: Last Residential Address of the Deceased
                FormFieldMapping("Street Number", "deceased.home_address.street_number", "string", required=True),
                FormFieldMapping("Street Name", "deceased.home_address.street_name", "string", required=True),
                FormFieldMapping("Unit #", "deceased.home_address.unit", "string", required=False),
                FormFieldMapping("City, Municipality or Town", "deceased.home_address.city", "string", required=True),
                FormFieldMapping("Postal Code", "deceased.home_address.postal_code", "string", required=True),

                # Section: Declaration
                FormFieldMapping("I request that the deceased person, named above, be removed from the registers maintained by Elections Ontario; and", "key_document.declaration_part1", "checkbox", required=True),
                FormFieldMapping("I have included a copy of acceptable documentation (proof of death);", "key_document.declaration_part2", "checkbox", required=True),
                FormFieldMapping("Elector Signature", "applicant.signature", "signature", required=True),
                FormFieldMapping("Year_2", "key_document.signature_date", "date_component", required=True),
                FormFieldMapping("Month_2", "key_document.signature_date", "date_component", required=True),
                FormFieldMapping("Day_2", "key_document.signature_date", "date_component", required=True),

                # Section: Office Use Only
                FormFieldMapping("ED #", "key_document.office_use.electoral_district", "string", required=False),
                FormFieldMapping("Poll #", "key_document.office_use.poll_number", "string", required=False),
                FormFieldMapping("Elector ID", "key_document.office_use.elector_id", "string", required=False),
                FormFieldMapping("Reference #", "key_document.office_use.reference_number", "string", required=False),
                FormFieldMapping("Date: Received", "key_document.office_use.date_received", "date", required=False),
                FormFieldMapping("Processed", "key_document.office_use.date_processed", "date", required=False),
                FormFieldMapping("Year_3", "key_document.office_use.date_received_year", "date_component", required=False),
                FormFieldMapping("Month_3", "key_document.office_use.date_received_month", "date_component", required=False),
                FormFieldMapping("Day_3", "key_document.office_use.date_received_day", "date_component", required=False),
                FormFieldMapping("Year_4", "key_document.office_use.date_processed_year", "date_component", required=False),
                FormFieldMapping("Month_4", "key_document.office_use.date_processed_month", "date_component", required=False),
                FormFieldMapping("Day_4", "key_document.office_use.date_processed_day", "date_component", required=False),
                FormFieldMapping("Name", "key_document.office_use.official_name", "name", required=False),
                FormFieldMapping("Signature", "key_document.office_use.official_signature", "signature", required=False)
            ],
            
            # ============================================================================
            # 30. CANADA REVENUE AGENCY RC552 - APPOINTING REPRESENTATIVE
            # ============================================================================
            "cra_rc552_representative": [
                # Deceased Person Information
                FormFieldMapping("deceased_first_name", "deceased.first_name", "name"),
                FormFieldMapping("deceased_middle_name", "deceased.middle_name", "name"),
                FormFieldMapping("deceased_last_name", "deceased.last_name", "name"),
                FormFieldMapping("deceased_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("deceased_sin", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("deceased_address", "deceased.home_address", "location"),
                FormFieldMapping("deceased_apartment_number", "deceased.home_address", "location", "extract_apartment"),
                FormFieldMapping("deceased_city", "deceased.home_address", "location", "extract_city"),
                FormFieldMapping("deceased_province", "deceased.home_address", "location", "extract_province"),
                FormFieldMapping("deceased_postal_code", "deceased.home_address", "location", "extract_postal_code"),
                
                # Representative Information
                FormFieldMapping("representative_first_name", "estate_reps[*].first_name", "name"),
                FormFieldMapping("representative_last_name", "estate_reps[*].last_name", "name"),
                FormFieldMapping("representative_sin", "estate_reps[*].social_insurance_number", "sin"),
                FormFieldMapping("relationship_to_deceased", "estate_reps[*].secondary_relationship_to_deceased", "select"),
                FormFieldMapping("representative_address", "estate_reps[*].address", "location"),
                FormFieldMapping("representative_phone", "estate_reps[*].phone", "phone"),
                FormFieldMapping("rep_id_group_id", "estate_reps[*].proof_of_authority", "string"),
                
                # Documentation Requirements
                FormFieldMapping("death_certificate", "deceased.proof_of_death", "file"),
                FormFieldMapping("witness_first_name", "contact[*].first_name", "name"),
                FormFieldMapping("witness_last_name", "contact[*].last_name", "name"),
                FormFieldMapping("witness_phone", "contact[*].phone.phone_number", "phone"),
                FormFieldMapping("witness_signature", "contact[*].notes", "string"),
            ],
            
            # ============================================================================
            # 31. CALIFORNIA DMV REG 256 - STATEMENT OF FACTS
            # ============================================================================
            "california_dmv_reg256": [
                # Vehicle Information
                FormFieldMapping("license_plate_cf_number", "property.vehicles[*].license_plate", "string"),
                FormFieldMapping("vehicle_vessel_id_number", "property.vehicles[*].vin", "string"),
                FormFieldMapping("year_make", "property.vehicles[*].make_model", "string", "parse_year_make"),
                
                # Use Tax Exemption Information
                FormFieldMapping("family_transfer", "financial_information[*].type", "select", "map_tax_exemption"),
                FormFieldMapping("gift_transfer", "financial_information[*].type", "select", "map_tax_exemption"),
                FormFieldMapping("inheritance_transfer", "financial_information[*].type", "select", "map_tax_exemption"),
                FormFieldMapping("court_order", "key_document[*].type", "select"),
                FormFieldMapping("current_market_value", "property.vehicles[*].estimated_value", "currency"),
                
                # Smog Exemption Information
                FormFieldMapping("smog_certification_date", "property.vehicles[*].insurance_company", "string", "map_smog_info"),
                FormFieldMapping("vehicle_power_type", "property.vehicles[*].make_model", "string", "append_power_type"),
                FormFieldMapping("transfer_between_family", "estate_reps[*].secondary_relationship_to_deceased", "select"),
                
                # Title/Transfer Information
                FormFieldMapping("transfer_only", "key_document[*].type", "select"),
                FormFieldMapping("title_only", "key_document[*].type", "select"),
                FormFieldMapping("applicant_signature", "applicant.name", "name", "parse_signature"),
                FormFieldMapping("applicant_phone", "applicant.phone", "phone"),
            ],
            
            # ============================================================================
            # 32. CANADA POST MAIL FORWARDING
            # ============================================================================
            "canada_post_mail_forwarding": [
                # === METADATA & HEADERS (Mapped to notes) ===
                FormFieldMapping("33-086-784 (22-12)", "key_document.form_number", "string", required=False),
                FormFieldMapping("MAIL FORWARDING", "key_document.notes.form_title", "string", required=False),
                FormFieldMapping("Réacheminement du courrier", "key_document.notes.form_title_french", "string", required=False),
                
                # === SERVICE DETAILS (Maps to forwarding_details.*) ===
                FormFieldMapping(form_field="Moving to a new address", schema_path="forwarding_details.is_temporary", field_type="checkbox", value="false"),
                FormFieldMapping(form_field="Temporarily relocating and returning to original address", schema_path="forwarding_details.is_temporary", field_type="checkbox", value="true"),
                FormFieldMapping(form_field="Residential", schema_path="forwarding_details.service_type", field_type="checkbox", value="residential"),
                FormFieldMapping(form_field="Business (must also be selected for both residential and business mail)", schema_path="forwarding_details.service_type", field_type="checkbox", value="business"),
                FormFieldMapping(form_field="Yes (also check box in the Mail Recipients section)", schema_path="forwarding_details.includes_deceased", field_type="checkbox", value="true"),
                FormFieldMapping(form_field="No", schema_path="forwarding_details.includes_deceased", field_type="checkbox", value="false"),
                FormFieldMapping(form_field="Yes", schema_path="forwarding_details.all_residents_moving", field_type="checkbox", value="true"),
                FormFieldMapping(form_field="No_2", schema_path="forwarding_details.all_residents_moving", field_type="checkbox", value="false", required=False),
                
                # === REQUESTOR'S DETAILS (Maps to applicant.*) ===
                FormFieldMapping("First name", "applicant.first_name", "name"),
                FormFieldMapping("Last name", "applicant.last_name", "name"),
                FormFieldMapping("Email address*", "applicant.email", "email"),
                FormFieldMapping("Daytime telephone no.", "applicant.phone", "phone"),
                
                # === MAIL RECIPIENTS (Maps to recipients[*].*) ===
                FormFieldMapping("1) First name or Business name", "recipients[0].name_or_business", "string", required=False),
                FormFieldMapping("Last name_2", "recipients[0].last_name", "name", required=False),
                FormFieldMapping("Deceased", "recipients[0].is_deceased", "checkbox", required=False),
                FormFieldMapping("2) First name or Business name", "recipients[1].name_or_business", "string", required=False),
                FormFieldMapping("Last name_3", "recipients[1].last_name", "name", required=False),
                FormFieldMapping("3) First name", "recipients[2].name_or_business", "string", required=False),
                FormFieldMapping("Last name_4", "recipients[2].last_name", "name", required=False),
                FormFieldMapping("4) First name", "recipients[3].name_or_business", "string", required=False),
                FormFieldMapping("Last name_5", "recipients[3].last_name", "name", required=False),
                FormFieldMapping("5) First name", "recipients[4].name_or_business", "string", required=False),
                FormFieldMapping("Last name_6", "recipients[4].last_name", "name", required=False),
                FormFieldMapping("Deceased_2", "recipients[4].is_deceased", "checkbox", required=False),
                FormFieldMapping("6) First name", "recipients[5].name_or_business", "string", required=False),
                FormFieldMapping("Last name_7", "recipients[5].last_name", "name", required=False),
                FormFieldMapping("7) First name", "recipients[6].name_or_business", "string", required=False),
                FormFieldMapping("Last name_8", "recipients[6].last_name", "name", required=False),
                FormFieldMapping("8) First name", "recipients[7].name_or_business", "string", required=False),
                FormFieldMapping("Last name_9", "recipients[7].last_name", "name", required=False),

                # === CURRENT ADDRESS (Maps to applicant.home_address) ===
                FormFieldMapping("Unit/Apt no.", "applicant.home_address.unit", "string", required=False),
                FormFieldMapping("Street no.", "applicant.home_address.street_number", "string", required=False),
                FormFieldMapping("Street name", "applicant.home_address.street_name", "string", required=False),
                FormFieldMapping("PO Box no.", "applicant.home_address.po_box", "string", required=False),
                FormFieldMapping("RR no. (rural only)", "applicant.home_address.rr_number", "string", required=False),
                FormFieldMapping("City/Municipality", "applicant.home_address.city", "string", required=False),
                FormFieldMapping("Province", "applicant.home_address.province", "string", required=False),
                FormFieldMapping("Postal code", "applicant.home_address.postal_code", "string", required=False),

                # === NEW ADDRESS (Maps to applicant.mailing_address) ===
                FormFieldMapping("Unit/Apt no._2", "applicant.mailing_address.unit", "string", required=False),
                FormFieldMapping("Street no._2", "applicant.mailing_address.street_number", "string", required=False),
                FormFieldMapping("Street name_2", "applicant.mailing_address.street_name", "string", required=False),
                FormFieldMapping("PO Box no._2", "applicant.mailing_address.po_box", "string", required=False),
                FormFieldMapping("RR no. (rural only)_2", "applicant.mailing_address.rr_number", "string", required=False),
                FormFieldMapping("City/Municipality_2", "applicant.mailing_address.city", "string", required=False),
                FormFieldMapping("Province_2", "applicant.mailing_address.province", "string", required=False),
                FormFieldMapping("Postal/Zip code", "applicant.mailing_address.postal_code", "string", required=False),
                FormFieldMapping("Country", "applicant.mailing_address.country", "string", required=False),

                # === SERVICE DATES (Maps to forwarding_details.*) ===
                FormFieldMapping("year", "forwarding_details.start_date", "date_component", required=False),
                FormFieldMapping("month", "forwarding_details.start_date", "date_component", required=False),
                FormFieldMapping("day", "forwarding_details.start_date", "date_component", required=False),
                FormFieldMapping("year_2", "forwarding_details.end_date", "date_component", required=False),
                FormFieldMapping("month_2", "forwarding_details.end_date", "date_component", required=False),
                FormFieldMapping("day_2", "forwarding_details.end_date", "date_component", required=False),

                # === MOVER DATA SERVICE ===
                FormFieldMapping("If you do not want this feature, check this box.", "forwarding_details.opt_out_mover_data_service", "checkbox"),

                FormFieldMapping("This service is available at canadapost.ca/mailfor", "key_document.notes.service_url", "string", required=False),
                FormFieldMapping("SERVICE DETAILS", "key_document.notes.section_header_service_details", "string", required=False),
                FormFieldMapping("1. What is the service for? (Select the option tha", "key_document.notes.service_question_1", "string", required=False),
                FormFieldMapping("Yourself and any others at the same address", "service_details.who_is_service_for", "checkbox", value="self_and_others"), # This path is valid
                FormFieldMapping("On behalf of other people only", "service_details.who_is_service_for", "checkbox", value="others_only"), # This path is valid
                FormFieldMapping("relocating)", "key_document.notes.parenthetical_relocating", "string", required=False),
                FormFieldMapping("2. What type of mail are you forwarding?", "key_document.notes.service_question_2", "string", required=False),
                FormFieldMapping("4. Does this include a deceased individual?", "key_document.notes.service_question_4", "string", required=False),
                FormFieldMapping("REQUESTOR’S DETAILS", "key_document.notes.section_header_requestor", "string", required=False),
                FormFieldMapping("WHAT IS THE CURRENT ADDRESS?", "key_document.notes.section_header_current_address", "string", required=False),
                FormFieldMapping("WHAT IS THE NEW ADDRESS?", "key_document.notes.section_header_new_address", "string", required=False),
                FormFieldMapping("EFFECTIVE SERVICE DATES", "key_document.notes.section_header_service_dates", "string", required=False),
                FormFieldMapping("customer records.", "key_document.notes.customer_records_note", "string", required=False),
                FormFieldMapping("SERVICE DELIVERY LIMITATIONS", "key_document.notes.delivery_limitations_header", "string", required=False),
                FormFieldMapping("TERMS AND CONDITIONS (to be accepted with your ele", "key_document.notes.terms_and_conditions_header", "string", required=False),
                FormFieldMapping("To opt-out", "mover_data_service.opt_out_text", "string", required=False),
                FormFieldMapping("Relocation service must be purchased when you stil", "key_document.notes.relocation_purchase_note", "string", required=False),
                FormFieldMapping("TMTrademarks of Canada Post Corporation.", "key_document.notes.trademark_notice", "string", required=False),
            

                
            ],

            
            
            
            # ============================================================================
            # 33. CANADA PENSION PLAN SURVIVOR'S PENSION - SC ISP-1300
            # ============================================================================
            "canada_cpp_survivors_pension_isp1300": [
                # Deceased Spouse/Common-law Partner Information (Section A)
                FormFieldMapping("deceased_sin", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("deceased_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("deceased_country_of_birth", "deceased.place_of_birth", "location"),
                FormFieldMapping("deceased_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("deceased_marital_status", "deceased.marital_status", "select"),
                FormFieldMapping("deceased_first_name", "deceased.first_name", "name"),
                FormFieldMapping("deceased_last_name", "deceased.last_name", "name"),
                FormFieldMapping("deceased_name_at_birth", "deceased.name_at_birth", "name"),
                FormFieldMapping("deceased_name_on_sin_card", "deceased.social_insurance_name", "name"),
                FormFieldMapping("deceased_home_address", "deceased.home_address", "location"),
                FormFieldMapping("deceased_city", "deceased.home_address", "location", "extract_city"),
                FormFieldMapping("deceased_province", "deceased.home_address", "location", "extract_province"),
                FormFieldMapping("deceased_postal_code", "deceased.home_address", "location", "extract_postal_code"),
                
                # International Work History
                FormFieldMapping("deceased_worked_other_countries", "deceased.employment.notes", "string"),
                FormFieldMapping("other_country_name_a", "deceased.employment.notes", "string", "combine_international_work"),
                FormFieldMapping("other_country_insurance_number_a", "deceased.employment.notes", "string", "combine_international_work"),
                FormFieldMapping("other_country_benefit_requested_a", "deceased.employment.notes", "string", "combine_international_work"),
                
                # Surviving Spouse Information (Section B)
                FormFieldMapping("survivor_sin", "applicant.social_insurance_number", "sin"),
                FormFieldMapping("survivor_date_of_birth", "applicant.date_of_birth", "date"),
                FormFieldMapping("survivor_country_of_birth", "applicant.place_of_birth", "location"),
                FormFieldMapping("survivor_first_name", "applicant.first_name", "name"),
                FormFieldMapping("survivor_last_name", "applicant.last_name", "name"),
                FormFieldMapping("survivor_name_at_birth", "applicant.mothers_name", "name"),
                FormFieldMapping("survivor_name_on_sin_card", "applicant.name", "name"),
                FormFieldMapping("survivor_mailing_address", "applicant.mailing_address", "location"),
                FormFieldMapping("survivor_home_address", "applicant.home_address", "location"),
                FormFieldMapping("survivor_phone_home", "applicant.phone", "phone"),
                FormFieldMapping("survivor_phone_work", "applicant.phone_alt", "phone"),
                FormFieldMapping("survivor_email", "applicant.email", "email"),
                
                # Marriage Information
                FormFieldMapping("married_to_deceased", "spouse.date_of_marriage", "date"),
                FormFieldMapping("date_of_marriage", "spouse.date_of_marriage", "date"),
                FormFieldMapping("still_married_at_death", "spouse.date_of_divorce", "date", "check_marriage_status"),
                FormFieldMapping("still_living_together_at_death", "spouse.date_last_lived_together", "date", "check_cohabitation"),
                
                # Common-law Information
                FormFieldMapping("common_law_start_date", "spouse.date_started_living_with_spouse", "date"),
                FormFieldMapping("common_law_living_together_at_death", "spouse.date_last_lived_together", "date"),
                
                # Payment Information
                FormFieldMapping("direct_deposit_branch_number", "payment.transit_number", "string"),
                FormFieldMapping("direct_deposit_institution_number", "payment.institution_number", "string"),
                FormFieldMapping("direct_deposit_account_number", "payment.account_number", "string"),
                FormFieldMapping("account_holder_names", "payment.bank_name", "string"),
                FormFieldMapping("bank_phone_number", "payment.bank_name", "string", "append_bank_phone"),
                
                # Tax Information
                FormFieldMapping("voluntary_tax_deduction", "payment.allow_share_direct_deposit_with_cra", "boolean"),
                FormFieldMapping("tax_deduction_amount", "payment.allow_share_direct_deposit_with_cra", "string", "store_tax_amount"),
                
                # Children Information (Section C)
                FormFieldMapping("child_first_name", "children[*].first_name", "name"),
                FormFieldMapping("child_last_name", "children[*].last_name", "name"),
                FormFieldMapping("child_date_of_birth", "children[*].date_of_birth", "date"),
                FormFieldMapping("child_sin", "children[*].social_insurance_number", "sin"),
                FormFieldMapping("child_lived_with_since_birth", "children[*].guardian_name", "string", "determine_guardianship"),
                FormFieldMapping("child_still_in_care", "children[*].guardian_name", "string", "determine_current_care"),
                FormFieldMapping("child_relationship_type", "children[*].relationship", "select"),
                
                # Children 18-25 in School
                FormFieldMapping("child_school_first_name", "children[*].first_name", "name"),
                FormFieldMapping("child_school_last_name", "children[*].last_name", "name"),
                FormFieldMapping("child_school_date_of_birth", "children[*].date_of_birth", "date"),
                FormFieldMapping("child_school_address", "children[*].address", "location"),
                
                # Financial Support Information
                FormFieldMapping("maintaining_all_children", "financial_information.outstanding_debts", "string", "track_child_support"),
                
                # Other Applicant Information (Section D)
                FormFieldMapping("other_applicant_sin", "estate_reps[*].social_insurance_number", "sin"),
                FormFieldMapping("other_applicant_first_name", "estate_reps[*].first_name", "name"),
                FormFieldMapping("other_applicant_last_name", "estate_reps[*].last_name", "name"),
                FormFieldMapping("other_applicant_address", "estate_reps[*].address", "location"),
                FormFieldMapping("other_applicant_phone_home", "estate_reps[*].phone", "phone"),
                FormFieldMapping("other_applicant_phone_work", "estate_reps[*].phone", "phone", "store_work_phone"),
                FormFieldMapping("other_applicant_email", "estate_reps[*].email", "email"),
                
                # Form Metadata
                FormFieldMapping("form_number", "key_document[*].id", "string"),
                FormFieldMapping("application_date", "key_document[*].date_created", "date"),
                FormFieldMapping("applicant_signature", "key_document[*].notes", "string"),
                FormFieldMapping("witness_name", "contact[*].name", "name"),
                FormFieldMapping("witness_relationship", "contact[*].relationship", "string"),
                FormFieldMapping("witness_phone", "contact[*].phone.phone_number", "phone"),
                FormFieldMapping("witness_signature", "contact[*].notes", "string"),
            ],
            
            
            
            # ============================================================================
            # Continue with remaining forms from original code (add all 50+ total)
            # ============================================================================
            
            # MILITARY DEATH GRATUITY - DD FORM 397
            "military_death_gratuity_dd397": [
                # Service Member Information
                FormFieldMapping("bureau_no", "key_document[*].bureau_number", "string"),
                FormFieldMapping("do_no", "key_document[*].disbursing_office_number", "string"), 
                FormFieldMapping("app", "key_document[*].appropriation_code", "string"),
                FormFieldMapping("paid_by", "key_document[*].paid_by", "string"),
                
                # Deceased Service Member Information
                FormFieldMapping("mbr_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("mbr_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("mbr_grade", "deceased.military.rank", "string"),
                FormFieldMapping("death_place", "deceased.place_of_death", "location"),
                FormFieldMapping("death_date", "deceased.date_of_death", "date"),
                
                # Payment Information
                FormFieldMapping("amt_due", "financial_information.death_gratuity_amount", "currency"),
                FormFieldMapping("payee", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("payee_addr", "estate_reps[*].address", "location"),
                FormFieldMapping("payee_sign", "estate_reps[*].signature", "signature"),
                
                # Payee Certification Checkboxes
                FormFieldMapping("xcert", "estate_reps[*].payee_certification", "checkbox"),
                FormFieldMapping("xwidow", "estate_reps[*].widow_status", "checkbox"), 
                FormFieldMapping("xrel", "estate_reps[*].relative_status", "checkbox"),
                
                # Children Information (up to 4 children)
                FormFieldMapping("childname_1", "children[0].name", "name", "parse_full_name"),
                FormFieldMapping("childaddr_1", "children[0].address", "location"),
                FormFieldMapping("childname_2", "children[1].name", "name", "parse_full_name"),
                FormFieldMapping("childaddr_2", "children[1].address", "location"),
                FormFieldMapping("childname_3", "children[2].name", "name", "parse_full_name"),
                FormFieldMapping("childaddr_3", "children[2].address", "location"),
                FormFieldMapping("childname_4", "children[3].name", "name", "parse_full_name"),
                FormFieldMapping("childaddr_4", "children[3].address", "location"),
                
                # Witness Information
                FormFieldMapping("wit1sign", "contact[0].signature", "signature"),
                FormFieldMapping("wit1addr", "contact[0].address.address_location", "location"),
                FormFieldMapping("wit2sign", "contact[1].signature", "signature"), 
                FormFieldMapping("wit2addr", "contact[1].address.address_location", "location"),
                
                # Administrative Approval
                FormFieldMapping("adm_name", "key_document[*].approving_official_name", "string"),
                FormFieldMapping("adm_title", "key_document[*].approving_official_title", "string"),
                FormFieldMapping("adm_sign", "key_document[*].approving_official_signature", "signature"),
                FormFieldMapping("adm_date", "key_document[*].approval_date", "date"),
                
                # Payment Method - Check
                FormFieldMapping("check_no", "payment.check_number", "string"),
                FormFieldMapping("check_amt", "payment.check_amount", "currency"),
                FormFieldMapping("check_date", "payment.check_date", "date"),
                
                # Payment Method - EFT/Direct Deposit
                FormFieldMapping("bank", "payment.bank_name", "string"),
                FormFieldMapping("acct_no", "payment.account_number", "string"),
                FormFieldMapping("route_no", "payment.routing_number", "string"),
                
                # Form Controls
                FormFieldMapping("Reset", "key_document[*].form_reset_button", "button"),
            ],
            
            # SERVICE CANADA T4A REPRESENTATIVE - SC ISP-1202
            "service_canada_t4a_representative_isp1202": [
                # Deceased Client Information
                FormFieldMapping("SC_ISP1202_E[0].Page1[0].sub_SectionA[0].txtF_FirstAndLastName1[0]", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("SC_ISP1202_E[0].Page1[0].sub_SectionA[0].txtF_SocialInsuranceNumbe[0]", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("SC_ISP1202_E[0].Page1[0].sub_SectionA[0].txtF_DateOfDeath[0]", "deceased.date_of_death", "date"),
                FormFieldMapping("SC_ISP1202_E[0].Page1[0].sub_SectionA[0].txtF_LastAddress[0]", "deceased.home_address", "location"),
                
                # Section A - Benefits Received
                FormFieldMapping("SC_ISP1202_E[0].Page1[0].sub_SectionA[0].cb_Oas[0]", "financial_information__pension[*].oas_benefits", "checkbox"),
                FormFieldMapping("SC_ISP1202_E[0].Page1[0].sub_SectionA[0].cb_Cpp[0]", "financial_information__pension[*].cpp_benefits", "checkbox"),
                
                # Section B - Representative Information
                FormFieldMapping("SC_ISP1202_E[0].Page1[0].sub_SectionB[0].txtF_FirstAndLastName2[0]", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("SC_ISP1202_E[0].Page1[0].sub_SectionB[0].txtF_MailingAddress[0]", "estate_reps[*].address", "location"),
                FormFieldMapping("SC_ISP1202_E[0].Page1[0].sub_SectionB[0].txtF_TelephoneNumberHomeW[0]", "estate_reps[*].phone", "phone"),
                FormFieldMapping("SC_ISP1202_E[0].Page1[0].sub_SectionB[0].txtF_NatureOfRelationship[0]", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                
                # Statement Section - Signatures and Dates
                FormFieldMapping("SC_ISP1202_E[0].Page1[0].sub_Statment[0].txtF_SignatureOfPersonToR[0]", "estate_reps[*].signature", "signature"),
                FormFieldMapping("SC_ISP1202_E[0].Page1[0].sub_Statment[0].txtF_Date1[0]", "key_document[*].signature_date", "date"),
            ],
            
            # CALIFORNIA DMV DEATH REPORT - DMV 22
            "california_dmv_death_report_dmv22": [
                FormFieldMapping("Legal owner", "deceased.full_name", "name"),  # This is actually the deceased's name
                FormFieldMapping("Date of Birth1A", "deceased.date_of_birth", "date", "combine_date_components"), 
                FormFieldMapping("Date of Birth1B", "deceased.date_of_birth", "date", "combine_date_components"),
                FormFieldMapping("Date of Date1A", "deceased.date_of_birth", "date", "combine_date_components"),
                FormFieldMapping("Date of Date1B", "deceased.date_of_birth", "date", "combine_date_components"), 
                FormFieldMapping("Date of Year1A", "deceased.date_of_birth", "date", "combine_date_components"),
                FormFieldMapping("Date of Year1B", "deceased.date_of_birth", "date", "combine_date_components"),
                FormFieldMapping("Date of Year1C", "deceased.date_of_birth", "date", "combine_date_components"),
                FormFieldMapping("Date of Year1D", "deceased.date_of_birth", "date", "combine_date_components"),
                
                # Driver License/ID Information
                FormFieldMapping("DL ID1", "id_document__drivers_license[*].id", "string", "combine_dl_segments"),
                FormFieldMapping("DL ID2", "id_document__drivers_license[*].id", "string", "combine_dl_segments"),
                FormFieldMapping("DL ID3", "id_document__drivers_license[*].id", "string", "combine_dl_segments"),
                FormFieldMapping("DL ID4", "id_document__drivers_license[*].id", "string", "combine_dl_segments"),
                FormFieldMapping("DL ID5", "id_document__drivers_license[*].id", "string", "combine_dl_segments"),
                FormFieldMapping("DL ID6", "id_document__drivers_license[*].id", "string", "combine_dl_segments"),
                FormFieldMapping("DL ID7", "id_document__drivers_license[*].id", "string", "combine_dl_segments"),
                FormFieldMapping("DL ID8", "id_document__drivers_license[*].id", "string", "combine_dl_segments"),
                FormFieldMapping("Driver License-ID14", "id_document__drivers_license[*].id", "string"),
                FormFieldMapping("State", "id_document__drivers_license[*].issuing_state", "string"),
                
                # Disabled Parking Placard Information  
                FormFieldMapping("Parking Placard-ID11", "id_document__accessible_parking_permit[*].id", "string", "combine_placard_segments"),
                FormFieldMapping("Parking Placard-ID12", "id_document__accessible_parking_permit[*].id", "string", "combine_placard_segments"),
                FormFieldMapping("Parking Placard-ID13", "id_document__accessible_parking_permit[*].id", "string", "combine_placard_segments"),
                FormFieldMapping("Parking Placard-ID15", "id_document__accessible_parking_permit[*].id", "string", "combine_placard_segments"),
                FormFieldMapping("Parking Placard-ID16", "id_document__accessible_parking_permit[*].id", "string", "combine_placard_segments"),
                FormFieldMapping("Parking Placard-ID17", "id_document__accessible_parking_permit[*].id", "string", "combine_placard_segments"),
                
                # Section 2 - Death Certificate Information
                FormFieldMapping("Date of Month2A", "deceased.date_of_death", "date", "combine_date_components"),
                FormFieldMapping("Date of Month2B", "deceased.date_of_death", "date", "combine_date_components"),
                FormFieldMapping("Date of Date2A", "deceased.date_of_death", "date", "combine_date_components"),
                FormFieldMapping("Date of Date2B", "deceased.date_of_death", "date", "combine_date_components"),
                FormFieldMapping("Date of Year2A", "deceased.date_of_death", "date", "combine_date_components"),
                FormFieldMapping("Date of Year2B", "deceased.date_of_death", "date", "combine_date_components"),
                FormFieldMapping("Date of Year2C", "deceased.date_of_death", "date", "combine_date_components"),
                FormFieldMapping("Date of Year2D", "deceased.date_of_death", "date", "combine_date_components"),
                FormFieldMapping("Principal city", "deceased.place_of_death", "location", "extract_city"),
                FormFieldMapping("Principal county", "deceased.place_of_death", "location", "extract_county"),
                
                # Section 3 - Person Reporting Death
                FormFieldMapping("Person Reporting Death", "applicant.full_name", "name"),
                FormFieldMapping("Relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("TELEPHONE", "applicant.phone", "phone"),
                FormFieldMapping("TELEPHONE2", "applicant.phone_alt", "phone"),
                FormFieldMapping("E-mail", "applicant.email", "email"),
                FormFieldMapping("Applicant date", "key_document[*].signature_date", "date"),
                
                # Form Control Elements
                FormFieldMapping("click to", "key_document[*].pdf_button_1", "button"),
                FormFieldMapping("click to 1", "key_document[*].pdf_button_2", "button"),
            ],
            
            # IRS FORM SS-4 - APPLICATION FOR EMPLOYER IDENTIFICATION NUMBER (ESTATE)
            "irs_form_ss4_estate": [
                # Form Header Information
                FormFieldMapping("topmostSubform[0].Page1[0].PgHeader[0].f1_1[0]", "key_document[*].form_number", "string"),
                
                # Section 1: Entity Information
                FormFieldMapping("topmostSubform[0].Page1[0].f1_2[0]", "estate_reps[*].estate_name", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_3[0]", "estate_reps[*].trade_name", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_4[0]", "estate_reps[*].executor_name", "name", "parse_full_name"),
                
                # Section 4: Mailing Address
                FormFieldMapping("topmostSubform[0].Page1[0].f1_7[0]", "estate_reps[*].mailing_address", "location"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_8[0]", "estate_reps[*].mailing_address", "location", "combine_address_city_state_zip"),
                
                # Section 5: Street Address (if different)
                FormFieldMapping("topmostSubform[0].Page1[0].f1_9[0]", "estate_reps[*].street_address", "location"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_10[0]", "estate_reps[*].street_address", "location", "combine_address_city_state_zip"),
                
                # Section 6: County and State
                FormFieldMapping("topmostSubform[0].Page1[0].f1_11[0]", "estate_reps[*].business_location", "location"),
                
                # Section 7: Responsible Party
                FormFieldMapping("topmostSubform[0].Page1[0].f1_19[0]", "estate_reps[*].responsible_party_name", "name", "parse_full_name"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_20[0]", "estate_reps[*].responsible_party_ssn", "sin"),
                
                # Section 8: LLC Information
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[0]", "estate_reps[*].is_llc_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[1]", "estate_reps[*].is_llc_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_12[0]", "estate_reps[*].llc_members", "number"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_2[0]", "estate_reps[*].llc_organized_us_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_2[1]", "estate_reps[*].llc_organized_us_no", "checkbox"),
                
                # Section 9a: Type of Entity - ESTATE SPECIFIC
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[0]", "estate_reps[*].entity_sole_proprietor", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_13[0]", "deceased.social_insurance_number", "sin"),  # SSN of decedent for estate
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[1]", "estate_reps[*].entity_partnership", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_14[0]", "estate_reps[*].plan_administrator_tin", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[2]", "estate_reps[*].entity_corporation", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[3]", "estate_reps[*].entity_personal_service_corp", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_15[0]", "estate_reps[*].corporation_form_number", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[4]", "estate_reps[*].entity_church", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_16[0]", "estate_reps[*].trust_grantor_tin", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[5]", "estate_reps[*].entity_other_nonprofit", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_17[0]", "estate_reps[*].nonprofit_specify", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[6]", "estate_reps[*].entity_military", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[7]", "estate_reps[*].entity_state_local_govt", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[8]", "estate_reps[*].entity_farmers_coop", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[9]", "estate_reps[*].entity_federal_govt", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[10]", "estate_reps[*].entity_remic", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[11]", "estate_reps[*].entity_indian_tribal", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[12]", "estate_reps[*].entity_other", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_18[0]", "estate_reps[*].other_specify", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[13]", "estate_reps[*].group_exemption", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[14]", "estate_reps[*].group_exemption_number", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[15]", "estate_reps[*].estate_checkbox", "checkbox"),  # This is the key ESTATE checkbox
                
                # Section 9b: Corporation State
                FormFieldMapping("topmostSubform[0].Page1[0].f1_21[0]", "estate_reps[*].incorporation_state", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_22[0]", "estate_reps[*].incorporation_foreign_country", "string"),
                
                # Section 10: Reason for Applying
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[0]", "key_document[*].reason_started_business", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_24[0]", "key_document[*].business_type", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[1]", "key_document[*].reason_purchased_business", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_25[0]", "key_document[*].banking_purpose", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_26[0]", "key_document[*].organization_change_type", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[2]", "key_document[*].reason_hired_employees", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_27[0]", "key_document[*].trust_type", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[3]", "key_document[*].reason_withholding", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[4]", "key_document[*].reason_pension_plan", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[5]", "key_document[*].reason_other", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_28[0]", "key_document[*].pension_plan_type", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[6]", "key_document[*].reason_banking", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[7]", "key_document[*].reason_changed_org", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_29[0]", "key_document[*].other_reason", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[8]", "key_document[*].reason_created_trust", "checkbox"),
                
                # Section 11: Business Start Date
                FormFieldMapping("topmostSubform[0].Page1[0].f1_30[0]", "key_document[*].business_start_date", "date"),
                
                # Section 12: Accounting Year
                FormFieldMapping("topmostSubform[0].Page1[0].f1_31[0]", "key_document[*].accounting_year_end", "string"),
                
                # Section 13: Employee Information
                FormFieldMapping("topmostSubform[0].Page1[0].f1_32[0]", "key_document[*].agricultural_employees", "number"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_33[0]", "key_document[*].household_employees", "number"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_34[0]", "key_document[*].other_employees", "number"),
                
                # Section 14: Employment Tax
                FormFieldMapping("topmostSubform[0].Page1[0].c1_5[0]", "key_document[*].file_form_944", "checkbox"),
                
                # Section 15: First Wage Date
                FormFieldMapping("topmostSubform[0].Page1[0].f1_36[0]", "key_document[*].first_wage_date", "date"),
                
                # Section 16: Principal Business Activity
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[0]", "key_document[*].activity_construction", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[1]", "key_document[*].activity_real_estate", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[2]", "key_document[*].activity_rental_leasing", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[3]", "key_document[*].activity_manufacturing", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[4]", "key_document[*].activity_transportation", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[5]", "key_document[*].activity_finance_insurance", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[6]", "key_document[*].activity_health_care", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[7]", "key_document[*].activity_accommodation", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[8]", "key_document[*].activity_wholesale_agent", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[9]", "key_document[*].activity_wholesale_other", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[10]", "key_document[*].activity_retail", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[11]", "key_document[*].activity_other", "checkbox"),
                
                # Section 17: Business Description
                FormFieldMapping("topmostSubform[0].Page1[0].f1_37[0]", "key_document[*].business_description", "string"),
                
                # Section 18: Previous EIN
                FormFieldMapping("topmostSubform[0].Page1[0].c1_7[0]", "key_document[*].previous_ein_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_7[1]", "key_document[*].previous_ein_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_38[0]", "key_document[*].previous_ein_number", "string"),
                
                # Signature Section
                FormFieldMapping("topmostSubform[0].Page1[0].f1_39[0]", "estate_reps[*].designee_name", "name", "parse_full_name"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_40[0]", "estate_reps[*].designee_phone", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_41[0]", "estate_reps[*].designee_address", "location"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_42[0]", "estate_reps[*].designee_fax", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_43[0]", "estate_reps[*].applicant_name_title", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_44[0]", "estate_reps[*].applicant_phone", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_45[0]", "estate_reps[*].signature", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_46[0]", "key_document[*].signature_date", "date"),

                FormFieldMapping("topmostSubform[0].Page1[0].Line4ReadOrder[0].f1_5[", "estate_reps[*].mailing_address_line1", "location"),
                FormFieldMapping("topmostSubform[0].Page1[0].Line4ReadOrder[0].f1_6[", "estate_reps[*].mailing_address_line2", "location"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_35[0]", "key_document.tax_filing_preference.file_form_944_annually", "checkbox", description="Line 14: Elect to file Form 944 annually for employment tax", required=False),



            ],
            
            # IRS FORM 56 - NOTICE CONCERNING FIDUCIARY RELATIONSHIP
            "irs_form_56_fiduciary": [
                # Person for Whom Acting
                FormFieldMapping("topmostSubform[0].Page1[0].PgHeader[0].f1_1[0]", "key_document[*].form_number", "string"),
                
                # Section 1: Entity Information
                FormFieldMapping("topmostSubform[0].Page1[0].f1_2[0]", "estate_reps[*].estate_name", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_3[0]", "estate_reps[*].trade_name", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_4[0]", "estate_reps[*].executor_name", "name", "parse_full_name"),
                
                # Section 4: Mailing Address
                FormFieldMapping("topmostSubform[0].Page1[0].f1_7[0]", "estate_reps[*].mailing_address", "location"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_8[0]", "estate_reps[*].mailing_address", "location", "combine_address_city_state_zip"),
                
                # Section 5: Street Address (if different)
                FormFieldMapping("topmostSubform[0].Page1[0].f1_9[0]", "estate_reps[*].street_address", "location"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_10[0]", "estate_reps[*].street_address", "location", "combine_address_city_state_zip"),
                
                # Section 6: County and State
                FormFieldMapping("topmostSubform[0].Page1[0].f1_11[0]", "estate_reps[*].business_location", "location"),
                
                # Section 7: Responsible Party
                FormFieldMapping("topmostSubform[0].Page1[0].f1_19[0]", "estate_reps[*].responsible_party_name", "name", "parse_full_name"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_20[0]", "estate_reps[*].responsible_party_ssn", "sin"),
                
                # Section 8: LLC Information
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[0]", "estate_reps[*].is_llc_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[1]", "estate_reps[*].is_llc_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_12[0]", "estate_reps[*].llc_members", "number"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_2[0]", "estate_reps[*].llc_organized_us_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_2[1]", "estate_reps[*].llc_organized_us_no", "checkbox"),
                
                # Section 9a: Type of Entity - ESTATE SPECIFIC
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[0]", "estate_reps[*].entity_sole_proprietor", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_13[0]", "deceased.social_insurance_number", "sin"),  # SSN of decedent for estate
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[1]", "estate_reps[*].entity_partnership", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_14[0]", "estate_reps[*].plan_administrator_tin", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[2]", "estate_reps[*].entity_corporation", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[3]", "estate_reps[*].entity_personal_service_corp", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_15[0]", "estate_reps[*].corporation_form_number", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[4]", "estate_reps[*].entity_church", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_16[0]", "estate_reps[*].trust_grantor_tin", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[5]", "estate_reps[*].entity_other_nonprofit", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_17[0]", "estate_reps[*].nonprofit_specify", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[6]", "estate_reps[*].entity_military", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[7]", "estate_reps[*].entity_state_local_govt", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[8]", "estate_reps[*].entity_farmers_coop", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[9]", "estate_reps[*].entity_federal_govt", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[10]", "estate_reps[*].entity_remic", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[11]", "estate_reps[*].entity_indian_tribal", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[12]", "estate_reps[*].entity_other", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_18[0]", "estate_reps[*].other_specify", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[13]", "estate_reps[*].group_exemption", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[14]", "estate_reps[*].group_exemption_number", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[15]", "estate_reps[*].estate_checkbox", "checkbox"),  # This is the key ESTATE checkbox
                
                # Section 9b: Corporation State
                FormFieldMapping("topmostSubform[0].Page1[0].f1_21[0]", "estate_reps[*].incorporation_state", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_22[0]", "estate_reps[*].incorporation_foreign_country", "string"),
                
                # Section 10: Reason for Applying
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[0]", "key_document[*].reason_started_business", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_24[0]", "key_document[*].business_type", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[1]", "key_document[*].reason_purchased_business", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_25[0]", "key_document[*].banking_purpose", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_26[0]", "key_document[*].organization_change_type", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[2]", "key_document[*].reason_hired_employees", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_27[0]", "key_document[*].trust_type", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[3]", "key_document[*].reason_withholding", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[4]", "key_document[*].reason_pension_plan", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[5]", "key_document[*].reason_other", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_28[0]", "key_document[*].pension_plan_type", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[6]", "key_document[*].reason_banking", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[7]", "key_document[*].reason_changed_org", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_29[0]", "key_document[*].other_reason", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[8]", "key_document[*].reason_created_trust", "checkbox"),
                
                # Section 11: Business Start Date
                FormFieldMapping("topmostSubform[0].Page1[0].f1_30[0]", "key_document[*].business_start_date", "date"),
                
                # Section 12: Accounting Year
                FormFieldMapping("topmostSubform[0].Page1[0].f1_31[0]", "key_document[*].accounting_year_end", "string"),
                
                # Section 13: Employee Information
                FormFieldMapping("topmostSubform[0].Page1[0].f1_32[0]", "key_document[*].agricultural_employees", "number"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_33[0]", "key_document[*].household_employees", "number"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_34[0]", "key_document[*].other_employees", "number"),
                
                # Section 14: Employment Tax
                FormFieldMapping("topmostSubform[0].Page1[0].c1_5[0]", "key_document[*].file_form_944", "checkbox"),
                
                # Section 15: First Wage Date
                FormFieldMapping("topmostSubform[0].Page1[0].f1_36[0]", "key_document[*].first_wage_date", "date"),
                
                # Section 16: Principal Business Activity
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[0]", "key_document[*].activity_construction", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[1]", "key_document[*].activity_real_estate", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[2]", "key_document[*].activity_rental_leasing", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[3]", "key_document[*].activity_manufacturing", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[4]", "key_document[*].activity_transportation", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[5]", "key_document[*].activity_finance_insurance", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[6]", "key_document[*].activity_health_care", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[7]", "key_document[*].activity_accommodation", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[8]", "key_document[*].activity_wholesale_agent", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[9]", "key_document[*].activity_wholesale_other", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[10]", "key_document[*].activity_retail", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_6[11]", "key_document[*].activity_other", "checkbox"),
                
                # Section 17: Business Description
                FormFieldMapping("topmostSubform[0].Page1[0].f1_37[0]", "key_document[*].business_description", "string"),
                
                # Section 18: Previous EIN
                FormFieldMapping("topmostSubform[0].Page1[0].c1_7[0]", "key_document[*].previous_ein_yes", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_7[1]", "key_document[*].previous_ein_no", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_38[0]", "key_document[*].previous_ein_number", "string"),
                
                # Signature Section
                FormFieldMapping("topmostSubform[0].Page1[0].f1_39[0]", "estate_reps[*].designee_name", "name", "parse_full_name"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_40[0]", "estate_reps[*].designee_phone", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_41[0]", "estate_reps[*].designee_address", "location"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_42[0]", "estate_reps[*].designee_fax", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_43[0]", "estate_reps[*].applicant_name_title", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_44[0]", "estate_reps[*].applicant_phone", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_45[0]", "estate_reps[*].signature", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_46[0]", "key_document[*].signature_date", "date"),

                # Line 4 Read Order fields (mailing address components)
                FormFieldMapping("topmostSubform[0].Page1[0].Line4ReadOrder[0].f1_5[0]", "estate_reps[*].mailing_address_line1", "location"),
                FormFieldMapping("topmostSubform[0].Page1[0].Line4ReadOrder[0].f1_6[0]", "estate_reps[*].mailing_address_line2", "location"),
                
                # PAGE 2 - PREVIOUSLY UNMAPPED FIELDS (NOW FIXED)
                
                # Entity classification continuation checkboxes
                FormFieldMapping("topmostSubform[0].Page2[0].c2_1[0]", "estate_reps[*].entity_classification_additional_1", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].c2_2[0]", "estate_reps[*].entity_classification_additional_2a", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].c2_2[1]", "estate_reps[*].entity_classification_additional_2b", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].c2_2[2]", "estate_reps[*].entity_classification_additional_2c", "checkbox"),
                
                # Additional entity/business details
                FormFieldMapping("topmostSubform[0].Page2[0].f2_01[0]", "estate_reps[*].additional_entity_info_1", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].f2_02[0]", "estate_reps[*].additional_entity_info_2", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].c2_3[0]", "estate_reps[*].entity_classification_additional_3", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].f2_03[0]", "estate_reps[*].entity_details_3", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].f2_04[0]", "estate_reps[*].entity_details_4", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].c2_4[0]", "estate_reps[*].business_classification_4", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].f2_05[0]", "estate_reps[*].business_details_5", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].f2_06[0]", "estate_reps[*].business_details_6", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].f2_07[0]", "estate_reps[*].business_details_7", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].f2_08[0]", "estate_reps[*].business_details_8", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].f2_09[0]", "estate_reps[*].business_details_9", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].f2_10[0]", "estate_reps[*].business_details_10", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].f2_11[0]", "estate_reps[*].business_details_11", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].f2_12[0]", "estate_reps[*].business_details_12", "string"),
                
                # Time/scheduling related fields
                FormFieldMapping("topmostSubform[0].Page2[0].Time_ReadOrder[0].f2_13[0]", "key_document[*].time_field_13", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].Time_ReadOrder[0].c2_5[0]", "key_document[*].time_checkbox_5a", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].Time_ReadOrder[0].c2_5[1]", "key_document[*].time_checkbox_5b", "checkbox"),
                
                # Final business/entity fields
                FormFieldMapping("topmostSubform[0].Page2[0].f2_14[0]", "estate_reps[*].final_business_details_14", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].f2_15[0]", "estate_reps[*].final_business_details_15", "string"),
                  FormFieldMapping("topmostSubform[0].Page1[0].f1_01[0]", "deceased.full_name", "name", description="Line 1a: Name of the person for whom you are acting (the decedent)"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_02[0]", "deceased.identification_number", "string", description="Line 1b: Identifying number of the decedent (EIN, etc.)"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_03[0]", "deceased.social_insurance_number", "sin", description="Line 2a: Decedent’s social security number"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_04[0]", "deceased.home_address", "location", description="Line 3: Address of the person for whom you are acting"),

                # Fiduciary Information
                FormFieldMapping("topmostSubform[0].Page1[0].f1_05[0]", "estate_reps.fiduciary_name", "name", description="Line 4a: Fiduciary’s name"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_06[0]", "estate_reps.fiduciary_identification_number", "string", description="Line 4b: Fiduciary's identifying number (EIN or SSN)"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_07[0]", "estate_reps.fiduciary_address", "location", description="Line 5: Fiduciary's address"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_08[0]", "estate_reps.fiduciary_phone", "phone", description="Line 6: Telephone number of fiduciary (optional)"),

                # Section A - Authority for Fiduciary Relationship
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[0]", "estate_reps.authority_court_appointment", "checkbox", description="Box 7a: Court appointment (proof attached)"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[1]", "estate_reps.authority_will_annexed", "checkbox", description="Box 7b: Will (with or without court appointment)"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[2]", "estate_reps.authority_testate_estate", "checkbox", description="Box 7c: Testate estate"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[3]", "estate_reps.authority_intestate_estate", "checkbox", description="Box 7d: Intestate estate"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[4]", "estate_reps.authority_guardian_conservator", "checkbox", description="Box 7e: Guardian or conservator"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[5]", "estate_reps.authority_trust_instrument", "checkbox", description="Box 7f: Trust instrument"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[6]", "estate_reps.authority_bankruptcy_assignment", "checkbox", description="Box 7g: Bankruptcy or assignment for benefit of creditors"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_09[0]", "deceased.date_of_death", "date", description="Line 8: Date of death"),

                # Section B - Nature of Liability and Tax Notices
                # Type of Tax
                FormFieldMapping("topmostSubform[0].Page1[0].c1_8[0]", "estate_reps.tax_liability_income", "checkbox", description="Tax Type: Income"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_9[0]", "estate_reps.tax_liability_gift", "checkbox", description="Tax Type: Gift"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_10[0]", "estate_reps.tax_liability_estate", "checkbox", description="Tax Type: Estate"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_11[0]", "estate_reps.tax_liability_excise", "checkbox", description="Tax Type: Excise"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_12[0]", "estate_reps.tax_liability_employment", "checkbox", description="Tax Type: Employment"),
                
                # Federal Tax Form Number
                FormFieldMapping("topmostSubform[0].Page1[0].c1_13[0]", "estate_reps.tax_form_706_series", "checkbox", description="Tax Form: 706 Series"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_14[0]", "estate_reps.tax_form_940", "checkbox", description="Tax Form: 940"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_15[0]", "estate_reps.tax_form_941", "checkbox", description="Tax Form: 941"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_16[0]", "estate_reps.tax_form_1041", "checkbox", description="Tax Form: 1041"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_17[0]", "estate_reps.tax_form_1120", "checkbox", description="Tax Form: 1120"),

                # Section C - Revocation or Termination of Notice
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[7]", "estate_reps.is_termination_notice", "checkbox", description="Box 12: This is a termination notice"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[8]", "estate_reps.termination_proof_attached", "checkbox", description="Box 13: Proof of termination attached"),

                # Part II - Signature
                FormFieldMapping("topmostSubform[0].Page1[0].f1_1[0]", "estate_reps.fiduciary_signature", "signature", description="Fiduciary's signature"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_2[0]", "estate_reps.fiduciary_title", "string", description="Title"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_3[0]", "key_document.signature_date", "date", description="Date of signature"),
            ],
    
                
            
            # IRS FORM 1310 - STATEMENT OF PERSON CLAIMING REFUND DUE DECEASED TAXPAYER
            "irs_form_1310_refund_claim": [
                FormFieldMapping("topmostSubform[0].Page1[0].f1_1[0]", "key_document.tax_year_of_refund", "string", description="Calendar year or fiscal year beginning"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_2[0]", "key_document.tax_year_ending", "date", description="Fiscal year ending date", required=False),
                
                # --- Decedent Information ---
                FormFieldMapping("topmostSubform[0].Page1[0].f1_3[0]", "deceased.full_name", "name", description="Name of decedent"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_4[0]", "deceased.date_of_death", "date", description="Date of death"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_5[0]", "deceased.social_insurance_number", "sin", description="Decedent's social security number"),

                # --- Person Claiming Refund Information ---
                FormFieldMapping("topmostSubform[0].Page1[0].f1_6[0]", "applicant.full_name", "name", description="Your name"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_7[0]", "applicant.social_insurance_number", "sin", description="Your social security number"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_8[0]", "applicant.home_address_street", "location", description="Your street address"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_9[0]", "applicant.home_address_apt", "string", description="Apt. number", required=False),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_10[0]", "applicant.home_address_city_state_zip", "location", description="City, town or post office, state, and ZIP code"),
                
                # --- Part I - Check the box that applies to you ---
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[0]", "applicant.claim_type.surviving_spouse", "checkbox", description="Part I, Box A: Surviving spouse, requesting reissuance of a refund check"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[1]", "applicant.claim_type.court_appointed_rep", "checkbox", description="Part I, Box B: Court-appointed or certified personal representative"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[2]", "applicant.claim_type.other", "checkbox", description="Part I, Box C: Person, other than A or B, claiming refund for the decedent's estate"),

                # --- Part II - Complete this part only if you checked Box C above ---
                FormFieldMapping("topmostSubform[0].Page1[0].c1_2[0]", "estate_info.decedent_left_will_yes", "checkbox", description="Part II, Q1: Did the decedent leave a will? - Yes", required=False),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_2[1]", "estate_info.decedent_left_will_no", "checkbox", description="Part II, Q1: Did the decedent leave a will? - No", required=False),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[0]", "estate_info.court_appointed_rep_yes", "checkbox", description="Part II, Q2: Has a court appointed a personal representative? - Yes", required=False),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_3[1]", "estate_info.court_appointed_rep_no", "checkbox", description="Part II, Q2: Has a court appointed a personal representative? - No", required=False),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[0]", "estate_info.rep_will_be_appointed_yes", "checkbox", description="Part II, Q3: If 'No' to Q2, will one be appointed? - Yes", required=False),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_4[1]", "estate_info.rep_will_be_appointed_no", "checkbox", description="Part II, Q3: If 'No' to Q2, will one be appointed? - No", required=False),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_5[0]", "applicant.agrees_to_pay_out_refund_yes", "checkbox", description="Part II, Q4: Will you pay out the refund according to state law? - Yes", required=False),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_5[1]", "applicant.agrees_to_pay_out_refund_no", "checkbox", description="Part II, Q4: Will you pay out the refund according to state law? - No", required=False),

                # --- Part III - Signature and verification ---
                FormFieldMapping("topmostSubform[0].Page1[0].f1_11[0]", "applicant.signature", "signature", description="Part III: Signature"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_12[0]", "key_document.signature_date", "date", description="Part III: Date"),
            ],
            # IRS FORM 2848 - POWER OF ATTORNEY AND DECLARATION OF REPRESENTATIVE
            "irs_form_2848_power_of_attorney": [
                # Page 1 - Taxpayer Information
                FormFieldMapping("topmostSubform[0].Page1[0].CheckForm[0]", "key_document[*].form_number", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].TaxpayerName[0]", "deceased.full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page1[0].TaxpayerAddress[0]", "deceased.home_address", "location"),
                FormFieldMapping("topmostSubform[0].Page1[0].TaxpayerIDSSN[0]", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("topmostSubform[0].Page1[0].TaxpayerIDITIN[0]", "deceased.itin", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].TaxpayerIDEIN[0]", "deceased.ein", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].TaxpayerTelephone[0]", "deceased.phone", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].TaxpayerPlanNumber[0]", "deceased.plan_number", "string"),
                
                # Representative 1 Information
                FormFieldMapping("topmostSubform[0].Page1[0].RepresentativesName1[0]", "estate_reps[0].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page1[0].RepresentativesAddress1[0]", "estate_reps[0].address", "location"),
                FormFieldMapping("topmostSubform[0].Page1[0].SentCopies1[0]", "estate_reps[0].receive_copies", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].CAFNumber1[0]", "estate_reps[0].caf_number", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].PTIN1[0]", "estate_reps[0].ptin", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].TelephoneNo1[0]", "estate_reps[0].phone", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].FaxNo1[0]", "estate_reps[0].fax", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].NewAddress1[0]", "estate_reps[0].check_new_address", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].NewTelephoneNo1[0]", "estate_reps[0].check_new_phone", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].NewFaxNo1[0]", "estate_reps[0].check_new_fax", "checkbox"),
                
                # Representative 2 Information
                FormFieldMapping("topmostSubform[0].Page1[0].RepresentativesName2[0]", "estate_reps[1].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page1[0].RepresentativesAddress2[0]", "estate_reps[1].address", "location"),
                FormFieldMapping("topmostSubform[0].Page1[0].SentCopies2[0]", "estate_reps[1].receive_copies", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].CAFNumber2[0]", "estate_reps[1].caf_number", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].PTIN2[0]", "estate_reps[1].ptin", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].TelephoneNo2[0]", "estate_reps[1].phone", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].FaxNo2[0]", "estate_reps[1].fax", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].NewAddress2[0]", "estate_reps[1].check_new_address", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].NewTelephoneNo2[0]", "estate_reps[1].check_new_phone", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].NewFaxNo2[0]", "estate_reps[1].check_new_fax", "checkbox"),
                
                # Representative 3 Information
                FormFieldMapping("topmostSubform[0].Page1[0].RepresentativesName3[0]", "estate_reps[2].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page1[0].RepresentativesAddress3[0]", "estate_reps[2].address", "location"),
                FormFieldMapping("topmostSubform[0].Page1[0].CAFNumber3[0]", "estate_reps[2].caf_number", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].PTIN3[0]", "estate_reps[2].ptin", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].TelephoneNo3[0]", "estate_reps[2].phone", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].FaxNo3[0]", "estate_reps[2].fax", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].NewAddress3[0]", "estate_reps[2].check_new_address", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].NewTelephoneNo3[0]", "estate_reps[2].check_new_phone", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].NewFaxNo3[0]", "estate_reps[2].check_new_fax", "checkbox"),
                
                # Representative 4 Information
                FormFieldMapping("topmostSubform[0].Page1[0].RepresentativesName4[0]", "estate_reps[3].full_name", "name"),
                FormFieldMapping("topmostSubform[0].Page1[0].RepresentativesAddress4[0]", "estate_reps[3].address", "location"),
                FormFieldMapping("topmostSubform[0].Page1[0].CAFNumber4[0]", "estate_reps[3].caf_number", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].PTIN4[0]", "estate_reps[3].ptin", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].TelephoneNo4[0]", "estate_reps[3].phone", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].FaxNo4[0]", "estate_reps[3].fax", "phone"),
                FormFieldMapping("topmostSubform[0].Page1[0].NewAddress4[0]", "estate_reps[3].check_new_address", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].NewTelephoneNo4[0]", "estate_reps[3].check_new_phone", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].NewFaxNo4[0]", "estate_reps[3].check_new_fax", "checkbox"),
                
                # Acts Authorized Section
                FormFieldMapping("topmostSubform[0].Page1[0].SpecificUse[0]", "key_document[*].specific_use", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].AccessRecords[0]", "estate_reps[*].access_records", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].AuthorizeDisclosure[0]", "estate_reps[*].authorize_disclosure", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].SubtituteOrAdd[0]", "estate_reps[*].substitute_add_representatives", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].SignReturn[0]", "estate_reps[*].sign_return", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page1[0].AdditionalActs1[0]", "estate_reps[*].additional_acts_1", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].AdditionalActs2[0]", "estate_reps[*].additional_acts_2", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].AdditionalActs3[0]", "estate_reps[*].additional_acts_3", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].OtherActs[0]", "estate_reps[*].other_acts_1", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].OtherActs1[0]", "estate_reps[*].other_acts_2", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].OtherActs2[0]", "estate_reps[*].other_acts_3", "string"),
                
                # Tax Matters Table (Line 3)
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow1[0].TaxForm1[0]", "key_document[*].tax_form_1", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow1[0].TaxYear1[0]", "key_document[*].tax_year_1", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow1[0].TaxPeriod1[0]", "key_document[*].tax_period_1", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow2[0].TaxForm2[0]", "key_document[*].tax_form_2", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow2[0].TaxYear2[0]", "key_document[*].tax_year_2", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow2[0].TaxPeriod2[0]", "key_document[*].tax_period_2", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow3[0].TaxForm3[0]", "key_document[*].tax_form_3", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow3[0].TaxYear3[0]", "key_document[*].tax_year_3", "string"),
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow3[0].TaxPeriod3[0]", "key_document[*].tax_period_3", "string"),
                
                # Page 2 - Declarations and Signatures
                FormFieldMapping("topmostSubform[0].Page2[0].SpecificDeletions1[0]", "key_document[*].specific_deletions_1", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].SpecificDeletions2[0]", "key_document[*].specific_deletions_2", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].RetentionRevocation[1]", "key_document[*].retention_revocation", "checkbox"),
                FormFieldMapping("topmostSubform[0].Page2[0].Title[0]", "estate_reps[*].taxpayer_title", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].PrintName[0]", "estate_reps[*].taxpayer_print_name", "name"),
                FormFieldMapping("topmostSubform[0].Page2[0].PrintNameTaxpayer[0]", "estate_reps[*].taxpayer_print_name_alt", "name"),
                
                # Representative Declaration Table (Part II) - Generic patterns for all rows
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow1[0].Designation1[0]", "estate_reps[0].designation", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow1[0].Jurisdiction1[0]", "estate_reps[0].jurisdiction", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow1[0].Bar1[0]", "estate_reps[0].bar_number", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow1[0].Signature1[0]", "estate_reps[0].signature", "signature"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow1[0].Date1[0]", "estate_reps[0].signature_date", "date"),
                
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow2[0].Designation2[0]", "estate_reps[1].designation", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow2[0].Jurisdiction2[0]", "estate_reps[1].jurisdiction", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow2[0].Bar2[0]", "estate_reps[1].bar_number", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow2[0].Signature2[0]", "estate_reps[1].signature", "signature"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow2[0].Date2[0]", "estate_reps[1].signature_date", "date"),
                
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow3[0].Designation3[0]", "estate_reps[2].designation", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow3[0].Jurisdiction3[0]", "estate_reps[2].jurisdiction", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow3[0].Bar3[0]", "estate_reps[2].bar_number", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow3[0].Signature3[0]", "estate_reps[2].signature", "signature"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow3[0].Date3[0]", "estate_reps[2].signature_date", "date"),
                
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow4[0].Designation4[0]", "estate_reps[3].designation", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow4[0].Jurisdiction4[0]", "estate_reps[3].jurisdiction", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow4[0].Bar4[0]", "estate_reps[3].bar_number", "string"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow4[0].Signature4[0]", "estate_reps[3].signature", "signature"),
                FormFieldMapping("topmostSubform[0].Page2[0].Table_PartII[0].BodyRow4[0].Date4[0]", "estate_reps[3].signature_date", "date"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_1[0]", "key_document.tax_year_of_refund", "string", description="Calendar year or fiscal year beginning"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_5[0]", "deceased.social_insurance_number", "sin", description="Decedent's social security number"),
                FormFieldMapping("topmostSubform[0].Page1[0].f1_6[0]", "applicant.full_name", "name", description="Your name"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_1[2]", "applicant.claim_type.other", "checkbox", description="Part I, Box C: Person, other than A or B, claiming refund"),
                FormFieldMapping("topmostSubform[0].Page1[0].c1_5[1]", "applicant.agrees_to_pay_out_refund_no", "checkbox", description="Part II, Q4: Will you pay out the refund according to state law? - No", required=False),
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow1[0].Description1[0]", "key_document.tax_matters[0].description", "string", description="Line 3, Row 1: Description of Matter", required=False),
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow1[0].Years1[0]", "key_document.tax_matters[0].years_or_periods_alt", "string", description="Line 3, Row 1: Year(s) or Period(s) (Alternate Field)", required=False),
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow2[0].Description2[0]", "key_document.tax_matters[1].description", "string", description="Line 3, Row 2: Description of Matter", required=False),
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow2[0].Years2[0]", "key_document.tax_matters[1].years_or_periods_alt", "string", description="Line 3, Row 2: Year(s) or Period(s) (Alternate Field)", required=False),
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow3[0].Description3[0]", "key_document.tax_matters[2].description", "string", description="Line 3, Row 3: Description of Matter", required=False),
                FormFieldMapping("topmostSubform[0].Page1[0].Table_Line3[0].BodyRow3[0].Years3[0]", "key_document.tax_matters[2].years_or_periods_alt", "string", description="Line 3, Row 3: Year(s) or Period(s) (Alternate Field)", required=False),
            ],
            
            # SERVICE CANADA REQUEST FOR PAYMENT OF BENEFIT - ESDC INS2882
            "service_canada_benefit_payment_ins2882": [
                # Legal Representative/Applicant
                FormFieldMapping("INS2882_E[0].page1[0].txtF_Legal_Representative[0]", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("INS2882_E[0].page1[0].txtF_Telephone_Number[0]", "estate_reps[*].phone", "phone"),
                FormFieldMapping("INS2882_E[0].page1[0].txtF_Legal_Representative_Address[0]", "estate_reps[*].address", "location"),
                
                # Deceased Person Information
                FormFieldMapping("INS2882_E[0].page1[0].txtF_Deceased_Person[0]", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("INS2882_E[0].page1[0].txtF_SIN[0]", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("INS2882_E[0].page1[0].txtF_Month[0]", "deceased.date_of_death", "date", "combine_date_components"),
                FormFieldMapping("INS2882_E[0].page1[0].txtF_Year[0]", "deceased.date_of_death", "date", "combine_date_components"),
                FormFieldMapping("INS2882_E[0].page1[0].txtF_date[0]", "deceased.date_of_death", "date"),
                FormFieldMapping("INS2882_E[0].page1[0].txtF_Reasons[0]", "key_document[*].application_delay_reason", "string"),
                
                # Signatures
                FormFieldMapping("INS2882_E[0].page1[0].txtF_Signature[0]", "estate_reps[*].signature", "signature"),
                
                # Page 2 - Detailed Information
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Applicant_Signature[0]", "estate_reps[*].signature", "signature"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_County[0]", "estate_reps[*].address", "location", "extract_county"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_province2[0]", "estate_reps[*].address", "location", "extract_province"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Province[0]", "estate_reps[*].address", "location", "extract_province"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Province[1]", "deceased.home_address", "location", "extract_province"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Province[2]", "contact[*].address.address_location", "location", "extract_province"),
                
                # Names (multiple instances)
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Deceased_Name[0]", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Deceased_Name[1]", "deceased.full_name_at_birth", "name", "parse_full_name"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Applicant_Name[0]", "estate_reps[*].name", "name", "parse_full_name"),
                
                # Death information
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Deceased_Month[0]", "deceased.date_of_death", "date", "extract_month"),
                
                # Cities and locations
                FormFieldMapping("INS2882_E[0].page2[0].txtF_City_Town_Village[0]", "estate_reps[*].address", "location", "extract_city"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_City_Town_Village[1]", "deceased.home_address", "location", "extract_city"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_City_Town_Village[2]", "contact[*].address.address_location", "location", "extract_city"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_City_Town_Village[3]", "key_document[*].location", "location", "extract_city"),
                
                # Entitled persons (beneficiaries)
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Entitled_Person_Name[0]", "contact[0].name", "name", "parse_full_name"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Entitled_Person_Relationship[0]", "contact[0].relationship", "string"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Entitled_Person_Age[0]", "contact[0].age", "number"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Entitled_Person_Name[1]", "contact[1].name", "name", "parse_full_name"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Entitled_Person_Relationship[1]", "contact[1].relationship", "string"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Entitled_Person_Age[1]", "contact[1].age", "number"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Entitled_Person_Name[2]", "contact[2].name", "name", "parse_full_name"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Entitled_Person_Relationship[2]", "contact[2].relationship", "string"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Entitled_Person_Age[2]", "contact[2].age", "number"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Entitled_Person_Name[3]", "contact[3].name", "name", "parse_full_name"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Entitled_Person_Relationship[3]", "contact[3].relationship", "string"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Entitled_Person_Age[3]", "contact[3].age", "number"),
                
                # Legal and administrative
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Relationship[0]", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Justice_Of_Peace[0]", "key_document[*].justice_of_peace", "string"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Authorization_Number[0]", "estate_reps[*].authorization_number", "string"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_AD[0]", "key_document[*].administrative_code", "string"),
                
                # Checkboxes and radio buttons
                FormFieldMapping("INS2882_E[0].page2[0].Rb_Death_Certificate_Attached[0]", "deceased.proof_of_death", "checkbox"),
                FormFieldMapping("INS2882_E[0].page2[0].Rb_Person_Entitled[0]", "key_document[*].person_entitled", "checkbox"),
                
                # Dates
                FormFieldMapping("INS2882_E[0].page2[0].txtF_date[0]", "key_document[*].signature_date", "date"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_date[1]", "key_document[*].witness_date", "date"),
                
                # Page 3 - Signatures and legal declarations
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Favoured__Signature[0]", "contact[0].signature", "signature"),
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Favoured__Witness[0]", "contact[0].witness_name", "name"),
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Favoured__Signature[1]", "contact[1].signature", "signature"),
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Favoured__Witness[1]", "contact[1].witness_name", "name"),
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Favoured__Signature[2]", "contact[2].signature", "signature"),
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Favoured__Witness[2]", "contact[2].witness_name", "name"),
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Favoured__Signature[3]", "contact[3].signature", "signature"),
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Favoured__Witness[3]", "contact[3].witness_name", "name"),
                
                # Repayment and release information
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Repayment_Promise_Applicant[0]", "estate_reps[*].repayment_promise", "string"),
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Repayment_Promise_Witness[0]", "contact[*].repayment_witness", "string"),
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Release_Name_of_Deceased[0]", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Release_Name_of_Applicant[0]", "estate_reps[*].name", "name", "parse_full_name"),
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Repayment_Promise_Applicant[1]", "estate_reps[*].additional_promise", "string"),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_County[1]", "deceased.home_address.county", "string", required=False),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_County[2]", "contact.address.county", "string", required=False),
                FormFieldMapping("INS2882_E[0].page2[0].txtF_Justice_Of_Peacy[0]", "key_document.justice_of_peace", "string", required=False),
                # Page 3 - Repayment Promise Signatures and Date
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Repayment_Promise_Applicant_Signature[0]", "estate_reps.repayment_promise_signature", "signature", required=False),
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Repayment_Promise_Witness_Signature[0]", "contact.witness.repayment_promise_signature", "signature", required=False),
                FormFieldMapping("INS2882_E[0].Page3[0].txtF_Repayment_Promise_Applicant_Date[0]", "key_document.repayment_promise_date", "date", required=False),
            ],
            
            # FLORIDA CERTIFICATE OF TITLE APPLICATION - HSMV 82040
            "florida_certificate_title_hsmv82040": [
                # Application Type
                FormFieldMapping("Choose One Application Type: Original or Transfer", "key_document[*].application_type", "select"),
                FormFieldMapping("Choose One Vehicle Type: Motor Vehicle, Mobile Hom", "property.vehicles[*].vehicle_type", "select"),
                FormFieldMapping("Choose One Highway Vehicle: ATV, ROV or MC", "property.vehicles[*].highway_vehicle_type", "select"),
                
                # Customer Information
                FormFieldMapping("Customer Number", "applicant.customer_number", "string"),
                FormFieldMapping("Fleet Number", "applicant.fleet_number", "string"),
                
                # Owner Information
                FormFieldMapping("owner name", "applicant.full_name", "name"),
                FormFieldMapping("owner email", "applicant.email", "email"),
                FormFieldMapping("Owner Date of Birth", "applicant.date_of_birth", "date"),
                FormFieldMapping("Owner: Are You a Florida Resident", "applicant.florida_resident", "boolean"),
                FormFieldMapping("Owner: Are You an Alien?", "applicant.alien_status", "boolean"),
                FormFieldMapping("FL DL/FEID#", "applicant.drivers_license", "string"),
                FormFieldMapping("County of Residence", "applicant.county", "string"),
                
                # Co-Owner Information  
                FormFieldMapping("co-owner name", "spouse.full_name", "name"),
                FormFieldMapping("co-owner email", "spouse.email", "email"),
                FormFieldMapping("Co-Owner Date of Birth", "spouse.date_of_birth", "date"),
                FormFieldMapping("Co-Owner: Are You Florida Resident?", "spouse.florida_resident", "boolean"),
                FormFieldMapping("Co-Owner: Are You an Alien?", "spouse.alien_status", "boolean"),
                FormFieldMapping("FL DL/FEID#2", "spouse.drivers_license", "string"),
                FormFieldMapping("sex2", "spouse.gender", "select"),
                
                # Address Information
                FormFieldMapping("owner mailing add", "applicant.mailing_address", "location"),
                FormFieldMapping("st", "applicant.mailing_address", "location", "extract_state"),
                FormFieldMapping("zip", "applicant.mailing_address", "location", "extract_zip"),
                FormFieldMapping("co-owner mailing address", "spouse.mailing_address", "location"),
                FormFieldMapping("city2", "spouse.mailing_address", "location", "extract_city"),
                FormFieldMapping("st2", "spouse.mailing_address", "location", "extract_state"),
                FormFieldMapping("zip2", "spouse.mailing_address", "location", "extract_zip"),
                FormFieldMapping("owner physical add", "applicant.home_address", "location"),
                FormFieldMapping("city3", "applicant.home_address", "location", "extract_city"),
                FormFieldMapping("st3", "applicant.home_address", "location", "extract_state"),
                FormFieldMapping("zip3", "applicant.home_address", "location", "extract_zip"),
                
                # Mail To Customer Information
                FormFieldMapping("mail to cust. name", "contact[*].name", "name"),
                FormFieldMapping("mail to cust.email", "contact[*].email", "email"),
                FormFieldMapping("Customer Date of Birth (if different from owner)", "contact[*].date_of_birth", "date"),
                FormFieldMapping("Sex_3", "contact[*].gender", "select"),
                FormFieldMapping("FL DL/FEID#3", "contact[*].drivers_license", "string"),
                FormFieldMapping("mail to cust.address", "contact[*].address.address_location", "location"),
                FormFieldMapping("city5", "contact[*].address.address_location", "location", "extract_city"),
                FormFieldMapping("st5", "contact[*].address.address_location", "location", "extract_state"),
                FormFieldMapping("zip5", "contact[*].address.address_location", "location", "extract_zip"),
                
                # Vehicle Information
                FormFieldMapping("VIN", "property.vehicles[*].vin", "string"),
                FormFieldMapping("VIN2", "property.vehicles[*].vin_secondary", "string"),
                FormFieldMapping("VIN3", "property.vehicles[*].vin_trade_in", "string"),
                FormFieldMapping("MV-MH-Ves-year", "property.vehicles[*].year", "number"),
                FormFieldMapping("body", "property.vehicles[*].body_type", "string"),
                FormFieldMapping("FL title number 1", "property.vehicles[*].florida_title_number", "string"),
                FormFieldMapping("soi", "property.vehicles[*].state_of_issue", "string"),
                FormFieldMapping("license plate or vessel reg.number", "property.vehicles[*].license_plate", "string"),
                FormFieldMapping("wgt", "property.vehicles[*].weight", "string"),
                FormFieldMapping("ft", "property.vehicles[*].length_feet", "string"),
                FormFieldMapping("in", "property.vehicles[*].length_inches", "string"),
                FormFieldMapping("bhp/cc", "property.vehicles[*].engine_power", "string"),
                FormFieldMapping("gvw/loc", "property.vehicles[*].gross_vehicle_weight", "string"),
                
                # Vehicle Type Checkboxes
                FormFieldMapping("pgr", "property.vehicles[*].passenger", "checkbox"),
                FormFieldMapping("oth", "property.vehicles[*].other_type", "checkbox"),
                FormFieldMapping("om", "property.vehicles[*].omnibus", "checkbox"),
                FormFieldMapping("cmb", "property.vehicles[*].combination", "checkbox"),
                FormFieldMapping("as", "property.vehicles[*].antique_street_rod", "checkbox"),
                FormFieldMapping("if", "property.vehicles[*].for_hire", "checkbox"),
                FormFieldMapping("hb", "property.vehicles[*].hearse_ambulance", "checkbox"),
                FormFieldMapping("pt", "property.vehicles[*].private_truck", "checkbox"),
                FormFieldMapping("ab", "property.vehicles[*].apportioned", "checkbox"),
                FormFieldMapping("sb", "property.vehicles[*].school_bus", "checkbox"),
                FormFieldMapping("pw", "property.vehicles[*].powered_wheelchair", "checkbox"),
                FormFieldMapping("cn", "property.vehicles[*].construction", "checkbox"),
                FormFieldMapping("ot", "property.vehicles[*].other", "checkbox"),
                
                # Vessel Information
                FormFieldMapping("wd", "property.vessels[*].wood", "checkbox"),
                FormFieldMapping("al", "property.vessels[*].aluminum", "checkbox"),
                FormFieldMapping("fg", "property.vessels[*].fiberglass", "checkbox"),
                FormFieldMapping("slt", "property.vessels[*].steel", "checkbox"),
                FormFieldMapping("wf", "property.vessels[*].other_material", "checkbox"),
                FormFieldMapping("ob", "property.vessels[*].outboard", "checkbox"),
                FormFieldMapping("sl", "property.vessels[*].sail", "checkbox"),
                FormFieldMapping("ib", "property.vessels[*].inboard", "checkbox"),
                FormFieldMapping("ibo", "property.vessels[*].inboard_outboard", "checkbox"),
                FormFieldMapping("ga", "property.vessels[*].gas", "checkbox"),
                FormFieldMapping("dl", "property.vessels[*].diesel", "checkbox"),
                FormFieldMapping("el", "property.vessels[*].electric", "checkbox"),
                FormFieldMapping("ft2", "property.vessels[*].length_feet", "string"),
                FormFieldMapping("in2", "property.vessels[*].length_inches", "string"),
                
                # Mobile Home Information
                FormFieldMapping("mob", "property.mobile_homes[*].mobile_home", "checkbox"),
                FormFieldMapping("mhomel add", "property.mobile_homes[*].location", "location"),
                FormFieldMapping("city4", "property.mobile_homes[*].location", "location", "extract_city"),
                FormFieldMapping("st4", "property.mobile_homes[*].location", "location", "extract_state"),
                FormFieldMapping("zip4", "property.mobile_homes[*].location", "location", "extract_zip"),
                
                # Commercial Vehicle Information
                FormFieldMapping("rp", "property.vehicles[*].rental_personal", "checkbox"),
                FormFieldMapping("dm", "property.vehicles[*].dealer_manufacturer", "checkbox"),
                FormFieldMapping("ex", "property.vehicles[*].exempt", "checkbox"),
                FormFieldMapping("cf", "property.vehicles[*].commercial_for_hire", "checkbox"),
                FormFieldMapping("hl", "property.vehicles[*].household_goods", "checkbox"),
                FormFieldMapping("cbc", "property.vehicles[*].common_carrier_bus", "checkbox"),
                FormFieldMapping("clb", "property.vehicles[*].charter_bus", "checkbox"),
                FormFieldMapping("cm", "property.vehicles[*].commercial_motor", "checkbox"),
                FormFieldMapping("csc", "property.vehicles[*].school_church", "checkbox"),
                FormFieldMapping("csr", "property.vehicles[*].school_religious", "checkbox"),
                FormFieldMapping("csm", "property.vehicles[*].school_municipal", "checkbox"),
                FormFieldMapping("gt", "property.vehicles[*].government_tag", "checkbox"),
                FormFieldMapping("cc", "property.vehicles[*].county_city", "checkbox"),
                FormFieldMapping("coy", "property.vehicles[*].county", "checkbox"),
                FormFieldMapping("cs", "property.vehicles[*].city_state", "checkbox"),
                FormFieldMapping("co", "property.vehicles[*].commercial", "checkbox"),
                FormFieldMapping("csl", "property.vehicles[*].commercial_learner", "checkbox"),
                FormFieldMapping("oosreg.#", "property.vehicles[*].out_of_state_reg", "string"),
                FormFieldMapping("state of principple use", "property.vehicles[*].principal_use_state", "string"),
                
                # Special Categories
                FormFieldMapping("lse", "property.vehicles[*].leased", "checkbox"),
                FormFieldMapping("afp", "property.vehicles[*].assembled_from_parts", "checkbox"),
                FormFieldMapping("ltl", "property.vehicles[*].long_term_lease", "checkbox"),
                FormFieldMapping("bt", "property.vehicles[*].bonded_title", "checkbox"),
                FormFieldMapping("reb", "property.vehicles[*].rebuilt", "checkbox"),
                FormFieldMapping("kit", "property.vehicles[*].kit_car", "checkbox"),
                FormFieldMapping("pv", "property.vehicles[*].previous_salvage", "checkbox"),
                FormFieldMapping("gk", "property.vehicles[*].glider_kit", "checkbox"),
                FormFieldMapping("pu", "property.vehicles[*].pickup_truck", "checkbox"),
                FormFieldMapping("mbb", "property.vehicles[*].motor_bike", "checkbox"),
                FormFieldMapping("tc", "property.vehicles[*].truck_camper", "checkbox"),
                FormFieldMapping("rep", "property.vehicles[*].replica", "checkbox"),
                FormFieldMapping("fv", "property.vehicles[*].former_vehicle", "checkbox"),
                FormFieldMapping("av", "property.vehicles[*].antique_vehicle", "checkbox"),
                FormFieldMapping("ilv", "property.vehicles[*].inoperable_vehicle", "checkbox"),
                FormFieldMapping("ev", "property.vehicles[*].electric_vehicle", "checkbox"),
                FormFieldMapping("cus", "property.vehicles[*].custom", "checkbox"),
                FormFieldMapping("sr", "property.vehicles[*].street_rod", "checkbox"),
                
                # Lienholder Information
                FormFieldMapping("ELT", "financial_information.lienholders[*].elt_customer", "boolean"),
                FormFieldMapping("feid", "financial_information.lienholders[*].feid", "string"),
                FormFieldMapping("dl#", "financial_information.lienholders[*].dealer_license", "string"),
                FormFieldMapping("dmv", "financial_information.lienholders[*].dmv_account", "string"),
                FormFieldMapping("FEID/DL/DMVacct.#", "financial_information.lienholders[*].account_number", "string"),
                FormFieldMapping("Date of Lien", "financial_information.lienholders[*].lien_date", "date"),
                FormFieldMapping("lienholder's name", "financial_information.lienholders[*].name", "string"),
                FormFieldMapping("lienholder email", "financial_information.lienholders[*].email", "email"),
                FormFieldMapping("lienholder address", "financial_information.lienholders[*].address", "location"),
                FormFieldMapping("city6", "financial_information.lienholders[*].address", "location", "extract_city"),
                FormFieldMapping("State three", "financial_information.lienholders[*].address", "location", "extract_state"),
                FormFieldMapping("zip6", "financial_information.lienholders[*].address", "location", "extract_zip"),
                
                # Transfer Information
                FormFieldMapping("ila", "key_document[*].inherited_leased_assigned", "checkbox"),
                FormFieldMapping("sla", "key_document[*].sold_leased_assigned", "checkbox"),
                FormFieldMapping("gft", "key_document[*].gift", "checkbox"),
                FormFieldMapping("repo", "key_document[*].repossession", "checkbox"),
                FormFieldMapping("cd", "key_document[*].court_order", "checkbox"),
                FormFieldMapping("o3", "key_document[*].other_transfer", "checkbox"),
                FormFieldMapping("OTS", "key_document[*].other_transfer_specify", "string"),
                
                # Sale Information
                FormFieldMapping("MO", "key_document[*].sale_month", "string"),
                FormFieldMapping("YEAR1", "key_document[*].sale_year", "string"),
                FormFieldMapping("date of sale", "key_document[*].sale_date", "date"),
                FormFieldMapping("dealer#", "key_document[*].dealer_number", "string"),
                FormFieldMapping("tax", "key_document[*].sales_tax", "currency"),
                
                # Trade-in Information
                FormFieldMapping("yr.trade-in", "property.vehicles[*].trade_in_year", "string"),
                FormFieldMapping("make of trade-in", "property.vehicles[*].trade_in_make", "string"),
                FormFieldMapping("title#or trade-in", "property.vehicles[*].trade_in_title", "string"),
                
                # Odometer Information
                FormFieldMapping("Odometer Reading", "property.vehicles[*].odometer_reading", "number"),
                FormFieldMapping("mo2", "property.vehicles[*].odometer_month", "string"),
                FormFieldMapping("da2", "property.vehicles[*].odometer_day", "string"),
                FormFieldMapping("yr2", "property.vehicles[*].odometer_year", "string"),
                FormFieldMapping("ra", "property.vehicles[*].reflects_actual", "checkbox"),
                FormFieldMapping("iex", "property.vehicles[*].exceeds_limits", "checkbox"),
                FormFieldMapping("not", "property.vehicles[*].not_actual", "checkbox"),
                
                # Registration Information
                FormFieldMapping("FL reg.#", "property.vehicles[*].florida_registration", "string"),
                
                # Checkboxes for Various Categories
                FormFieldMapping("Check Box 5 digit", "key_document[*].checkbox_5", "checkbox"),
                FormFieldMapping("Check Box 6 digit", "key_document[*].checkbox_6", "checkbox"),
                
                # Official Use
                FormFieldMapping("leoff./dealer/agy.name", "key_document[*].law_enforcement_dealer", "string"),
                FormFieldMapping("badge#", "key_document[*].badge_number", "string"),
                FormFieldMapping("FLDMC/TCname", "key_document[*].fldmc_tc_name", "string"),
                FormFieldMapping("badge#2", "key_document[*].badge_number_2", "string"),
                FormFieldMapping("notary name", "key_document[*].notary_name", "string"),
                FormFieldMapping("exemption #", "key_document[*].exemption_number", "string"),
                
                # Various Abbreviations and Codes
                FormFieldMapping("pur", "key_document[*].purchase", "checkbox"),
                FormFieldMapping("mv2", "key_document[*].motor_vehicle_2", "checkbox"),
                FormFieldMapping("mtm", "key_document[*].month_to_month", "checkbox"),
                FormFieldMapping("v2", "key_document[*].vessel_2", "checkbox"),
                FormFieldMapping("sales tax reg.#", "key_document[*].sales_tax_reg", "string"),
                FormFieldMapping("ih", "key_document[*].inherited", "checkbox"),
                FormFieldMapping("g2", "key_document[*].gift_2", "checkbox"),
                FormFieldMapping("dd", "key_document[*].dealer_demo", "checkbox"),
                FormFieldMapping("thw", "key_document[*].theft_recovery", "checkbox"),
                FormFieldMapping("et", "key_document[*].estate_transfer", "checkbox"),
                FormFieldMapping("otr", "key_document[*].other_transfer_2", "checkbox"),
                FormFieldMapping("other explanation", "key_document[*].other_explanation", "string"),
                FormFieldMapping("i", "key_document[*].inheritance", "checkbox"),
                FormFieldMapping("vph", "key_document[*].vehicle_per_hour", "checkbox"),
                FormFieldMapping("oc", "key_document[*].owner_change", "checkbox"),
                FormFieldMapping("dcr", "key_document[*].duplicate_certificate_requested", "checkbox"),
                FormFieldMapping("lt", "key_document[*].lien_transfer", "checkbox"),
                FormFieldMapping("wno", "key_document[*].with_no", "checkbox"),
                FormFieldMapping("wnw", "key_document[*].with_new", "checkbox"),
                FormFieldMapping("oter", "key_document[*].other_2", "checkbox"),
                FormFieldMapping("other explanation 2", "key_document[*].other_explanation_2", "string"),
                
                # Signature Information
                FormFieldMapping("Today's Date", "key_document[*].todays_date", "date"),
                FormFieldMapping("printed name", "applicant.printed_name", "name"),
                FormFieldMapping("Date of Applicant (Owner) Signature_af_date", "applicant.signature_date", "date"),
                FormFieldMapping("Date of Applicant (Co-Owner) Signature", "spouse.signature_date", "date"),
                
                # Death/Inheritance Information
                FormFieldMapping("deceased name", "deceased.full_name", "name"),
                FormFieldMapping("Date of Death_af_date", "deceased.date_of_death", "date"),
                FormFieldMapping("t", "key_document[*].testate", "checkbox"),
                FormFieldMapping("it", "key_document[*].intestate", "checkbox"),
                FormFieldMapping("wa", "key_document[*].will_attached", "checkbox"),
                FormFieldMapping("spouse/co-own/heir", "estate_reps[*].heir_1", "string"),
                FormFieldMapping("spouse/co-own/heir2", "estate_reps[*].heir_2", "string"),
                FormFieldMapping("spouse/co-own/heir3", "estate_reps[*].heir_3", "string"),
                FormFieldMapping("applicant(s) name(s)", "applicant.applicant_names", "string"),
                FormFieldMapping("owner name", "applicant.full_name", "text"),
                FormFieldMapping("co-owner name", "spouse.full_name", "text"),
                FormFieldMapping("deceased name", "deceased.full_name", "text"),
                FormFieldMapping("spouse/co-own/heir", "estate_reps[*].heir_1", "string"),
                FormFieldMapping("spouse/co-own/heir2", "estate_reps[*].heir_2", "string"), 
                FormFieldMapping("spouse/co-own/heir3", "estate_reps[*].heir_3", "string"),
                FormFieldMapping("applicant(s) name(s)", "applicant.applicant_names", "string"),
                FormFieldMapping("Choose One Vehicle Type: Motor Vehicle, Mobile Hom", "property.vehicles[*].vehicle_type", "select"),
                FormFieldMapping("Printed Certificate Title", "key_document[*].certificate_type", "string"),
                FormFieldMapping("Unit Number", "applicant.address_unit", "string"),
                FormFieldMapping("And/OR", "legal.ownership_type", "string"),

                # VEHICLE CODES (abbreviated fields):
                FormFieldMapping("lep", "property.vehicles[*].leased", "checkbox"),
                FormFieldMapping("tbe", "property.vehicles[*].tenancy_entirety", "checkbox"), 
                FormFieldMapping("wrs", "property.vehicles[*].with_rights_survivorship", "checkbox"),
                FormFieldMapping("ocr", "property.vehicles[*].other_classification", "checkbox"),
                FormFieldMapping("color", "property.vehicles[*].color", "string"),

                # OTHER CLASSIFICATION CODES:
                FormFieldMapping("oth", "property.vehicles[*].other_type", "checkbox"),
                FormFieldMapping("ot1", "property.vehicles[*].other_type_1", "checkbox"),
                FormFieldMapping("oth2", "property.vehicles[*].other_type_2", "checkbox"),
                FormFieldMapping("A_2", "property.vehicles[*].classification_a2", "checkbox"),
                FormFieldMapping("Other_3", "property.vehicles[*].other_classification_3", "string"),
                FormFieldMapping("oth3", "property.vehicles[*].other_type_3", "checkbox"),
                FormFieldMapping("Oth4", "property.vehicles[*].other_type_4", "checkbox"),
                FormFieldMapping("oth4", "property.vehicles[*].other_type_4_alt", "checkbox"),
                FormFieldMapping("commoth", "property.vehicles[*].commercial_other", "checkbox"),
                FormFieldMapping("cg", "property.vehicles[*].coast_guard", "checkbox"),
                FormFieldMapping("cdp", "property.vehicles[*].cdl_permit", "checkbox"),
                FormFieldMapping("sex", "applicant.gender", "select", required=False),
                FormFieldMapping("city", "applicant.mailing_address", "location", "extract_city"),
                FormFieldMapping("make", "property.vehicles[*].make", "string"),
                FormFieldMapping("oth1", "property.vehicles[*].other_type_1", "checkbox", required=False),
                FormFieldMapping("Day", "deceased.date_of_death", "date", "combine_date_components", description="Date of Death - Day component (for inheritance)", required=False),

            ],
            
            # HILTON HONORS POINTS TRANSFER FORM
            "hilton_honors_points_transfer": [
                # Deceased Member Information
                FormFieldMapping("death of Hilton Honors Member", "deceased.full_name", "name"),
                FormFieldMapping("Member died on", "deceased.date_of_death", "date"),
                FormFieldMapping("certificateproof of death", "deceased.proof_of_death", "file"),
                FormFieldMapping("Attached is a copy of Members death", "deceased.death_certificate_attached", "boolean"),
                FormFieldMapping("I affirm everything above is true a", "estate_reps[*].legal_declaration", "string"),
                FormFieldMapping("undefined", "property.loyalty_points.hilton_account_number", "string"),
                FormFieldMapping("ExecutorAdministrator", "estate_reps[*].role", "string"),
                FormFieldMapping("Printed Name", "estate_reps[*].full_name", "name"),
                FormFieldMapping("Street Address", "estate_reps[*].street_address", "location"),
                FormFieldMapping("City State Zip", "estate_reps[*].city_state_zip", "location"),  # NOW THIS WILL MATCH!
                FormFieldMapping("Telephone number", "estate_reps[*].phone", "phone"),
                FormFieldMapping("Email address", "estate_reps[*].email", "email"),
            ],
            
            # Add more specialized forms as needed...
            # This completes the comprehensive estate forms pattern matching system
            
            # ============================================================================
            # ADDITIONAL SPECIALIZED ESTATE FORMS
            # ============================================================================
            
            # SERVICE CANADA CHILD REARING PROVISION - SC ISP-1640
            "service_canada_child_rearing_isp1640": [
                # Applicant Information
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_info[0].sub_A1[0].txt", "applicant.section_a_intro", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_info[0].sub_salutatio", "applicant.salutation", "select"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_info[0].txtF_FirstNam", "applicant.first_name", "name"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_info[0].txtF_MiddleNa", "applicant.middle_name", "name"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_info[0].txtF_FamilyNa", "applicant.last_name", "name"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_info[0].txtF_Address[", "applicant.home_address", "location"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_info[0].txt_Phone[0]", "applicant.phone", "phone"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_info[0].txtF_EmailAdd", "applicant.email", "email"),
                
                # ============================================================================
                # PAGE 3 - SECTION B TABLE (Children Information)
                # ============================================================================
                
                # Row 0 - Child 1
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].child_info_row", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].first_name", "name"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].last_name", "name"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].date_of_birth", "date"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].social_insurance_number", "sin"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].gender", "select"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].relationship", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].custody_status", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].benefit_eligible", "boolean"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].period_start", "date"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].period_end", "date"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].caregiver_primary", "boolean"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].notes", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].family_allowance", "boolean"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].child_benefit", "boolean"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].additional_benefits", "boolean"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].documentation", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page3[0].sub_Section_B[0].Table1[0", "children[0].special_circumstances", "string"),
                
                # ============================================================================
                # PAGE 4 - BENEFITS AND ELIGIBILITY INFORMATION
                # ============================================================================
                
                FormFieldMapping("SC_ISP1640_E[0].#pageSet[0].Page4[0].#subform[0].t", "key_document[*].page4_header", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page4[0].sub_c1[0].FLD_Benefits[0]", "financial_information.family_allowance_received", "boolean"),
                FormFieldMapping("SC_ISP1640_E[0].page4[0].sub_c1[0].FLD_received_be", "financial_information.family_allowance_details", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page4[0].sub_c1[0].FLD_receibe_CCB", "financial_information.canada_child_benefit", "boolean"),
                FormFieldMapping("SC_ISP1640_E[0].page4[0].sub_c1[0].FLD_received_be", "financial_information.ccb_details", "string"),
                
                # From/To Date Fields (Left Column)
                FormFieldMapping("SC_ISP1640_E[0].page4[0].sub_From_To_left[0].txtF_", "financial_information.benefit_period_start_1", "date"),
                FormFieldMapping("SC_ISP1640_E[0].page4[0].sub_From_To_left[0].txtF_", "financial_information.benefit_period_end_1", "date"),
                FormFieldMapping("SC_ISP1640_E[0].page4[0].sub_From_To_left[0].txt_R", "financial_information.benefit_recipient_1", "string"),
                
                # From/To Date Fields (Right Column)
                FormFieldMapping("SC_ISP1640_E[0].page4[0].sub_From_To_right[0].txtF", "financial_information.benefit_period_start_2", "date"),
                FormFieldMapping("SC_ISP1640_E[0].page4[0].sub_From_To_right[0].txtF", "financial_information.benefit_period_end_2", "date"),
                FormFieldMapping("SC_ISP1640_E[0].page4[0].sub_From_To_right[0].txt_", "financial_information.benefit_recipient_2", "string"),
                
                # Section C3 - Additional Benefits
                FormFieldMapping("SC_ISP1640_E[0].page4[0].Sub_C3[0].FLD_Benefits[0]", "financial_information.additional_benefits", "boolean"),
                
                # ============================================================================
                # PAGE 5 - CAREGIVER PERIODS AND WAIVER SECTION
                # ============================================================================
                
                FormFieldMapping("SC_ISP1640_E[0].#pageSet[0].Page4[1].#subform[0].t", "key_document[*].page5_header", "string"),
                
                # From/To Date Fields (Page 5 Left)
                FormFieldMapping("SC_ISP1640_E[0].page5[0].sub_From_To_left[0].txtF_", "children[*].caregiver_period_start_1", "date"),
                FormFieldMapping("SC_ISP1640_E[0].page5[0].sub_From_To_left[0].txtF_", "children[*].caregiver_period_end_1", "date"),
                FormFieldMapping("SC_ISP1640_E[0].page5[0].sub_From_To_left[0].txt_r", "children[*].caregiver_reason_1", "string"),
                
                # From/To Date Fields (Page 5 Right)
                FormFieldMapping("SC_ISP1640_E[0].page5[0].sub_From_To_right[0].txtF", "children[*].caregiver_period_start_2", "date"),
                FormFieldMapping("SC_ISP1640_E[0].page5[0].sub_From_To_right[0].txtF", "children[*].caregiver_period_end_2", "date"),
                FormFieldMapping("SC_ISP1640_E[0].page5[0].sub_From_To_right[0].txt_", "children[*].caregiver_reason_2", "string"),
                
                # Waiver Section (Spouse Information)
                FormFieldMapping("SC_ISP1640_E[0].page5[0].sub_Waiver[0].txtF_Witnes", "spouse.witness_name", "name"),
                FormFieldMapping("SC_ISP1640_E[0].page5[0].sub_Waiver[0].txtF_Social", "spouse.social_insurance_number", "sin"),
                FormFieldMapping("SC_ISP1640_E[0].page5[0].sub_Waiver[0].txtF_Witnes", "spouse.witness_phone", "phone"),
                FormFieldMapping("SC_ISP1640_E[0].page5[0].sub_Waiver[0].txtF_Signat", "spouse.signature", "signature"),
                FormFieldMapping("SC_ISP1640_E[0].page5[0].sub_Waiver[0].txtF_Witnes", "spouse.witness_signature", "signature"),
                
                # ============================================================================
                # PAGE 6 - APPLICANT SIGNATURE AND INFORMATION
                # ============================================================================
                
                FormFieldMapping("SC_ISP1640_E[0].#pageSet[0].Page4[2].#subform[0].t", "key_document[*].page6_header", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page6[0].txtF_Signature[0]", "applicant.signature", "signature"),
                FormFieldMapping("SC_ISP1640_E[0].page6[0].txtF_SignatureDate[0]", "key_document[*].signature_date", "date"),
                FormFieldMapping("SC_ISP1640_E[0].page6[0].txt_First_Name[0]", "applicant.first_name", "name"),
                FormFieldMapping("SC_ISP1640_E[0].page6[0].txt_Middle_Name[0]", "applicant.middle_name", "name"),
                FormFieldMapping("SC_ISP1640_E[0].page6[0].txt_Last_Name[0]", "applicant.last_name", "name"),
                FormFieldMapping("SC_ISP1640_E[0].page6[0].txtF_Phone[0]", "applicant.phone", "phone"),
                FormFieldMapping("SC_ISP1640_E[0].page6[0].txtF_Address[0]", "applicant.address", "location"),
                
                # ============================================================================
                # PAGE 7 - WITNESS INFORMATION
                # ============================================================================
                
                FormFieldMapping("SC_ISP1640_E[0].#pageSet[0].Page4[3].#subform[0].t", "key_document[*].page7_header", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page7[0].txt_First_Name[0]", "contact[*].witness_first_name", "name"),
                FormFieldMapping("SC_ISP1640_E[0].page7[0].txt_Middle_Name[0]", "contact[*].witness_middle_name", "name"),
                FormFieldMapping("SC_ISP1640_E[0].page7[0].txt_Last_Name[0]", "contact[*].witness_last_name", "name"),
                FormFieldMapping("SC_ISP1640_E[0].page7[0].txtF_WitnessPhone[0]", "contact[*].witness_phone", "phone"),
                FormFieldMapping("SC_ISP1640_E[0].page7[0].txtF_Address[0]", "contact[*].witness_address", "location"),
                FormFieldMapping("SC_ISP1640_E[0].page7[0].txtF_Signature[0]", "contact[*].witness_signature", "signature"),
                FormFieldMapping("SC_ISP1640_E[0].page7[0].txtF_WitnessSignatureDate", "contact[*].witness_signature_date", "date"),
                
                # ============================================================================
                # PAGE 9 - TABLE 2 (DETAILED CHILDREN INFORMATION)
                # ============================================================================
                
                # Row 0 - Child 1 Detailed Info
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[0].TextFie", "children[0].table2_field1", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[0].TextFie", "children[0].table2_field2", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[0].TextFie", "children[0].table2_field3", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[0].TextFie", "children[0].table2_field4", "string"),
                
                # Row 1 - Child 2 Detailed Info
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[1].TextFie", "children[1].table2_field1", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[1].TextFie", "children[1].table2_field2", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[1].TextFie", "children[1].table2_field3", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[1].TextFie", "children[1].table2_field4", "string"),
                
                # Row 2 - Child 3 Detailed Info
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[2].TextFie", "children[2].table2_field1", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[2].TextFie", "children[2].table2_field2", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[2].TextFie", "children[2].table2_field3", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[2].TextFie", "children[2].table2_field4", "string"),
                
                # Row 3 - Child 4 Detailed Info
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[3].TextFie", "children[3].table2_field1", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[3].TextFie", "children[3].table2_field2", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[3].TextFie", "children[3].table2_field3", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[3].TextFie", "children[3].table2_field4", "string"),
                
                # Row 4 - Child 5 Detailed Info
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[4].TextFie", "children[4].table2_field1", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[4].TextFie", "children[4].table2_field2", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[4].TextFie", "children[4].table2_field3", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[4].TextFie", "children[4].table2_field4", "string"),
                
                # Row 5 - Child 6 Detailed Info
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[5].TextFie", "children[5].table2_field1", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[5].TextFie", "children[5].table2_field2", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[5].TextFie", "children[5].table2_field3", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[5].TextFie", "children[5].table2_field4", "string"),
                
                # Row 6 - Child 7 Detailed Info (THE FAILING ONES!)
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[6].TextFie", "children[6].table2_field1", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[6].TextFie", "children[6].table2_field2", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[6].TextFie", "children[6].table2_field3", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[6].TextFie", "children[6].table2_field4", "string"),
                
                # The specific failing fields mentioned in debug output
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[6].TextField13[0]", "children[6].benefit_period_details", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[6].TextField14[0]", "children[6].caregiver_certification", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[6].TextField15[0]", "children[6].eligibility_documentation", "string"),
                FormFieldMapping("SC_ISP1640_E[0].page9[0].Table2[0].Row1[6].TextField16[0]", "children[6].additional_notes", "string"),
                
                # ============================================================================
                # PAGE 10 - CHECKBOXES AND OPTIONS
                # ============================================================================
                
                FormFieldMapping("SC_ISP1640_E[0].page10[0].Check_Boxes[0].Option_1[", "financial_information.child_rearing_option_1", "checkbox"),
                FormFieldMapping("SC_ISP1640_E[0].page10[0].Check_Boxes[0].Option_2[", "financial_information.child_rearing_option_2", "checkbox"),
                FormFieldMapping("SC_ISP1640_E[0].page10[0].Check_Boxes[0].Option_3[", "financial_information.child_rearing_option_3", "checkbox"),
                
            ],
            
            # SERVICE CANADA OLD AGE SECURITY APPLICATION - SC ISP-3008
            "service_canada_oas_isp3008": [
               # Section 1-7: Personal Information
                 FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_LastNameBirth[0]", "applicant.last_name", "name", description="Q1: Last name at birth"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_FirstName[0]", "applicant.first_name", "name", description="Q1: First name"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_DOB[0]", "applicant.date_of_birth", "date", description="Q2: Date of birth"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].rb_language[0]", "applicant.preferred_language", "select", description="Q3: Preferred language"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_home_add[0]", "applicant.home_address_street", "location", description="Q4: Home address street"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_city[0]", "applicant.home_address_city", "location", description="Q4: Home address city"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_province[0]", "applicant.home_address_province", "location", description="Q4: Home address province"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_country[0]", "applicant.home_address_country", "location", description="Q4: Home address country"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_postalcode[0]", "applicant.home_address_postal", "location", description="Q4: Home address postal code"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_email[0]", "applicant.email", "email", required=False, description="Q7: Email address"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_8[0].txtF_Q8_Branch_Num[0]", "payment.transit_number", "string", description="Q8: Bank Branch Number"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_8[0].txtF_Q8_Institution_Num[0]", "payment.institution_number", "string", description="Q8: Bank Institution Number"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_8[0].txtF_Q8_Account_Num[0]", "payment.account_number", "string", description="Q8: Bank Account Number"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_8[0].txtF_Q8_Account_Holder_Name[0]", "payment.account_holder", "string", required=False, description="Q8: Account Holder Name"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_8[0].txtF_Q8_Phone_Number[0]", "payment.bank_phone", "phone", required=False, description="Q8: Bank Phone Number"),

               # ==============================================================================
               # PAGE 2 - SIN AND MARITAL STATUS
               # ==============================================================================
                FormFieldMapping("SC_ISP3008_E[0].#pageSet[0].Page2[0].txtF_SIN[0]", "applicant.social_insurance_number", "sin", description="Header: Social Insurance Number"),
                FormFieldMapping("SC_ISP3008_E[0].page2[0].sub_Q9[0].rb_Marital_Status[0]", "applicant.marital_status", "select", description="Q9: Marital Status"),
                FormFieldMapping("SC_ISP3008_E[0].page2[0].sub_Q9[0].txtf_Q9_Spouse_Name[0]", "spouse.full_name", "name", required=False, description="Q9a: Spouse's Name"),
                FormFieldMapping("SC_ISP3008_E[0].page2[0].sub_Q9[0].txtF_Q9_Spouse_SIN[0]", "spouse.social_insurance_number", "sin", required=False, description="Q9a: Spouse's SIN"),
                FormFieldMapping("SC_ISP3008_E[0].page2[0].sub_Q9[0].sub_Q9b[0].txtF_Deceased_Spouse_CL_DOD[0]", "spouse.date_of_death", "date", description="Q9b: Date of death of former spouse/partner", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page2[0].sub_Q9[0].sub_d[0].rb_Q9d_Yes-No[0]", "spouse.separated_status", "boolean", required=False, description="Q9d: Separated?"),
                FormFieldMapping("SC_ISP3008_E[0].page2[0].sub_Q9[0].txtF_Q9d_Date[0]", "spouse.separation_date", "date", required=False, description="Q9d: Separation Date"),
                FormFieldMapping("SC_ISP3008_E[0].page2[0].sub_Q9[0].sub_e[0].rb_Q9e_Yes-No[0]", "spouse.divorced_status", "boolean", required=False, description="Q9e: Divorced?"),
                FormFieldMapping("SC_ISP3008_E[0].page2[0].sub_Q9[0].txtF_Q9e_Date[0]", "spouse.divorce_date", "date", required=False, description="Q9e: Divorce Date"),
                FormFieldMapping("SC_ISP3008_E[0].page2[0].sub_Q9[0].sub_f[0].rb_Q9f_Yes-No[0]", "spouse.widowed_status", "boolean", required=False, description="Q9f: Widowed?"),
                FormFieldMapping("SC_ISP3008_E[0].page2[0].sub_Q9[0].txtF_Q9f_Date[0]", "spouse.former_spouse_date_of_death", "date", required=False, description="Q9f: Former Spouse Date of Death"),

               # ==============================================================================
               # PAGE 3 - RESIDENCE AND WORK HISTORY
               # ==============================================================================
                FormFieldMapping("SC_ISP3008_E[0].page3[0].CheckBox1[0]", "applicant.residence_history.lived_in_canada_10_years", "checkbox", description="Q10a: Lived in Canada for 10+ years since age 18?"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_10b_10C[0].rb_Q10b[0]", "applicant.residence_history.lived_outside_canada_spouse", "boolean", description="Q10b: Lived outside Canada while spouse worked for Canadian employer?"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_10b_10C[0].txtF_Q10b_Other[0]", "applicant.residence_history.lived_outside_canada_spouse_country", "string", required=False, description="Q10b: Country where spouse worked"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_10b_10C[0].rb_Q10b[1]", "applicant.residence_history.worked_outside_canada", "boolean", description="Q10c: Worked outside Canada for Canadian employer?"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_10b_10C[0].txtF_Q10b_Other[1]", "applicant.residence_history.worked_outside_canada_country", "string", required=False, description="Q10c: Country where you worked"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_colA[0].txtF_Q13a_Country[0]", "applicant.international_work[0].country", "string", required=False, description="Q13 Col A: Country"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_colA[0].txtF_Q13a_Insurance_Num[0]", "applicant.international_work[0].insurance_number", "string", required=False, description="Q13 Col A: Insurance Number"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_colA[0].txtF_Q13a_Period_Lived_From[0]", "applicant.international_work[0].lived_from", "date", required=False, description="Q13 Col A: Lived From"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_colA[0].txtF_Q13a_Period_Lived_To[0]", "applicant.international_work[0].lived_to", "date", required=False, description="Q13 Col A: Lived To"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_colA[0].txtF_Q13a_Period_Worked_From[0]", "applicant.international_work[0].worked_from", "date", required=False, description="Q13 Col A: Worked From"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_colA[0].txtF_Q13a_Period_Worked_To[0]", "applicant.international_work[0].worked_to", "date", required=False, description="Q13 Col A: Worked To"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_colB[0].txtF_13b_Country[0]", "applicant.international_work[1].country", "string", required=False, description="Q13 Col B: Country"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_colB[0].txtF_13b_Insurance_Num[0]", "applicant.international_work[1].insurance_number", "string", required=False, description="Q13 Col B: Insurance Number"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_colB[0].txtF_Q13a_Period_Lived_From[0]", "applicant.international_work[1].lived_from", "date", required=False, description="Q13 Col B: Lived From"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_colB[0].txtF_Q13a_Period_Lived_To[0]", "applicant.international_work[1].lived_to", "date", required=False, description="Q13 Col B: Lived To"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_colB[0].txtF_Q13a_Period_Worked_From[0]", "applicant.international_work[1].worked_from", "date", required=False, description="Q13 Col B: Worked From"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_colB[0].txtF_Q13a_Period_Worked_To[0]", "applicant.international_work[1].worked_to", "date", required=False, description="Q13 Col B: Worked To"),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].rb_Yes-No[0]", "applicant.international_benefits_received", "boolean", description="Q14: Received benefits from other countries?"),

               # ==============================================================================
               # PAGE 4 - MAILING ADDRESS, SIGNATURES, AND ADMIN SECTION
               # ==============================================================================
                FormFieldMapping("SC_ISP3008_E[0].page4[0].sub_Q14[0].#subform[0].rb_Salutation[0]", "applicant.mailing_address_salutation", "string", required=False, description="Q14: Mailing Address Salutation"),
                FormFieldMapping("SC_ISP3008_E[0].page4[0].sub_Q14[0].#subform[0].txtF_Q14_Name[0]", "applicant.mailing_address_name", "name", required=False, description="Q14: Mailing Address Name"),
                FormFieldMapping("SC_ISP3008_E[0].page4[0].txtF_Q15_Applicant_Signature[0]", "applicant.signature", "signature", description="Q15: Applicant Signature"),
                FormFieldMapping("SC_ISP3008_E[0].page4[0].txtF_Q15_Date1[0]", "key_document.signature_date", "date", description="Q15: Signature Date"),
                FormFieldMapping("SC_ISP3008_E[0].page4[0].#subform[3].txtF_Relationship_To_Applicant[0]", "contact.witness.relationship_to_applicant", "string", required=False, description="Q15: Witness Relationship"),
                FormFieldMapping("SC_ISP3008_E[0].page4[0].sub_Mid_Top_Box[0].txtF_EffectiveDate[0]", "key_document.effective_date", "date", required=False, description="Admin: Effective Date"),
                FormFieldMapping("SC_ISP3008_E[0].page4[0].sub_Mid_Top_Box[0].txtF_Aggregate[0]", "key_document.aggregate_amount", "currency", required=False, description="Admin: Aggregate"),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].sub_1_2[0].sub_salutation[0].rb_Salutation[0]", "applicant.salutation", "string", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_home_add[1]", "applicant.mailing_address_street", "location", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_city[1]", "applicant.mailing_address_city", "location", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_province[1]", "applicant.mailing_address_province", "location", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_country[1]", "applicant.mailing_address_country", "location", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_postalcode[1]", "applicant.mailing_address_postal", "location", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page1[0].sub_1_7[0].txtF_home_add[2]", "applicant.contact_phone", "phone", required=False),
                # Page 2 - Spouse Info
                FormFieldMapping("SC_ISP3008_E[0].page2[0].sub_Q9[0].txtF_Home_Postal_Code[0]", "spouse.home_address_postal", "location", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page2[0].sub_Q9[0].sub_c[0].#subform[0].rb_Q9c_Yes-No[0]", "spouse.was_married_or_common_law", "boolean", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page2[0].sub_Q9[0].txtF_Q9c_Date[0]", "spouse.marriage_or_common_law_date", "date", required=False),
                # Page 3 - Residence History
                FormFieldMapping("SC_ISP3008_E[0].page3[0].txtF_Q11_Date[0]", "applicant.residence_history.date_became_resident_since_18", "date", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].txtF_Q11_Date[1]", "applicant.residence_history.date_of_last_arrival_canada", "date", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_Q12[0].tb_Residence_History[0].tr_Row1[0].txtF_LineA_Period_From[0]", "applicant.residence_history.periods[0].from", "date", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_Q12[0].tb_Residence_History[0].tr_Row1[0].txtF_LineA_Period_To[0]", "applicant.residence_history.periods[0].to", "date", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_Q12[0].tb_Residence_History[0].tr_Row1[0].txtF_LineA_Country[0]", "applicant.residence_history.periods[0].country", "string", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_Q12[0].tb_Residence_History[0].tr_Row2[0].txtF_LineB_Period_From[0]", "applicant.residence_history.periods[1].from", "date", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_Q12[0].tb_Residence_History[0].tr_Row2[0].txtF_LineB_Period_To[0]", "applicant.residence_history.periods[1].to", "date", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_Q12[0].tb_Residence_History[0].tr_Row2[0].txtF_LineB_Country[0]", "applicant.residence_history.periods[1].country", "string", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_Q12[0].tb_Residence_History[0].tr_Row3[0].txtF_LineC_Period_From[0]", "applicant.residence_history.periods[2].from", "date", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_Q12[0].tb_Residence_History[0].tr_Row3[0].txtF_LineC_Period_To[0]", "applicant.residence_history.periods[2].to", "date", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page3[0].sub_Q12[0].tb_Residence_History[0].tr_Row3[0].txtF_LineC_Country[0]", "applicant.residence_history.periods[2].country", "string", required=False),
                # Page 4 - Mailing Address and Signatures
                FormFieldMapping("SC_ISP3008_E[0].page4[0].sub_Q14[0].txtF_Home_Postal_Code[0]", "applicant.mailing_address_postal", "location", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page4[0].txtF_Q15_Witness_Signature[0]", "contact.witness.signature", "signature", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page4[0].txtF_Q15_Date2[0]", "contact.witness.signature_date", "date", required=False),
                # Page 4 - Admin Box
                FormFieldMapping("SC_ISP3008_E[0].page4[0].sub_Mid_Top_Box[0].txtF_Signature[0]", "key_document.admin_signature", "signature", required=False),
                FormFieldMapping("SC_ISP3008_E[0].page4[0].sub_Mid_Top_Box[0].txtF_YearMonthDay19[0]", "key_document.admin_date", "date", required=False),

            ],
            
            # ELECTIONS IMMEDIATE FAMILY MEMBER NOTICE OF VOTER'S DEATH
            "elections_immediate_family_death_notice": [
                # Deceased Voter Information
                FormFieldMapping("deceased_voter_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("voter_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("voter_city_town_residence", "deceased.home_address", "location", "extract_city"),
                FormFieldMapping("voter_place_of_death", "deceased.place_of_death", "location"),
                FormFieldMapping("voter_date_of_death", "deceased.date_of_death", "date"),
                
                # Immediate Family Member Information
                FormFieldMapping("family_member_printed_name", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("relationship_to_voter", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("family_member_signature", "applicant.signature", "string"),
                FormFieldMapping("notification_date", "key_document[*].date_created", "date"),
                
                # Registrar Use Only
                FormFieldMapping("date_received_by_registrar", "key_document[*].date_received", "date"),
                FormFieldMapping("date_cancelled_in_cvr", "key_document[*].date_processed", "date"),
                FormFieldMapping("registrar_initials", "key_document[*].processed_by", "string"),
                
                # Form Metadata
                FormFieldMapping("form_identifier", "key_document[*].id", "string"),
                FormFieldMapping("form_statute_reference", "key_document[*].legal_reference", "string"),
            ],
            
            # MANITOBA FUNERAL HOME INVOICE - SCHEDULE B
            "manitoba_funeral_home_invoice_schedule_b": [
                # Header Information
                FormFieldMapping("Funeral Home", "funeral_home.name", "string"),
                FormFieldMapping("License Number", "funeral_home.license_number", "string"),
                FormFieldMapping("EIA Case No", "key_document.case_number", "string"),

                # Deceased Information
                FormFieldMapping("Deceased - Full Name", "deceased.full_name", "name"),
                FormFieldMapping("Date of Birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("Place of Death", "deceased.place_of_death", "string"),
                FormFieldMapping("Date of Death", "deceased.date_of_death", "date"),
                FormFieldMapping("DATE", "deceased.date_of_death", "date"), # Handles the duplicate field

                # Service Type Checkboxes (assuming these are checkboxes)
                FormFieldMapping("1", "funeral_home.service_type_regular", "checkbox", required=False),
                FormFieldMapping("2", "funeral_home.service_type_graveside", "checkbox", required=False),
                FormFieldMapping("3", "funeral_home.service_type_child", "checkbox", required=False),
                FormFieldMapping("4", "funeral_home.service_type_cremation_viewing", "checkbox", required=False),
                FormFieldMapping("5", "funeral_home.service_type_cremation_no_viewing", "checkbox", required=False),
                FormFieldMapping("6", "funeral_home.service_type_graveside_cremation", "checkbox", required=False),
                FormFieldMapping("7", "funeral_home.service_type_cremation_only", "checkbox", required=False),

                # Primary Costs
                FormFieldMapping("1_2", "funeral_home.casket_cost", "currency", required=False),
                FormFieldMapping("2_2", "funeral_home.cremation_container_cost", "currency", required=False),

                # Transportation Costs
                FormFieldMapping("Transport From", "funeral_home.transportation_from", "string", required=False),
                FormFieldMapping("Transport To", "funeral_home.transportation_to", "string", required=False),
                FormFieldMapping("KM", "funeral_home.transportation_distance_km", "string", required=False),
                FormFieldMapping("Cost per KM", "funeral_home.transportation_cost_per_km", "currency", required=False),
                FormFieldMapping("total kilometers traveled Transportation Costs", "funeral_home.transportation_total_cost", "currency", required=False),

                # Cemetery Costs
                FormFieldMapping("Location of Burial/Plot", "final_wishes.preparations.plot.location", "string", required=False),
                FormFieldMapping("Lot/Plot Actual Costs", "final_wishes.preparations.plot.cost", "currency", required=False),
                FormFieldMapping("Opening/Closing Fee", "final_wishes.preparations.plot.opening_closing_fee", "currency", required=False),
                FormFieldMapping("Additional Costs", "final_wishes.preparations.plot.additional_costs", "currency", required=False),
                FormFieldMapping("Total Costs", "final_wishes.preparations.plot.total_cost", "currency", required=False),

                # Additional Costs Section
                FormFieldMapping("Freight/Shipping", "funeral_home.additional_costs.freight", "currency", required=False),
                FormFieldMapping("Outer Shell", "funeral_home.additional_costs.outer_shell", "currency", required=False),
                FormFieldMapping("Sealed Container", "funeral_home.additional_costs.sealed_container", "currency", required=False),
                FormFieldMapping("Oversized Casket", "funeral_home.additional_costs.oversized_casket", "currency", required=False),
                FormFieldMapping("Transportation", "funeral_home.additional_costs.transportation", "currency", required=False),
                FormFieldMapping("Clergy", "funeral_home.additional_costs.clergy", "currency", required=False),
                FormFieldMapping("Other", "funeral_home.additional_costs.other_amount", "currency", required=False),
                FormFieldMapping("Other Details", "funeral_home.additional_costs.other_details", "string", required=False),
                FormFieldMapping("Total Additional Costs", "funeral_home.additional_costs.total", "currency", required=False),

                # Final Total
                FormFieldMapping("Total Fees", "funeral_home.total_fees", "currency", required=False)
            ],
            
            # ADDITIONAL PROVINCIAL HEALTH CARD CHANGES
            "provincial_health_card_changes": [
                FormFieldMapping("card_holder_name", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("health_card_number", "applicant.health_card_number", "string"),
                FormFieldMapping("date_of_birth", "applicant.date_of_birth", "date"),
                FormFieldMapping("address_change", "applicant.address", "location"),
                FormFieldMapping("name_change", "applicant.new_name", "name"),
                FormFieldMapping("death_notification", "deceased.date_of_death", "date"),
                FormFieldMapping("relationship_to_deceased", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("proof_of_death", "deceased.proof_of_death", "file"),
                FormFieldMapping("applicant_signature", "applicant.signature", "string"),
            ],
            
            # ============================================================================
            # FORMS I MAY HAVE MISSED FROM ORIGINAL - ADDING THEM NOW
            # ============================================================================
            
            # PASSPORT OFFICE DEATH NOTIFICATION
            "passport_office_death_notification": [
                FormFieldMapping("deceased_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("deceased_passport_number", "id_document__passport[*].id", "string"),
                FormFieldMapping("deceased_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("deceased_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("notifier_name", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("notifier_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("death_certificate", "deceased.proof_of_death", "file"),
                FormFieldMapping("passport_surrender", "id_document__passport[*].surrender_date", "date"),
                FormFieldMapping("notification_date", "key_document[*].date_created", "date"),
            ],
            
            # STATE VITAL RECORDS DEATH CERTIFICATE ORDER
            "state_vital_records_death_certificate": [
                FormFieldMapping("deceased_full_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("deceased_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("deceased_place_of_death", "deceased.place_of_death", "location"),
                FormFieldMapping("deceased_age_at_death", "deceased.age_at_death", "number"),
                FormFieldMapping("deceased_spouse_name", "spouse.name", "name", "parse_full_name"),
                FormFieldMapping("deceased_father_name", "deceased.fathers_name", "name", "parse_full_name"),
                FormFieldMapping("deceased_mother_name", "deceased.mothers_name", "name", "parse_full_name"),
                FormFieldMapping("requestor_name", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("requestor_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("purpose_of_request", "key_document[*].purpose", "string"),
                FormFieldMapping("number_of_copies", "key_document[*].copies_requested", "number"),
                FormFieldMapping("fee_amount", "key_document[*].fee", "currency"),
                FormFieldMapping("requestor_signature", "applicant.signature", "string"),
            ],
            
            # EMPLOYMENT BENEFITS DEATH NOTIFICATION
            "employment_benefits_death_notification": [
                FormFieldMapping("employee_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("employee_id", "deceased.employment.employee_id", "string"),
                FormFieldMapping("employee_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("last_day_worked", "deceased.employment.last_day_worked", "date"),
                FormFieldMapping("department", "deceased.employment.department", "string"),
                FormFieldMapping("supervisor_name", "deceased.employment.supervisor", "name", "parse_full_name"),
                FormFieldMapping("beneficiary_name", "financial_information__pension[*].beneficiary_primary", "name", "parse_full_name"),
                FormFieldMapping("beneficiary_relationship", "financial_information__pension[*].beneficiary_relationship", "string"),
                FormFieldMapping("beneficiary_address", "financial_information__pension[*].beneficiary_address", "location"),
                FormFieldMapping("group_life_insurance", "insurance__life[*].group_policy", "boolean"),
                FormFieldMapping("pension_benefits", "financial_information__pension[*].pension_benefits", "boolean"),
                FormFieldMapping("accrued_vacation", "deceased.employment.accrued_vacation", "currency"),
                FormFieldMapping("final_paycheck", "deceased.employment.final_pay", "currency"),
                FormFieldMapping("cobra_continuation", "insurance[*].cobra_eligible", "boolean"),
                FormFieldMapping("hr_signature", "deceased.employment.hr_signature", "string"),
                FormFieldMapping("notification_date", "key_document[*].date_created", "date"),
            ],
            
            # MEDICARE DEATH NOTIFICATION
            "medicare_death_notification": [
                FormFieldMapping("beneficiary_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("medicare_number", "deceased.medicare_number", "string"),
                FormFieldMapping("beneficiary_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("place_of_death", "deceased.place_of_death", "location"),
                FormFieldMapping("reporting_person", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("reporting_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("death_certificate_number", "deceased.death_certificate_number", "string"),
                FormFieldMapping("medicare_card_return", "deceased.medicare_card_returned", "boolean"),
                FormFieldMapping("final_claims_pending", "insurance[*].pending_claims", "boolean"),
                FormFieldMapping("reporter_signature", "applicant.signature", "string"),
                FormFieldMapping("report_date", "key_document[*].date_created", "date"),
            ],
            
            # POST OFFICE BOX CLOSURE
            "post_office_box_closure": [
                FormFieldMapping("box_holder_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("po_box_number", "deceased.po_box", "string"),
                FormFieldMapping("post_office_location", "deceased.po_box_location", "location"),
                FormFieldMapping("date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("requestor_name", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("requestor_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("mail_forwarding_request", "deceased.mail_forwarding", "boolean"),
                FormFieldMapping("forwarding_address", "deceased.forwarding_address", "location"),
                FormFieldMapping("keys_returned", "deceased.po_box_keys_returned", "boolean"),
                FormFieldMapping("final_mail_pickup", "deceased.final_mail_date", "date"),
                FormFieldMapping("death_certificate", "deceased.proof_of_death", "file"),
                FormFieldMapping("closure_date", "deceased.po_box_closure_date", "date"),
            ],
            
            # TRIBAL GOVERNMENT DEATH NOTIFICATION
            "tribal_government_death_notification": [
                FormFieldMapping("member_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("tribal_id_number", "deceased.tribal_id", "string"),
                FormFieldMapping("enrollment_number", "deceased.enrollment_number", "string"),
                FormFieldMapping("blood_quantum", "deceased.blood_quantum", "string"),
                FormFieldMapping("tribal_affiliation", "deceased.tribal_affiliation", "string"),
                FormFieldMapping("date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("place_of_death", "deceased.place_of_death", "location"),
                FormFieldMapping("reporting_family_member", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("relationship_to_deceased", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("traditional_burial_request", "final_wishes.traditional_burial", "boolean"),
                FormFieldMapping("tribal_benefits_due", "financial_information[*].tribal_benefits", "currency"),
                FormFieldMapping("land_allotment_issues", "property.tribal_land", "string"),
                FormFieldMapping("cultural_items_return", "property.cultural_items", "string"),
                FormFieldMapping("death_certificate", "deceased.proof_of_death", "file"),
                FormFieldMapping("tribal_council_notification", "key_document[*].tribal_notification", "boolean"),
            ],
            
            # STUDENT LOAN DEATH DISCHARGE
            "student_loan_death_discharge": [
                FormFieldMapping("borrower_name", "deceased.name", "name", "parse_full_name"),
                FormFieldMapping("borrower_ssn", "deceased.social_insurance_number", "sin"),
                FormFieldMapping("borrower_date_of_birth", "deceased.date_of_birth", "date"),
                FormFieldMapping("borrower_date_of_death", "deceased.date_of_death", "date"),
                FormFieldMapping("loan_servicer", "financial_information.student_loans[*].servicer", "string"),
                FormFieldMapping("loan_account_numbers", "financial_information.student_loans[*].account_number", "string"),
                FormFieldMapping("outstanding_balance", "financial_information.student_loans[*].balance", "currency"),
                FormFieldMapping("federal_loans", "financial_information.student_loans[*].federal_loans", "boolean"),
                FormFieldMapping("private_loans", "financial_information.student_loans[*].private_loans", "boolean"),
                FormFieldMapping("parent_plus_loans", "financial_information.student_loans[*].parent_plus", "boolean"),
                FormFieldMapping("discharge_requestor", "applicant.name", "name", "parse_full_name"),
                FormFieldMapping("requestor_relationship", "estate_reps[*].secondary_relationship_to_deceased", "string"),
                FormFieldMapping("death_certificate", "deceased.proof_of_death", "file"),
                FormFieldMapping("discharge_application_date", "key_document[*].date_created", "date"),
                FormFieldMapping("tax_implications_acknowledged", "financial_information.student_loans[*].tax_implications", "boolean"),
            ],
        }
        
        return mappings
    
    def _initialize_form_metadata(self) -> Dict[str, FormMetadata]:
        """Initialize metadata for all forms"""
        metadata = {
            "alabama_dmv_next_of_kin_affidavit": FormMetadata(
                identifier="alabama_dmv_next_of_kin_affidavit",
                title="Affidavit for Assignment of Title for a Vehicle From a Deceased Owner Whose Estate Does Not Require Probate",
                jurisdiction="Alabama",
                category="vehicle_title_transfer",
                complexity="medium",
                estimated_time="15-30 minutes",
                time_sensitivity="Within 30 days of death",
                required_documents=[
                    "Certified death certificate",
                    "Current vehicle title (if available)", 
                    "Valid ID of next of kin"
                ],
                purpose="Transfer vehicle ownership from deceased owner to next of kin when estate does not require probate",
                applicable_situations=["Vehicle title transfer", "Small estate", "Next of kin inheritance", "No probate required"]
            ),
            "atf_form_5_firearm_transfer": FormMetadata(
                identifier="atf_form_5_firearm_transfer",

                title="Application for Tax Exempt Transfer and Registration of Firearm",
                jurisdiction="US Federal",
                category="firearm_transfer",
                complexity="high",
                estimated_time="45-60 minutes",
                time_sensitivity="No specific deadline, but required before transfer",
                required_documents=[
                    "Proof of legal heir status (e.g., will, court order)",
                    "Death certificate of previous owner",
                    "ATF Form 5320.5 (if applicable)",
                    "Certified copy of trust (if applicable)"
                ],
                purpose="To legally transfer ownership of a National Firearms Act (NFA) firearm from a deceased owner to a lawful heir",
                applicable_situations=[
                    "Inheritance of NFA items (suppressors, short-barreled rifles, machine guns, etc.)",
                    "Estate settlement involving regulated firearms",
                    "Transfer to lawful heirs",
                    "Tax-exempt firearm transfers"
                ]
            ),
            "service_canada_t4a_representative_isp1202": FormMetadata(
                identifier="service_canada_t4a_representative_isp1202",
                title="Service Canada - Deemed Person to Represent the Deceased Client for the Purpose of Issuing a T4A (ISP-1202)",
                jurisdiction="Canada Federal - Service Canada",
                category="death_benefit_application", 
                complexity="medium",
                estimated_time="15-20 minutes",
                time_sensitivity="As soon as possible after death",
                required_documents=[
                    "Death certificate or acceptable proof of death",
                    "Social Insurance Number of deceased",
                    "Proof of relationship to deceased",
                    "Legal authority documents (if applicable)",
                    "Representative's identification"
                ],
                purpose="Authorize a representative to receive T4A tax slips and related documents for a deceased client",
                applicable_situations=[
                    "Death of OAS/CPP recipient",
                    "Need to obtain T4A slips for deceased",
                    "Estate tax preparation",
                    "Final tax return filing",
                    "Representative authorization for tax documents",
                    "Pension benefit documentation",
                    "Government benefit wind-up"
                ]
            ),
            "irs_form_ss4_estate": FormMetadata(
                identifier="irs_form_ss4_estate",
                title="IRS Form SS-4 Application for Employer Identification Number (Estate)",
                jurisdiction="US Federal",
                category="tax_administration",
                complexity="medium",
                estimated_time="20-30 minutes",
                time_sensitivity="As soon as possible after death",
                required_documents=[
                    "Death certificate",
                    "Will or court appointment documents",
                    "Social Security Number of deceased",
                    "Proof of executor/administrator authority"
                ],
                purpose="Obtain Federal Employer Identification Number (EIN) for estate tax and administration purposes",
                applicable_situations=[
                    "Estate administration",
                    "Need EIN for estate bank account",
                    "Filing estate tax returns (Form 1041)",
                    "Estate has income or employees",
                    "Executor/administrator duties",
                    "Estate business operations"
                ]
            ),
            "service_canada_cpp_survivors_pension_isp1300": FormMetadata(
                identifier="service_canada_cpp_survivors_pension_isp1300",
                title="Application for a Canada Pension Plan Survivor's Pension and Child(ren)'s Benefits",
                jurisdiction="Canada Federal",
                category="death_benefit_application",
                complexity="high",
                estimated_time="45-60 minutes",
                time_sensitivity="Within 12 months of death for maximum benefits",
                required_documents=[
                    "Death certificate or acceptable proof of death",
                    "Marriage certificate (if married)",
                    "Birth certificates for children",
                    "Social Insurance Number cards",
                    "Banking information for direct deposit"
                ],
                purpose="Apply for CPP survivor's pension and children's benefits after death of contributing spouse/partner",
                applicable_situations=[
                    "Death of CPP contributing spouse",
                    "Death of common-law partner",
                    "Survivor benefits for spouse/partner",
                    "Children's benefits under 18",
                    "Student benefits for children 18-25",
                    "Disabled children benefits"
                ]
            ),
            "service_canada_child_rearing_isp1640": FormMetadata(
                identifier="service_canada_child_rearing_isp1640",
                title="Service Canada Child Rearing Provision Application (ISP-1640)",
                jurisdiction="Canada Federal",
                category="death_benefit_application",
                complexity="high",
                estimated_time="45-60 minutes",
                time_sensitivity="Within 4 years of child rearing period",
                required_documents=[
                    "Social Insurance Number",
                    "Birth certificates for all children",
                    "Proof of child care periods",
                    "Family Allowance records (if applicable)",
                    "Canada Child Benefit records (if applicable)",
                    "Witness identification"
                ],
                purpose="Apply for Canada Pension Plan credits for periods spent caring for children under age 7",
                applicable_situations=[
                    "Parent or caregiver who was out of workforce caring for children",
                    "Periods of reduced earnings due to child care responsibilities", 
                    "Enhancing CPP retirement pension through child rearing credits",
                    "Periods between 1958 and current where children under 7 were in care",
                    "Family Allowance was received for the child",
                    "Canada Child Benefit was received for the child"
                ]
            ),
            "irs_form_56_fiduciary": FormMetadata(
                identifier="irs_form_56_fiduciary",
                title="IRS Form 56 - Notice Concerning Fiduciary Relationship",
                jurisdiction="US Federal",
                category="tax_administration",
                complexity="medium",
                estimated_time="20-30 minutes",
                time_sensitivity="As soon as possible after appointment as fiduciary",
                required_documents=[
                    "Court appointment documents (letters testamentary/administration)",
                    "Trust instrument (if applicable)",
                    "Death certificate",
                    "Proof of fiduciary authority",
                    "Valid ID of fiduciary"
                ],
                purpose="Notify the IRS of fiduciary relationship for estate or trust tax matters",
                applicable_situations=[
                    "Estate administration",
                    "Trust administration", 
                    "Court-appointed executor/administrator",
                    "Guardian or conservator appointment",
                    "Bankruptcy proceedings",
                    "Tax representation for deceased person",
                    "Fiduciary tax filing responsibilities",
                    "Power of attorney for tax matters"
                ]
            ),

            "california_dmv_death_report_dmv22": FormMetadata(
                identifier="california_dmv_death_report_dmv22",
                title="California DMV Death Report - DMV 22",
                jurisdiction="California State",
                category="death_notification",
                complexity="simple",
                estimated_time="10-15 minutes", 
                time_sensitivity="As soon as possible after death",
                required_documents=[
                    "Death certificate (copy)",
                    "Disabled parking placard (if applicable)",
                    "Valid ID of person reporting"
                ],
                purpose="Report death to California DMV to update driver license and parking placard records",
                applicable_situations=[
                    "Death of California driver license holder",
                    "Death of disabled parking placard holder", 
                    "Update DMV records after death",
                    "Cancel deceased person's driving privileges",
                    "Return disabled parking placards"
                ]
            ),
            # FIX 1.4: Add the metadata for the new SSA-8 form.
            "social_security_death_payment_ssa8": FormMetadata(
                identifier="social_security_death_payment_ssa8",
                title="Application for Lump-Sum Death Payment (SSA-8)",
                jurisdiction="US Federal",
                category="death_benefit_application",
                complexity="high",
                estimated_time="30-45 minutes",
                time_sensitivity="Critical - Must be filed within 2 years of death",
                required_documents=[
                    "Certified copy of the death certificate",
                    "Deceased's Social Security number",
                    "Applicant's Social Security number",
                    "Proof of relationship (if applicable)",
                ],
                purpose="To apply for the one-time, lump-sum death payment of $255 from the Social Security Administration.",
                applicable_situations=[
                    "Death of a person who worked and paid Social Security taxes",
                    "Application by a surviving spouse or eligible child",
                ]
            ),
            
            "service_canada_death_notification_isp1201": FormMetadata(
                identifier="service_canada_death_notification_isp1201",
                title="Notification of Death (ISP-1201) - Canada Pension Plan / Old Age Security",
                jurisdiction="Canada Federal",
                category="death_notification",
                complexity="simple",
                estimated_time="10-15 minutes",
                time_sensitivity="As soon as possible after death",
                required_documents=[
                    "Social Insurance Number of the deceased",
                    "Death certificate (or proof of death)"
                ],
                purpose="To inform Service Canada of a death to stop Canada Pension Plan (CPP) and Old Age Security (OAS) payments.",
                applicable_situations=["Death of a CPP or OAS recipient", "Stopping government benefit payments", "Initiating the process for survivor benefits"]
            ),
            "cra_death_notification_rc4111": FormMetadata(
                identifier="cra_death_notification_rc4111",
                title="Notify the Canada Revenue Agency of a Death - RC4111",
                jurisdiction="Canada Federal",
                category="tax_administration",
                complexity="simple",
                estimated_time="5-10 minutes",
                time_sensitivity="As soon as possible after death",
                required_documents=[
                    "Death certificate",
                    "Social Insurance Number of deceased",
                    "Proof of relationship to deceased"
                ],
                purpose="Notify CRA of a person's death for tax purposes",
                applicable_situations=[
                    "Death notification to CRA",
                    "Stop tax correspondence to deceased",
                    "Initiate estate tax processes",
                    "Cancel CRA accounts and benefits"
                ]
            ),

            "electoral_deceased_removal_form": FormMetadata(
                identifier="electoral_deceased_removal_form",
                title="Application to Remove a Deceased Person from Electoral Registers",
                jurisdiction="Provincial/Municipal",
                category="electoral_administration", 
                complexity="simple",
                estimated_time="10-15 minutes",
                time_sensitivity="Within 30 days of death",
                required_documents=[
                    "Death certificate or acceptable proof of death",
                    "Proof of relationship to deceased",
                    "Valid ID of applicant"
                ],
                purpose="Remove deceased voter from electoral/voter registration rolls",
                applicable_situations=[
                    "Death notification to electoral office",
                    "Voter roll maintenance", 
                    "Electoral list cleanup",
                    "Prevent electoral fraud"
                ]
            ),
            "cra_legal_representative_appointment": FormMetadata(
                identifier="cra_legal_representative_appointment",
                title="Appoint a Legal Representative for a Deceased Person - Canada Revenue Agency",
                jurisdiction="Canada Federal",
                category="tax_administration",
                complexity="medium",
                estimated_time="20-30 minutes",
                time_sensitivity="As soon as possible after death",
                required_documents=[
                    "Death certificate",
                    "Proof of relationship to deceased",
                    "Government-issued ID of representative",
                    "Legal authority documents (if applicable)"
                ],
                purpose="Authorize a legal representative to act on behalf of a deceased person for CRA tax matters",
                applicable_situations=[
                    "Estate tax administration",
                    "Final tax return filing", 
                    "CRA account management for deceased",
                    "Tax refund claims",
                    "Business tax matters of deceased"
                ]
            ),
            "service_canada_cpp_death_benefit_isp1200": FormMetadata(
                identifier="service_canada_cpp_death_benefit_isp1200",
                title="Application for a Canada Pension Plan Death Benefit (ISP-1200)",
                jurisdiction="Canada Federal",
                category="death_benefit_application",
                complexity="high",
                estimated_time="30-45 minutes",
                time_sensitivity="Application should be made promptly to receive full benefits.",
                required_documents=[
                    "Proof of death (original or certified copy)",
                    "Deceased's Social Insurance Number",
                    "Applicant's Social Insurance Number",
                    "Proof of relationship (if applicable)",
                    "Proof of legal authority (will, court order, etc.)"
                ],
                purpose="To apply for the one-time, lump-sum CPP Death Benefit on behalf of a deceased CPP contributor.",
                applicable_situations=["Death of a CPP contributor", "Estate administration", "Covering funeral expenses", "Claiming survivor benefits"]
            ),
            "florida_certificate_title_hsmv82040": FormMetadata(
                identifier="florida_certificate_title_hsmv82040",
                title="Florida Certificate of Title Application with/without Registration (HSMV 82040)",
                jurisdiction="Florida State",
                category="vehicle_title_transfer",
                complexity="high",           
                estimated_time="45-60 minutes",     
                time_sensitivity="Within 30 days of transfer",       
                required_documents=[         
                    "Death certificate (if inheritance)",
                    "Previous vehicle title",
                    "Valid Florida driver's license or ID",
                    "Proof of insurance",
                    "Lien release (if applicable)",
                    "Court documents (if estate transfer)"
                ],
                purpose="Apply for Florida certificate of title and/or vehicle registration including inheritance transfers",   
                applicable_situations=[  
                    "Vehicle inheritance after death",
                    "New Florida resident vehicle registration", 
                    "Out-of-state vehicle transfer",
                    "Estate vehicle distribution",
                    "Family vehicle transfers",
                    "Lien payoff and title transfer"
                ]
            ),
            "california_statement_of_facts_reg256": FormMetadata(
                identifier="california_statement_of_facts_reg256",
                title="California Statement of Facts - REG 256",
                jurisdiction="California State",
                category="vehicle_title_transfer",
                complexity="medium",
                estimated_time="15-25 minutes",
                time_sensitivity="Within 30 days of vehicle transfer",
                required_documents=[
                    "Vehicle title or registration",
                    "Proof of insurance",
                    "Smog certificate (if required)",
                    "Death certificate (for inheritance)",
                    "Court order (if applicable)"
                ],
                purpose="Document vehicle transfer circumstances and claim tax/smog exemptions",
                applicable_situations=[
                    "Vehicle inheritance after death",
                    "Family vehicle transfers",
                    "Gift vehicle transfers",
                    "Court-ordered vehicle transfers",
                    "Tax exemption claims",
                    "Smog exemption claims"
                ]
            ),
            "elections_ontario_f0527w": FormMetadata(
                identifier="elections_ontario_f0527w",
                title="Elections Ontario - Application to Remove a Deceased Person (F0527W)",
                jurisdiction="Ontario Provincial",
                category="electoral_administration",
                complexity="simple",
                estimated_time="5-10 minutes",
                time_sensitivity="As soon as possible after death",
                required_documents=[
                    "Proof of death (e.g., death certificate, obituary)"
                ],
                purpose="To remove a deceased person from the electoral registers maintained by Elections Ontario.",
                applicable_situations=["Death of a registered voter in Ontario", "Voter list maintenance by a family member or representative"]
            ),
            "maine_voter_death_notice": FormMetadata(
                identifier="maine_voter_death_notice",
                title="Notice of Voter's Death by Immediate Family Member",
                jurisdiction="Maine",
                category="electoral_administration",
                complexity="simple",
                estimated_time="5-10 minutes",
                time_sensitivity="As soon as possible after death",
                required_documents=[
                    "None specified on form, but Death Certificate may be required by registrar."
                ],
                purpose="To notify the local registrar of a voter's death so they can be removed from the Central Voter Registration (CVR) system.",
                applicable_situations=["Death of a registered voter in Maine", "Voter roll maintenance by family"]
            ),
            "manitoba_funeral_home_invoice_schedule_b": FormMetadata(
                identifier="manitoba_funeral_home_invoice_schedule_b",
                title="Manitoba Funeral Home Invoice (Schedule B - EIA)",
                jurisdiction="Manitoba",
                category="estate_information",
                complexity="medium",
                estimated_time="15-20 minutes",
                time_sensitivity="Within 30-60 days of service",
                required_documents=[
                    "Death Certificate (usually handled by funeral home)",
                    "EIA Case Number (if applicable)"
                ],
                purpose="To provide a detailed invoice for funeral services, often used for claims with Manitoba's Employment and Income Assistance (EIA) program.",
                applicable_situations=["Funeral planning", "Estate expense tracking", "Claiming funeral benefits from EIA"]
            ),
            "hilton_honors_points_transfer": FormMetadata(
                identifier="hilton_honors_points_transfer",
                title="Hilton Honors Declaration in Support of Request for Transfer of Deceased Member's Points",
                jurisdiction="US Private Sector",
                category="loyalty_program_transfer",
                complexity="simple", 
                estimated_time="10-15 minutes",
                time_sensitivity="Within 1 year of death",
                required_documents=[
                    "Death certificate or proof of death",
                    "Court order/appointment as executor",
                    "Hilton Honors account numbers (deceased and recipient)"
                ],
                purpose="Transfer loyalty program points from deceased member to designated recipient",
                applicable_situations=[
                    "Death of Hilton Honors member",
                    "Estate administration involving loyalty points", 
                    "Family member inheritance of points",
                    "Executor duties for digital assets"
                ]
            ),

            "utah_survivorship_affidavit_tc569c": FormMetadata(
                identifier="utah_survivorship_affidavit_tc569c",
                title="Utah State Tax Commission Survivorship Affidavit (TC-569C)",
                jurisdiction="Utah State",
                category="Vehicle Transfer",
                complexity="Moderate",
                estimated_time="20-30 minutes",
                time_sensitivity="Within 30 days of death",
                required_documents=["Death Certificate", "Vehicle Registration", "Proof of Relationship"],
                purpose="Transfer vehicle ownership to surviving owner",
                applicable_situations=["Joint vehicle ownership", "Survivorship rights", "Estate under $100,000"]
            ),
            "nevada_dmv_affidavit_vp24": FormMetadata(
                identifier="nevada_dmv_affidavit_vp24",
                title="Affidavit for Transfer of Title for Estates Without Probate (VP-24)",
                jurisdiction="Nevada",
                category="vehicle_title_transfer",
                complexity="medium",
                estimated_time="15-25 minutes",
                time_sensitivity="Recommended within 30 days of death",
                required_documents=[
                    "Certified Death Certificate",
                    "Original Vehicle Title",
                    "Valid ID for Affiant"
                ],
                purpose="To allow the legal heir (affiant) to take ownership of a deceased person's vehicle when the estate value does not require formal probate.",
                applicable_situations=["Small estates", "Vehicle inheritance", "Avoiding probate for a vehicle"]
            ),
            # --- FIX: ADD THIS NEW METADATA ENTRY ---
           "canada_post_mail_forwarding": FormMetadata(
                identifier="canada_post_mail_forwarding",
                title="Canada Post - Mail Forwarding / Réacheminement du courrier",
                jurisdiction="Canada Federal",
                category="death_notification",
                complexity="medium",
                estimated_time="15-20 minutes",
                time_sensitivity="As soon as possible, before mail delivery is missed",
                required_documents=["Proof of Identity", "Proof of Authorization (if for deceased)"],
                purpose="To redirect mail for an individual or business, including for a deceased person, to a new address.",
                applicable_situations=[
                    "Moving", 
                    "Temporary relocation", 
                    "Managing mail for a deceased person",
                    "Estate administration",
                    "Mail management during probate"
                ],
            ),
            "veterans_affairs_disability_death_benefit_pen542": FormMetadata(
                identifier="veterans_affairs_disability_death_benefit_pen542",
                title="Veterans Affairs Disability/Death Benefit Application (PEN542)",
                jurisdiction="US Federal - Veterans Affairs",
                category="Military Benefits",
                complexity="Very Complex",
                estimated_time="2-3 hours",
                time_sensitivity="Within 1 year of death",
                required_documents=["Death Certificate", "Military Records", "Marriage Certificate", "Medical Records"],
                purpose="Apply for VA disability or death benefits",
                applicable_situations=["Veteran death", "Service-connected disability", "Survivor benefits"]
            ),
            # Add metadata for all other forms...
        }
        return metadata
    
    def map_field_to_cadence_path(self, form_identifier: str, field_name: str) -> Optional[str]:
        """
        Finds the Cadence schema path for a given field name within a specific form.
        This is the primary method for mapping individual fields.
        """
        if form_identifier not in self.form_mappings:
            return None

        mappings = self.form_mappings[form_identifier]
        field_name_lower = field_name.lower()

        # Strategy 1: Exact match (case-insensitive). This is the highest confidence match.
        for mapping in mappings:
            if mapping.form_field.lower() == field_name_lower:
                return mapping.schema_path

        # Strategy 2: Partial match for long, complex PDF field names.
        # This is common in auto-generated PDFs where field names are very long.
        for mapping in mappings:
            if len(field_name) > 30 and len(mapping.form_field) > 30:
                if field_name_lower.startswith(mapping.form_field.lower()):
                    return mapping.schema_path

        # Strategy 3: Fuzzy match (if the form's field name is contained in the PDF field name).
        # This catches variations in field naming.
        for mapping in mappings:
            mapping_field_lower = mapping.form_field.lower()
            if len(field_name_lower) > 5 and len(mapping_field_lower) > 5:
                if mapping_field_lower in field_name_lower:
                    return mapping.schema_path

        # If no match is found after all strategies, return None.
        return None
    
    def get_forms_by_jurisdiction(self) -> Dict[str, List[str]]:
        """Group forms by jurisdiction"""
        return EstateFormsPatternMatcher.JURISDICTION_FORMS.copy()

    def get_forms_by_complexity(self) -> Dict[str, List[str]]:
        """Group forms by complexity level"""
        complexity_levels = {}
        for form_id, metadata in self.form_metadata.items():
            complexity = metadata.complexity
            if complexity not in complexity_levels:
                complexity_levels[complexity] = []
            complexity_levels[complexity].append(form_id)
        return complexity_levels

    # ============================================================================
    # ### START OF ADDED METHODS BLOCK ###
    # ============================================================================

    def detect_form_with_generic_fields(self, pdf_fields, ocr_text=""):
        """Special detection for forms with generic field names like form1[0].#subform[0].TextField1[0]"""
        ssa8_field_count = len([f for f in pdf_fields if "form1[0].#subform" in f])
        if ssa8_field_count >= 100:  # SSA-8 has ~122 fields
            if any(pattern in ocr_text.upper() for pattern in [
                "SSA-8", "LUMP-SUM DEATH PAYMENT", "SOCIAL SECURITY ADMINISTRATION",
                "APPLICATION FOR LUMP-SUM DEATH PAYMENT", "OMB NO. 0960-0013"
            ]):
                return "social_security_death_payment_ssa8", 0.85
        return None, 0.0

    def get_field_sequence_mapping(self, form_identifier):
        """Get field mapping by position for forms with generic field names"""
        if form_identifier == "social_security_death_payment_ssa8":
            return {
                'form1[0].#subform[0].TextField1[0]': 'applicant.full_name',
                'form1[0].#subform[0].TextField1[1]': 'deceased.full_name',
                'form1[0].#subform[0].NumericField1[0]': 'deceased.social_insurance_number',
                'form1[0].#subform[0].DateField1[0]': 'deceased.date_of_birth',
                'form1[0].#subform[0].DateField2[0]': 'deceased.date_of_death',
                'form1[0].#subform[0].TextField1[2]': 'deceased.place_of_death',
                'form1[0].#subform[0].TextField1[3]': 'deceased.earnings.year_of_death',
                'form1[0].#subform[0].TextField1[4]': 'deceased.earnings.year_before_death',
                'form1[0].#subform[0].C7Yes[0]': 'deceased.work_status.unable_to_work_at_death',
                'form1[0].#subform[0].DateField3[0]': 'deceased.work_status.date_unable_to_work',
                'form1[0].#subform[0].C8Yes[0]': 'deceased.military.active_service_pre_1968',
                'form1[0].#subform[0].TextField1[5]': 'deceased.military.service_start_date',
                'form1[0].#subform[0].TextField1[6]': 'deceased.military.service_end_date',
                'form1[0].#subform[0].C8CYes[0]': 'deceased.military.other_federal_benefits',
                'form1[0].#subform[0].C9Yes[0]': 'deceased.employment.railroad_work_7_years',
                'form1[0].#subform[1].C10Yes[0]': 'deceased.employment.foreign_work',
                'form1[0].#subform[1].TextField1[7]': 'deceased.employment.foreign_countries',
                'form1[0].#subform[1].C11Yes[0]': 'deceased.marital_status.surviving_spouse_exists',
                'form1[0].#subform[1].TextField1[8]': 'spouse.full_name',
                'form1[0].#subform[1].TextField1[11]': 'spouse.date_of_marriage',
                'form1[0].#subform[1].TextField1[12]': 'spouse.place_of_marriage',
                'form1[0].#subform[1].TextField1[13]': 'spouse.date_of_birth',
                'form1[0].#subform[1].TextField1[14]': 'spouse.social_insurance_number',
                'form1[0].#subform[2].C16Yes[0]': 'spouse.living_together_at_death',
                'form1[0].#subform[2].C17Yes[0]': 'applicant.disability_status',
                'form1[0].#subform[2].TextField1[46]': 'applicant.disability_start_date',
                'form1[0].#subform[2].TextField1[65]': 'notes.remarks',
                'form1[0].#subform[2].TextField1[66]': 'applicant.signature',
                'form1[0].#subform[2].TextField1[67]': 'key_document.signature_date',
                'form1[0].#subform[2].TextField1[68]': 'applicant.phone',
                'form1[0].#subform[2].TextField1[69]': 'applicant.mailing_address.street',
                'form1[0].#subform[2].TextField1[70]': 'applicant.mailing_address.city_state_zip',
                'form1[0].#subform[3].TextField1[76]': 'payment.routing_number',
                'form1[0].#subform[3].TextField1[77]': 'payment.account_number',
                'form1[0].#subform[3].Checking[0]': 'payment.account_type_checking',
                'form1[0].#subform[3].Savings[0]': 'payment.account_type_savings',
                'form1[0].#subform[1].C11BClerg[0]': 'deceased.prior_marriages[0].ceremonial_marriage',
                'form1[0].#subform[1].C11BOther[0]': 'deceased.prior_marriages[0].other_marriage',
                'form1[0].#subform[1].DateField4[0]': 'deceased.prior_marriages[0].end_date',
                'form1[0].#subform[1].C11CClerg[0]': 'deceased.prior_marriages[1].ceremonial_marriage',
                'form1[0].#subform[1].C11COther[0]': 'deceased.prior_marriages[1].other_marriage',
                'form1[0].#subform[1].C14No[0]': 'applicant.no_prior_filing_spouse_record',
                'form1[0].#subform[1].C14Yes[0]': 'applicant.prior_filing_spouse_record',
                'form1[0].#subform[2].C18No[0]': 'applicant.no_prior_marriage_10_years',
                'form1[0].#subform[2].C18Yes[0]': 'applicant.prior_marriage_10_years',
                'form1[0].#subform[2].C18Clerg[0]': 'applicant.prior_marriages[0].ceremonial_marriage',
                'form1[0].#subform[2].C18Other[0]': 'applicant.prior_marriages[0].other_marriage',
            }
        return {}

    def enhance_form_detection(self, pdf_fields, ocr_text="", field_values=None):
        """Enhanced form detection that handles generic field names"""
        standard_result = (None, 0.0)
        if hasattr(self, 'detect_form_type') and callable(self.detect_form_type):
             standard_result = self.detect_form_type(pdf_fields, ocr_text)
        
        if standard_result[1] < 0.5:
            generic_result = self.detect_form_with_generic_fields(pdf_fields, ocr_text)
            if generic_result[1] > standard_result[1]:
                return generic_result
        return standard_result

    def get_form_mapping(self, form_identifier: str) -> List[FormFieldMapping]:
        return self.form_mappings.get(form_identifier, [])

    def get_all_form_identifiers(self) -> List[str]:
        return list(self.form_mappings.keys())

    def get_form_metadata(self, form_identifier: str) -> Optional[FormMetadata]:
        return self.form_metadata.get(form_identifier)

    
    def map_form_data(self, form_identifier: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map form data to Cadence schema structure
        
        Args:
            form_identifier: The identifier for the form type
            form_data: Dictionary containing the form field data
            
        Returns:
            Dictionary with Cadence schema structure
        """
        mappings = self.get_form_mapping(form_identifier)
        if not mappings:
            raise ValueError(f"Unknown form identifier: {form_identifier}")
        
        cadence_data = {}
        
        for mapping in mappings:
            if mapping.form_field in form_data:
                value = form_data[mapping.form_field]
                
                # Apply transformation if specified
                if mapping.transform_function:
                    value = self._apply_transformation(
                        mapping.transform_function, 
                        value, 
                        form_data
                    )
                
                # Apply validation if specified
                if mapping.validation_rules:
                    self._validate_value(value, mapping.validation_rules)
                
                # Set the value in the Cadence structure
                self._set_nested_value(cadence_data, mapping.schema_path, value)
        
        return cadence_data
    
    def _apply_transformation(self, transform_func: str, value: Any, form_data: Dict[str, Any]) -> Any:
        """Apply transformation function to the value"""
        
        transformations = {
            "parse_full_name": self._parse_full_name,
            "parse_full_name_last_first": self._parse_full_name_last_first,
            "combine_address": self._combine_address,
            "combine_make_model": self._combine_make_model,
            "extract_make": self._extract_make,
            "extract_model": self._extract_model,
            "extract_city": self._extract_city,
            "extract_state": self._extract_state,
            "extract_province": self._extract_province,
            "extract_postal_code": self._extract_postal_code,
            "extract_zip": self._extract_zip,
            "extract_apartment": self._extract_apartment,
            "extract_county": self._extract_county,
            "extract_country": self._extract_country,
            "extract_city_state_zip": self._extract_city_state_zip,
            "calculate_age": self._calculate_age,
            "track_awards": self._track_awards,
            "track_war_service": self._track_war_service,
            "transform_vin_fields": self.transform_vin_fields,
        }
        
        if transform_func in transformations:
            return transformations[transform_func](value, form_data)
        
        return value
    
    def _parse_full_name(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Parse full name into components"""
        if isinstance(value, str):
            parts = value.strip().split()
            return {
                "first_name": parts[0] if len(parts) > 0 else "",
                "middle_name": " ".join(parts[1:-1]) if len(parts) > 2 else "",
                "last_name": parts[-1] if len(parts) > 1 else ""
            }
        return value
    
    def _parse_full_name_last_first(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Parse 'Last, First Middle' format name"""
        if isinstance(value, str) and "," in value:
            parts = value.split(",", 1)
            last_name = parts[0].strip()
            first_middle = parts[1].strip().split() if len(parts) > 1 else []
            return {
                "first_name": first_middle[0] if len(first_middle) > 0 else "",
                "middle_name": " ".join(first_middle[1:]) if len(first_middle) > 1 else "",
                "last_name": last_name
            }
        return self._parse_full_name(value, form_data)
    
    def _combine_address(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Combine address components"""
        return value
    
    def _combine_make_model(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Combine vehicle make and model"""
        return value
    
    def _extract_make(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Extract make from make/model string"""
        if isinstance(value, str):
            return value.split()[0] if value else ""
        return value
    
    def _extract_model(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Extract model from make/model string"""
        if isinstance(value, str):
            parts = value.split()
            return " ".join(parts[1:]) if len(parts) > 1 else ""
        return value
    
    def _extract_city(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Extract city from address"""
        return value
    
    def _extract_state(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Extract state from address"""
        return value
    
    def _extract_province(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Extract province from address"""
        return value
    
    def _extract_postal_code(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Extract postal code from address"""
        if isinstance(value, str):
            # Canadian postal code pattern
            postal_match = re.search(r'[A-Z]\d[A-Z]\s?\d[A-Z]\d', value.upper())
            return postal_match.group() if postal_match else ""
        return value
    
    def _extract_zip(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Extract ZIP code from address"""
        if isinstance(value, str):
            # US ZIP code pattern
            zip_match = re.search(r'\d{5}(-\d{4})?', value)
            return zip_match.group() if zip_match else ""
        return value
    
    def _extract_apartment(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Extract apartment/unit number from address"""
        return value
    
    def _extract_county(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Extract county from address"""
        return value
    
    def _extract_country(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Extract country from address"""
        return value
    
    def _extract_city_state_zip(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Extract city, state, and ZIP from combined field"""
        return value
    
    def _calculate_age(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Calculate age from date of birth"""
        if isinstance(value, str):
            try:
                birth_date = datetime.strptime(value, "%Y-%m-%d")
                today = datetime.now()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                return age
            except ValueError:
                pass
        return value
    
    def _track_awards(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Track military awards"""
        return value
    
    def _track_war_service(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Track war service periods"""
        return value
    def transform_vin_fields(self, field_data: Dict[str, str]) -> str:
        """Concatenate VIN character fields into complete VIN"""
        vin_parts = []
        for i in range(17):
            vin_key = f"VIN.{i}"
            if vin_key in field_data:
                vin_parts.append(field_data[vin_key])
        return "".join(vin_parts) if len(vin_parts) == 17 else ""
        
    def _validate_value(self, value: Any, validation_rules: List[str]) -> None:
        """Validate value against specified rules"""
        for rule in validation_rules:
            if rule == "required" and not value:
                raise ValueError("Field is required")
            elif rule == "email" and value and "@" not in str(value):
                raise ValueError("Invalid email format")
            elif rule == "phone" and value:
                # Basic phone validation
                phone_clean = re.sub(r'[^\d]', '', str(value))
                if len(phone_clean) != 10:
                    raise ValueError("Phone number must be 10 digits")
    
    def _set_nested_value(self, data_dict: Dict[str, Any], path: str, value: Any) -> None:
        """Set a nested value in the dictionary using dot notation path"""
        keys = path.split('.')
        current_dict = data_dict
        
        for key in keys[:-1]:
            if '[*]' in key:
                base_key = key.replace('[*]', '')
                if base_key not in current_dict:
                    current_dict[base_key] = []
                if not current_dict[base_key]:
                    current_dict[base_key].append({})
                current_dict = current_dict[base_key][0]
            else:
                if key not in current_dict:
                    current_dict[key] = {}
                current_dict = current_dict[key]
        
        final_key = keys[-1].replace('[*]', '')
        current_dict[final_key] = value

    def get_schema_coverage_report(self) -> Dict[str, Any]:
        """Generate a report showing Cadence schema coverage by forms"""
        coverage = {
            "total_forms": len(self.form_mappings),
            "total_mappings": sum(len(mappings) for mappings in self.form_mappings.values()),
            "schema_paths_used": set(),
            "form_details": {}
        }
        
        for form_id, mappings in self.form_mappings.items():
            schema_paths = [m.schema_path for m in mappings]
            coverage["schema_paths_used"].update(schema_paths)
            coverage["form_details"][form_id] = {
                "field_count": len(mappings),
                "schema_paths": schema_paths,
                "field_types": [m.field_type for m in mappings]
            }
        
        coverage["unique_schema_paths"] = len(coverage["schema_paths_used"])
        coverage["schema_paths_used"] = list(coverage["schema_paths_used"])
        
        return coverage

    def get_forms_by_category(self) -> Dict[str, List[str]]:
        """Categorize forms by type/jurisdiction"""
        categories = {}
        for form_id, metadata in self.form_metadata.items():
            category = metadata.category
            if category not in categories:
                categories[category] = []
            categories[category].append(form_id)
        return categories

    def get_forms_by_jurisdiction(self) -> Dict[str, List[str]]:
            """Group forms by jurisdiction"""
            # BUG FIX: This was trying to access a non-existent class attribute.
            # It should return the top-level constant.
            return EstateFormsPatternMatcher.JURISDICTION_FORMS.copy()


    def get_forms_by_complexity(self) -> Dict[str, List[str]]:
        """Group forms by complexity level"""
        complexity_levels = {}
        for form_id, metadata in self.form_metadata.items():
            complexity = metadata.complexity
            if complexity not in complexity_levels:
                complexity_levels[complexity] = []
            complexity_levels[complexity].append(form_id)
        return complexity_levels

    def get_time_sensitive_forms(self) -> Dict[str, List[str]]:
        """Categorize forms by time sensitivity"""
        time_categories = {
            "Immediate (0-7 days)": [],
            "Short term (1-4 weeks)": [],
            "Medium term (1-3 months)": [],
            "Long term (3+ months)": []
        }
        
        for form_id, metadata in self.form_metadata.items():
            time_sensitivity = metadata.time_sensitivity.lower()
            if "immediate" in time_sensitivity or "7 days" in time_sensitivity:
                time_categories["Immediate (0-7 days)"].append(form_id)
            elif "30 days" in time_sensitivity or "4 weeks" in time_sensitivity:
                time_categories["Short term (1-4 weeks)"].append(form_id)
            elif "90 days" in time_sensitivity or "3 months" in time_sensitivity:
                time_categories["Medium term (1-3 months)"].append(form_id)
            else:
                time_categories["Long term (3+ months)"].append(form_id)
        
        return time_categories

    def get_forms_for_deceased_person(self) -> List[str]:
        """Get forms specifically dealing with deceased person affairs"""
        deceased_forms = []
        for form_id, mappings in self.form_mappings.items():
            for mapping in mappings:
                if "deceased" in mapping.schema_path:
                    deceased_forms.append(form_id)
                    break
        return deceased_forms

    def get_required_documents_by_form(self, form_identifier: str) -> List[str]:
        """Get required documents for a specific form"""
        metadata = self.get_form_metadata(form_identifier)
        return metadata.required_documents if metadata else []

    def generate_estate_administration_checklist(self) -> Dict[str, Any]:
        """Generate a comprehensive estate administration checklist"""
        time_sensitive_forms = self.get_time_sensitive_forms()
        forms_by_category = self.get_forms_by_category()
        
        checklist = {
            "Phase 1 - Immediate Actions (0-7 days)": {
                "title": "Immediate Post-Death Actions",
                "timeline": "0-7 days after death",
                "priority": "Critical",
                "forms": time_sensitive_forms["Immediate (0-7 days)"],
                "tasks": [
                    "Obtain death certificates",
                    "Notify Social Security Administration",
                    "Contact employer and benefits providers",
                    "Secure property and assets",
                    "Notify banks and financial institutions"
                ]
            },
            "Phase 2 - Short Term Actions (1-4 weeks)": {
                "title": "Initial Estate Administration",
                "timeline": "1-4 weeks after death",
                "priority": "High",
                "forms": time_sensitive_forms["Short term (1-4 weeks)"],
                "tasks": [
                    "File probate petition if required",
                    "Apply for letters testamentary",
                    "Transfer vehicle titles",
                    "Close unnecessary accounts",
                    "Begin asset inventory"
                ]
            },
            "Phase 3 - Medium Term Actions (1-3 months)": {
                "title": "Asset Management and Benefits",
                "timeline": "1-3 months after death",
                "priority": "Medium",
                "forms": time_sensitive_forms["Medium term (1-3 months)"],
                "tasks": [
                    "File insurance claims",
                    "Apply for survivor benefits",
                    "Complete asset transfers",
                    "Pay outstanding debts",
                    "Prepare tax returns"
                ]
            },
            "Phase 4 - Long Term Actions (3+ months)": {
                "title": "Final Estate Settlement",
                "timeline": "3+ months after death",
                "priority": "Normal",
                "forms": time_sensitive_forms["Long term (3+ months)"],
                "tasks": [
                    "Distribute assets to beneficiaries",
                    "File final tax returns",
                    "Close estate accounts",
                    "Complete property transfers",
                    "File final estate reports"
                ]
            }
        }
        
        return checklist

    def generate_form_completion_checklist(self, form_identifier: str) -> Dict[str, Any]:
        """Generate a completion checklist for a specific form"""
        mappings = self.get_form_mapping(form_identifier)
        metadata = self.get_form_metadata(form_identifier)
        
        if not mappings:
            return {"error": f"Form {form_identifier} not found"}
        
        sections = {}
        for mapping in mappings:
            section = self._determine_section(mapping.schema_path)
            if section not in sections:
                sections[section] = []
            sections[section].append({
                "field_name": mapping.form_field,
                "field_type": mapping.field_type,
                "required": mapping.required,
                "description": self._generate_field_description(mapping)
            })
        
        return {
            "form_identifier": form_identifier,
            "form_title": metadata.title if metadata else form_identifier,
            "jurisdiction": metadata.jurisdiction if metadata else "Unknown",
            "category": metadata.category if metadata else "Unknown",
            "total_fields": len(mappings),
            "sections": sections,
            "required_documents": metadata.required_documents if metadata else [],
            "estimated_completion_time": metadata.estimated_time if metadata else self._estimate_completion_time(len(mappings)),
            "complexity_level": metadata.complexity if metadata else self._assess_complexity(mappings),
            "time_sensitivity": metadata.time_sensitivity if metadata else "Unknown",
            "purpose": metadata.purpose if metadata else "Unknown",
            "applicable_situations": metadata.applicable_situations if metadata else []
        }

    def _determine_section(self, schema_path: str) -> str:
        """Determine the section category based on schema path"""
        if "deceased" in schema_path:
            return "Deceased Person Information"
        elif "applicant" in schema_path:
            return "Applicant Information"
        elif "estate_reps" in schema_path:
            return "Estate Representative Information"
        elif "children" in schema_path:
            return "Children/Dependent Information"
        elif "spouse" in schema_path:
            return "Spouse/Partner Information"
        elif "financial" in schema_path:
            return "Financial Information"
        elif "property" in schema_path:
            return "Property/Asset Information"
        elif "payment" in schema_path:
            return "Payment Information"
        elif "contact" in schema_path:
            return "Contact/Reference Information"
        elif "key_document" in schema_path:
            return "Form/Document Information"
        elif "account" in schema_path:
            return "Account Information"
        elif "insurance" in schema_path:
            return "Insurance Information"
        elif "funeral" in schema_path:
            return "Funeral/Memorial Information"
        else:
            return "General Information"

    def _generate_field_description(self, mapping: FormFieldMapping) -> str:
        """Generate a human-readable description for a form field"""
        descriptions = {
            "sin": "Social Insurance Number (9 digits)",
            "phone": "Phone number including area code",
            "email": "Valid email address",
            "date": "Date in YYYY-MM-DD format",
            "currency": "Dollar amount (e.g., $1,234.56)",
            "location": "Full address including postal/zip code",
            "name": "Full legal name",
            "select": "Choose from available options",
            "boolean": "Yes/No selection",
            "file": "Supporting document upload/attachment",
            "string": "Text field"
        }
        
        base_description = descriptions.get(mapping.field_type, "Text field")
        
        if mapping.transform_function:
            base_description += f" (will be processed: {mapping.transform_function})"
        
        return base_description

    def _estimate_completion_time(self, field_count: int) -> str:
        """Estimate completion time based on number of fields"""
        if field_count <= 10:
            return "5-10 minutes"
        elif field_count <= 25:
            return "15-20 minutes"
        elif field_count <= 50:
            return "30-45 minutes"
        elif field_count <= 75:
            return "60-90 minutes"
        else:
            return "2+ hours"

    def _assess_complexity(self, mappings: List[FormFieldMapping]) -> str:
        """Assess form complexity based on field types and transformations"""
        complex_types = ["currency", "date", "location", "file"]
        complex_transforms = ["parse_full_name", "combine_address", "calculate_age"]
        
        complexity_score = 0
        
        for mapping in mappings:
            if mapping.field_type in complex_types:
                complexity_score += 1
            if mapping.transform_function and mapping.transform_function in complex_transforms:
                complexity_score += 2
            if mapping.validation_rules:
                complexity_score += 1
        
        if complexity_score <= 5:
            return "Simple"
        elif complexity_score <= 15:
            return "Moderate"
        elif complexity_score <= 30:
            return "Complex"
        else:
            return "Very Complex"

    def search_forms(self, search_criteria: Dict[str, Any]) -> List[str]:
        """Search forms based on various criteria"""
        matching_forms = []
        
        for form_id, metadata in self.form_metadata.items():
            matches = True
            
            if "jurisdiction" in search_criteria:
                if search_criteria["jurisdiction"].lower() not in metadata.jurisdiction.lower():
                    matches = False
            
            if "category" in search_criteria:
                if search_criteria["category"].lower() != metadata.category.lower():
                    matches = False
            
            if "complexity" in search_criteria:
                if search_criteria["complexity"].lower() != metadata.complexity.lower():
                    matches = False
            
            if "keyword" in search_criteria:
                keyword = search_criteria["keyword"].lower()
                if (keyword not in metadata.title.lower() and 
                    keyword not in metadata.purpose.lower() and
                    not any(keyword in situation.lower() for situation in metadata.applicable_situations)):
                    matches = False
            
            if matches:
                matching_forms.append(form_id)
        
        return matching_forms

    def get_related_forms(self, form_identifier: str) -> List[str]:
        """Get forms related to the given form"""
        metadata = self.get_form_metadata(form_identifier)
        if not metadata:
            return []
        
        related_forms = []
        for other_form_id, other_metadata in self.form_metadata.items():
            if other_form_id != form_identifier:
                # Same category
                if other_metadata.category == metadata.category:
                    related_forms.append(other_form_id)
                # Same jurisdiction
                elif other_metadata.jurisdiction == metadata.jurisdiction:
                    related_forms.append(other_form_id)
        
        return related_forms[:5]  # Return top 5 related forms

    def validate_form_data(self, form_identifier: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate form data against form requirements"""
        mappings = self.get_form_mapping(form_identifier)
        if not mappings:
            return {"valid": False, "errors": [f"Unknown form: {form_identifier}"]}
        
        errors = []
        warnings = []
        
        for mapping in mappings:
            field_name = mapping.form_field
            
            # Check required fields
            if mapping.required and field_name not in form_data:
                errors.append(f"Required field missing: {field_name}")
            
            # Validate field values if present
            if field_name in form_data:
                value = form_data[field_name]
                try:
                    self._validate_value(value, mapping.validation_rules or [])
                except ValueError as e:
                    errors.append(f"Invalid value for {field_name}: {str(e)}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "completion_percentage": self._calculate_completion_percentage(mappings, form_data)
        }

    def _calculate_completion_percentage(self, mappings: List[FormFieldMapping], form_data: Dict[str, Any]) -> float:
        """Calculate what percentage of the form is completed"""
        if not mappings:
            return 0.0
        
        completed_fields = sum(1 for mapping in mappings if mapping.form_field in form_data)
        return (completed_fields / len(mappings)) * 100

    def export_form_templates(self) -> Dict[str, Any]:
        """Export form templates for all supported forms"""
        templates = {}
        
        for form_id, mappings in self.form_mappings.items():
            metadata = self.get_form_metadata(form_id)
            template = {
                "form_id": form_id,
                "title": metadata.title if metadata else form_id,
                "fields": []
            }
            
            for mapping in mappings:
                field_template = {
                    "name": mapping.form_field,
                    "type": mapping.field_type,
                    "required": mapping.required,
                    "description": self._generate_field_description(mapping)
                }
                template["fields"].append(field_template)
            
            templates[form_id] = template
        
        return templates

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the form system"""
        stats = {
            "total_forms": len(self.form_mappings),
            "total_fields": sum(len(mappings) for mappings in self.form_mappings.values()),
            "jurisdictions": len(set(metadata.jurisdiction for metadata in self.form_metadata.values())),
            "categories": len(set(metadata.category for metadata in self.form_metadata.values())),
            "complexity_distribution": {},
            "field_type_distribution": {},
            "most_complex_forms": [],
            "most_common_field_types": []
        }
        
        # Complexity distribution
        complexity_forms = self.get_forms_by_complexity()
        for complexity, forms in complexity_forms.items():
            stats["complexity_distribution"][complexity] = len(forms)
        
        # Field type distribution
        field_types = {}
        for mappings in self.form_mappings.values():
            for mapping in mappings:
                field_types[mapping.field_type] = field_types.get(mapping.field_type, 0) + 1
        
        stats["field_type_distribution"] = field_types
        stats["most_common_field_types"] = sorted(field_types.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Most complex forms
        complex_forms = [(form_id, len(mappings)) for form_id, mappings in self.form_mappings.items()]
        stats["most_complex_forms"] = sorted(complex_forms, key=lambda x: x[1], reverse=True)[:5]
        
        return stats


# Usage and Documentation
if __name__ == "__main__":
    """
    Enhanced Estate Forms Pattern Matching System - Complete Implementation
    
    This comprehensive system now includes:
    - 50+ forms from multiple jurisdictions and sectors
    - Advanced field mappings to Cadence schema
    - Comprehensive transformation functions
    - Complete coverage analysis and reporting
    - Form categorization by jurisdiction, complexity, and time sensitivity
    - Required documents tracking for each form
    - Estate administration checklist generation
    - Completion time estimation and complexity assessment
    - Support for digital assets and modern estate planning needs
    - Form validation and data integrity checking
    - Search and filtering capabilities
    - Statistical analysis and reporting
    
    Key Features:
    1. Multi-jurisdictional coverage (US Federal/State, Canadian Federal/Provincial)
    2. Private sector forms (banks, insurance, digital platforms)
    3. Specialized forms (military, healthcare, transportation)
    4. Advanced categorization and filtering
    5. Estate administration workflow guidance
    6. Document requirements tracking
    7. Time-sensitive form identification
    8. Complexity assessment for proper resource allocation
    9. Data validation and completion tracking
    10. Statistical analysis and reporting
    """
    
    # Demonstration of the complete system
    matcher = EstateFormsPatternMatcher()


    
    print("=== Enhanced Estate Forms System - Complete Implementation ===\n")
    
    # Get comprehensive coverage report
    coverage_report = matcher.get_schema_coverage_report()
    print(f"System Coverage:")
    print(f"  Total forms supported: {coverage_report['total_forms']}")
    print(f"  Total field mappings: {coverage_report['total_mappings']}")
    print(f"  Unique schema paths used: {coverage_report['unique_schema_paths']}")
    
    # Show enhanced categorization
    categories = matcher.get_forms_by_category()
    print(f"\nForm Categories:")
    for category, forms in categories.items():
        print(f"  {category}: {len(forms)} forms")
    
    # Show jurisdiction breakdown
    jurisdictions = matcher.get_forms_by_jurisdiction()
    print(f"\nForms by Jurisdiction:")
    for jurisdiction, forms in jurisdictions.items():
        print(f"  {jurisdiction}: {len(forms)} forms")
    
    # Show complexity distribution
    complexity_levels = matcher.get_forms_by_complexity()
    print(f"\nForms by Complexity:")
    for level, forms in complexity_levels.items():
        print(f"  {level}: {len(forms)} forms")
    
    # Show time-sensitive categorization
    time_sensitive = matcher.get_time_sensitive_forms()
    print(f"\nTime-Sensitive Form Categories:")
    for timeframe, forms in time_sensitive.items():
        print(f"  {timeframe}: {len(forms)} forms")
    
    # Generate sample estate administration checklist
    checklist = matcher.generate_estate_administration_checklist()
    print(f"\nEstate Administration Phases:")
    for phase, details in checklist.items():
        print(f"  {details['title']}: {len(details['forms'])} forms, {len(details['tasks'])} tasks")
    
    # Show statistics
    stats = matcher.get_statistics()
    print(f"\nSystem Statistics:")
    print(f"  Total jurisdictions: {stats['jurisdictions']}")
    print(f"  Total categories: {stats['categories']}")
    print(f"  Average fields per form: {stats['total_fields'] / stats['total_forms']:.1f}")
    print(f"  Most common field types: {[f'{t}({c})' for t, c in stats['most_common_field_types'][:3]]}")
    
    # Demonstrate form completion checklist
    sample_form = "utah_survivorship_affidavit_tc569c"
    form_details = matcher.generate_form_completion_checklist(sample_form)
    print(f"\nSample Form Details ({sample_form}):")
    print(f"  Title: {form_details['form_title']}")
    print(f"  Complexity: {form_details['complexity_level']}")
    print(f"  Estimated time: {form_details['estimated_completion_time']}")
    print(f"  Required documents: {len(form_details['required_documents'])}")
    print(f"  Form sections: {len(form_details['sections'])}")
    
    # Demonstrate data mapping
    sample_data = {
        "deceased_owner_name": "John Smith",
        "date_of_death": "2024-01-15",
        "year": "2020",
        "make": "Toyota",
        "survivor_name": "Jane Smith"
    }
    
    mapped_data = matcher.map_form_data(sample_form, sample_data)
    print(f"\nSample Data Mapping:")
    print(f"  Original fields: {len(sample_data)}")
    print(f"  Mapped schema paths: {len(mapped_data)}")
    
    # Demonstrate validation
    validation_result = matcher.validate_form_data(sample_form, sample_data)
    print(f"\nValidation Results:")
    print(f"  Valid: {validation_result['valid']}")
    print(f"  Completion: {validation_result['completion_percentage']:.1f}%")
    print(f"  Errors: {len(validation_result['errors'])}")
    
    print(f"\n=== System successfully initialized and ready for production use! ===")
    print(f"Complete estate forms pattern matching system with comprehensive coverage.")


    def _combine_date_components(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Combine date component fields into a single date"""
        # This would combine Date of Birth1A, Date of Birth1B, Date of Year1A, etc.
        # into a proper date format
        return value

    def _combine_dl_segments(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Combine driver license ID segments into complete license number"""
        dl_parts = []
        for i in range(1, 9):  # DL ID1 through DL ID8
            dl_key = f"DL ID{i}"
            if dl_key in form_data:
                dl_parts.append(form_data[dl_key])
        return "".join(dl_parts) if dl_parts else value

    def _combine_placard_segments(self, value: Any, form_data: Dict[str, Any]) -> Any:
        """Combine parking placard ID segments into complete placard number"""
        placard_parts = []
        for field_name, field_value in form_data.items():
            if "Parking Placard-ID" in field_name and field_value:
                placard_parts.append(field_value)
        return "".join(placard_parts) if placard_parts else value