# HRMS UI & DocType Field Reference Manual: Jahan Kodak

This document provides a comprehensive, field-by-field reference guide for all DocTypes in the Frappe HRMS (`hrms`) app. For every DocType, this manual explains its core purpose, step-by-step UI usage, and a detailed field dictionary explaining what each field means, how it works, and how to use it based on real-world business scenarios at **Jahan Kodak**.

---

## Table of Contents
1. [Core Employee Management](#1-core-employee-management)
2. [Leave & Time-Off Management](#2-leave--time-off-management)
3. [Attendance & Shift Tracking](#3-attendance--shift-tracking)
4. [Payroll Processing & Compensation](#4-payroll-processing--compensation)
5. [Expense Claims & Travel Management](#5-expense-claims--travel-management)
6. [Recruitment & Applicant Tracking](#6-recruitment--applicant-tracking)
7. [Onboarding & Separation](#7-onboarding--separation)
8. [Performance Management & Appraisals](#8-performance-management--appraisals)
9. [Employee Training & Skill Management](#9-employee-training--skill-management)
10. [Employee Tax Exemption & Benefits](#10-employee-tax-exemption--benefits)
11. [Vehicle Fleet & Daily Work Summaries](#11-vehicle-fleet--daily-work-summaries)
12. [HRMS System Settings](#12-hrms-system-settings)

---

## 1. Core Employee Management

### 1.1 Employee (`Employee`)
* **Purpose:** The central identity record for every worker in the organization. Stores personal, employment, payroll, and organizational assignment details.
* **UI Path:** `HR -> Employee -> Employee List -> Add Employee`

#### Field Dictionary & Real-World Usage

| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `first_name` | Data | Employee's given first name. Mandatory. | `Ahmad` |
| `last_name` | Data | Employee's surname or family name. | `Rahimi` |
| `employee_name` | Data | Auto-generated full display name. | `Ahmad Rahimi` |
| `status` | Select | Current employment status (`Active`, `Inactive`, `Left`, `Suspended`). | Set to `Active` on hiring, `Left` upon resignation. |
| `gender` | Select | Gender classification (`Male`, `Female`, `Other`). | Used for HR reporting and labor statistics. |
| `date_of_birth` | Date | Employee's birth date. Validates minimum age constraints. | `1995-04-12` |
| `date_of_joining` | Date | Official start date at Jahan Kodak. | `2024-01-15` (Used to calculate leave eligibility and gratuity). |
| `company` | Link | Legal entity employing the user. Mandatory. | `Jahan Kodak` |
| `department` | Link | Organizational department. | `Sales - JK` or `Warehouse - JK` |
| `designation` | Link | Official job title. | `Store Cashier`, `Branch Manager`, `Inventory Manager` |
| `reports_to` | Link | Direct manager/supervisor (links to another Employee). | Links Cashier to `HR-EMP-00012` (Branch Manager). |
| `branch` | Link | Associated physical location. | `Kabul Center`, `Shahr-e-Naw` |
| `employment_type` | Link | Classification (`Full-time`, `Part-time`, `Contract`). | `Full-Time` |
| `user_id` | Link | Associated ERPNext System User login. | `ahmad.rahimi@jahankodak.af` (Allows employee to submit leave requests). |
| `payroll_cost_center` | Link | Cost Center to debit salary expenses. | `Kabul Center - JK` |
| `cell_number` | Data | Primary phone number for official notifications. | `+93 70 123 4567` |
| `prefered_email` | Select | Email address used for notifications (`Company Email`, `Personal Email`, `User ID`). | `Company Email` |
| `bank_name` | Data | Employee's banking institution for direct salary deposit. | `Da Afghanistan Bank` or `Azizi Bank` |
| `bank_ac_no` | Data | Bank account number for salary transfer. | `001102003004` |
| `ctc` | Currency | Cost to Company (annual total compensation value). | `360,000` AFN/year |

---

### 1.2 Employment Type (`Employment Type`)
* **Purpose:** Defines categories of employment contract terms.
* **UI Path:** `HR -> Setup -> Employment Type`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employment_type_name` | Data | Unique name of the contract type. | `Full-Time Permanent`, `Intern`, `Seasonal Contract` |

---

### 1.3 Employee Grade (`Employee Grade`)
* **Purpose:** Categorizes organizational hierarchy levels for benefit entitlements, pay scales, and approval authorities.
* **UI Path:** `HR -> Setup -> Employee Grade`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `name` / `grade_name` | Data | Grade designation identifier. | `Grade 1 (Junior)`, `Grade 3 (Management)` |
| `default_leave_policy` | Link | Default leave entitlement package associated with this grade. | `Executive Leave Policy` |
| `salary_structure` | Link | Standard base salary template for this grade. | `Store Cashier Grade 1 Structure` |

---

### 1.4 Employee Health Insurance (`Employee Health Insurance`)
* **Purpose:** Records health coverage details and policy numbers for staff.
* **UI Path:** `HR -> Employee -> Employee Health Insurance`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employee` | Link | Targeted employee record. | `EMP-00045` |
| `health_insurance_provider` | Link/Data | Insurance company name. | `Afghan National Insurance Company` |
| `policy_number` | Data | Official health policy reference ID. | `POL-9920112` |
| `coverage_amount` | Currency | Maximum financial coverage limit per annum. | `100,000` AFN |

---

### 1.5 Employee Promotion (`Employee Promotion`)
* **Purpose:** Formal document tracking position changes, title updates, and salary adjustments.
* **UI Path:** `HR -> Employee -> Employee Promotion`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employee` | Link | Employee being promoted. | `EMP-00018` |
| `promotion_date` | Date | Effective date of new role/salary. | `2026-08-01` |
| `current_designation` | Link | Pre-promotion job title (read-only). | `Assistant Store Manager` |
| `new_designation` | Link | Approved post-promotion job title. | `Branch Manager` |
| `current_department` | Link | Existing department assignment. | `Sales - JK` |
| `new_department` | Link | New department assignment. | `Sales - JK` |

---

### 1.6 Employee Transfer (`Employee Transfer`)
* **Purpose:** Handles employee movements across departments, branches, or companies.
* **UI Path:** `HR -> Employee -> Employee Transfer`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employee` | Link | Employee being relocated. | `EMP-00022` |
| `transfer_date` | Date | Effective relocation date. | `2026-09-01` |
| `current_branch` | Link | Existing store/office location. | `Kabul Center` |
| `new_branch` | Link | Destination store/office location. | `Shahr-e-Naw` |
| `current_department` | Link | Existing department. | `Warehouse - JK` |
| `new_department` | Link | New department. | `Warehouse - JK` |

---

### 1.7 Employee Separation (`Employee Separation`)
* **Purpose:** Manages the offboarding workflow, exit interviews, and clearance tasks when an employee leaves.
* **UI Path:** `HR -> Employee -> Employee Separation`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employee` | Link | Employee departing the company. | `EMP-00009` |
| `resignation_letter_date` | Date | Date formal notice was submitted. | `2026-07-01` |
| `exit_interview` | Link | Reference to the completed exit interview. | `EXT-INT-00004` |
| `status` | Select | Clearance status (`Pending`, `In Process`, `Completed`). | `In Process` |

---

## 2. Leave & Time-Off Management

### 2.1 Leave Type (`Leave Type`)
* **Purpose:** Master rule configuration for specific time-off categories (Annual, Sick, Casual, Unpaid).
* **UI Path:** `HR -> Leaves -> Leave Type`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `leave_type_name` | Data | Descriptive name of the leave category. | `Annual Leave` |
| `is_allocable` | Checkbox | Enable if HR must allocate explicit days per cycle. | Checked (`1`) for Annual Leave, Unchecked (`0`) for Unpaid Leave. |
| `is_carry_forward` | Checkbox | Unused days roll over into the next annual period. | Checked (`1`) |
| `is_lwp` | Checkbox | Leave Without Pay (automatically deducts salary on payroll). | Checked (`1`) for Unpaid Leave. |
| `is_optional_leave` | Checkbox | Restricted to optional/floating holidays. | Unchecked (`0`) |
| `max_continuous_days_allowed` | Int | Upper limit of consecutive days taken per application. | `14` (Prevents single application exceeding 2 weeks without director approval). |

---

### 2.2 Leave Application (`Leave Application`)
* **Purpose:** Official request by an employee to take time off.
* **UI Path:** `HR -> Leaves -> Leave Application`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employee` | Link | Employee requesting leave. | `EMP-00014` |
| `leave_type` | Link | Category of leave. | `Annual Leave` |
| `from_date` | Date | Start date of leave period. | `2026-08-10` |
| `to_date` | Date | End date of leave period (inclusive). | `2026-08-15` |
| `total_leave_days` | Float | Calculated working days consumed. | `5` |
| `half_day` | Checkbox | Check if application is for a half-day shift. | `0` |
| `reason` | Small Text | Justification provided by applicant. | `Family vacation` |
| `status` | Select | Workflow state (`Open`, `Approved`, `Rejected`, `Cancelled`). | Approved by direct supervisor. |
| `leave_approver` | Link | System user assigned to review request. | `manager@jahankodak.af` |

---

### 2.3 Leave Allocation (`Leave Allocation`)
* **Purpose:** Grants specific leave day balances to an employee for a defined time period.
* **UI Path:** `HR -> Leaves -> Leave Allocation`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employee` | Link | Target employee. | `EMP-00030` |
| `leave_type` | Link | Leave type being allocated. | `Annual Leave` |
| `from_date` | Date | Start of validity period. | `2026-01-01` |
| `to_date` | Date | Expiry date of validity period. | `2026-12-31` |
| `new_leaves_allocated` | Float | Number of credit days granted. | `20.0` |

---

### 2.4 Leave Policy (`Leave Policy`) & Assignment (`Leave Policy Assignment`)
* **Purpose:** Combines multiple Leave Types into a single rule-set and assigns it to employees in bulk.
* **UI Path:** `HR -> Leaves -> Leave Policy` / `Leave Policy Assignment`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `title` | Data | Policy name. | `Standard Staff Policy 2026` |
| `leave_policy_details` | Table | List of leave types and annual day limits. | `Annual Leave: 20 days`, `Sick Leave: 10 days`, `Casual Leave: 5 days`. |
| `assignment_date` | Date | Date policy assignment takes effect. | `2026-01-01` |

---

## 3. Attendance & Shift Tracking

### 3.1 Attendance (`Attendance`)
* **Purpose:** Stores daily presence records for payroll calculations.
* **UI Path:** `HR -> Attendance -> Attendance`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employee` | Link | Employee record. | `EMP-00012` |
| `attendance_date` | Date | Date of attendance entry. | `2026-07-23` |
| `status` | Select | Status (`Present`, `Absent`, `On Leave`, `Half Day`, `Work From Home`). | `Present` |
| `shift` | Link | Associated shift definition. | `Day Shift` |
| `in_time` | Datetime | First clock-in timestamp. | `2026-07-23 07:55:12` |
| `out_time` | Datetime | Final clock-out timestamp. | `2026-07-23 17:04:45` |
| `late_entry` | Checkbox | System-generated flag if clock-in is after shift grace period. | `0` |
| `early_exit` | Checkbox | System-generated flag if clock-out is before shift end. | `0` |

---

### 3.2 Shift Type (`Shift Type`)
* **Purpose:** Defines working hours, grace periods, auto-attendance rules, and overtime thresholds.
* **UI Path:** `HR -> Attendance -> Shift Type`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `shift_name` | Data | Name of the shift schedule. | `Day Shift` or `Retail Store Shift` |
| `start_time` | Time | Official shift commencement time. | `08:00:00` |
| `end_time` | Time | Official shift conclusion time. | `17:00:00` |
| `enable_auto_attendance` | Checkbox | Auto-marks Attendance from Employee Checkins. | Checked (`1`) |
| `late_mark_grace_period` | Int | Allowed grace period in minutes before marking late. | `15` (Arrival up to 08:15 AM is not flagged late). |
| `early_exit_grace_period` | Int | Allowed grace period before shift end in minutes. | `10` |
| `determine_check_in_and_check_out` | Select | Logic strategy (`Alternating entries`, `Strictly by In-Out timestamps`). | `Strictly by In-Out timestamps` |

---

### 3.3 Employee Checkin (`Employee Checkin`)
* **Purpose:** Raw biometric machine or mobile app GPS check-in logs.
* **UI Path:** `HR -> Attendance -> Employee Checkin`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employee` | Link | Employee identifier. | `EMP-00008` |
| `time` | Datetime | Exact punch timestamp. | `2026-07-23 07:58:30` |
| `log_type` | Select | Punch direction (`IN`, `OUT`). | `IN` |
| `device_id` | Data | Biometric scanner ID or mobile device location tag. | `KABUL-POS-TERMINAL-01` |

---

## 4. Payroll Processing & Compensation

### 4.1 Payroll Entry (`Payroll Entry`)
* **Purpose:** Batch document for generating month-end Salary Slips for a group of employees.
* **UI Path:** `Payroll -> Payroll Entry -> Add Payroll Entry`

#### Field Dictionary & Real-World Usage

| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `posting_date` | Date | Accounting posting date for salary entries. | `2026-07-31` |
| `company` | Link | Employer company. Mandatory. | `Jahan Kodak` |
| `payroll_frequency` | Select | Frequency (`Monthly`, `Fortnightly`, `Weekly`). | `Monthly` |
| `start_date` | Date | Payroll period start date. | `2026-07-01` |
| `end_date` | Date | Payroll period end date. | `2026-07-31` |
| `branch` | Link | Filter payroll by branch. | `Kabul Center` (Generates slips only for Kabul staff). |
| `department` | Link | Filter payroll by department. | `Sales - JK` |
| `payroll_payable_account` | Link | Balance sheet liability account for accrued salaries. | `Payroll Payable - JK` |
| `cost_center` | Link | Default Cost Center for salary expenses. | `Kabul Center - JK` |
| `employees` | Table | List of included employees auto-fetched by criteria. | Table containing 15 branch cashiers & managers. |
| `workflow_state` | Link | Approval state (`Draft`, `Pending HR Approval`, `Pending Finance Approval`, `Approved`). | `Pending Finance Approval` |

---

### 4.2 Salary Structure (`Salary Structure`)
* **Purpose:** Defines base earnings, allowances, and deductions formula for an employee role or grade.
* **UI Path:** `Payroll -> Salary Structure`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `name` / `title` | Data | Name of the compensation structure. | `Retail Store Manager Package` |
| `company` | Link | Associated company. | `Jahan Kodak` |
| `payroll_frequency` | Select | Frequency of payment. | `Monthly` |
| `earnings` | Table | Table of addition components (Basic, Allowances). | `Basic Salary: 25,000 AFN`, `House Rent: 5,000 AFN`. |
| `deductions` | Table | Table of subtraction components (Taxes, LWP). | `Income Tax: Formula-based`, `Unpaid Leave: Auto-calculated`. |

---

### 4.3 Salary Structure Assignment (`Salary Structure Assignment`)
* **Purpose:** Binds a specific `Salary Structure` to an individual `Employee` with an effective date and base amount.
* **UI Path:** `Payroll -> Salary Structure Assignment`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employee` | Link | Target employee. | `EMP-00005` |
| `salary_structure` | Link | Selected compensation structure. | `Store Cashier Grade 1 Structure` |
| `from_date` | Date | Date from which salary rate takes effect. | `2026-01-01` |
| `base` | Currency | Monthly base pay numeric input. | `30,000` AFN |

---

### 4.4 Salary Component (`Salary Component`)
* **Purpose:** Building block items used inside Salary Structures (Earnings/Deductions).
* **UI Path:** `Payroll -> Salary Component`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `salary_component` | Data | Display name on salary slips. | `Basic Salary`, `House Rent Allowance` |
| `type` | Select | Classification (`Earning`, `Deduction`). | `Earning` |
| `is_tax_applicable` | Checkbox | Subject to income tax deduction. | Checked (`1`) for Basic Salary. |
| `depends_on_payment_days` | Checkbox | Pro-rated based on absent/unpaid days. | Checked (`1`) |
| `amount_based_on_formula` | Checkbox | Calculated dynamically via Python expression. | `base * 0.20` (House Rent is 20% of base salary). |

---

### 4.5 Salary Slip (`Salary Slip`)
* **Purpose:** Individual monthly payslip record detailing gross earnings, deductions, and net salary.
* **UI Path:** `Payroll -> Salary Slip`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employee` | Link | Target employee. | `EMP-00012` |
| `employee_name` | Data | Full name. | `Ahmad Rahimi` |
| `posting_date` | Date | Entry date. | `2026-07-31` |
| `payment_days` | Float | Number of payable days after deducting unpaid absences. | `30.0` |
| `gross_pay` | Currency | Total sum of earnings before deductions. | `30,000` AFN |
| `total_deduction` | Currency | Total sum of taxes and deductions. | `1,500` AFN |
| `net_pay` | Currency | Final takeaway salary (`Gross Pay - Total Deduction`). | `28,500` AFN |

---

## 5. Expense Claims & Travel Management

### 5.1 Expense Claim (`Expense Claim`)
* **Purpose:** Employee requests reimbursement for official out-of-pocket business expenses.
* **UI Path:** `HR -> Expense Claim -> Expense Claim`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employee` | Link | Claimant employee. | `EMP-00003` |
| `posting_date` | Date | Date claim submitted. | `2026-07-20` |
| `expenses` | Table | Itemized expenses table. | Row 1: `Travel Expense`, 2,500 AFN, Receipt attached. |
| `total_claimed_amount` | Currency | Sum of claimed line items. | `2,500` AFN |
| `approval_status` | Select | Status (`Draft`, `Approved`, `Rejected`). | `Approved` |
| `payable_account` | Link | Liability account to credit payment. | `Employee Claim Payable - JK` |

---

### 5.2 Travel Request (`Travel Request`)
* **Purpose:** Formal pre-approval request for official business travel.
* **UI Path:** `HR -> Travel -> Travel Request`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employee` | Link | Traveling employee. | `EMP-00002` (Procurement Officer) |
| `purpose_of_travel` | Link/Data | Justification. | `Supplier Auditing & Cargo Coordination` |
| `means_of_transport` | Select | Mode (`Flight`, `Car`, `Train`). | `Flight` |
| `travel_itinerary` | Table | Schedule of departure and arrival locations/dates. | `Kabul -> Herat`, `2026-08-05` to `2026-08-08`. |

---

## 6. Recruitment & Applicant Tracking

### 6.1 Job Requisition (`Job Requisition`)
* **Purpose:** Internal request by a department manager for hiring new headcount.
* **UI Path:** `HR -> Recruitment -> Job Requisition`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `designation` | Link | Position requested. | `Store Cashier` |
| `department` | Link | Department requesting head count. | `Sales - JK` |
| `no_of_positions` | Int | Number of vacancies required. | `3` |
| `reason_for_requisition` | Select | Purpose (`New Position`, `Replacement`). | `New Position` (Opening new store branch). |

---

### 6.2 Job Opening (`Job Opening`)
* **Purpose:** Public job advertisement post linked to applicant portals.
* **UI Path:** `HR -> Recruitment -> Job Opening`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `job_title` | Data | External job title posting. | `Branch Manager - Shahr-e-Naw` |
| `designation` | Link | Target designation master. | `Branch Manager` |
| `status` | Select | Posting state (`Open`, `Closed`). | `Open` |
| `description` | Text Editor | Job duties and candidate requirements. | Detailed role responsibilities and qualifications. |

---

### 6.3 Job Applicant (`Job Applicant`)
* **Purpose:** Candidate profile store containing resume details, contact info, and recruitment stage tracking.
* **UI Path:** `HR -> Recruitment -> Job Applicant`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `applicant_name` | Data | Full candidate name. | `Mohammad Bilal` |
| `email_id` | Data | Contact email. | `bilal.candidate@gmail.com` |
| `phone_number` | Data | Mobile number. | `+93 79 987 6543` |
| `job_title` | Link | Job vacancy applied for. | `Branch Manager - Shahr-e-Naw` |
| `status` | Select | Stage (`Open`, `Replied`, `Interview`, `Hold`, `Accepted`, `Rejected`). | `Interview` |

---

### 6.4 Interview (`Interview`)
* **Purpose:** Schedules candidate interview evaluation sessions with assigned interviewers.
* **UI Path:** `HR -> Recruitment -> Interview`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `job_applicant` | Link | Targeted candidate. | `Mohammad Bilal` |
| `interview_round` | Link | Assessment stage. | `Technical & Managerial Round` |
| `scheduled_on` | Date | Interview date. | `2026-07-28` |
| `from_time` | Time | Start time. | `10:00:00` |
| `to_time` | Time | End time. | `11:00:00` |
| `interviewers` | Table | Panel of evaluator employees. | `EMP-00001` (HR Manager), `EMP-00004` (Sales Director). |

---

## 7. Onboarding & Separation

### 7.1 Job Offer (`Job Offer`)
* **Purpose:** Formal offer letter sent to selected applicant detailing designation and proposed start date.
* **UI Path:** `HR -> Recruitment -> Job Offer`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `job_applicant` | Link | Selected candidate. | `Mohammad Bilal` |
| `offer_date` | Date | Date offer issued. | `2026-07-29` |
| `designation` | Link | Role offered. | `Branch Manager` |
| `status` | Select | Status (`Draft`, `Awaiting Response`, `Accepted`, `Rejected`). | `Accepted` |

---

### 7.2 Employee Onboarding (`Employee Onboarding`)
* **Purpose:** Automates onboarding checklists (hardware allocation, email setup, document verification).
* **UI Path:** `HR -> Employee -> Employee Onboarding`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `job_applicant` | Link | Candidate profile. | `Mohammad Bilal` |
| `company` | Link | Employer entity. | `Jahan Kodak` |
| `department` | Link | Assigned department. | `Sales - JK` |
| `activities` | Table | Checklist of tasks assigned to HR/IT teams. | Task 1: `Setup Laptop & POS Credentials`, Task 2: `Collect Tazkira ID Copy`. |

---

## 8. Performance Management & Appraisals

### 8.1 Appraisal (`Appraisal`)
* **Purpose:** Periodic performance evaluation document comparing actual achievements against Key Result Areas (KRAs) and Goals.
* **UI Path:** `HR -> Performance -> Appraisal`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employee` | Link | Employee being reviewed. | `EMP-00012` |
| `appraisal_cycle` | Link | Review period master. | `Annual Review 2026` |
| `total_score` | Float | System-calculated weighted performance rating score. | `4.2` / 5.0 |

---

### 8.2 Goal (`Goal`) & KRA (`KRA`)
* **Purpose:** Defines specific measurable targets assigned to employees.
* **UI Path:** `HR -> Performance -> Goal` / `KRA`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `title` | Data | Goal title. | `Achieve Monthly Branch Target of 2M AFN` |
| `employee` | Link | Target employee. | `EMP-00012` (Branch Manager) |
| `progress` | Percent | Completion progress percentage. | `85%` |

---

## 9. Employee Training & Skill Management

### 9.1 Training Event (`Training Event`)
* **Purpose:** Schedules corporate training sessions for staff development.
* **UI Path:** `HR -> Training -> Training Event`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `event_name` | Data | Name of session. | `POS & Inventory Audit Training 2026` |
| `trainer_name` | Data | Instructor name. | `Zubair Ahmad` |
| `employees` | Table | List of participating staff. | All branch managers and head cashiers. |

---

## 10. Employee Tax Exemption & Benefits

### 10.1 Employee Tax Exemption Declaration (`Employee Tax Exemption Declaration`)
* **Purpose:** Employee declares non-taxable investments or deductible expenses to lower income tax calculations.
* **UI Path:** `Payroll -> Tax Exemption -> Tax Exemption Declaration`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `employee` | Link | Declaring employee. | `EMP-00004` |
| `payroll_period` | Link | Financial tax year period. | `FY 2026` |
| `declarations` | Table | Itemized tax exemption categories and declared amounts. | Exemption category for charitable donations or medical costs. |

---

## 11. Vehicle Fleet & Daily Work Summaries

### 11.1 Vehicle Log (`Vehicle Log`)
* **Purpose:** Tracks fuel expenses, odometer readings, and maintenance logs for company delivery vehicles.
* **UI Path:** `HR -> Fleet Management -> Vehicle Log`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `license_plate` | Link | Vehicle registration plate. | `KBL-40912` |
| `employee` | Link | Driver/Employee responsible. | `EMP-00020` |
| `odometer` | Int | Odometer reading at entry. | `45,200` km |
| `fuel_qty` | Float | Liters of fuel added. | `50` L |
| `price` | Currency | Total fuel expense cost. | `3,200` AFN |

---

### 11.2 Daily Work Summary (`Daily Work Summary`)
* **Purpose:** Automated daily progress email summary collected from employees.
* **UI Path:** `HR -> Daily Work Summary`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `user` | Link | User sending daily update. | `ahmad.rahimi@jahankodak.af` |
| `status` | Select | Status (`Draft`, `Sent`). | `Sent` |

---

## 12. HRMS System Settings

### 12.1 HR Settings (`HR Settings`)
* **Purpose:** Global default settings for HR module behaviour.
* **UI Path:** `HR -> Setup -> HR Settings`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `auto_leave_encashment` | Checkbox | Automatically encash un-availed leave at year end. | Unchecked (`0`) |
| `restrict_backdated_leave` | Checkbox | Prevents employees from filing leaves for past dates. | Checked (`1`) |

---

### 12.2 Payroll Settings (`Payroll Settings`)
* **Purpose:** Global rules for salary calculations, roundings, and tax defaults.
* **UI Path:** `Payroll -> Setup -> Payroll Settings`

#### Field Dictionary
| Field Name | Type | Description & System Logic | Real-World Usage Example |
| :--- | :--- | :--- | :--- |
| `calculate_payroll_working_days_based_on` | Select | Logic basis (`Leave Application`, `Attendance`). | `Attendance` |
| `password_policy` | Data | Encryption key rules for PDF salary slip password protection. | Auto-generated password using Employee DOB. |
