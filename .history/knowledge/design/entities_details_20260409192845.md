# Insurance Domain - Entity Details

This document outlines the top 20 entities in the insurance domain along with their key attributes.

## 1. Policy
The core insurance contract entity.

**Attributes:**
- policy_id (PK)
- policy_number (unique)
- policy_type (auto, health, life, property, etc.)
- policy_holder_id (FK)
- insurer_id (FK)
- start_date
- end_date
- status (active, expired, cancelled, lapsed)
- premium_amount
- premium_frequency (monthly, quarterly, annually)
- coverage_amount
- deductible
- terms_and_conditions
- created_date
- last_modified_date
- renewal_date

## 2. Claim
Represents a request for compensation under a policy.

**Attributes:**
- claim_id (PK)
- claim_number (unique)
- policy_id (FK)
- claimant_id (FK)
- claim_type (damage, theft, accident, medical, death)
- claim_date
- incident_date
- claim_amount
- approved_amount
- status (submitted, under_review, approved, rejected, settled, closed)
- description
- assigned_adjuster_id (FK)
- settlement_date
- payment_date
- rejection_reason
- created_date
- last_modified_date

## 3. Customer (Policyholder)
Individual or organization purchasing insurance.

**Attributes:**
- customer_id (PK)
- customer_type (individual, corporate)
- first_name
- last_name
- date_of_birth
- gender
- email
- phone_number
- alternate_phone
- occupation
- annual_income
- address_id (FK)
- identification_type (SSN, passport, driver_license)
- identification_number
- risk_profile (low, medium, high)
- customer_since
- status (active, inactive, blacklisted)
- created_date
- last_modified_date

## 4. Agent/Broker
Insurance sales representative.

**Attributes:**
- agent_id (PK)
- agent_code (unique)
- first_name
- last_name
- email
- phone_number
- license_number
- license_expiry_date
- specialization (life, health, auto, property, commercial)
- agency_name
- commission_rate
- address_id (FK)
- performance_rating
- total_policies_sold
- active_policies_count
- status (active, inactive, suspended)
- hire_date
- created_date
- last_modified_date

## 5. Insurer (Insurance Company)
The insurance provider organization.

**Attributes:**
- insurer_id (PK)
- company_name
- registration_number
- license_number
- email
- phone_number
- website
- headquarters_address_id (FK)
- financial_rating
- total_assets
- established_date
- specializations
- claim_settlement_ratio
- customer_service_rating
- status (active, inactive)
- created_date
- last_modified_date

## 6. Premium
Payment for insurance coverage.

**Attributes:**
- premium_id (PK)
- policy_id (FK)
- premium_amount
- due_date
- payment_date
- payment_status (pending, paid, overdue, waived)
- payment_method_id (FK)
- late_fee
- discount_applied
- discount_amount
- net_amount
- payment_frequency (monthly, quarterly, semi_annually, annually)
- grace_period_end_date
- receipt_number
- created_date
- last_modified_date

## 7. Coverage
Specific protection provided by a policy.

**Attributes:**
- coverage_id (PK)
- policy_id (FK)
- coverage_type (liability, collision, comprehensive, medical, etc.)
- coverage_name
- coverage_description
- coverage_limit
- deductible
- coverage_amount
- start_date
- end_date
- exclusions
- conditions
- is_mandatory
- premium_portion
- status (active, inactive)
- created_date
- last_modified_date

## 8. Beneficiary
Person entitled to receive policy benefits.

**Attributes:**
- beneficiary_id (PK)
- policy_id (FK)
- beneficiary_type (primary, contingent, tertiary)
- first_name
- last_name
- relationship_to_policyholder
- date_of_birth
- percentage_share
- email
- phone_number
- address_id (FK)
- identification_type
- identification_number
- status (active, inactive, deceased)
- created_date
- last_modified_date

## 9. Underwriter
Professional who evaluates risk and determines policy terms.

**Attributes:**
- underwriter_id (PK)
- employee_code
- first_name
- last_name
- email
- phone_number
- specialization (life, health, property, casualty)
- license_number
- experience_years
- risk_assessment_limit
- policies_underwritten_count
- approval_rating
- department
- supervisor_id (FK)
- status (active, inactive)
- hire_date
- created_date
- last_modified_date

## 10. Risk Assessment
Evaluation of potential risks for underwriting.

**Attributes:**
- assessment_id (PK)
- policy_id (FK)
- underwriter_id (FK)
- assessment_date
- risk_score
- risk_category (low, medium, high, very_high)
- risk_factors
- medical_history_reviewed
- credit_score
- occupation_risk
- lifestyle_factors
- previous_claims_count
- recommendation (approve, reject, approve_with_conditions)
- conditions
- approved_premium
- notes
- created_date
- last_modified_date

## 11. Payment
Financial transaction for premiums or claims.

**Attributes:**
- payment_id (PK)
- payment_type (premium, claim_settlement, refund)
- related_entity_id (policy_id or claim_id)
- payer_id (FK)
- payee_id (FK)
- amount
- payment_date
- payment_method (credit_card, debit_card, bank_transfer, check, cash, digital_wallet)
- transaction_reference
- payment_status (pending, completed, failed, refunded)
- currency
- exchange_rate
- processing_fee
- net_amount
- receipt_url
- created_date
- last_modified_date

## 12. Document
Supporting documents for policies and claims.

**Attributes:**
- document_id (PK)
- document_type (policy_document, claim_form, medical_report, police_report, invoice, receipt, photo, video)
- document_name
- file_path
- file_size
- file_format
- related_entity_type (policy, claim, customer)
- related_entity_id
- uploaded_by_id (FK)
- upload_date
- document_date
- description
- verification_status (pending, verified, rejected)
- verified_by_id (FK)
- verification_date
- is_confidential
- retention_period
- created_date
- last_modified_date

## 13. Incident
Event that triggers a claim.

**Attributes:**
- incident_id (PK)
- incident_type (accident, theft, fire, flood, medical_emergency, death, natural_disaster)
- incident_date
- incident_time
- location_address_id (FK)
- latitude
- longitude
- description
- severity (minor, moderate, major, catastrophic)
- police_report_filed
- police_report_number
- witnesses_count
- weather_conditions
- estimated_damage
- related_policy_id (FK)
- related_claim_id (FK)
- reported_by_id (FK)
- reported_date
- created_date
- last_modified_date

## 14. Vehicle
Insured vehicle entity (for auto insurance).

**Attributes:**
- vehicle_id (PK)
- policy_id (FK)
- owner_id (FK)
- make
- model
- year
- vin_number (unique)
- registration_number
- body_type (sedan, suv, truck, coupe, etc.)
- fuel_type (petrol, diesel, electric, hybrid)
- engine_capacity
- color
- purchase_date
- purchase_price
- current_market_value
- odometer_reading
- usage_type (personal, commercial, ride_sharing)
- parking_location
- anti_theft_devices
- safety_features
- previous_accidents_count
- status (active, sold, totaled)
- created_date
- last_modified_date

## 15. Property
Insured property entity (for property insurance).

**Attributes:**
- property_id (PK)
- policy_id (FK)
- owner_id (FK)
- property_type (residential, commercial, industrial, agricultural)
- address_id (FK)
- structure_type (house, apartment, condo, office, warehouse)
- year_built
- square_footage
- number_of_rooms
- number_of_stories
- construction_type (wood, brick, concrete, steel)
- roof_type
- foundation_type
- heating_system
- cooling_system
- electrical_system
- plumbing_system
- security_system
- fire_protection_system
- purchase_price
- current_market_value
- assessment_value
- previous_claims_count
- status (active, sold, demolished)
- created_date
- last_modified_date

## 16. Medical Record
Health information (for health/life insurance).

**Attributes:**
- record_id (PK)
- customer_id (FK)
- policy_id (FK)
- record_date
- record_type (checkup, diagnosis, treatment, prescription, lab_result, imaging)
- provider_name
- provider_specialty
- diagnosis_codes (ICD codes)
- procedure_codes (CPT codes)
- medications
- allergies
- chronic_conditions
- pre_existing_conditions
- height
- weight
- bmi
- blood_pressure
- blood_group
- smoking_status
- alcohol_consumption
- family_medical_history
- hospitalization_history
- surgical_history
- document_id (FK)
- is_confidential
- created_date
- last_modified_date

## 17. Quote
Preliminary insurance offer before policy issuance.

**Attributes:**
- quote_id (PK)
- quote_number (unique)
- customer_id (FK)
- agent_id (FK)
- insurance_type (auto, health, life, property)
- quote_date
- valid_until
- coverage_details
- coverage_amount
- deductible
- premium_amount
- premium_frequency
- discount_applied
- discount_percentage
- final_premium
- risk_factors
- terms_and_conditions
- status (draft, sent, viewed, accepted, rejected, expired, converted_to_policy)
- policy_id (FK - if converted)
- notes
- created_date
- last_modified_date

## 18. Policy Renewal
Continuation of an existing policy.

**Attributes:**
- renewal_id (PK)
- original_policy_id (FK)
- new_policy_id (FK)
- renewal_date
- renewal_type (automatic, manual)
- previous_premium
- new_premium
- premium_change_percentage
- previous_coverage_amount
- new_coverage_amount
- terms_changed
- changes_description
- renewal_status (pending, approved, rejected, completed)
- renewal_notice_sent_date
- customer_response_date
- customer_action (accepted, rejected, requested_modification)
- processed_by_id (FK)
- process_date
- effective_date
- created_date
- last_modified_date

## 19. Commission
Agent compensation for policy sales.

**Attributes:**
- commission_id (PK)
- agent_id (FK)
- policy_id (FK)
- commission_type (new_business, renewal, referral)
- policy_premium
- commission_rate
- commission_amount
- payment_status (pending, approved, paid, withheld)
- calculation_date
- payment_date
- payment_method_id (FK)
- tax_withheld
- net_commission
- payment_reference
- fiscal_year
- fiscal_quarter
- notes
- created_date
- last_modified_date

## 20. Endorsement
Modification or addition to an existing policy.

**Attributes:**
- endorsement_id (PK)
- endorsement_number (unique)
- policy_id (FK)
- endorsement_type (add_coverage, remove_coverage, increase_limit, decrease_limit, change_beneficiary, change_address, change_vehicle, add_driver)
- request_date
- effective_date
- requested_by (policyholder, agent, insurer)
- requested_by_id (FK)
- description
- changes_detail
- premium_impact
- new_premium_amount
- additional_documents_required
- status (requested, under_review, approved, rejected, implemented)
- approved_by_id (FK)
- approval_date
- implementation_date
- reason_for_change
- notes
- created_date
- last_modified_date

---

## Entity Relationships Overview

### Primary Relationships:
- **Customer** → **Policy** (1:N - A customer can have multiple policies)
- **Policy** → **Claim** (1:N - A policy can have multiple claims)
- **Policy** → **Premium** (1:N - A policy has multiple premium payments)
- **Policy** → **Coverage** (1:N - A policy includes multiple coverages)
- **Policy** → **Beneficiary** (1:N - A policy can have multiple beneficiaries)
- **Agent** → **Policy** (1:N - An agent sells multiple policies)
- **Underwriter** → **Risk Assessment** (1:N - An underwriter performs multiple assessments)
- **Policy** → **Document** (1:N - A policy has multiple documents)
- **Claim** → **Document** (1:N - A claim has multiple supporting documents)
- **Incident** → **Claim** (1:N - An incident may result in multiple claims)
- **Quote** → **Policy** (1:1 - A quote may convert to a policy)
- **Policy** → **Endorsement** (1:N - A policy can have multiple endorsements)
- **Policy** → **Policy Renewal** (1:N - A policy can be renewed multiple times)
- **Agent** → **Commission** (1:N - An agent receives multiple commissions)

### Supporting Entities:
- **Address** - Shared by Customer, Agent, Insurer, Property, Incident
- **Payment Method** - Used for Premium and Payment transactions

---

## Notes on Implementation

1. **Normalization**: Consider creating separate address, contact, and payment method entities for better data management.

2. **Audit Trail**: All entities include created_date and last_modified_date for tracking changes.

3. **Status Fields**: Most entities include status fields for lifecycle management.

4. **Soft Deletes**: Consider implementing soft delete patterns rather than hard deletes to maintain historical data.

5. **Temporal Data**: Some entities may benefit from temporal tables to track historical changes (e.g., Policy, Coverage).

6. **Security**: Implement role-based access control (RBAC) and data encryption for sensitive information like SSN, medical records, and financial data.

7. **Compliance**: Ensure compliance with regulations like HIPAA (health data), GDPR (personal data), and industry-specific insurance regulations.

8. **Scalability**: Consider partitioning strategies for high-volume tables like Claim, Payment, and Document.
