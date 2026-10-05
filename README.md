
1. SYSTEM ACTORS

* Club Lead (Primary Actor):
  Submits event proposals with budget requests, generates event tickets with QR
  codes after approval, and monitors registration records.

* Campus Admin (Primary Actor):
  Reviews submitted proposals, evaluates proposed budgets, and records approval
  or rejection decisions with mandatory remarks.

* Student (Primary Actor):
  Browses approved events, purchases tickets via payment processing, and
  downloads/views issued QR-code tickets.

* System / Payment Gateway (Supporting Actor):
  Validates proposal inputs, processes transactions, updates ticket inventory,
  and generates unique QR tokens.


2. LIST OF SYSTEM USE CASES

* UC-1: Submit Event Proposal & Budget
  - Primary Actor: Club Lead
  - Description: Allows the Club Lead to enter event metadata (name, date,
    venue, description, expected participants, budget) and submit the proposal.

* UC-2: Review & Approve/Reject Proposal
  - Primary Actor: Campus Admin
  - Description: Enables the Campus Admin to inspect submitted proposals and
    record an approval or rejection decision.

* UC-3: Generate Event QR Tickets
  - Primary Actor: Club Lead
  - Description: Allows the Club Lead to initialize and generate unique
    QR-code tickets for an approved event.

* UC-4: Purchase Event Ticket
  - Primary Actor: Student
  - Description: Allows the Student to select ticket quantities, process
    payment, and acquire an event ticket.

* UC-5: View & Download QR Ticket
  - Primary Actor: Student
  - Description: Enables students to access and download their issued
    QR-code tickets post-purchase.

* UC-6: View Event Registration Info
  - Primary Actor: Club Lead
  - Description: Allows the Club Lead to track participant registrations and
    ticket availability for their events.

* UC-7: Authenticate User
  - Primary Actor: Shared (Club Lead, Campus Admin, Student)
  - Description: Verifies credentials and enforces role-based access control.

* UC-8: Provide Rejection Remarks
  - Primary Actor: Campus Admin
  - Description: Logs formal justification when a budget proposal is rejected.


3. USE CASE RELATIONSHIPS («include» & «extend»)

A. «include» Relationships (Mandatory Sub-flows)
-------------------------------------------------

1. Purchase Event Ticket  --«include»-->  Authenticate User
   Rationale: Students must be authenticated to complete ticket purchases and
   link passes to their accounts.

2. Submit Event Proposal & Budget  --«include»-->  Authenticate User
   Rationale: Requires verified Club Lead authentication to prevent
   unauthorized submissions.

3. Review & Approve/Reject Proposal  --«include»-->  Authenticate User
   Rationale: Requires administrative sign-in to access approval privileges.


B. «extend» Relationships (Optional / Conditional Flows)
---------------------------------------------------------

1. Provide Rejection Remarks  --«extend»-->  Review & Approve/Reject Proposal
   Extension Point: Proposal Rejected
   Rationale: Only executed when the Campus Admin rejects an event/budget
   proposal.


4. REQUIREMENT TRACEABILITY MATRIX (MAPPING TO MEMBER 1 FRs)

Requirement ID | Requirement Description                   | Associated Use Case                         | Primary Actor
------------------------------------------------------------------------------------------------------------------------
FR-001         | Event Proposal & Budget Submission        | UC-1: Submit Event Proposal & Budget        | Club Lead
FR-002         | Review & Approve/Reject Proposal          | UC-2: Review & Approve/Reject Proposal      | Campus Admin
FR-003         | Generate QR Tickets for Approved Events   | UC-3: Generate Event QR Tickets             | Club Lead
FR-004         | Purchase Event Ticket via Payment         | UC-4: Purchase Event Ticket                 | Student
FR-005         | View/Download Tickets & Monitor Regs      | UC-5: View & Download QR Ticket /           | Student /
               |                                           | UC-6: View Event Registration Info          | Club Lead


5. AGILE BACKLOG & JIRA IMPLEMENTATION

The project requirements were converted into an Agile backlog and managed using
Jira as part of the Software Engineering Lab 2.

Jira Space:
My Software Team

The Agile implementation includes:

* 8 Epics
* 16 User Stories
* Fibonacci-based Story Point estimation
* Priority assignment
* Team-member assignment
* Sprint planning
* Active Sprint tracking
* Burndown monitoring
* Timeline tracking
* Status tracking using To Do, In Progress, In Review, and Done


6. JIRA EPICS

The project backlog was divided into the following eight Epics:

1. User Authentication & Access Control
2. Event Proposal & Budget Management
3. Proposal Review & Budget Approval
4. QR Ticket Generation
5. Event Ticket Booking
6. QR Ticket Access
7. Registration Monitoring
8. System Security & Performance


7. USER STORIES & STORY POINTS

Issue       | User Story                         | Story Points
----------------------------------------------------------------
SCRUM-13    | User Login                         | 3
SCRUM-14    | Role-Based Access                  | 5
SCRUM-15    | Create Event Proposal              | 5
SCRUM-16    | Submit Event Proposal              | 3
SCRUM-17    | Review Event Proposal              | 5
SCRUM-18    | Approve or Reject Budget           | 5
SCRUM-19    | Generate QR Tickets                | 8
SCRUM-20    | Generate Unique Ticket IDs         | 5
SCRUM-21    | Browse Approved Events             | 3
SCRUM-22    | Purchase Event Ticket              | 8
SCRUM-23    | View Purchased QR Ticket           | 3
SCRUM-24    | Download QR Ticket                 | 2
SCRUM-25    | View Event Registration            | 3
SCRUM-26    | View Ticket Availability           | 3
SCRUM-27    | Enforce Authenticated Access       | 5
SCRUM-28    | Maintain Response Performance      | 5

Total Estimated Backlog: 71 Story Points


8. TEAM ALLOCATION

* Chiranth J
  - Epics 1–2
  - SCRUM-13 to SCRUM-16
  - Total: 16 Story Points

* Chris John Paul
  - Epics 3–4
  - SCRUM-17 to SCRUM-20
  - Total: 23 Story Points

* Deeksha G
  - Epics 5–6
  - SCRUM-21 to SCRUM-24
  - Total: 16 Story Points

* Janhavi R
  - Epics 7–8
  - SCRUM-25 to SCRUM-28
  - Total: 16 Story Points


9. SPRINT PLANNING & EXECUTION

Sprint 1
--------

Sprint 1 focused on the initial core workflow of the system.

Stories included:

* SCRUM-13: User Login
* SCRUM-14: Role-Based Access
* SCRUM-15: Create Event Proposal
* SCRUM-16: Submit Event Proposal
* SCRUM-17: Review Event Proposal
* SCRUM-18: Approve or Reject Budget
* SCRUM-19: Generate QR Tickets

Total Sprint 1 Estimate: 34 Story Points

Sprint 1 was completed and closed successfully.


Sprint 2
--------

Sprint 2 was planned to cover the remaining functionality of the system.

Stories included:

* SCRUM-20: Generate Unique Ticket IDs
* SCRUM-21: Browse Approved Events
* SCRUM-22: Purchase Event Ticket
* SCRUM-23: View Purchased QR Ticket
* SCRUM-24: Download QR Ticket
* SCRUM-25: View Event Registration
* SCRUM-26: View Ticket Availability
* SCRUM-27: Enforce Authenticated Access
* SCRUM-28: Maintain Response Performance

Total Sprint 2 Estimate: 37 Story Points

Sprint 2 has been started and is being tracked using the Jira Active Sprint
board.


10. JIRA WORKFLOW & PROGRESS TRACKING

The team used Jira to manage the project using an Agile workflow.

The following activities were completed:

* Created and configured the Jira Software space.
* Created eight project Epics.
* Created sixteen User Stories.
* Assigned Story Points using Fibonacci estimation.
* Assigned work to all four team members.
* Organized User Stories under their respective Epics.
* Created Sprint 1.
* Completed Sprint 1.
* Created and started Sprint 2.
* Used the Active Sprint board to track work.
* Moved issues between To Do, In Progress, In Review, and Done.
* Monitored Sprint progress.
* Reviewed Sprint Insights.
* Used the Burndown Chart to analyze progress.
* Used the Timeline to visualize the project plan.
* Used the Jira Summary to monitor overall project status.


11. SPRINT PROGRESS

Sprint 1:

Status: COMPLETED

The initial authentication, event proposal, budget review, and QR ticket
generation workflow was completed as part of the Agile simulation.


Sprint 2:

Status: IN PROGRESS

Sprint 2 contains the remaining ticketing, registration, authentication,
security, and performance-related stories.

The Sprint 2 board is being used to track the progress of the remaining
User Stories.


12. LAB 2 DELIVERABLES

The following Agile and Jira deliverables have been completed:

* Jira backlog containing Epics and User Stories
* Story Point assignments
* Priority assignments
* Team-member assignments
* Sprint 1 planning
* Sprint 2 planning
* Active Sprint board
* Sprint progress tracking
* Sprint Insights
* Burndown Chart
* Jira Timeline
* Jira Summary
* Sprint reflection
* Professional Lab 2 report


13. CURRENT PROJECT STATUS

Component / Activity                         Status
----------------------------------------------------------------
Lab 1 Requirements                           Completed
System Actors                                Completed
System Use Cases                             Completed
Use Case Relationships                       Completed
Requirement Traceability                     Completed
Jira Space Setup                             Completed
Epics                                        Completed
User Stories                                 Completed
Story Point Estimation                       Completed
Team Assignments                             Completed
Sprint 1                                     Completed
Sprint 2                                     Started
Active Sprint Board                         Completed
Burndown Tracking                            Completed
Sprint Insights                              Completed
Timeline                                     Completed
Lab 2 Report                                 Completed


14. PROJECT DOCUMENTATION

The project documentation includes:

* Original Software Engineering project documentation
* Student Club Event Ticketing & Budget Portal requirements
* System actors and use cases
* Use case relationships
* Requirement traceability
* Agile backlog
* Jira Epics and User Stories
* Sprint planning and execution
* Jira progress tracking
* Sprint analysis and reflection
* Lab 2 Agile/Jira report


