# 🗳️ UBNHS Voting System

Welcome to the official voting system for UB National High School (UBNHS)! This system empowers students, faculty, and staff to participate in secure, fair, and transparent elections—whether for student council, classroom representatives, or school-wide polls.

## 🎯 Purpose
To provide a digital platform that facilitates voting within UBNHS, ensuring accessibility, integrity, and ease of use for all eligible participants.

## 🛠️ System Design

### 1. **User Roles**
- **Admin**: Manages elections, adds candidates, views results.
- **Voter**: Registered users eligible to cast votes.

### 2. **Authentication**
- Generate Qr Code using student LRN.
- Admin Page protected by role-based access control.

### 3. **Voting Interface**
- User-friendly UI for selecting candidates or options.
- Confirmation step before final vote submission.
- Real-time feedback for successful vote casting.

### 4. **Voting Logic**
- One vote per user per election.
- Supports multiple voting formats:
  - **Majority Vote**
  - **Ranked Choice**
  - **Yes/No Referendum**

### 5. **Security Measures**
- Encrypted vote storage
- IP and timestamp logging
- Optional anonymity toggle for sensitive polls

### 6. **Result Reporting**
- Dashboard with real-time vote counts
- Export options: CSV, PDF, EXCEL
- Audit trail for validation
