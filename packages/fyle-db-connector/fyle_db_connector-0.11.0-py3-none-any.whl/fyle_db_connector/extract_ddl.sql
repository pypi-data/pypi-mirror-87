DROP TABLE IF EXISTS fyle_extract_employees;
DROP TABLE IF EXISTS fyle_extract_expenses;
DROP TABLE IF EXISTS fyle_extract_expense_custom_properties;
DROP TABLE IF EXISTS fyle_extract_corporate_credit_card_expenses;
DROP TABLE IF EXISTS fyle_extract_settlements;
DROP TABLE IF EXISTS fyle_extract_reimbursements;
DROP TABLE IF EXISTS fyle_extract_advances;
DROP TABLE IF EXISTS fyle_extract_advance_requests;
DROP TABLE IF EXISTS fyle_extract_attachments;
DROP TABLE IF EXISTS fyle_extract_categories;
DROP TABLE IF EXISTS fyle_extract_projects;
DROP TABLE IF EXISTS fyle_extract_cost_centers;
DROP TABLE IF EXISTS fyle_extract_reports;

CREATE TABLE fyle_extract_employees (
  "id" TEXT,
  "created_at" DATETIME,
  "updated_at" DATETIME,
  "employee_email" TEXT,
  "employee_code" TEXT,
  "full_name" TEXT,
  "joining_date" TEXT,
  "location" TEXT,
  "level_id" TEXT,
  "level" TEXT,
  "business_unit" TEXT,
  "department_id" TEXT,
  "department" TEXT,
  "sub_department" TEXT,
  "approver1_email" TEXT,
  "approver2_email" TEXT,
  "approver3_email" TEXT,
  "title" TEXT,
  "branch_ifsc" TEXT,
  "branch_account" TEXT,
  "mobile" TEXT,
  "delegatee_email" TEXT,
  "default_cost_center_name" TEXT,
  "disabled" INTEGER,
  "org_id" TEXT,
  "org_name" TEXT
);

CREATE TABLE fyle_extract_expenses (
  "id" TEXT,
  "employee_id" TEXT,
  "employee_email" TEXT,
  "employee_code" TEXT,
  "spent_at" DATETIME,
  "currency" TEXT,
  "amount" INTEGER,
  "foreign_currency" TEXT,
  "foreign_amount" TEXT,
  "purpose" TEXT,
  "project_id" TEXT,
  "project_name" TEXT,
  "cost_center_id" TEXT,
  "cost_center_name" TEXT,
  "category_id" INTEGER,
  "category_code" TEXT,
  "category_name" TEXT,
  "sub_category" TEXT,
  "settlement_id" TEXT,
  "expense_number" TEXT,
  "claim_number" TEXT,
  "trip_request_id" TEXT,
  "state" TEXT,
  "report_id" TEXT,
  "fund_source" TEXT,
  "reimbursable" INTEGER,
  "created_at" DATETIME,
  "updated_at" DATETIME,
  "approved_at" DATETIME,
  "settled_at" DATETIME,
  "verified" INTEGER,
  "split_group_id" TEXT,
  "split_group_user_amount" INTEGER,
  "verified_at" DATETIME,
  "reimbursed_at" DATETIME,
  "added_to_report_at" DATETIME,
  "report_submitted_at" DATETIME,
  "vendor" TEXT,
  "has_attachments" INTEGER,
  "billable" TEXT,
  "exported" INTEGER,
  "approved_by" TEXT,
  "org_id" TEXT,
  "org_name" TEXT,
  "created_by" TEXT
);

CREATE TABLE fyle_extract_expense_custom_properties (
  "expense_id" text,
  "name" text,
  "value" text
);

CREATE TABLE fyle_extract_corporate_credit_card_expenses (
  "id" TEXT,
  "employee_email" TEXT,
  "org_user_id" TEXT,
  "org_id" TEXT,
  "org_name" TEXT,
  "created_at" DATETIME,
  "updated_at" DATETIME,
  "spent_at" DATETIME,
  "amount" REAL,
  "currency" TEXT,
  "foreign_amount" REAL,
  "foreign_currency" TEXT,
  "vendor" TEXT,
  "description" TEXT,
  "settlement_id" TEXT,
  "corporate_credit_card_account_number" TEXT,
  "personal" INTEGER,
  "expense_id" TEXT,
  "reimbursement_state" TEXT,
  "transaction_type" TEXT,
  "state" TEXT,
  "exported" INTEGER,
  "exported_at" DATETIME,
  "expense_split_group_id" TEXT
);

CREATE TABLE fyle_extract_settlements (
  "id" TEXT,
  "created_at" DATETIME,
  "updated_at" DATETIME,
  "opening_date" TEXT,
  "closing_date" TEXT,
  "employee_id" TEXT,
  "employee_email" TEXT,
  "employee_code" TEXT,
  "creator_employee_id" TEXT,
  "creator_employee_email" TEXT,
  "creator_employee_code" TEXT,
  "org_id" TEXT,
  "org_name" TEXT,
  "exported" INTEGER
);

CREATE TABLE fyle_extract_reimbursements (
  "id" TEXT,
  "created_at" DATETIME,
  "updated_at" DATETIME,
  "employee_id" TEXT,
  "employee_email" TEXT,
  "employee_code" TEXT,
  "org_id" TEXT,
  "org_name" TEXT,
  "currency" TEXT,
  "amount" REAL,
  "state" TEXT,
  "report_ids" TEXT,
  "unique_id" TEXT,
  "purpose" TEXT,
  "settlement_id" TEXT,
  "exported" INTEGER
);

CREATE TABLE IF NOT EXISTS fyle_extract_advances (
"id" TEXT,
  "created_at" DATETIME,
  "updated_at" DATETIME,
  "employee_id" TEXT,
  "employee_email" TEXT,
  "employee_code" TEXT,
  "project_id" TEXT,
  "project_name" TEXT,
  "currency" TEXT,
  "amount" INTEGER,
  "purpose" TEXT,
  "issued_at" DATETIME,
  "payment_mode" TEXT,
  "original_currency" TEXT,
  "original_amount" TEXT,
  "reference" TEXT,
  "settlement_id" TEXT,
  "trip_request_id" TEXT,
  "advance_number" TEXT,
  "advance_request_id" TEXT,
  "settled_at" DATETIME,
  "approved_by" TEXT,
  "created_by" TEXT,
  "exported" INTEGER,
  "export_ids" TEXT,
  "org_id" TEXT,
  "org_name" TEXT
);

CREATE TABLE fyle_extract_advance_requests (
"updated_at" DATETIME,
  "created_at" DATETIME,
  "approved_at" DATETIME,
  "id" TEXT,
  "purpose" TEXT,
  "notes" TEXT,
  "state" TEXT,
  "currency" TEXT,
  "amount" REAL,
  "advance_id" TEXT,
  "advance_request_number" TEXT,
  "trip_request_id" TEXT,
  "project_id" REAL,
  "source" TEXT,
  "is_sent_back" INTEGER,
  "is_pulled_back" INTEGER,
  "org_id" TEXT,
  "org_name" TEXT,
  "employee_email" TEXT,
  "employee_name" TEXT,
  "employee_id" TEXT,
  "exported" INTEGER
);

CREATE TABLE fyle_extract_attachments (
  "filename" TEXT,
  "content" TEXT,
  "password" TEXT,
  "expense_id" TEXT
);

CREATE TABLE fyle_extract_categories (
  "id" INTEGER,
  "name" TEXT,
  "code" TEXT,
  "enabled" INTEGER,
  "fyle_category" TEXT,
  "sub_category" TEXT,
  "created_at" DATETIME,
  "updated_at" DATETIME,
  "org_id" TEXT,
  "org_name" TEXT
);


CREATE TABLE fyle_extract_projects (
  "id" TEXT,
  "name" TEXT,
  "description" TEXT,
  "active" INTEGER,
  "approver1_employee_id" TEXT,
  "approver1_employee_email" TEXT,
  "approver1_employee_code" TEXT,
  "approver2_employee_id" TEXT,
  "approver2_employee_email" TEXT,
  "approver2_employee_code" TEXT,
  "org_id" TEXT,
  "code" TEXT,
  "org_name" TEXT
);

CREATE TABLE fyle_extract_cost_centers (
  "id" TEXT,
  "name" TEXT,
  "description" TEXT,
  "code" TEXT,
  "active" INTEGER,
  "org_id" TEXT,
  "org_name" TEXT
);

CREATE TABLE IF NOT EXISTS fyle_extract_reports (
  "id" TEXT,
  "employee_id" TEXT,
  "employee_email" TEXT,
  "employee_code" TEXT,
  "state" TEXT,
  "amount" INTEGER,
  "purpose" TEXT,
  "claim_number" TEXT,
  "created_at" DATETIME,
  "updated_at" DATETIME,
  "approved_at" DATETIME,
  "reimbursed_at" DATETIME,
  "trip_request_id" TEXT,
  "settlement_id" TEXT,
  "org_id" TEXT,
  "org_name" TEXT,
  "verified" INTEGER,
  "exported" INTEGER,
  "approved_by" TEXT,
  "created_by" TEXT,
  "settled_at" DATETIME
);