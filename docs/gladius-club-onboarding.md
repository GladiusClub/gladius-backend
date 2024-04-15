---
description: Onboarding a user and setting up roles
---

# Gladius Club onboarding

## Developer Documentation: Club Management System

### Overview

This document describes the frontend and backend interactions for managing club ownership, courses, and memberships.

### Processes

#### 1. Create Club Owner

* **Frontend**: Collects and sends owner's email and UID.
* **Backend**: Triggers creation of the club owner user.

#### 2. Create Club Owner User

* **Backend**: Authenticates and creates a user record with a wallet in `/users`. Waits for document creation confirmation.
* **Frontend**: Checks `/users` for the new document.

#### 3. Set Club Owner in the Contract

* **Frontend**: Invokes `SignupGladiusClub`.
* **Backend**: Processes `club_owner_UID` and `club_name`, creates club doc, sets the club name, copies wallet to `/clubs/{clubUID}`, executes Stellar transaction to set as sports club ([link](https://testnet.stellarchain.io/operations/4843481864359937)), adds owner to club doc, and assigns `owner` role in `club_roles`.

#### 3.5 Add Calendar to the Club

* **Frontend**: Adds calendar link to club document.

#### 4. Create Course

* **Frontend**: Calls `SignupGladiusClubCourse`.
* **Backend**: Receives details, creates course in specified club ([link](https://testnet.stellarchain.io/operations/4852161993261057)).

#### 5. Add Student to Club

* **Backend**: Requires parent UID, student UID, club UID, course/group ID to enroll student.

***

This compact format ensures quick reference and straightforward understanding, focusing on key processes and interactions.
