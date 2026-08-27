================================================================================
1. SYSTEM ACTORS
================================================================================

* Club Lead (Primary Actor):
  Submits event proposals with budget requests, generates event tickets with QR codes after approval, and monitors registration records.

* Campus Admin (Primary Actor):
  Reviews submitted proposals, evaluates proposed budgets, and records approval or rejection decisions with mandatory remarks.

* Student (Primary Actor):
  Browses approved events, purchases tickets via payment processing, and downloads/views issued QR-code tickets.

* System / Payment Gateway (Supporting Actor):
  Validates proposal inputs, processes transactions, updates ticket inventory, and generates unique QR tokens.


================================================================================
2. LIST OF SYSTEM USE CASES
================================================================================

* UC-1: Submit Event Proposal & Budget
  - Primary Actor: Club Lead
  - Description: Allows the Club Lead to enter event metadata (name, date, venue, description, expected participants, budget) and submit the proposal.

* UC-2: Review & Approve/Reject Proposal
  - Primary Actor: Campus Admin
  - Description: Enables the Campus Admin to inspect submitted proposals and record an approval or rejection decision.

* UC-3: Generate Event QR Tickets
  - Primary Actor: Club Lead
  - Description: Allows the Club Lead to initialize and generate unique QR-code tickets for an approved event.

* UC-4: Purchase Event Ticket
  - Primary Actor: Student
  - Description: Allows the Student to select ticket quantities, process payment, and acquire an event ticket.

* UC-5: View & Download QR Ticket
  - Primary Actor: Student
  - Description: Enables students to access and download their issued QR-code tickets post-purchase.

* UC-6: View Event Registration Info
  - Primary Actor: Club Lead
  - Description: Allows the Club Lead to track participant registrations and ticket availability for their events.

* UC-7: Authenticate User
  - Primary Actor: Shared (Club Lead, Campus Admin, Student)
  - Description: Verifies credentials and enforces role-based access control.

* UC-8: Provide Rejection Remarks
  - Primary Actor: Campus Admin
  - Description: Logs formal justification when a budget proposal is rejected.


================================================================================
3. USE CASE RELATIONSHIPS («include» & «extend»)
================================================================================

A. «include» Relationships (Mandatory Sub-flows)
-------------------------------------------------
1. Purchase Event Ticket  --«include»-->  Authenticate User
   Rationale: Students must be authenticated to complete ticket purchases and link passes to their accounts.

2. Submit Event Proposal & Budget  --«include»-->  Authenticate User
   Rationale: Requires verified Club Lead authentication to prevent unauthorized submissions.

3. Review & Approve/Reject Proposal  --«include»-->  Authenticate User
   Rationale: Requires administrative sign-in to access approval privileges.


B. «extend» Relationships (Optional / Conditional Flows)
--------------------------------------------------------
1. Provide Rejection Remarks  --«extend»-->  Review & Approve/Reject Proposal
   Extension Point: Proposal Rejected
   Rationale: Only executed when the Campus Admin rejects an event/budget proposal.


================================================================================
4. REQUIREMENT TRACEABILITY MATRIX (MAPPING TO MEMBER 1 FRs)
================================================================================

Requirement ID | Requirement Description                   | Associated Use Case                         | Primary Actor
------------------------------------------------------------------------------------------------------------------------
FR-001         | Event Proposal & Budget Submission        | UC-1: Submit Event Proposal & Budget        | Club Lead
FR-002         | Review & Approve/Reject Proposal          | UC-2: Review & Approve/Reject Proposal      | Campus Admin
FR-003         | Generate QR Tickets for Approved Events   | UC-3: Generate Event QR Tickets             | Club Lead
FR-004         | Purchase Event Ticket via Payment         | UC-4: Purchase Event Ticket                 | Student
FR-005         | View/Download Tickets & Monitor Regs      | UC-5: View & Download QR Ticket /           | Student /
               |                                           | UC-6: View Event Registration Info          | Club Lead
================================================================================
