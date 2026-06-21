"""
Comprehensive Cadence Schema Definitions - COMPLETE VERSION

Contains the complete schema paths, field types, value options,
and schema metadata for estate form processing.
COMPLETE: All schema paths including missing paths now loaded
"""

from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from .models import FieldType, SchemaField 

"""@dataclass
class SchemaField:
    
    path: str
    field_type: str
    description: str
    value_options: List[str]
    is_array: bool = False
    is_required: bool = False
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {} """

class CadenceSchema:
    """Comprehensive Cadence schema loader and manager - COMPLETE WITH ALL MISSING PATHS"""
    
    def __init__(self):
        self.schema_paths = self._load_cadence_schema()
        self.field_types = self._load_schema_field_types()
        self.value_options = self._load_schema_value_options()
        self.schema_fields = self._build_schema_fields()
        
        print(f"✅ Schema loaded: {len(self.schema_paths)} paths")
    
    def _load_cadence_schema(self) -> List[str]:
        """Load complete Cadence schema including all missing paths - ALL 650+ PATHS"""
        return [
            # ===== EXISTING SCHEMA PATHS =====
            # Deceased person fields
            "deceased.phone[*].phone_number",
            "deceased.phone[*].type",
            "deceased.phone[*].service_provider",
            "deceased.email[*].email_address",
            "deceased.email[*].type",
            "deceased.employment.status[*]",
            "deceased.employment.notes",
            "deceased.military.discharge_document",
            "deceased.military.branch_of_service",
            "deceased.name",  # Full name (for backward compatibility)
            "deceased.first_name",
            "deceased.middle_name",
            "deceased.last_name",
            "deceased.maiden_name",
            "deceased.mothers_maiden_name",
            "deceased.date_of_birth",
            "deceased.social_insurance_number",
            "deceased.date_of_death",
            "deceased.cause_of_death",
            "deceased.place_of_death",
            "deceased.marital_status",
            "deceased.place_of_birth",
            "deceased.name_at_birth",
            "deceased.mothers_name",
            "deceased.fathers_name",
            "deceased.fathers_family_name",
            "deceased.health_care_number",
            "deceased.social_insurance_name",
            "deceased.gender",
            "deceased.birth_certificate_location_hint",
            "deceased.ethnicity",
            "deceased.citizenship_status",
            "deceased.date_of_funeral",
            "deceased.proof_of_death",
            "deceased.voter_registration",
            "deceased.pension_plans[*]",
            "deceased.home_address",
            "deceased.mailing_address",
            "deceased.is_mailing_address_same_as_home_address",
            "deceased.home_address.street",
            "deceased.home_address.city",
            "deceased.home_address.state",
            "deceased.home_address.zip_code",
            "deceased.home_address.street",
            "deceased.home_address.city",
            "deceased.home_address.state",
            "deceased.home_address.zip_code",
            
            # Date and applicant fields
            "date.today",
            "applicant.name",  # Full name (for backward compatibility)
            "applicant.first_name",
            "applicant.middle_name", 
            "applicant.last_name",
            "applicant.address",
            "applicant.phone",
            "applicant.phone_alt",
            "applicant.social_insurance_number",
            "applicant.role",
            "applicant.place_of_birth",
            "applicant.date_of_birth",
            "applicant.email",
            "applicant.mailing_address",
            "applicant.home_address",
            
            # Spouse fields
            "spouse.name",  # Full name (for backward compatibility)
            "spouse.first_name",
            "spouse.middle_name",
            "spouse.last_name",
            "spouse.date_of_birth",
            "spouse.social_insurance_number",
            "spouse.name_at_birth",
            "spouse.name_social_insurance",
            "spouse.address",
            "spouse.phone_number",
            "spouse.maiden_name",
            "spouse.place_of_birth",
            "spouse.mothers_name",
            "spouse.fathers_name",
            "spouse.date_of_marriage",
            "spouse.date_of_legal_separation",
            "spouse.date_of_divorce",
            "spouse.date_started_living_with_spouse",
            "spouse.date_last_lived_together",
            "spouse.marriage_location",
            "spouse.marriage_performed_by_name",
            "spouse.witness_1",
            "spouse.witness_2",
            "spouse.reason_for_no_marriage_certificate",
            "spouse.email",
            "spouse.home_address",
            "spouse.mailing_address",
            
            # Funeral home fields
            "funeral_home.funeral_director.name",
            "funeral_home.name",
            "funeral_home.address",
            "funeral_home.phone",
            "funeral_home.phone_alt",
            "funeral_home.email",
            "funeral_home.website",
            
            # Payment fields
            "payment.canadian_direct_deposit",
            "payment.allow_share_direct_deposit_with_cra",
            "payment.bank_name",
            "payment.account_number",
            "payment.transit_number",
            "payment.institution_number",
            
            # Children fields
            "children[*].name",  # Full name (for backward compatibility)
            "children[*].first_name",
            "children[*].middle_name",
            "children[*].last_name",
            "children[*].date_of_birth",
            "children[*].social_insurance_number",
            "children[*].place_of_birth",
            "children[*].address",
            "children[*].phone",
            "children[*].email",
            "children[*].gender",
            "children[*].relationship",
            "children[*].guardian_name",
            
            # Estate representatives fields
            "estate_reps[*].name",  # Full name (for backward compatibility)
            "estate_reps[*].first_name",
            "estate_reps[*].middle_name",
            "estate_reps[*].last_name",
            "estate_reps[*].phone",
            "estate_reps[*].email",
            "estate_reps[*].primary_relationship_to_deceased",
            "estate_reps[*].secondary_relationship_to_deceased",
            "estate_reps[*].address",
            "estate_reps[*].date_of_birth",
            "estate_reps[*].social_insurance_number",
            "estate_reps[*].proof_of_authority",
            "estate_reps[*].photo_id",
            "estate_reps[*].home_address",
            "estate_reps[*].mailing_address",
            "estate_reps[*].role",
            "estate_reps[*].appointment_date",
            
            # Contact fields
            "contact[*].address.address_location",
            "contact[*].address.type",
            "contact[*].phone.phone_number",
            "contact[*].phone.type",
            "contact[*].email.email_address",
            "contact[*].email.type",
            "contact[*].name",  # Full name (for backward compatibility)
            "contact[*].first_name",
            "contact[*].middle_name", 
            "contact[*].last_name",
            "contact[*].maiden_name",
            "contact[*].date_of_birth",
            "contact[*].gender",
            "contact[*].notes",
            "contact[*].relationship",
            "contact[*].professional_relationship",
            "contact[*].company_name",
            "contact[*].job_title",
            "contact[*].emergency_contact",
            
            # Will fields
            "will.location_hint",
            "will.date_created",
            "will.last_updated",
            "will.notes",
            "will.attachment",
            "will.executor_name",
            "will.lawyer_name",
            "will.lawyer_contact",
            "will.witness_1",
            "will.witness_2",
            "will.notarized",
            "will.copies_location",
            
            # Key documents
            "key_document[*].type",
            "key_document[*].name",
            "key_document[*].location_hint",
            "key_document[*].date_created",
            "key_document.signature_date",
            "key_document[*].last_updated",
            "key_document[*].notes",
            "key_document[*].id",
            "key_document[*].attachment",
            "key_document[*].issuing_authority",
            "key_document[*].document_number",
            
            # ID documents
            "id_document[*].type",
            "id_document[*].name",
            "id_document[*].id",
            "id_document[*].notes",
            "id_document[*].attachment",
            "id_document[*].expiry_date",
            "id_document[*].issuing_authority",
            "id_document[*].document_number",
            "id_document[*].issue_date",
            
            # Insurance
            "insurance[*].type",
            "insurance[*].name",
            "insurance[*].id",
            "insurance[*].notes",
            "insurance[*].attachment",
            "insurance[*].expiry_date",
            "insurance[*].policy_number",
            "insurance[*].premium",
            "insurance[*].beneficiary",
            "insurance[*].coverage_amount",
            "insurance[*].agent_name",
            "insurance[*].agent_contact",
            
            # Financial information
            "financial_information[*].type",
            "financial_information[*].name",
            "financial_information[*].id",
            "financial_information[*].notes",
            "financial_information[*].attachment",
            "financial_information[*].expiry_date",
            "financial_information[*].account_number",
            "financial_information[*].balance",
            "financial_information[*].institution_name",
            "financial_information[*].contact_person",
            "financial_information[*].branch_address",
            "financial_information[*].investment_type",
            "financial_information[*].maturity_date",
            "financial_information[*].beneficiary",
            "financial_information.total_estate_value",
            "financial_information.liquid_assets",
            "financial_information.real_estate_value",
            "financial_information.personal_property_value",
            "financial_information.outstanding_debts",
            
            # Bank accounts specific
            "financial_information.bank_accounts[*].account_number",
            "financial_information.bank_accounts[*].account_type",
            "financial_information.bank_accounts[*].bank_name",
            "financial_information.bank_accounts[*].branch_address",
            "financial_information.bank_accounts[*].balance",
            "financial_information.bank_accounts[*].joint_account",
            "financial_information.bank_accounts[*].contact_person",
            
            # Utilities
            "utility[*].type",
            "utility[*].name",
            "utility[*].id",
            "utility[*].notes",
            "utility[*].attachment",
            "utility[*].expiry_date",
            "utility[*].account_number",
            "utility[*].service_address",
            "utility[*].contact_phone",
            "utility[*].monthly_amount",
            
            # Property
            "property[*].type",
            "property[*].name",
            "property[*].notes",
            "property[*].id",
            "property[*].attachment",
            "property[*].address",
            "property[*].estimated_value",
            "property[*].mortgage_holder",
            "property[*].mortgage_balance",
            "property[*].property_tax_account",
            "property[*].insurance_company",
            "property[*].deed_location",
            
            # Real estate specific
            "property.real_estate[*].address",
            "property.real_estate[*].property_type",
            "property.real_estate[*].estimated_value",
            "property.real_estate[*].mortgage_holder",
            "property.real_estate[*].mortgage_balance",
            "property.real_estate[*].deed_location",
            "property.real_estate[*].property_tax_account",
            "property.real_estate[*].insurance_company",
            "property.real_estate[*].joint_ownership",
            
            # Vehicles specific
            "property.vehicles[*].make_model",
            "property.vehicles[*].year",
            "property.vehicles[*].vin",
            "property.vehicles[*].license_plate",
            "property.vehicles[*].estimated_value",
            "property.vehicles[*].loan_holder",
            "property.vehicles[*].loan_balance",
            "property.vehicles[*].insurance_company",
            "property.vehicles[*].registration_location",
            
            # Accounts
            "account[*].type",
            "account[*].name",
            "account[*].notes",
            "account[*].id",
            "account[*].email",
            "account[*].username",
            "account[*].password_location",
            "account[*].account_number",
            "account[*].subscription_cost",
            "account[*].renewal_date",
            "account[*].contact_info",
            
            # Final wishes - comprehensive
            "final_wishes.dependant_children.has_dependant_children",
            "final_wishes.dependant_children.notes",
            "final_wishes.dependant_children.guardian_arrangements",
            "final_wishes.pets.has_pets",
            "final_wishes.pets.notes",
            "final_wishes.pets.care_arrangements",
            "final_wishes.organ_donor.is_organ_donor",
            "final_wishes.organ_donor.notes",
            "final_wishes.organ_donor.registry_number",
            "final_wishes.disposition.vessel.type",
            "final_wishes.disposition.vessel.notes",
            "final_wishes.disposition.method.type",
            "final_wishes.disposition.method.notes",
            "final_wishes.disposition.location_description",
            "final_wishes.disposition.grave_marker_notes",
            "final_wishes.funeral.preferred_officiator.name",
            "final_wishes.funeral.preferred_officiator.notes",
            "final_wishes.funeral.ceremony.type",
            "final_wishes.funeral.ceremony.notes",
            "final_wishes.funeral.viewing.type",
            "final_wishes.funeral.viewing.notes",
            "final_wishes.funeral.military_honors.has_honors",
            "final_wishes.funeral.military_honors.notes",
            "final_wishes.funeral.florist.name",
            "final_wishes.funeral.florist.notes",
            "final_wishes.funeral.media.location_description",
            "final_wishes.funeral.media.notes",
            "final_wishes.funeral.funeral_home_name",
            "final_wishes.funeral.pallbearers",
            "final_wishes.funeral.clothing",
            "final_wishes.funeral.songs",
            "final_wishes.funeral.flowers",
            "final_wishes.funeral.readings",
            "final_wishes.funeral.notes",
            "final_wishes.funeral.food",
            "final_wishes.funeral.budget",
            "final_wishes.preparations.vessel.features",
            "final_wishes.preparations.vessel.notes",
            "final_wishes.preparations.plot.is_purchased",
            "final_wishes.preparations.plot.notes",
            "final_wishes.preparations.funeral_insurance.is_purchased",
            "final_wishes.preparations.funeral_insurance.notes",
            "final_wishes.preparations.body.type",
            "final_wishes.preparations.body.notes",
            "final_wishes.obituary.notes",
            "final_wishes.obituary.photo_location",
            "final_wishes.obituary.publication_preferences",
            
            # Task planner fields (Canada) - Complete set
            "task_planner.b_will",
            "task_planner.b_will_executor",
            "task_planner.b_multiple_executors",
            "task_planner.b_under_18",
            "task_planner.b_work_another_country",
            "task_planner.b_has_spouse",
            "task_planner.b_marriage_status",
            "task_planner.b_has_children",
            "task_planner.b_has_dependant_adults",
            "task_planner.b_has_pets_or_livestock",
            "task_planner.b_should_redirect_mail",
            "task_planner.b_has_physical_asset_insurance",
            "task_planner.b_has_or_lease_vehicles",
            "task_planner.b_has_firearms",
            "task_planner.b_has_pension_plan",
            "task_planner.b_has_life_insurance_or_annuities",
            "task_planner.b_has_trust",
            "task_planner.b_has_credit_cards_to_cancel",
            "task_planner.b_has_student_loans",
            "task_planner.b_has_extended_health_insurance",
            "task_planner.b_has_medic_alert",
            "task_planner.b_has_medical_equipment_to_return",
            "task_planner.b_online_accounts_to_close[*]",
            "task_planner.b_has_digital_currency",
            "task_planner.b_age_ca",
            "task_planner.b_last_province_ca",
            "task_planner.b_citizenship_ca",
            "task_planner.b_indigenous_status_ca",
            "task_planner.b_status_first_nations_ordinarily_on_reserve_or_crown_lands_ca",
            "task_planner.b_has_marriage_certificate_ca",
            "task_planner.b_surviving_spouse_age_ca",
            "task_planner.b_has_children_under_18_ca",
            "task_planner.b_has_children_18_25_full_time_school_ca",
            "task_planner.b_is_immigration_sponsor_ca",
            "task_planner.b_has_real_property_in_canada_ca",
            "task_planner.b_has_real_property_outside_canada_ca",
            "task_planner.b_has_farm_ca",
            "task_planner.b_has_mineral_rights_ca",
            "task_planner.b_is_tenant_ca",
            "task_planner.b_is_residential_landlord_ca",
            "task_planner.b_is_commercial_landlord_ca",
            "task_planner.b_companies_to_notify_ca[*]",
            "task_planner.b_licences_ids_ca[*]",
            "task_planner.b_education_employment_ca[*]",
            "task_planner.b_is_receiving_benefits_ca[*]",
            "task_planner.b_is_client_trustee_ca",
            "task_planner.b_has_csb_or_cpb_ca",
            "task_planner.b_has_other_investments_ca",
            "task_planner.b_programs_memberships_to_cancel_ca[*]",
            "task_planner.b_is_applying_for_cpp_death_benefit_ca",
            "task_planner.b_applying_for_cpp_death_benefit_as_ca",
            "task_planner.b_is_applying_for_qpp_death_benefit_ca",
            "task_planner.b_death_result_of_ca[*]",
            "task_planner.b_death_province_ca",
            "task_planner.b_estate_value_ca",
            
            # Task planner fields (USA) - Complete set
            "task_planner.b_age_usa",
            "task_planner.b_last_state_usa",
            "task_planner.b_citizenship_usa",
            "task_planner.b_indigenous_status_usa",
            "task_planner.b_surviving_spouse_age_usa",
            "task_planner.b_was_divorced_usa",
            "task_planner.b_has_children_age_usa[*]",
            "task_planner.b_green_card_sponsor_usa",
            "task_planner.b_has_real_property_in_united_states_usa",
            "task_planner.b_has_real_property_outside_united_states_usa",
            "task_planner.b_tenant_or_landlord_usa",
            "task_planner.b_services_to_notify_usa[*]",
            "task_planner.b_needs_to_notify_telecom_company_usa",
            "task_planner.b_telecom_companies_usa[*]",
            "task_planner.b_licences_ids_usa[*]",
            "task_planner.b_education_employment_usa[*]",
            "task_planner.b_is_receiving_benefits_usa",
            "task_planner.b_had_investments_usa",
            "task_planner.b_which_type_of_healthcare_usa[*]",
            "task_planner.b_programs_memberships_to_cancel_usa[*]",
            "task_planner.b_death_result_of_usa[*]",
            "task_planner.b_death_state_usa",
            "task_planner.b_estate_value_usa",
            "task_planner.b_insurance_and_annuities[*]",
            
            # Pre-need fields
            "pre_need.b_free_info",
            "pre_need.b_contact_at",
            "pre_need.b_contact_phone",
            "pre_need.b_contact_email",
            "pre_need.b_contact_notes",
            "pre_need.preferred_funeral_home",
            "pre_need.burial_plot_purchased",
            "pre_need.funeral_insurance",
            
            # Business documents - comprehensive
            "business_documents[*].type",
            "business_documents[*].business_name",
            "business_documents[*].name",
            "business_documents[*].location_hint",
            "business_documents[*].date_created",
            "business_documents[*].last_updated",
            "business_documents[*].notes",
            "business_documents[*].attachment",
            "business_documents[*].business_number",
            "business_documents[*].incorporation_date",
            "business_documents[*].registered_address",
            "business_documents[*].business_partners",
            "business_documents[*].accountant_contact",
            "business_documents[*].lawyer_contact",
            
            # Farm documents - comprehensive
            "farm_documents[*].type",
            "farm_documents[*].farm_name",
            "farm_documents[*].name",
            "farm_documents[*].location_hint",
            "farm_documents[*].date_created",
            "farm_documents[*].last_updated",
            "farm_documents[*].notes",
            "farm_documents[*].attachment",
            "farm_documents[*].expiry_date",
            "farm_documents[*].acreage",
            "farm_documents[*].livestock_count",
            "farm_documents[*].equipment_list",
            "farm_documents[*].crop_insurance",
            "farm_documents[*].agricultural_program_participation",
            
            # Specialized insurance types - comprehensive
            "insurance__health_medical[*].type",
            "insurance__health_medical[*].name",
            "insurance__health_medical[*].id",
            "insurance__health_medical[*].notes",
            "insurance__health_medical[*].attachment",
            "insurance__health_medical[*].expiry_date",
            "insurance__health_medical[*].policy_number",
            "insurance__health_medical[*].group_number",
            "insurance__health_medical[*].coverage_details",
            "insurance__health_medical[*].provider_network",
            
            "insurance__home_property[*].type",
            "insurance__home_property[*].name",
            "insurance__home_property[*].id",
            "insurance__home_property[*].notes",
            "insurance__home_property[*].attachment",
            "insurance__home_property[*].expiry_date",
            "insurance__home_property[*].policy_number",
            "insurance__home_property[*].coverage_amount",
            "insurance__home_property[*].deductible",
            "insurance__home_property[*].property_address",
            
            "insurance__life[*].type",
            "insurance__life[*].name",
            "insurance__life[*].id",
            "insurance__life[*].notes",
            "insurance__life[*].attachment",
            "insurance__life[*].expiry_date",
            "insurance__life[*].policy_number",
            "insurance__life[*].face_value",
            "insurance__life[*].cash_value",
            "insurance__life[*].beneficiary_primary",
            "insurance__life[*].beneficiary_secondary",
            
            "insurance__vehicle[*].type",
            "insurance__vehicle[*].name",
            "insurance__vehicle[*].id",
            "insurance__vehicle[*].notes",
            "insurance__vehicle[*].attachment",
            "insurance__vehicle[*].expiry_date",
            "insurance__vehicle[*].policy_number",
            "insurance__vehicle[*].vehicle_details",
            "insurance__vehicle[*].coverage_type",
            "insurance__vehicle[*].deductible",

            # ===== MISSING SCHEMA PATHS - NOW INCLUDED =====
            
            # ===== SPECIALIZED INSURANCE COMPANY TYPES =====
            # Individual insurance company specific paths
            "insurance__life__northwestern_mutual[*].type",
            "insurance__life__northwestern_mutual[*].name", 
            "insurance__life__northwestern_mutual[*].id",
            "insurance__life__northwestern_mutual[*].notes",
            "insurance__life__northwestern_mutual[*].attachment",
            "insurance__life__northwestern_mutual[*].expiry_date",
            
            "insurance__life__massmutual[*].type",
            "insurance__life__massmutual[*].name",
            "insurance__life__massmutual[*].id", 
            "insurance__life__massmutual[*].notes",
            "insurance__life__massmutual[*].attachment",
            "insurance__life__massmutual[*].expiry_date",
            
            "insurance__life__new_york_life[*].type",
            "insurance__life__new_york_life[*].name",
            "insurance__life__new_york_life[*].id",
            "insurance__life__new_york_life[*].notes", 
            "insurance__life__new_york_life[*].attachment",
            "insurance__life__new_york_life[*].expiry_date",
            
            "insurance__life__prudential[*].type",
            "insurance__life__prudential[*].name",
            "insurance__life__prudential[*].id",
            "insurance__life__prudential[*].notes",
            "insurance__life__prudential[*].attachment",
            "insurance__life__prudential[*].expiry_date",
            
            "insurance__life__lincoln_financial[*].type",
            "insurance__life__lincoln_financial[*].name",
            "insurance__life__lincoln_financial[*].id",
            "insurance__life__lincoln_financial[*].notes",
            "insurance__life__lincoln_financial[*].attachment", 
            "insurance__life__lincoln_financial[*].expiry_date",
            
            "insurance__life__john_hancock[*].type",
            "insurance__life__john_hancock[*].name",
            "insurance__life__john_hancock[*].id",
            "insurance__life__john_hancock[*].notes",
            "insurance__life__john_hancock[*].attachment",
            "insurance__life__john_hancock[*].expiry_date",
            
            "insurance__life__pacific_life[*].type",
            "insurance__life__pacific_life[*].name", 
            "insurance__life__pacific_life[*].id",
            "insurance__life__pacific_life[*].notes",
            "insurance__life__pacific_life[*].attachment",
            "insurance__life__pacific_life[*].expiry_date",
            
            "insurance__life__corebridge_financial[*].type",
            "insurance__life__corebridge_financial[*].name",
            "insurance__life__corebridge_financial[*].id",
            "insurance__life__corebridge_financial[*].notes",
            "insurance__life__corebridge_financial[*].attachment",
            "insurance__life__corebridge_financial[*].expiry_date",
            
            "insurance__life__midland_national[*].type",
            "insurance__life__midland_national[*].name",
            "insurance__life__midland_national[*].id",
            "insurance__life__midland_national[*].notes",
            "insurance__life__midland_national[*].attachment",
            "insurance__life__midland_national[*].expiry_date",
            
            "insurance__life__nationwide[*].type",
            "insurance__life__nationwide[*].name",
            "insurance__life__nationwide[*].id",
            "insurance__life__nationwide[*].notes",
            "insurance__life__nationwide[*].attachment",
            "insurance__life__nationwide[*].expiry_date",
            
            "insurance__life__pennmutual[*].type",
            "insurance__life__pennmutual[*].name",
            "insurance__life__pennmutual[*].id",
            "insurance__life__pennmutual[*].notes",
            "insurance__life__pennmutual[*].attachment",
            "insurance__life__pennmutual[*].expiry_date",
            
            "insurance__life__equitable[*].type",
            "insurance__life__equitable[*].name",
            "insurance__life__equitable[*].id",
            "insurance__life__equitable[*].notes",
            "insurance__life__equitable[*].attachment",
            "insurance__life__equitable[*].expiry_date",
            
            "insurance__life__national_life[*].type",
            "insurance__life__national_life[*].name",
            "insurance__life__national_life[*].id",
            "insurance__life__national_life[*].notes",
            "insurance__life__national_life[*].attachment",
            "insurance__life__national_life[*].expiry_date",
            
            "insurance__life__manulife[*].type",
            "insurance__life__manulife[*].name",
            "insurance__life__manulife[*].id",
            "insurance__life__manulife[*].notes",
            "insurance__life__manulife[*].attachment",
            "insurance__life__manulife[*].expiry_date",
            
            "insurance__life__industrial_alliance[*].type",
            "insurance__life__industrial_alliance[*].name",
            "insurance__life__industrial_alliance[*].id",
            "insurance__life__industrial_alliance[*].notes",
            "insurance__life__industrial_alliance[*].attachment",
            "insurance__life__industrial_alliance[*].expiry_date",
            
            "insurance__life__bmo[*].type",
            "insurance__life__bmo[*].name",
            "insurance__life__bmo[*].id", 
            "insurance__life__bmo[*].notes",
            "insurance__life__bmo[*].attachment",
            "insurance__life__bmo[*].expiry_date",
            
            "insurance__life__ivari[*].type",
            "insurance__life__ivari[*].name",
            "insurance__life__ivari[*].id",
            "insurance__life__ivari[*].notes",
            "insurance__life__ivari[*].attachment",
            "insurance__life__ivari[*].expiry_date",
            
            "deceased.name", "applicant.name", "spouse.name", "estate_reps[*].name", "children[*].name", "contact[*].name",
            
            # --- Nested Name objects ---
            "deceased.name.first", "deceased.name.middle", "deceased.name.last",
            "deceased.mothers_name.title", "deceased.mothers_name.first", "deceased.mothers_name.middle", "deceased.mothers_name.last",
            "deceased.fathers_name.title", "deceased.fathers_name.first", "deceased.fathers_name.middle", "deceased.fathers_name.last",
            "applicant.name.title", "applicant.name.first", "applicant.name.middle", "applicant.name.last",
            "spouse.name.title", "spouse.name.first", "spouse.name.middle", "spouse.name.last",
            "estate_reps[*].name.title", "estate_reps[*].name.first", "estate_reps[*].name.middle", "estate_reps[*].name.last",
            "children[*].name.title", "children[*].name.first", "children[*].name.middle", "children[*].name.last",
            "contact[*].name.title", "contact[*].name.first", "contact[*].name.middle", "contact[*].name.last",
            
            # --- Nested Phone objects ---
            "estate_reps[*].phone.digits", "estate_reps[*].phone.ext",

            # --- Nested Address objects ---
            "estate_reps[*].address.street", "estate_reps[*].address.city", "estate_reps[*].address.postal_code",
            "estate_reps[*].address.country", "estate_reps[*].address.country_code", "estate_reps[*].address.province",
            "estate_reps[*].address.province_code", "estate_reps[*].address.county",
            "spouse.place_of_birth.street", "spouse.place_of_birth.city", "spouse.place_of_birth.postal_code",
            "spouse.place_of_birth.country", "spouse.place_of_birth.country_code", "spouse.place_of_birth.province",
            "spouse.place_of_birth.province_code", "spouse.place_of_birth.county",
            "children[*].place_of_birth.street", "children[*].place_of_birth.city", "children[*].place_of_birth.postal_code",
            "children[*].place_of_birth.country", "children[*].place_of_birth.country_code", "children[*].place_of_birth.province",
            "children[*].place_of_birth.province_code", "children[*].place_of_birth.county",

            # --- Letter Template Paths (from 24.json and others) ---
            "primary_estate_rep.name",
            "primary_estate_rep.address.street",
            "primary_estate_rep.address.city",
            "primary_estate_rep.address.postal_code",
            "primary_estate_rep.phone",
            "primary_estate_rep.email",
            "secondary_estate_reps",
            "secondary_estate_reps[*].name",
            "secondary_estate_reps[*].address",
            "secondary_estate_reps[*].phone",
            "secondary_estate_reps[*].email",
            "id_document__drivers_license.0.id", # Specific index from letter

            # --- Specialized Insurance and Account Paths (from field-values.json) ---
            "insurance__home_property[*].type", "insurance__home_property[*].name", "insurance__home_property[*].id",
            "insurance__home_property[*].attachment", "insurance__home_property[*].expiry_date",
            "account__digital_account__google[*].type", "account__digital_account__google[*].name", "account__digital_account__google[*].notes",
            "account__digital_account__google[*].id", "account__digital_account__google[*].email",
            # ===== SPECIALIZED ACCOUNT TYPES =====
            
            "account__computer_login[*].type",
            "account__computer_login[*].name",
            "account__computer_login[*].notes",
            "account__computer_login[*].id",
            "account__computer_login[*].email",
            
            "account__crypto_wallet[*].type",
            "account__crypto_wallet[*].name",
            "account__crypto_wallet[*].notes",
            "account__crypto_wallet[*].id",
            "account__crypto_wallet[*].email",
            
            "account__digital_account__paypal[*].type",
            "account__digital_account__paypal[*].name",
            "account__digital_account__paypal[*].notes",
            "account__digital_account__paypal[*].id",
            "account__digital_account__paypal[*].email",
            
            "account__digital_account__google[*].type",
            "account__digital_account__google[*].name",
            "account__digital_account__google[*].notes",
            "account__digital_account__google[*].id",
            "account__digital_account__google[*].email",
            
            "account__digital_account__facebook[*].type",
            "account__digital_account__facebook[*].name",
            "account__digital_account__facebook[*].notes",
            "account__digital_account__facebook[*].id",
            "account__digital_account__facebook[*].email",
            
            "account__digital_account__instagram[*].type",
            "account__digital_account__instagram[*].name",
            "account__digital_account__instagram[*].notes",
            "account__digital_account__instagram[*].id",
            "account__digital_account__instagram[*].email",
            
            "account__digital_account__linkedin[*].type",
            "account__digital_account__linkedin[*].name",
            "account__digital_account__linkedin[*].notes",
            "account__digital_account__linkedin[*].id",
            "account__digital_account__linkedin[*].email",
            
            "account__digital_account__pinterest[*].type",
            "account__digital_account__pinterest[*].name",
            "account__digital_account__pinterest[*].notes",
            "account__digital_account__pinterest[*].id",
            "account__digital_account__pinterest[*].email",
            
            "account__digital_account__twitter[*].type",
            "account__digital_account__twitter[*].name",
            "account__digital_account__twitter[*].notes",
            "account__digital_account__twitter[*].id",
            "account__digital_account__twitter[*].email",
            
            "account__digital_account__flickr[*].type",
            "account__digital_account__flickr[*].name",
            "account__digital_account__flickr[*].notes",
            "account__digital_account__flickr[*].id",
            "account__digital_account__flickr[*].email",
            
            # ===== SPECIALIZED DOCUMENT TYPES =====
            
            "key_document__marriage_contract[*].type",
            "key_document__marriage_contract[*].name",
            "key_document__marriage_contract[*].location_hint",
            "key_document__marriage_contract[*].date_created",
            "key_document__marriage_contract[*].last_updated",
            "key_document__marriage_contract[*].notes",
            "key_document__marriage_contract[*].id",
            "key_document__marriage_contract[*].attachment",
            
            "key_document__military[*].type",
            "key_document__military[*].name",
            "key_document__military[*].location_hint",
            "key_document__military[*].date_created",
            "key_document__military[*].last_updated",
            "key_document__military[*].notes",
            "key_document__military[*].id",
            "key_document__military[*].attachment",
            
            "key_document__tax_documents[*].type",
            "key_document__tax_documents[*].name",
            "key_document__tax_documents[*].location_hint",
            "key_document__tax_documents[*].date_created",
            "key_document__tax_documents[*].last_updated",
            "key_document__tax_documents[*].notes",
            "key_document__tax_documents[*].id",
            "key_document__tax_documents[*].attachment",
            
            "key_document__trust[*].type",
            "key_document__trust[*].name",
            "key_document__trust[*].location_hint",
            "key_document__trust[*].date_created",
            "key_document__trust[*].last_updated", 
            "key_document__trust[*].notes",
            "key_document__trust[*].id",
            "key_document__trust[*].attachment",
            
            # ===== SPECIALIZED ID DOCUMENT TYPES =====
            
            "id_document__accessible_parking_permit[*].type",
            "id_document__accessible_parking_permit[*].name",
            "id_document__accessible_parking_permit[*].id",
            "id_document__accessible_parking_permit[*].notes",
            "id_document__accessible_parking_permit[*].attachment",
            "id_document__accessible_parking_permit[*].expiry_date",
            
            "id_document__drivers_license[*].type",
            "id_document__drivers_license[*].name",
            "id_document__drivers_license[*].id",
            "id_document__drivers_license[*].notes",
            "id_document__drivers_license[*].attachment", 
            "id_document__drivers_license[*].expiry_date",
            
            "id_document__firearm_license[*].type",
            "id_document__firearm_license[*].name",
            "id_document__firearm_license[*].id",
            "id_document__firearm_license[*].notes",
            "id_document__firearm_license[*].attachment",
            "id_document__firearm_license[*].expiry_date",
            
            "id_document__health_card[*].type",
            "id_document__health_card[*].name",
            "id_document__health_card[*].id",
            "id_document__health_card[*].notes",
            "id_document__health_card[*].attachment",
            "id_document__health_card[*].expiry_date",
            
            "id_document__nexus[*].type",
            "id_document__nexus[*].name",
            "id_document__nexus[*].id",
            "id_document__nexus[*].notes",
            "id_document__nexus[*].attachment",
            "id_document__nexus[*].expiry_date",
            
            "id_document__passport[*].type",
            "id_document__passport[*].name",
            "id_document__passport[*].id",
            "id_document__passport[*].notes",
            "id_document__passport[*].attachment",
            "id_document__passport[*].expiry_date",
            
            # ===== SPECIALIZED FINANCIAL TYPES =====
            
            "financial_information__bank_financial_services_provider[*].type",
            "financial_information__bank_financial_services_provider[*].name",
            "financial_information__bank_financial_services_provider[*].id",
            "financial_information__bank_financial_services_provider[*].notes",
            "financial_information__bank_financial_services_provider[*].attachment",
            "financial_information__bank_financial_services_provider[*].expiry_date",
            
            "financial_information__credit_card[*].type",
            "financial_information__credit_card[*].name",
            "financial_information__credit_card[*].id",
            "financial_information__credit_card[*].notes",
            "financial_information__credit_card[*].attachment",
            "financial_information__credit_card[*].expiry_date",
            
            "financial_information__investment_provider[*].type",
            "financial_information__investment_provider[*].name",
            "financial_information__investment_provider[*].id",
            "financial_information__investment_provider[*].notes",
            "financial_information__investment_provider[*].attachment",
            "financial_information__investment_provider[*].expiry_date",
            
            "financial_information__lease[*].type",
            "financial_information__lease[*].name", 
            "financial_information__lease[*].id",
            "financial_information__lease[*].notes",
            "financial_information__lease[*].attachment",
            "financial_information__lease[*].expiry_date",
            
            "financial_information__loan[*].type",
            "financial_information__loan[*].name",
            "financial_information__loan[*].id",
            "financial_information__loan[*].notes",
            "financial_information__loan[*].attachment",
            "financial_information__loan[*].expiry_date",
            
            "financial_information__pension[*].type",
            "financial_information__pension[*].name",
            "financial_information__pension[*].id",
            "financial_information__pension[*].notes",
            "financial_information__pension[*].attachment",
            "financial_information__pension[*].expiry_date",
            
            "financial_information__philanthropy_charity[*].type",
            "financial_information__philanthropy_charity[*].name",
            "financial_information__philanthropy_charity[*].id",
            "financial_information__philanthropy_charity[*].notes",
            "financial_information__philanthropy_charity[*].attachment",
            "financial_information__philanthropy_charity[*].expiry_date",
            
            # ===== SPECIALIZED PROPERTY TYPES =====
            
            "property__computer[*].type",
            "property__computer[*].name",
            "property__computer[*].notes",
            "property__computer[*].id",
            "property__computer[*].attachment",
            
            "property__firearm[*].type",
            "property__firearm[*].name",
            "property__firearm[*].notes",
            "property__firearm[*].id",
            "property__firearm[*].attachment",
            
            "property__real_estate[*].type",
            "property__real_estate[*].name",
            "property__real_estate[*].notes",
            "property__real_estate[*].id",
            "property__real_estate[*].attachment",
            
            "property__vehicle[*].type",
            "property__vehicle[*].name",
            "property__vehicle[*].notes",
            "property__vehicle[*].id",
            "property__vehicle[*].attachment",
            
            # ===== SPECIALIZED UTILITY TYPES =====
            
            "utility__electricity[*].type",
            "utility__electricity[*].name",
            "utility__electricity[*].id",
            "utility__electricity[*].notes",
            "utility__electricity[*].attachment",
            "utility__electricity[*].expiry_date",
            
            "utility__property_taxes[*].type",
            "utility__property_taxes[*].name",
            "utility__property_taxes[*].id",
            "utility__property_taxes[*].notes",
            "utility__property_taxes[*].attachment",
            "utility__property_taxes[*].expiry_date",
            
            "utility__gas_hydro[*].type",
            "utility__gas_hydro[*].name",
            "utility__gas_hydro[*].id",
            "utility__gas_hydro[*].notes",
            "utility__gas_hydro[*].attachment",
            "utility__gas_hydro[*].expiry_date",
            
            "utility__water[*].type",
            "utility__water[*].name",
            "utility__water[*].id",
            "utility__water[*].notes",
            "utility__water[*].attachment",
            "utility__water[*].expiry_date",
            
            "utility__internet[*].type",
            "utility__internet[*].name",
            "utility__internet[*].id",
            "utility__internet[*].notes",
            "utility__internet[*].attachment",
            "utility__internet[*].expiry_date",
            
            "utility__phone[*].type",
            "utility__phone[*].name",
            "utility__phone[*].id",
            "utility__phone[*].notes",
            "utility__phone[*].attachment",
            "utility__phone[*].expiry_date",
            
            # ===== BUSINESS DOCUMENT TYPES =====
            
            "business_documents__letter_of_intent[*].type",
            "business_documents__letter_of_intent[*].business_name",
            "business_documents__letter_of_intent[*].name",
            "business_documents__letter_of_intent[*].location_hint",
            "business_documents__letter_of_intent[*].date_created",
            "business_documents__letter_of_intent[*].last_updated",
            "business_documents__letter_of_intent[*].notes",
            "business_documents__letter_of_intent[*].attachment",
            
            "business_documents__succession_plan[*].type",
            "business_documents__succession_plan[*].business_name",
            "business_documents__succession_plan[*].name",
            "business_documents__succession_plan[*].location_hint",
            "business_documents__succession_plan[*].date_created",
            "business_documents__succession_plan[*].last_updated",
            "business_documents__succession_plan[*].notes",
            "business_documents__succession_plan[*].attachment",
            
            "business_documents__asset[*].type",
            "business_documents__asset[*].business_name",
            "business_documents__asset[*].name",
            "business_documents__asset[*].location_hint",
            "business_documents__asset[*].date_created",
            "business_documents__asset[*].last_updated",
            "business_documents__asset[*].notes",
            "business_documents__asset[*].attachment",
            
            "business_documents__liability[*].type",
            "business_documents__liability[*].business_name",
            "business_documents__liability[*].name",
            "business_documents__liability[*].location_hint",
            "business_documents__liability[*].date_created",
            "business_documents__liability[*].last_updated",
            "business_documents__liability[*].notes",
            "business_documents__liability[*].attachment",
            
            "business_documents__digital_asset[*].type",
            "business_documents__digital_asset[*].business_name",
            "business_documents__digital_asset[*].name",
            "business_documents__digital_asset[*].location_hint",
            "business_documents__digital_asset[*].date_created",
            "business_documents__digital_asset[*].last_updated",
            "business_documents__digital_asset[*].notes",
            "business_documents__digital_asset[*].attachment",
            
            "business_documents__tax[*].type",
            "business_documents__tax[*].business_name",
            "business_documents__tax[*].name",
            "business_documents__tax[*].location_hint",
            "business_documents__tax[*].date_created",
            "business_documents__tax[*].last_updated",
            "business_documents__tax[*].notes",
            "business_documents__tax[*].attachment",
            
            "business_documents__property_title[*].type",
            "business_documents__property_title[*].business_name",
            "business_documents__property_title[*].name",
            "business_documents__property_title[*].location_hint",
            "business_documents__property_title[*].date_created",
            "business_documents__property_title[*].last_updated",
            "business_documents__property_title[*].notes",
            "business_documents__property_title[*].attachment",
            
            "business_documents__insurance_policy[*].type",
            "business_documents__insurance_policy[*].business_name",
            "business_documents__insurance_policy[*].name",
            "business_documents__insurance_policy[*].location_hint",
            "business_documents__insurance_policy[*].date_created",
            "business_documents__insurance_policy[*].last_updated",
            "business_documents__insurance_policy[*].notes",
            "business_documents__insurance_policy[*].attachment",
            
            # ===== FARM DOCUMENT TYPES =====
            
            "farm_documents__operating_agreement[*].type",
            "farm_documents__operating_agreement[*].farm_name",
            "farm_documents__operating_agreement[*].name",
            "farm_documents__operating_agreement[*].location_hint",
            "farm_documents__operating_agreement[*].date_created",
            "farm_documents__operating_agreement[*].last_updated",
            "farm_documents__operating_agreement[*].notes",
            "farm_documents__operating_agreement[*].attachment",
            "farm_documents__operating_agreement[*].expiry_date",
            
            "farm_documents__land_title[*].type",
            "farm_documents__land_title[*].farm_name",
            "farm_documents__land_title[*].name",
            "farm_documents__land_title[*].location_hint",
            "farm_documents__land_title[*].date_created",
            "farm_documents__land_title[*].last_updated",
            "farm_documents__land_title[*].notes",
            "farm_documents__land_title[*].attachment",
            "farm_documents__land_title[*].expiry_date",
            
            "farm_documents__equipment_title[*].type",
            "farm_documents__equipment_title[*].farm_name",
            "farm_documents__equipment_title[*].name",
            "farm_documents__equipment_title[*].location_hint",
            "farm_documents__equipment_title[*].date_created",
            "farm_documents__equipment_title[*].last_updated",
            "farm_documents__equipment_title[*].notes",
            "farm_documents__equipment_title[*].attachment",
            "farm_documents__equipment_title[*].expiry_date",
            
            "farm_documents__insurance_policy[*].type",
            "farm_documents__insurance_policy[*].farm_name",
            "farm_documents__insurance_policy[*].name",
            "farm_documents__insurance_policy[*].location_hint",
            "farm_documents__insurance_policy[*].date_created",
            "farm_documents__insurance_policy[*].last_updated",
            "farm_documents__insurance_policy[*].notes",
            "farm_documents__insurance_policy[*].attachment",
            "farm_documents__insurance_policy[*].expiry_date",
            
            "farm_documents__lease[*].type",
            "farm_documents__lease[*].farm_name",
            "farm_documents__lease[*].name",
            "farm_documents__lease[*].location_hint",
            "farm_documents__lease[*].date_created",
            "farm_documents__lease[*].last_updated",
            "farm_documents__lease[*].notes",
            "farm_documents__lease[*].attachment",
            "farm_documents__lease[*].expiry_date",
            
            "farm_documents__water_rights[*].type",
            "farm_documents__water_rights[*].farm_name",
            "farm_documents__water_rights[*].name",
            "farm_documents__water_rights[*].location_hint",
            "farm_documents__water_rights[*].date_created",
            "farm_documents__water_rights[*].last_updated",
            "farm_documents__water_rights[*].notes",
            "farm_documents__water_rights[*].attachment",
            "farm_documents__water_rights[*].expiry_date",
            
            "farm_documents__conservation_program_contract[*].type",
            "farm_documents__conservation_program_contract[*].farm_name",
            "farm_documents__conservation_program_contract[*].name",
            "farm_documents__conservation_program_contract[*].location_hint",
            "farm_documents__conservation_program_contract[*].date_created",
            "farm_documents__conservation_program_contract[*].last_updated",
            "farm_documents__conservation_program_contract[*].notes",
            "farm_documents__conservation_program_contract[*].attachment",
            "farm_documents__conservation_program_contract[*].expiry_date",
            
            "farm_documents__environmental_compliance[*].type",
            "farm_documents__environmental_compliance[*].farm_name",
            "farm_documents__environmental_compliance[*].name",
            "farm_documents__environmental_compliance[*].location_hint",
            "farm_documents__environmental_compliance[*].date_created",
            "farm_documents__environmental_compliance[*].last_updated",
            "farm_documents__environmental_compliance[*].notes",
            "farm_documents__environmental_compliance[*].attachment",
            "farm_documents__environmental_compliance[*].expiry_date",
            
            "farm_documents__financial_statement[*].type",
            "farm_documents__financial_statement[*].farm_name",
            "farm_documents__financial_statement[*].name",
            "farm_documents__financial_statement[*].location_hint",
            "farm_documents__financial_statement[*].date_created",
            "farm_documents__financial_statement[*].last_updated",
            "farm_documents__financial_statement[*].notes",
            "farm_documents__financial_statement[*].attachment",
            "farm_documents__financial_statement[*].expiry_date",
            
            "farm_documents__tax[*].type",
            "farm_documents__tax[*].farm_name",
            "farm_documents__tax[*].name",
            "farm_documents__tax[*].location_hint",
            "farm_documents__tax[*].date_created",
            "farm_documents__tax[*].last_updated",
            "farm_documents__tax[*].notes",
            "farm_documents__tax[*].attachment",
            "farm_documents__tax[*].expiry_date",
            
            "farm_documents__agricultural_loan[*].type",
            "farm_documents__agricultural_loan[*].farm_name",
            "farm_documents__agricultural_loan[*].name",
            "farm_documents__agricultural_loan[*].location_hint",
            "farm_documents__agricultural_loan[*].date_created",
            "farm_documents__agricultural_loan[*].last_updated",
            "farm_documents__agricultural_loan[*].notes",
            "farm_documents__agricultural_loan[*].attachment",
            "farm_documents__agricultural_loan[*].expiry_date",
            
            "farm_documents__transfer_on_death_deed[*].type",
            "farm_documents__transfer_on_death_deed[*].farm_name",
            "farm_documents__transfer_on_death_deed[*].name",
            "farm_documents__transfer_on_death_deed[*].location_hint",
            "farm_documents__transfer_on_death_deed[*].date_created",
            "farm_documents__transfer_on_death_deed[*].last_updated",
            "farm_documents__transfer_on_death_deed[*].notes",
            "farm_documents__transfer_on_death_deed[*].attachment",
            "farm_documents__transfer_on_death_deed[*].expiry_date",
            
            "farm_documents__trust[*].type",
            "farm_documents__trust[*].farm_name",
            "farm_documents__trust[*].name",
            "farm_documents__trust[*].location_hint",
            "farm_documents__trust[*].date_created",
            "farm_documents__trust[*].last_updated",
            "farm_documents__trust[*].notes",
            "farm_documents__trust[*].attachment",
            "farm_documents__trust[*].expiry_date",
            
            "farm_documents__estate_plan_integration[*].type",
            "farm_documents__estate_plan_integration[*].farm_name",
            "farm_documents__estate_plan_integration[*].name",
            "farm_documents__estate_plan_integration[*].location_hint",
            "farm_documents__estate_plan_integration[*].date_created",
            "farm_documents__estate_plan_integration[*].last_updated",
            "farm_documents__estate_plan_integration[*].notes",
            "farm_documents__estate_plan_integration[*].attachment",
            "farm_documents__estate_plan_integration[*].expiry_date",
        ]
    
    def _load_schema_field_types(self) -> Dict[str, str]:
        """Load field types from schema dataset - COMPLETE WITH ALL MISSING TYPES"""
        return {
            # ===== EXISTING FIELD TYPES =====
            # Basic deceased fields
            "deceased.phone[*].phone_number": "phone",
            "deceased.email[*].email_address": "email",
            "deceased.name": "name",
            "deceased.first_name": "name",
            "deceased.middle_name": "name", 
            "deceased.last_name": "name",
            "deceased.maiden_name": "name",
            "deceased.mothers_maiden_name": "name",
            "deceased.date_of_birth": "date",
            "deceased.social_insurance_number": "sin",
            "deceased.date_of_death": "date",
            "deceased.place_of_death": "location",
            "deceased.place_of_birth": "location", 
            "deceased.mothers_name": "name",
            "deceased.fathers_name": "name",
            "deceased.home_address": "location",
            "deceased.mailing_address": "location",
            "deceased.proof_of_death": "file",
            "deceased.gender": "select",
            "deceased.marital_status": "select",
            "deceased.citizenship_status": "select",
            
            # Applicant fields
            "applicant.name": "name",
            "applicant.first_name": "name",
            "applicant.middle_name": "name",
            "applicant.last_name": "name",
            "applicant.address": "location",
            "applicant.phone": "phone",
            "applicant.email": "email",
            "applicant.date_of_birth": "date",
            "applicant.social_insurance_number": "sin",
            
            
            # Spouse fields
            "spouse.name": "name",
            "spouse.first_name": "name",
            "spouse.middle_name": "name",
            "spouse.last_name": "name",
            "spouse.maiden_name": "name",
            "spouse.date_of_birth": "date",
            "spouse.social_insurance_number": "sin",
            "spouse.address": "location",
            "spouse.phone_number": "phone",
            "spouse.place_of_birth": "location",
            "spouse.email": "email",
            "spouse.date_of_marriage": "date",
            "spouse.date_of_divorce": "date",
            
            # Children fields
            "children[*].name": "name",
            "children[*].first_name": "name",
            "children[*].middle_name": "name",
            "children[*].last_name": "name",
            "children[*].date_of_birth": "date",
            "children[*].social_insurance_number": "sin",
            "children[*].place_of_birth": "location",
            "children[*].phone": "phone",
            "children[*].email": "email",
            "children[*].address": "location",
            
            # Estate representatives
            "estate_reps[*].name": "name",
            "estate_reps[*].first_name": "name",
            "estate_reps[*].middle_name": "name",
            "estate_reps[*].last_name": "name",
            "estate_reps[*].phone": "phone",
            "estate_reps[*].email": "email",
            "estate_reps[*].address": "location",
            "estate_reps[*].date_of_birth": "date",
            "estate_reps[*].social_insurance_number": "sin",
            
            # Contact fields
            "contact[*].address.address_location": "location",
            "contact[*].phone.phone_number": "phone",
            "contact[*].email.email_address": "email",
            "contact[*].name": "name",
            "contact[*].first_name": "name",
            "contact[*].middle_name": "name",
            "contact[*].last_name": "name",
            "contact[*].maiden_name": "name",
            "contact[*].date_of_birth": "date",
            
            # Will fields
            "will.date_created": "date",
            "will.last_updated": "date",
            "will.attachment": "file",
            
            # Documents
            "id_document[*].expiry_date": "date",
            "id_document[*].attachment": "file",
            "key_document[*].date_created": "date",
            "key_document[*].attachment": "file",
            
            # Insurance
            "insurance[*].expiry_date": "date",
            "insurance[*].attachment": "file",
            "insurance[*].policy_number": "string",
            "insurance[*].premium": "currency",
            "insurance[*].coverage_amount": "currency",
            
            # Financial
            "financial_information[*].account_number": "string",
            "financial_information[*].balance": "currency",
            "financial_information.total_estate_value": "currency",
            "financial_information.bank_accounts[*].balance": "currency",
            
            # Property
            "property.real_estate[*].estimated_value": "currency",
            "property.real_estate[*].mortgage_balance": "currency",
            "property.vehicles[*].estimated_value": "currency",
            "property.vehicles[*].loan_balance": "currency",
            
            # Payment
            "payment.canadian_direct_deposit": "direct_deposit",
            "payment.account_number": "string",
            "payment.transit_number": "string",
            
            # Dates
            "date.today": "date",
            
            # Task planner booleans
            "task_planner.b_will": "boolean",
            "task_planner.b_has_spouse": "boolean", 
            "task_planner.b_has_children": "boolean",
            "task_planner.b_has_life_insurance_or_annuities": "boolean",

            # ===== MISSING FIELD TYPES - NOW INCLUDED =====
            # Core personal information fields
            "deceased.email": "email",
            "applicant.home_address": "address",
            "applicant.mailing_address": "address",
            "spouse.home_address": "address",
            "spouse.mailing_address": "address",
            
            "contact[*].company_name": "string",
            "contact[*].job_title": "string",
            "contact[*].emergency_contact": "boolean",
            
            "estate_reps[*].home_address": "address",
            "estate_reps[*].mailing_address": "address",
            "estate_reps[*].role": "select",
            "estate_reps[*].appointment_date": "date",
            
            "funeral_home.email": "email",
            "funeral_home.website": "url",
            
            # Financial information fields
            "financial_information.liquid_assets": "currency",
            "financial_information.real_estate_value": "currency",
            "financial_information.personal_property_value": "currency",
            "financial_information.outstanding_debts": "currency",
            
            "financial_information.bank_accounts[*].account_type": "select",
            "financial_information.bank_accounts[*].bank_name": "string",
            "financial_information.bank_accounts[*].branch_address": "address",
            "financial_information.bank_accounts[*].joint_account": "boolean",
            "financial_information.bank_accounts[*].contact_person": "string",
            
            # Property details
            "property.real_estate[*].property_type": "select",
            "property.real_estate[*].mortgage_holder": "string",
            "property.real_estate[*].deed_location": "string",
            "property.real_estate[*].property_tax_account": "string",
            "property.real_estate[*].insurance_company": "string",
            "property.real_estate[*].joint_ownership": "boolean",
            
            "property.vehicles[*].make_model": "string",
            "property.vehicles[*].year": "number",
            "property.vehicles[*].vin": "string",
            "property.vehicles[*].license_plate": "string",
            "property.vehicles[*].loan_holder": "string",
            "property.vehicles[*].loan_balance": "currency",
            "property.vehicles[*].insurance_company": "string",
            "property.vehicles[*].registration_location": "string",
            
            # Payment information
            "payment.bank_name": "string",
            "payment.institution_number": "string",
            
            # Pre-need arrangements
            "pre_need.preferred_funeral_home": "string",
            "pre_need.burial_plot_purchased": "boolean",
            "pre_need.funeral_insurance": "boolean",
            
            # Extended insurance details
            "insurance[*].agent_name": "string",
            "insurance[*].agent_contact": "string",
            
            "insurance__health_medical[*].policy_number": "string",
            "insurance__health_medical[*].group_number": "string",
            "insurance__health_medical[*].coverage_details": "text",
            "insurance__health_medical[*].provider_network": "string",
            
            "insurance__home_property[*].policy_number": "string",
            "insurance__home_property[*].coverage_amount": "currency",
            "insurance__home_property[*].deductible": "currency",
            "insurance__home_property[*].property_address": "address",
            
            "insurance__life[*].policy_number": "string",
            "insurance__life[*].face_value": "currency",
            "insurance__life[*].cash_value": "currency",
            "insurance__life[*].beneficiary_primary": "string",
            "insurance__life[*].beneficiary_secondary": "string",
            
            "insurance__vehicle[*].policy_number": "string",
            "insurance__vehicle[*].vehicle_details": "string",
            "insurance__vehicle[*].coverage_type": "select",
            "insurance__vehicle[*].deductible": "currency",

            # All insurance company specific fields
            "insurance__life__northwestern_mutual[*].type": "select",
            "insurance__life__northwestern_mutual[*].name": "select", 
            "insurance__life__northwestern_mutual[*].id": "string",
            "insurance__life__northwestern_mutual[*].notes": "string",
            "insurance__life__northwestern_mutual[*].attachment": "file",
            "insurance__life__northwestern_mutual[*].expiry_date": "date",
            
            "insurance__life__massmutual[*].type": "select",
            "insurance__life__massmutual[*].name": "select",
            "insurance__life__massmutual[*].id": "string", 
            "insurance__life__massmutual[*].notes": "string",
            "insurance__life__massmutual[*].attachment": "file",
            "insurance__life__massmutual[*].expiry_date": "date",
            
            "insurance__life__new_york_life[*].type": "select",
            "insurance__life__new_york_life[*].name": "select",
            "insurance__life__new_york_life[*].id": "string",
            "insurance__life__new_york_life[*].notes": "string", 
            "insurance__life__new_york_life[*].attachment": "file",
            "insurance__life__new_york_life[*].expiry_date": "date",
            
            "insurance__life__prudential[*].type": "select",
            "insurance__life__prudential[*].name": "select",
            "insurance__life__prudential[*].id": "string",
            "insurance__life__prudential[*].notes": "string",
            "insurance__life__prudential[*].attachment": "file",
            "insurance__life__prudential[*].expiry_date": "date",
            
            "insurance__life__lincoln_financial[*].type": "select",
            "insurance__life__lincoln_financial[*].name": "select",
            "insurance__life__lincoln_financial[*].id": "string",
            "insurance__life__lincoln_financial[*].notes": "string",
            "insurance__life__lincoln_financial[*].attachment": "file", 
            "insurance__life__lincoln_financial[*].expiry_date": "date",
            
            "insurance__life__john_hancock[*].type": "select",
            "insurance__life__john_hancock[*].name": "select",
            "insurance__life__john_hancock[*].id": "string",
            "insurance__life__john_hancock[*].notes": "string",
            "insurance__life__john_hancock[*].attachment": "file",
            "insurance__life__john_hancock[*].expiry_date": "date",
            
            "insurance__life__pacific_life[*].type": "select",
            "insurance__life__pacific_life[*].name": "select", 
            "insurance__life__pacific_life[*].id": "string",
            "insurance__life__pacific_life[*].notes": "string",
            "insurance__life__pacific_life[*].attachment": "file",
            "insurance__life__pacific_life[*].expiry_date": "date",
            
            "insurance__life__corebridge_financial[*].type": "select",
            "insurance__life__corebridge_financial[*].name": "select",
            "insurance__life__corebridge_financial[*].id": "string",
            "insurance__life__corebridge_financial[*].notes": "string",
            "insurance__life__corebridge_financial[*].attachment": "file",
            "insurance__life__corebridge_financial[*].expiry_date": "date",
            
            "insurance__life__midland_national[*].type": "select",
            "insurance__life__midland_national[*].name": "select",
            "insurance__life__midland_national[*].id": "string",
            "insurance__life__midland_national[*].notes": "string",
            "insurance__life__midland_national[*].attachment": "file",
            "insurance__life__midland_national[*].expiry_date": "date",
            
            "insurance__life__nationwide[*].type": "select",
            "insurance__life__nationwide[*].name": "select",
            "insurance__life__nationwide[*].id": "string",
            "insurance__life__nationwide[*].notes": "string",
            "insurance__life__nationwide[*].attachment": "file",
            "insurance__life__nationwide[*].expiry_date": "date",
            
            "insurance__life__pennmutual[*].type": "select",
            "insurance__life__pennmutual[*].name": "select",
            "insurance__life__pennmutual[*].id": "string",
            "insurance__life__pennmutual[*].notes": "string",
            "insurance__life__pennmutual[*].attachment": "file",
            "insurance__life__pennmutual[*].expiry_date": "date",
            
            "insurance__life__equitable[*].type": "select",
            "insurance__life__equitable[*].name": "select",
            "insurance__life__equitable[*].id": "string",
            "insurance__life__equitable[*].notes": "string",
            "insurance__life__equitable[*].attachment": "file",
            "insurance__life__equitable[*].expiry_date": "date",
            
            "insurance__life__national_life[*].type": "select",
            "insurance__life__national_life[*].name": "select",
            "insurance__life__national_life[*].id": "string",
            "insurance__life__national_life[*].notes": "string",
            "insurance__life__national_life[*].attachment": "file",
            "insurance__life__national_life[*].expiry_date": "date",
            
            "insurance__life__manulife[*].type": "select",
            "insurance__life__manulife[*].name": "select",
            "insurance__life__manulife[*].id": "string",
            "insurance__life__manulife[*].notes": "string",
            "insurance__life__manulife[*].attachment": "file",
            "insurance__life__manulife[*].expiry_date": "date",
            
            "insurance__life__industrial_alliance[*].type": "select",
            "insurance__life__industrial_alliance[*].name": "select",
            "insurance__life__industrial_alliance[*].id": "string",
            "insurance__life__industrial_alliance[*].notes": "string",
            "insurance__life__industrial_alliance[*].attachment": "file",
            "insurance__life__industrial_alliance[*].expiry_date": "date",
            
            "insurance__life__bmo[*].type": "select",
            "insurance__life__bmo[*].name": "select",
            "insurance__life__bmo[*].id": "string", 
            "insurance__life__bmo[*].notes": "string",
            "insurance__life__bmo[*].attachment": "file",
            "insurance__life__bmo[*].expiry_date": "date",
            
            "insurance__life__ivari[*].type": "select",
            "insurance__life__ivari[*].name": "select",
            "insurance__life__ivari[*].id": "string",
            "insurance__life__ivari[*].notes": "string",
            "insurance__life__ivari[*].attachment": "file",
            "insurance__life__ivari[*].expiry_date": "date",
            
            # All account specific fields  
            "account__computer_login[*].type": "select",
            "account__computer_login[*].name": "string",
            "account__computer_login[*].notes": "string",
            "account__computer_login[*].id": "string",
            "account__computer_login[*].email": "email",
            
            "account__crypto_wallet[*].type": "select",
            "account__crypto_wallet[*].name": "string",
            "account__crypto_wallet[*].notes": "string",
            "account__crypto_wallet[*].id": "string",
            "account__crypto_wallet[*].email": "email",
            
            "account__digital_account__paypal[*].type": "select",
            "account__digital_account__paypal[*].name": "string",
            "account__digital_account__paypal[*].notes": "string",
            "account__digital_account__paypal[*].id": "string",
            "account__digital_account__paypal[*].email": "email",
            
            "account__digital_account__google[*].type": "select",
            "account__digital_account__google[*].name": "string",
            "account__digital_account__google[*].notes": "string",
            "account__digital_account__google[*].id": "string",
            "account__digital_account__google[*].email": "email",
            
            "account__digital_account__facebook[*].type": "select",
            "account__digital_account__facebook[*].name": "string",
            "account__digital_account__facebook[*].notes": "string",
            "account__digital_account__facebook[*].id": "string",
            "account__digital_account__facebook[*].email": "email",
            
            "account__digital_account__instagram[*].type": "select",
            "account__digital_account__instagram[*].name": "string",
            "account__digital_account__instagram[*].notes": "string",
            "account__digital_account__instagram[*].id": "string",
            "account__digital_account__instagram[*].email": "email",
            
            "account__digital_account__linkedin[*].type": "select",
            "account__digital_account__linkedin[*].name": "string",
            "account__digital_account__linkedin[*].notes": "string",
            "account__digital_account__linkedin[*].id": "string",
            "account__digital_account__linkedin[*].email": "email",
            
            "account__digital_account__pinterest[*].type": "select",
            "account__digital_account__pinterest[*].name": "string",
            "account__digital_account__pinterest[*].notes": "string",
            "account__digital_account__pinterest[*].id": "string",
            "account__digital_account__pinterest[*].email": "email",
            
            "account__digital_account__twitter[*].type": "select",
            "account__digital_account__twitter[*].name": "string",
            "account__digital_account__twitter[*].notes": "string",
            "account__digital_account__twitter[*].id": "string",
            "account__digital_account__twitter[*].email": "email",
            
            "account__digital_account__flickr[*].type": "select",
            "account__digital_account__flickr[*].name": "string",
            "account__digital_account__flickr[*].notes": "string",
            "account__digital_account__flickr[*].id": "string",
            "account__digital_account__flickr[*].email": "email",
            
            # All document specific fields
            "key_document__marriage_contract[*].type": "select",
            "key_document__marriage_contract[*].name": "string",
            "key_document__marriage_contract[*].location_hint": "string",
            "key_document__marriage_contract[*].date_created": "date",
            "key_document__marriage_contract[*].last_updated": "date",
            "key_document__marriage_contract[*].notes": "string",
            "key_document__marriage_contract[*].id": "string",
            "key_document__marriage_contract[*].attachment": "file",
            
            "key_document__military[*].type": "select",
            "key_document__military[*].name": "string",
            "key_document__military[*].location_hint": "string",
            "key_document__military[*].date_created": "date",
            "key_document__military[*].last_updated": "date",
            "key_document__military[*].notes": "string",
            "key_document__military[*].id": "string",
            "key_document__military[*].attachment": "file",
            
            "key_document__tax_documents[*].type": "select",
            "key_document__tax_documents[*].name": "string",
            "key_document__tax_documents[*].location_hint": "string",
            "key_document__tax_documents[*].date_created": "date",
            "key_document__tax_documents[*].last_updated": "date",
            "key_document__tax_documents[*].notes": "string",
            "key_document__tax_documents[*].id": "string",
            "key_document__tax_documents[*].attachment": "file",
            
            "key_document__trust[*].type": "select",
            "key_document__trust[*].name": "string",
            "key_document__trust[*].location_hint": "string",
            "key_document__trust[*].date_created": "date",
            "key_document__trust[*].last_updated": "date", 
            "key_document__trust[*].notes": "string",
            "key_document__trust[*].id": "string",
            "key_document__trust[*].attachment": "file",
            
            # All ID document specific fields
            "id_document__accessible_parking_permit[*].type": "select",
            "id_document__accessible_parking_permit[*].name": "string",
            "id_document__accessible_parking_permit[*].id": "string",
            "id_document__accessible_parking_permit[*].notes": "string",
            "id_document__accessible_parking_permit[*].attachment": "file",
            "id_document__accessible_parking_permit[*].expiry_date": "date",
            
            "id_document__drivers_license[*].type": "select",
            "id_document__drivers_license[*].name": "string",
            "id_document__drivers_license[*].id": "string",
            "id_document__drivers_license[*].notes": "string",
            "id_document__drivers_license[*].attachment": "file", 
            "id_document__drivers_license[*].expiry_date": "date",
            
            "id_document__firearm_license[*].type": "select",
            "id_document__firearm_license[*].name": "string",
            "id_document__firearm_license[*].id": "string",
            "id_document__firearm_license[*].notes": "string",
            "id_document__firearm_license[*].attachment": "file",
            "id_document__firearm_license[*].expiry_date": "date",
            
            "id_document__health_card[*].type": "select",
            "id_document__health_card[*].name": "string",
            "id_document__health_card[*].id": "string",
            "id_document__health_card[*].notes": "string",
            "id_document__health_card[*].attachment": "file",
            "id_document__health_card[*].expiry_date": "date",
            
            "id_document__nexus[*].type": "select",
            "id_document__nexus[*].name": "string",
            "id_document__nexus[*].id": "string",
            "id_document__nexus[*].notes": "string",
            "id_document__nexus[*].attachment": "file",
            "id_document__nexus[*].expiry_date": "date",
            
            "id_document__passport[*].type": "select",
            "id_document__passport[*].name": "string",
            "id_document__passport[*].id": "string",
            "id_document__passport[*].notes": "string",
            "id_document__passport[*].attachment": "file",
            "id_document__passport[*].expiry_date": "date",
            
            # All utility specific fields
            "utility__electricity[*].type": "select",
            "utility__electricity[*].name": "string",
            "utility__electricity[*].id": "string",
            "utility__electricity[*].notes": "string",
            "utility__electricity[*].attachment": "file",
            "utility__electricity[*].expiry_date": "date",
            
            "utility__property_taxes[*].type": "select",
            "utility__property_taxes[*].name": "string",
            "utility__property_taxes[*].id": "string",
            "utility__property_taxes[*].notes": "string",
            "utility__property_taxes[*].attachment": "file",
            "utility__property_taxes[*].expiry_date": "date",
            
            "utility__gas_hydro[*].type": "select",
            "utility__gas_hydro[*].name": "string",
            "utility__gas_hydro[*].id": "string",
            "utility__gas_hydro[*].notes": "string",
            "utility__gas_hydro[*].attachment": "file",
            "utility__gas_hydro[*].expiry_date": "date",
            
            "utility__water[*].type": "select",
            "utility__water[*].name": "string",
            "utility__water[*].id": "string",
            "utility__water[*].notes": "string",
            "utility__water[*].attachment": "file",
            "utility__water[*].expiry_date": "date",
            
            "utility__internet[*].type": "select",
            "utility__internet[*].name": "string",
            "utility__internet[*].id": "string",
            "utility__internet[*].notes": "string",
            "utility__internet[*].attachment": "file",
            "utility__internet[*].expiry_date": "date",
            
            "utility__phone[*].type": "select",
            "utility__phone[*].name": "string",
            "utility__phone[*].id": "string",
            "utility__phone[*].notes": "string",
            "utility__phone[*].attachment": "file",
            "utility__phone[*].expiry_date": "date",
            
            # All property specific fields
            "property__computer[*].type": "select",
            "property__computer[*].name": "string",
            "property__computer[*].notes": "string",
            "property__computer[*].id": "string",
            "property__computer[*].attachment": "file",
            
            "property__firearm[*].type": "select",
            "property__firearm[*].name": "string",
            "property__firearm[*].notes": "string",
            "property__firearm[*].id": "string",
            "property__firearm[*].attachment": "file",
            
            "property__real_estate[*].type": "select",
            "property__real_estate[*].name": "string",
            "property__real_estate[*].notes": "string",
            "property__real_estate[*].id": "string",
            "property__real_estate[*].attachment": "file",
            
            "property__vehicle[*].type": "select",
            "property__vehicle[*].name": "string",
            "property__vehicle[*].notes": "string",
            "property__vehicle[*].id": "string",
            "property__vehicle[*].attachment": "file",
            
            # All financial specific fields
            "financial_information__bank_financial_services_provider[*].type": "select",
            "financial_information__bank_financial_services_provider[*].name": "string",
            "financial_information__bank_financial_services_provider[*].id": "string",
            "financial_information__bank_financial_services_provider[*].notes": "string",
            "financial_information__bank_financial_services_provider[*].attachment": "file",
            "financial_information__bank_financial_services_provider[*].expiry_date": "date",
            
            "financial_information__credit_card[*].type": "select",
            "financial_information__credit_card[*].name": "string",
            "financial_information__credit_card[*].id": "string",
            "financial_information__credit_card[*].notes": "string",
            "financial_information__credit_card[*].attachment": "file",
            "financial_information__credit_card[*].expiry_date": "date",
            
            "financial_information__investment_provider[*].type": "select",
            "financial_information__investment_provider[*].name": "string",
            "financial_information__investment_provider[*].id": "string",
            "financial_information__investment_provider[*].notes": "string",
            "financial_information__investment_provider[*].attachment": "file",
            "financial_information__investment_provider[*].expiry_date": "date",
            
            "financial_information__lease[*].type": "select",
            "financial_information__lease[*].name": "string", 
            "financial_information__lease[*].id": "string",
            "financial_information__lease[*].notes": "string",
            "financial_information__lease[*].attachment": "file",
            "financial_information__lease[*].expiry_date": "date",
            
            "financial_information__loan[*].type": "select",
            "financial_information__loan[*].name": "string",
            "financial_information__loan[*].id": "string",
            "financial_information__loan[*].notes": "string",
            "financial_information__loan[*].attachment": "file",
            "financial_information__loan[*].expiry_date": "date",
            
            "financial_information__pension[*].type": "select",
            "financial_information__pension[*].name": "string",
            "financial_information__pension[*].id": "string",
            "financial_information__pension[*].notes": "string",
            "financial_information__pension[*].attachment": "file",
            "financial_information__pension[*].expiry_date": "date",
            
            "financial_information__philanthropy_charity[*].type": "select",
            "financial_information__philanthropy_charity[*].name": "string",
            "financial_information__philanthropy_charity[*].id": "string",
            "financial_information__philanthropy_charity[*].notes": "string",
            "financial_information__philanthropy_charity[*].attachment": "file",
            "financial_information__philanthropy_charity[*].expiry_date": "date",

            # All business document specific fields
            "business_documents__letter_of_intent[*].type": "select",
            "business_documents__letter_of_intent[*].business_name": "string",
            "business_documents__letter_of_intent[*].name": "string",
            "business_documents__letter_of_intent[*].location_hint": "string",
            "business_documents__letter_of_intent[*].date_created": "date",
            "business_documents__letter_of_intent[*].last_updated": "date",
            "business_documents__letter_of_intent[*].notes": "string",
            "business_documents__letter_of_intent[*].attachment": "file",
            
            "business_documents__succession_plan[*].type": "select",
            "business_documents__succession_plan[*].business_name": "string",
            "business_documents__succession_plan[*].name": "string",
            "business_documents__succession_plan[*].location_hint": "string",
            "business_documents__succession_plan[*].date_created": "date",
            "business_documents__succession_plan[*].last_updated": "date",
            "business_documents__succession_plan[*].notes": "string",
            "business_documents__succession_plan[*].attachment": "file",
            
            "business_documents__asset[*].type": "select",
            "business_documents__asset[*].business_name": "string",
            "business_documents__asset[*].name": "string",
            "business_documents__asset[*].location_hint": "string",
            "business_documents__asset[*].date_created": "date",
            "business_documents__asset[*].last_updated": "date",
            "business_documents__asset[*].notes": "string",
            "business_documents__asset[*].attachment": "file",
            
            "business_documents__liability[*].type": "select",
            "business_documents__liability[*].business_name": "string",
            "business_documents__liability[*].name": "string",
            "business_documents__liability[*].location_hint": "string",
            "business_documents__liability[*].date_created": "date",
            "business_documents__liability[*].last_updated": "date",
            "business_documents__liability[*].notes": "string",
            "business_documents__liability[*].attachment": "file",
            
            "business_documents__digital_asset[*].type": "select",
            "business_documents__digital_asset[*].business_name": "string",
            "business_documents__digital_asset[*].name": "string",
            "business_documents__digital_asset[*].location_hint": "string",
            "business_documents__digital_asset[*].date_created": "date",
            "business_documents__digital_asset[*].last_updated": "date",
            "business_documents__digital_asset[*].notes": "string",
            "business_documents__digital_asset[*].attachment": "file",
            
            "business_documents__tax[*].type": "select",
            "business_documents__tax[*].business_name": "string",
            "business_documents__tax[*].name": "string",
            "business_documents__tax[*].location_hint": "string",
            "business_documents__tax[*].date_created": "date",
            "business_documents__tax[*].last_updated": "date",
            "business_documents__tax[*].notes": "string",
            "business_documents__tax[*].attachment": "file",
            
            "business_documents__property_title[*].type": "select",
            "business_documents__property_title[*].business_name": "string",
            "business_documents__property_title[*].name": "string",
            "business_documents__property_title[*].location_hint": "string",
            "business_documents__property_title[*].date_created": "date",
            "business_documents__property_title[*].last_updated": "date",
            "business_documents__property_title[*].notes": "string",
            "business_documents__property_title[*].attachment": "file",
            
            "business_documents__insurance_policy[*].type": "select",
            "business_documents__insurance_policy[*].business_name": "string",
            "business_documents__insurance_policy[*].name": "string",
            "business_documents__insurance_policy[*].location_hint": "string",
            "business_documents__insurance_policy[*].date_created": "date",
            "business_documents__insurance_policy[*].last_updated": "date",
            "business_documents__insurance_policy[*].notes": "string",
            "business_documents__insurance_policy[*].attachment": "file",
            
            # All farm document specific fields
            "farm_documents__operating_agreement[*].type": "select",
            "farm_documents__operating_agreement[*].farm_name": "string",
            "farm_documents__operating_agreement[*].name": "string",
            "farm_documents__operating_agreement[*].location_hint": "string",
            "farm_documents__operating_agreement[*].date_created": "date",
            "farm_documents__operating_agreement[*].last_updated": "date",
            "farm_documents__operating_agreement[*].notes": "string",
            "farm_documents__operating_agreement[*].attachment": "file",
            "farm_documents__operating_agreement[*].expiry_date": "date",
            
            "farm_documents__land_title[*].type": "select",
            "farm_documents__land_title[*].farm_name": "string",
            "farm_documents__land_title[*].name": "string",
            "farm_documents__land_title[*].location_hint": "string",
            "farm_documents__land_title[*].date_created": "date",
            "farm_documents__land_title[*].last_updated": "date",
            "farm_documents__land_title[*].notes": "string",
            "farm_documents__land_title[*].attachment": "file",
            "farm_documents__land_title[*].expiry_date": "date",
            
            "farm_documents__equipment_title[*].type": "select",
            "farm_documents__equipment_title[*].farm_name": "string",
            "farm_documents__equipment_title[*].name": "string",
            "farm_documents__equipment_title[*].location_hint": "string",
            "farm_documents__equipment_title[*].date_created": "date",
            "farm_documents__equipment_title[*].last_updated": "date",
            "farm_documents__equipment_title[*].notes": "string",
            "farm_documents__equipment_title[*].attachment": "file",
            "farm_documents__equipment_title[*].expiry_date": "date",
            
            "farm_documents__insurance_policy[*].type": "select",
            "farm_documents__insurance_policy[*].farm_name": "string",
            "farm_documents__insurance_policy[*].name": "string",
            "farm_documents__insurance_policy[*].location_hint": "string",
            "farm_documents__insurance_policy[*].date_created": "date",
            "farm_documents__insurance_policy[*].last_updated": "date",
            "farm_documents__insurance_policy[*].notes": "string",
            "farm_documents__insurance_policy[*].attachment": "file",
            "farm_documents__insurance_policy[*].expiry_date": "date",
            
            "farm_documents__lease[*].type": "select",
            "farm_documents__lease[*].farm_name": "string",
            "farm_documents__lease[*].name": "string",
            "farm_documents__lease[*].location_hint": "string",
            "farm_documents__lease[*].date_created": "date",
            "farm_documents__lease[*].last_updated": "date",
            "farm_documents__lease[*].notes": "string",
            "farm_documents__lease[*].attachment": "file",
            "farm_documents__lease[*].expiry_date": "date",
            
            "farm_documents__water_rights[*].type": "select",
            "farm_documents__water_rights[*].farm_name": "string",
            "farm_documents__water_rights[*].name": "string",
            "farm_documents__water_rights[*].location_hint": "string",
            "farm_documents__water_rights[*].date_created": "date",
            "farm_documents__water_rights[*].last_updated": "date",
            "farm_documents__water_rights[*].notes": "string",
            "farm_documents__water_rights[*].attachment": "file",
            "farm_documents__water_rights[*].expiry_date": "date",
            
            "farm_documents__conservation_program_contract[*].type": "select",
            "farm_documents__conservation_program_contract[*].farm_name": "string",
            "farm_documents__conservation_program_contract[*].name": "string",
            "farm_documents__conservation_program_contract[*].location_hint": "string",
            "farm_documents__conservation_program_contract[*].date_created": "date",
            "farm_documents__conservation_program_contract[*].last_updated": "date",
            "farm_documents__conservation_program_contract[*].notes": "string",
            "farm_documents__conservation_program_contract[*].attachment": "file",
            "farm_documents__conservation_program_contract[*].expiry_date": "date",
            
            "farm_documents__environmental_compliance[*].type": "select",
            "farm_documents__environmental_compliance[*].farm_name": "string",
            "farm_documents__environmental_compliance[*].name": "string",
            "farm_documents__environmental_compliance[*].location_hint": "string",
            "farm_documents__environmental_compliance[*].date_created": "date",
            "farm_documents__environmental_compliance[*].last_updated": "date",
            "farm_documents__environmental_compliance[*].notes": "string",
            "farm_documents__environmental_compliance[*].attachment": "file",
            "farm_documents__environmental_compliance[*].expiry_date": "date",
            
            "farm_documents__financial_statement[*].type": "select",
            "farm_documents__financial_statement[*].farm_name": "string",
            "farm_documents__financial_statement[*].name": "string",
            "farm_documents__financial_statement[*].location_hint": "string",
            "farm_documents__financial_statement[*].date_created": "date",
            "farm_documents__financial_statement[*].last_updated": "date",
            "farm_documents__financial_statement[*].notes": "string",
            "farm_documents__financial_statement[*].attachment": "file",
            "farm_documents__financial_statement[*].expiry_date": "date",
            
            "farm_documents__tax[*].type": "select",
            "farm_documents__tax[*].farm_name": "string",
            "farm_documents__tax[*].name": "string",
            "farm_documents__tax[*].location_hint": "string",
            "farm_documents__tax[*].date_created": "date",
            "farm_documents__tax[*].last_updated": "date",
            "farm_documents__tax[*].notes": "string",
            "farm_documents__tax[*].attachment": "file",
            "farm_documents__tax[*].expiry_date": "date",
            
            "farm_documents__agricultural_loan[*].type": "select",
            "farm_documents__agricultural_loan[*].farm_name": "string",
            "farm_documents__agricultural_loan[*].name": "string",
            "farm_documents__agricultural_loan[*].location_hint": "string",
            "farm_documents__agricultural_loan[*].date_created": "date",
            "farm_documents__agricultural_loan[*].last_updated": "date",
            "farm_documents__agricultural_loan[*].notes": "string",
            "farm_documents__agricultural_loan[*].attachment": "file",
            "farm_documents__agricultural_loan[*].expiry_date": "date",
            
            "farm_documents__transfer_on_death_deed[*].type": "select",
            "farm_documents__transfer_on_death_deed[*].farm_name": "string",
            "farm_documents__transfer_on_death_deed[*].name": "string",
            "farm_documents__transfer_on_death_deed[*].location_hint": "string",
            "farm_documents__transfer_on_death_deed[*].date_created": "date",
            "farm_documents__transfer_on_death_deed[*].last_updated": "date",
            "farm_documents__transfer_on_death_deed[*].notes": "string",
            "farm_documents__transfer_on_death_deed[*].attachment": "file",
            "farm_documents__transfer_on_death_deed[*].expiry_date": "date",
            
            "farm_documents__trust[*].type": "select",
            "farm_documents__trust[*].farm_name": "string",
            "farm_documents__trust[*].name": "string",
            "farm_documents__trust[*].location_hint": "string",
            "farm_documents__trust[*].date_created": "date",
            "farm_documents__trust[*].last_updated": "date",
            "farm_documents__trust[*].notes": "string",
            "farm_documents__trust[*].attachment": "file",
            "farm_documents__trust[*].expiry_date": "date",
            
            "farm_documents__estate_plan_integration[*].type": "select",
            "farm_documents__estate_plan_integration[*].farm_name": "string",
            "farm_documents__estate_plan_integration[*].name": "string",
            "farm_documents__estate_plan_integration[*].location_hint": "string",
            "farm_documents__estate_plan_integration[*].date_created": "date",
            "farm_documents__estate_plan_integration[*].last_updated": "date",
            "farm_documents__estate_plan_integration[*].notes": "string",
            "farm_documents__estate_plan_integration[*].attachment": "file",
            "farm_documents__estate_plan_integration[*].expiry_date": "date",

            
        }
    def _load_schema_value_options(self) -> Dict[str, List[str]]:
        """Load predefined value options from schema - COMPLETE WITH ALL MISSING OPTIONS"""
        return {
            # ===== EXISTING VALUE OPTIONS =====
            "deceased.phone[*].type": ["home", "mobile", "work", "fax"],
            "deceased.email[*].type": ["personal", "work", "other"],
            "deceased.employment.status[*]": ["unemployed", "social_services", "employment_insurance", "employed", "self_employed", "business_owner", "active_military", "retired", "volunteer", "veteran"],
            "deceased.marital_status": ["married", "common_law", "none", "single", "widowed", "divorced", "separated"],
            "deceased.gender": ["male", "female", "non_binary", "decline_answer"],
            "deceased.citizenship_status": ["canadian_citizen", "canadian_permanent_or_legal_resident", "canadian_temporary_resident_or_foreign_worker", "canadian_landed_immigrant_or_refugee", "us_citizen", "us_conditional_or_permanent_resident", "us_non_immigrant_or_temporary_resident", "us_undocumented_immigrant"],
            "deceased.voter_registration": ["yes", "no", "not_sure"],
            "deceased.pension_plans[*]": ["alberta_public_service_pp", "healthcare_ontario_pp", "ontario_municipal_employee_retirement_system", "college_applied_arts_tech_pp", "local_authorities_pp", "public_employees_pp", "saskatchewan_teachers_pp", "other", "not_sure", "none"],
            "estate_reps[*].primary_relationship_to_deceased": ["administrator-of-the-estate", "executor-of-the-estate", "power_of_attorney", "attorney_lawyer", "accountant", "life_insurance_agent", "general_insurance_broker", "financial_planner_investment_broker", "mortgage_broker", "real_estate_agent", "doctor", "religion_spiritual_affiliation", "preferred_funeral_home", "service_providers"],
            "estate_reps[*].secondary_relationship_to_deceased": ["spouse", "child", "grandchild", "parent", "sibling", "niece", "nephew", "grandmother", "grandfather", "aunt", "uncle", "cousin", "friend", "neighbor", "acquaintance", "none", "brother", "sister", "grandson", "granddaughter"],
            "insurance[*].type": ["critical_illness_insurance", "disability_insurance", "health_medical_insurance", "home_property_insurance", "vehicle_insurance", "life_insurance"],
            "insurance[*].name": ["manulife", "industrial_alliance", "bmo", "ivari", "greatwest_lifeco", "desjardins", "sunlife", "fairfax", "ia_financial_group", "canada_life", "rbc"],
            "financial_information[*].type": ["bank_financial_services_provider", "pension", "investment_provider", "loan", "lease", "credit_card", "philanthropy_charity"],
            "utility[*].type": ["property_taxes", "gas_hydro", "electricity", "water", "internet", "phone"],
            "property[*].type": ["vehicle", "real_estate", "firearm", "computer"],
            "property.real_estate[*].property_type": ["house", "condo", "townhouse", "apartment", "land", "commercial", "farm"],
            "property.vehicles[*].type": ["car", "truck", "motorcycle", "boat", "rv", "atv"],
            "account[*].type": ["computer_login", "digital_account", "subscription", "loyalty_rewards_program", "membership", "crypto_wallet"],
            "account[*].name": ["amazon", "apple", "google", "facebook", "instagram", "linkedin", "paypal", "netflix", "spotify", "airmiles", "aeroplan", "pc_optimum"],
            "task_planner.b_will": ["yes", "no", "not_sure"],
            "task_planner.b_has_spouse": ["yes", "no", "not_sure"],
            "task_planner.b_has_children": ["yes", "no", "not_sure"],
            "task_planner.b_age_ca": ["less_than_18", "18_25", "26_55", "55_59", "60_64", "65_69", ">=70", "not_sure"],
            "task_planner.b_last_province_ca": ["AB", "BC", "MB", "NB", "NL", "NT", "NS", "NU", "ON", "PE", "QC", "SK", "YT", "outside_of_canada"],
            "task_planner.b_citizenship_ca": ["canadian", "permanent_or_legal", "temporary_or_foreign_worker", "landed_immigrant_or_refugee", "not_sure"],
            "will.attachment": ["pdf", "doc", "image", "scan"],
            "key_document[*].type": ["birth_certificate", "death_certificate", "marriage_certificate", "divorce_decree", "will", "power_of_attorney", "passport", "drivers_license"],
            "id_document[*].type": ["passport", "drivers_license", "health_card", "sin_card", "citizenship_certificate"],

        
            # Account types
            "account__digital_account__google[*].type": ["digital_account"],
            "account__digital_account__paypal[*].type": ["digital_account"],
            "account__digital_account__facebook[*].type": ["digital_account"],
            "account__digital_account__instagram[*].type": ["digital_account"],
            "account__digital_account__linkedin[*].type": ["digital_account"],
            "account__digital_account__pinterest[*].type": ["digital_account"],
            "account__digital_account__twitter[*].type": ["digital_account"],
            "account__digital_account__flickr[*].type": ["digital_account"],
            "account__computer_login[*].type": ["computer_login"],
            "account__crypto_wallet[*].type": ["crypto_wallet"],
            
            # Insurance types
            "insurance__life__manulife[*].type": ["life_insurance"],
            "insurance__life__bmo[*].type": ["life_insurance"],
            "insurance__life__industrial_alliance[*].type": ["life_insurance"],
            "insurance__life__northwestern_mutual[*].type": ["life_insurance"],
            "insurance__life__massmutual[*].type": ["life_insurance"],
            "insurance__life__new_york_life[*].type": ["life_insurance"],
            "insurance__life__prudential[*].type": ["life_insurance"],
            "insurance__life__lincoln_financial[*].type": ["life_insurance"],
            "insurance__life__john_hancock[*].type": ["life_insurance"],
            "insurance__life__pacific_life[*].type": ["life_insurance"],
            "insurance__life__corebridge_financial[*].type": ["life_insurance"],
            "insurance__life__midland_national[*].type": ["life_insurance"],
            "insurance__life__nationwide[*].type": ["life_insurance"],
            "insurance__life__pennmutual[*].type": ["life_insurance"],
            "insurance__life__equitable[*].type": ["life_insurance"],
            "insurance__life__national_life[*].type": ["life_insurance"],
            "insurance__life__ivari[*].type": ["life_insurance"],
            
            # Utility types
            "utility__electricity[*].type": ["electricity"],
            "utility__water[*].type": ["water"],
            "utility__gas_hydro[*].type": ["gas_hydro"],
            "utility__internet[*].type": ["internet"],
            "utility__phone[*].type": ["phone"],
            "utility__property_taxes[*].type": ["property_taxes"],
            
            # Property types
            "property__computer[*].type": ["computer"],
            "property__firearm[*].type": ["firearm"],
            "property__real_estate[*].type": ["real_estate"],
            "property__vehicle[*].type": ["vehicle"],
            "property.vehicles[*].vin": "string",
            "property.vehicles[0].make": "string",
            "property.vehicles[0].model": "string",
            "property.vehicles[0].title_number": "string",
            "property.vehicles[*].license_plate": "string",
            
           
            # ID document types
            "id_document__passport[*].type": ["passport"],
            "id_document__drivers_license[*].type": ["drivers_license"],
            "id_document__health_card[*].type": ["health_card"],
            "id_document__nexus[*].type": ["nexus"],
            "id_document__firearm_license[*].type": ["firearm_license"],
            "id_document__accessible_parking_permit[*].type": ["accessible_parking_permit"],
            
            # Estate representative roles
            "estate_reps[*].role": ["executor", "trustee", "power_of_attorney", "guardian", "administrator"],
            
            # Bank account types
            "financial_information.bank_accounts[*].account_type": ["checking", "savings", "money_market", "cd", "investment"],
            
            # Property types
            "property.real_estate[*].property_type": ["primary_residence", "vacation_home", "rental_property", "commercial", "land"],
            
            # Vehicle insurance coverage types
            "insurance__vehicle[*].coverage_type": ["liability", "comprehensive", "collision", "full_coverage"],

            # Financial types
            "financial_information__bank_financial_services_provider[*].type": ["bank_financial_services_provider"],
            "financial_information__credit_card[*].type": ["credit_card"],
            "financial_information__investment_provider[*].type": ["investment_provider"],
            "financial_information__lease[*].type": ["lease"],
            "financial_information__loan[*].type": ["loan"],
            "financial_information__pension[*].type": ["pension"],
            "financial_information__philanthropy_charity[*].type": ["philanthropy_charity"],

            # Key document types
            "key_document__marriage_contract[*].type": ["marriage_contract"],
            "key_document__military[*].type": ["military"],
            "key_document__tax_documents[*].type": ["tax_documents"],
            "key_document__trust[*].type": ["trust"],
            "key_document.notes": "string",
            "key_document.notary_date": "date",
            "key_document.notary_month_year_text": "string",
            "key_document.notary_signature": "signature",
            "key_document.notary_commission_expiry": "date",
            "key_document[*].last_updated": "date",


            # Business document types
            "business_documents__letter_of_intent[*].type": ["letter_of_intent"],
            "business_documents__succession_plan[*].type": ["succession_plan"],
            "business_documents__asset[*].type": ["asset"],
            "business_documents__liability[*].type": ["liability"],
            "business_documents__digital_asset[*].type": ["digital_asset"],
            "business_documents__tax[*].type": ["tax"],
            "business_documents__property_title[*].type": ["property_title"],
            "business_documents__insurance_policy[*].type": ["insurance_policy"],

            # Farm document types
            "farm_documents__operating_agreement[*].type": ["operating_agreement"],
            "farm_documents__land_title[*].type": ["land_title"],
            "farm_documents__equipment_title[*].type": ["equipment_title"],
            "farm_documents__insurance_policy[*].type": ["insurance_policy"],
            "farm_documents__lease[*].type": ["lease"],
            "farm_documents__water_rights[*].type": ["water_rights"],
            "farm_documents__conservation_program_contract[*].type": ["conservation_program_contract"],
            "farm_documents__environmental_compliance[*].type": ["environmental_compliance"],
            "farm_documents__financial_statement[*].type": ["financial_statement"],
            "farm_documents__tax[*].type": ["tax"],
            "farm_documents__agricultural_loan[*].type": ["agricultural_loan"],
            "farm_documents__transfer_on_death_deed[*].type": ["transfer_on_death_deed"],
            "farm_documents__trust[*].type": ["trust"],
            "farm_documents__estate_plan_integration[*].type": ["estate_plan_integration"],
        }


    def _build_schema_fields(self) -> Dict[str, SchemaField]:
        """Build comprehensive schema field objects"""
        schema_fields = {}
        
        for path in self.schema_paths:
            field_type = self.field_types.get(path, self._infer_field_type(path))
            value_options = self.value_options.get(path, [])
            
            schema_field = SchemaField(
                path=path,
                field_type=field_type,
                description=self._generate_field_description(path),
                value_options=value_options,
                is_array="[*]" in path,
                is_required=self._is_required_field(path)
            )
            
            schema_fields[path] = schema_field
        
        return schema_fields
    
    def _infer_field_type(self, path: str) -> str:
        """Infer field type from path pattern"""
        path_lower = path.lower()
        
        if any(x in path_lower for x in ["name", "first_name", "middle_name", "last_name", "maiden_name"]):
            return "name"
        elif any(x in path_lower for x in ["phone", "telephone", "mobile"]):
            return "phone"
        elif "email" in path_lower:
            return "email"
        elif any(x in path_lower for x in ["address", "location", "place"]):
            return "location"
        elif any(x in path_lower for x in ["date", "birth", "death", "created", "updated"]):
            return "date"
        elif any(x in path_lower for x in ["attachment", "document", "file", "proof"]):
            return "file"
        elif "sin" in path_lower or "social_insurance" in path_lower:
            return "sin"
        elif any(x in path_lower for x in ["value", "amount", "balance", "premium", "cost"]):
            return "currency"
        elif "task_planner.b_" in path_lower:
            return "boolean"
        elif any(x in path_lower for x in ["account_number", "policy_number", "id", "number"]):
            return "string"
        else:
            return "string"
    
    def _generate_field_description(self, path: str) -> str:
        """Generate human-readable description for field"""
        parts = path.split('.')
        field_name = parts[-1].replace('_', ' ')
        
        if path.startswith("deceased."):
            if "first_name" in path:
                return "Deceased person's first name"
            elif "middle_name" in path:
                return "Deceased person's middle name"
            elif "last_name" in path:
                return "Deceased person's last name"
            else:
                return f"Deceased person's {field_name}"
        elif path.startswith("applicant."):
            if "first_name" in path:
                return "Applicant's first name"
            elif "middle_name" in path:
                return "Applicant's middle name"
            elif "last_name" in path:
                return "Applicant's last name"
            else:
                return f"Applicant's {field_name}"
        elif path.startswith("spouse."):
            if "first_name" in path:
                return "Spouse's first name"
            elif "middle_name" in path:
                return "Spouse's middle name"
            elif "last_name" in path:
                return "Spouse's last name"
            else:
                return f"Spouse's {field_name}"
        elif path.startswith("estate_reps"):
            if "first_name" in path:
                return "Estate representative's first name"
            elif "middle_name" in path:
                return "Estate representative's middle name"
            elif "last_name" in path:
                return "Estate representative's last name"
            else:
                return f"Estate representative's {field_name}"
        elif path.startswith("children"):
            if "first_name" in path:
                return "Child's first name"
            elif "middle_name" in path:
                return "Child's middle name"
            elif "last_name" in path:
                return "Child's last name"
            else:
                return f"Child's {field_name}"
        elif path.startswith("contact"):
            if "first_name" in path:
                return "Contact's first name"
            elif "middle_name" in path:
                return "Contact's middle name"
            elif "last_name" in path:
                return "Contact's last name"
            else:
                return f"Contact's {field_name}"
        elif path.startswith("task_planner.b_"):
            return f"Task planner: {parts[-1].replace('b_', '').replace('_', ' ')}"
        elif path.startswith("final_wishes"):
            return f"Final wishes: {field_name}"
        elif path.startswith("insurance"):
            return f"Insurance: {field_name}"
        elif path.startswith("financial"):
            return f"Financial: {field_name}"
        elif path.startswith("property"):
            return f"Property: {field_name}"
        elif path.startswith("account"):
            return f"Account: {field_name}"
        elif path.startswith("utility"):
            return f"Utility: {field_name}"
        elif path.startswith("key_document"):
            return f"Key document: {field_name}"
        elif path.startswith("id_document"):
            return f"ID document: {field_name}"
        elif path.startswith("business_documents"):
            return f"Business document: {field_name}"
        elif path.startswith("farm_documents"):
            return f"Farm document: {field_name}"
        else:
            return field_name.title()
    
    def _is_required_field(self, path: str) -> bool:
        """Determine if field is required"""
        required_fields = {
            "deceased.name", "deceased.date_of_death", "deceased.social_insurance_number",
            "applicant.name", "applicant.phone", "applicant.address",
            "date.today"
        }
        
        return path in required_fields
    
    def get_schema_paths(self) -> List[str]:
        """Get all schema paths"""
        return self.schema_paths.copy()
    
    def get_field_type(self, path: str) -> str:
        """Get field type for a specific path"""
        return self.field_types.get(path, "string")
    
    def get_value_options(self, path: str) -> List[str]:
        """Get value options for a specific path"""
        return self.value_options.get(path, [])
    
    def get_schema_field(self, path: str) -> Optional[SchemaField]:
        """Get schema field object for a specific path"""
        return self.schema_fields.get(path)
    
    def search_paths(self, query: str) -> List[str]:
        """Search schema paths by query string"""
        query_lower = query.lower()
        matching_paths = []
        
        for path in self.schema_paths:
            if query_lower in path.lower():
                matching_paths.append(path)
        
        return matching_paths
    
    def get_paths_by_type(self, field_type: str) -> List[str]:
        """Get all paths of a specific field type"""
        matching_paths = []
        
        for path, ftype in self.field_types.items():
            if ftype == field_type:
                matching_paths.append(path)
        
        return matching_paths
    
    def get_entity_paths(self, entity: str) -> List[str]:
        """Get all paths for a specific entity (deceased, applicant, etc.)"""
        matching_paths = []
        
        for path in self.schema_paths:
            if path.startswith(f"{entity}."):
                matching_paths.append(path)
        
        return matching_paths
    
    def validate_path(self, path: str) -> bool:
        """Validate if a path exists in the schema"""
        return path in self.schema_paths
    
    def get_missing_paths_by_category(self) -> Dict[str, List[str]]:
        """Group missing paths by category - NOW INCLUDES ALL MISSING PATHS"""
        categories = {
            "core_personal_info": [],
            "extended_financial": [],
            "extended_property": [],
            "payment_preneed": [],
            "extended_insurance": [],
            "specialized_insurance": [],
            "specialized_accounts": [],
            "specialized_documents": [],
            "specialized_utilities": [],
            "specialized_properties": [],
            "specialized_financial": [],
            "business_documents": [],
            "farm_documents": []
        }

        # Get all the previously missing paths that are now included
        missing_paths = [path for path in self.schema_paths if any(x in path for x in [
            "insurance__life__", "account__", "key_document__", "id_document__", 
            "utility__", "property__", "financial_information__", 
            "business_documents__", "farm_documents__"
        ])]
        
        for path in missing_paths:
            if "insurance__life__" in path:
                categories["specialized_insurance"].append(path)
            elif "account__" in path:
                categories["specialized_accounts"].append(path)
            elif "key_document__" in path or "id_document__" in path:
                categories["specialized_documents"].append(path)
            elif "utility__" in path:
                categories["specialized_utilities"].append(path)
            elif "property__" in path:
                categories["specialized_properties"].append(path)
            elif "financial_information__" in path:
                categories["specialized_financial"].append(path)
            elif "business_documents__" in path:
                categories["business_documents"].append(path)
            elif "farm_documents__" in path:
                categories["farm_documents"].append(path)
        
        return categories
    
    def get_statistics(self) -> Dict:
        """Get schema statistics - COMPLETE WITH ALL PATHS"""
        print(f"🔍 Calculating statistics for {len(self.schema_paths)} paths...")
        
        entities = set(p.split('.')[0] for p in self.schema_paths if '.' in p)
        array_fields = [p for p in self.schema_paths if "[*]" in p]
        required_fields = [p for p in self.schema_paths if self._is_required_field(p)]
        task_planner_fields = [p for p in self.schema_paths if p.startswith("task_planner")]
        insurance_fields = [p for p in self.schema_paths if "insurance" in p]
        specialized_fields = [p for p in self.schema_paths if "__" in p]
        
        stats = {
            "total_paths": len(self.schema_paths),
            "field_types": len(set(self.field_types.values())),
            "value_options": len(self.value_options),
            "array_fields": len(array_fields),
            "required_fields": len(required_fields),
            "entities": len(entities),
            "task_planner_fields": len(task_planner_fields),
            "insurance_fields": len(insurance_fields),
            "specialized_fields": len(specialized_fields),
            "entity_list": sorted(list(entities)),
            "field_type_counts": {},
            "category_counts": {}
        }
        
        # Count by field type
        for ftype in set(self.field_types.values()):
            count = len(self.get_paths_by_type(ftype))
            stats["field_type_counts"][ftype] = count
        
        # Count by category
        categories = self.get_missing_paths_by_category()
        stats["category_counts"] = {k: len(v) for k, v in categories.items()}
        
        print(f"✅ Statistics: {stats['total_paths']} total paths, {stats['entities']} entities, {stats['specialized_fields']} specialized fields")
        return stats

    def get_core_fields_summary(self) -> Dict:
        """Get summary of core fields"""
        core_fields = {
            "personal_names": [path for path in self.schema_paths if any(name in path for name in ["first_name", "middle_name", "last_name"])],
            "addresses_emails": [path for path in self.schema_paths if any(field in path for field in ["email", "address"])],
            "financial_details": [path for path in self.schema_paths if any(field in path for field in ["account_number", "balance", "value", "premium"])],
            "insurance_details": [path for path in self.schema_paths if any(field in path for field in ["policy_number", "coverage", "beneficiary"])],
            "property_details": [path for path in self.schema_paths if any(field in path for field in ["make_model", "vin", "deed_location"])]
        }
        
        return {category: len(fields) for category, fields in core_fields.items()}

# Helper functions for accessing missing paths information
def get_missing_paths() -> List[str]:
    """Get all previously missing schema paths that are now included"""
    cadence_schema = CadenceSchema()
    return [path for path in cadence_schema.schema_paths if any(x in path for x in [
        "insurance__life__", "account__", "key_document__", "id_document__", 
        "utility__", "property__", "financial_information__", 
        "business_documents__", "farm_documents__"
    ])]

def get_missing_field_type(path: str) -> str:
    """Get field type for previously missing path"""
    cadence_schema = CadenceSchema()
    return cadence_schema.get_field_type(path)

def get_missing_value_options(path: str) -> List[str]:
    """Get value options for previously missing path"""
    cadence_schema = CadenceSchema()
    return cadence_schema.get_value_options(path)

def get_missing_paths_by_category() -> Dict[str, List[str]]:
    """Group previously missing paths by category"""
    cadence_schema = CadenceSchema()
    return cadence_schema.get_missing_paths_by_category()

def get_statistics() -> Dict:
    """Get complete schema statistics"""
    cadence_schema = CadenceSchema()
    return cadence_schema.get_statistics()

def get_core_fields_summary() -> Dict:
    """Get summary of core fields"""
    cadence_schema = CadenceSchema()
    return cadence_schema.get_core_fields_summary()

# Global schema instance
cadence_schema = CadenceSchema()

if __name__ == "__main__":
    stats = get_statistics()
    core_summary = get_core_fields_summary()
    
    print(f"Complete Schema Statistics:")
    print(f"Total paths: {stats['total_paths']}")
    print(f"Entities: {stats['entities']}")
    print(f"Categories: {stats['category_counts']}")
    print(f"Field types: {stats['field_types']}")
    print(f"Paths with value options: {stats['value_options']}")
    print(f"Specialized fields: {stats['specialized_fields']}")
    print(f"\nCore Fields Summary: {core_summary}")
    print(f"\nAll previously missing schema paths have been successfully integrated!")
    
  