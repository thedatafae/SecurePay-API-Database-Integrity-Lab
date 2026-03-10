# 🚩 SecurePay Defect Log

This document details the high-impact bugs identified during the execution of the SecurePay Test Plan.

---

## BUG-001: Critical Transactional Rollback Failure
* **Severity:** 🔴 Critical
* **Test Case:** `TC_5.1: Rollback Verification`
* **Description:** When a transfer is sent to a non-existent `receiver_id`, the system returns a 500 error but **still deducts money** from the sender.
* **Evidence:** Postman logic check captured balance at `1000` before error and `900` after error.
* **Impact:** Direct financial loss for the user.



---

## BUG-002: Schema Data Type Mismatch
* **Severity:** 🟡 Medium
* **Test Case:** `TC_1.3: DType Enforcement`
* **Description:** MySQL `DECIMAL` values are mapped as `Strings` in the JSON response (e.g., `"1000.00"`).
* **Impact:** Potential for mathematical errors in the Frontend (string concatenation instead of addition).



---

## BUG-003: Unhandled Exception (Ghost User)
* **Severity:** 🟡 Medium
* **Test Case:** `TC_4.3: Ghost User Security`
* **Description:** The API returns an `Internal Server Error (500)` rather than a `404 Not Found` when a receiver ID does not exist.
* **Impact:** Poor user experience and potential server-side information leakage.
