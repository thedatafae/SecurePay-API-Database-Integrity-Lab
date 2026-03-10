# 🛡️ SecurePay: API & Database Integrity Lab

A specialized SQA automation project designed to validate **API-to-Database persistence** and **transactional integrity**. This lab utilizes a "Grey-Box" testing approach to ensure that high-level API responses accurately reflect the low-level MySQL state.



## 🛠️ Tech Stack & Tools
* **Language:** Python (Flask)
* **Database:** MySQL (Relational Schema)
* **Automation:** Postman & Newman CLI
* **Reporting:** Newman `htmlextra`

## 📁 Project Structure
* `/backend`: Flask API logic with intentional "hidden" bugs.
* `/database`: SQL scripts for schema, seeding, and manual integrity checks.
* `/testing`: Postman Collections and Environment variables.
* `/reports`: Automated HTML test execution dashboards.

## 🚦 Getting Started
1. **Database:** Import `database/schema.sql` and `database/seed_data.sql` into MySQL.
2. **API:** Run `pip install -r requirements.txt` and start the server with `python backend/main.py`.
3. **Tests:** Execute the Newman suite:
   ```bash
   newman run testing/Collection.json -e testing/Env.json -r htmlextra --reporter-htmlextra-export reports/Report.html
   ```

   
