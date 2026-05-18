# AI Usage Log

## Project: Momo SMS Data Visualization
## Team: Execution Trio

This document logs all AI tool interactions during the development of this project, in compliance with the AI Usage Policy. All team-specific design decisions, analysis, and implementation were done by team members. AI was used as a learning and verification tool, not as a replacement for original work.

---

## Log Entries

### Entry 1: SQL Best Practices and Constraints
- **Date:** 16 May 2026
- **Tool Used:** Claude (Anthropic)
- **Team Member:** Henriette
- **Purpose:** Learning best practices for writing SQL DDL statements, including proper use of CHECK constraints, FOREIGN KEY constraints, and column comments for documentation.
- **What Was Asked:** How to properly structure CREATE TABLE statements with constraints, what CHECK constraints are appropriate for columns like status and user_type, and how to add meaningful column comments.
- **How It Was Used:** The guidance was used to understand SQL syntax patterns. All table designs and column choices were made by the team based on our own analysis of the MoMo SMS data.

### Entry 2: Database Normalization (1NF, 2NF, 3NF)
- **Date:** 15 May 2026
- **Tool Used:** Claude (Anthropic)
- **Team Member:** Apongseh Foghang
- **Purpose:** Understanding normalization forms and how to identify transitive dependencies, partial dependencies, and redundant attributes.
- **What Was Asked:** How to check if our tables satisfy 1NF, 2NF, and 3NF, and what constitutes a transitive dependency.
- **How It Was Used:** We applied normalization concepts to evaluate our own table designs. This led to team decisions such as removing the direction and service_code columns from Transaction_Categories after identifying they were determined by category_name rather than category_id.

### Entry 3: Grammar and Syntax Checking in Documentation
- **Date:** 18 May 2026
- **Tool Used:** Claude (Anthropic)
- **Team Member:** Luigi
- **Purpose:** Reviewing documentation text for grammar, clarity, and consistency.
- **What Was Asked:** Proofreading of the design rationale, data dictionary descriptions, and README database documentation section for grammatical errors and unclear phrasing.
- **How It Was Used:** AI suggestions were reviewed and selectively applied. All technical content and design decisions in the documentation were written by team members.

### Entry 4: Code Syntax Verification
- **Date:** 18 May 2026
- **Tool Used:** Claude (Anthropic)
- **Team Member:** Luigi
- **Purpose:** Verifying SQL syntax for CREATE TABLE statements, INSERT statements, and INDEX creation.
- **What Was Asked:** Whether our SQL scripts would run without errors, including correct placement of constraints, proper data types, and valid foreign key references.
- **How It Was Used:** AI was used to catch syntax errors before running scripts. All SQL logic, table structure, and sample data were designed by the team.

### Entry 5: JSON Structure Best Practices
- **Date:** 18 May 2026
- **Tool Used:** Claude (Anthropic)
- **Team Member:** Henriette
- **Purpose:** Understanding how relational database tables are typically serialized into JSON format for API responses.
- **What Was Asked:** Why tables are represented as arrays of objects in JSON, how foreign keys translate to nested objects, and how SQL data types map to JSON types.
- **How It Was Used:** The concepts were applied to create our JSON schema examples. All data values and entity structures in the JSON file reflect our own database design.

---

## Summary

| Area of AI Use | Purpose | Original Work By Team |
|---|---|---|
| SQL best practices | Learning syntax patterns for constraints and comments | All table designs, column choices, and data types chosen by team from MoMo data analysis |
| Normalization | Understanding 1NF, 2NF, 3NF concepts | All normalization decisions made by team after evaluating our specific tables |
| Grammar checking | Proofreading documentation text | All technical content and design rationale written by team |
| Code syntax verification | Catching SQL syntax errors before execution | All SQL logic and sample data created by team |
| JSON structure | Learning serialization patterns | All JSON schemas designed by team to match our database |

---

## Policy Compliance Statement

We confirm that AI tools were used solely for learning concepts, verifying syntax, and checking grammar. All design decisions, data analysis, entity identification, relationship modeling, and implementation logic are original work by team members. No AI-generated code was copied directly into the project without understanding and adapting it to our specific requirements.