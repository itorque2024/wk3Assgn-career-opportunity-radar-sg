
📊 Career Opportunity Radar — Singapore Job Market Dashboard

An interactive dashboard designed to help job seekers in Singapore identify high-demand sectors, competitive salary ranges, and relative job market competition using large-scale job posting data.

Built with Streamlit + DuckDB, powered by an enhanced dataset of ~1 million job postings.

⸻

1️⃣ Business Context

Business Objective

Provide data-driven insights to help job seekers prioritise roles and sectors based on:
	•	Hiring demand
	•	Salary levels
	•	Competition intensity
	•	Time trends

Target User

Job seekers in Singapore (fresh graduates, mid-career professionals, career switchers).

Value Proposition

The dashboard supports practical decisions such as:
	•	Where to focus applications
	•	Which sectors offer strong demand and pay
	•	Which roles may face high competition
	•	How demand and salary evolve over time

⸻

2️⃣ Dataset
	•	Source: Singapore job postings dataset (~1,048,585 records)
	•	Time coverage: 2023
	•	Format: Parquet (columnar storage for efficient querying)

⸻

3️⃣ Data Processing & Feature Engineering

The dataset was cleaned and enhanced to support analytical querying:

Cleaning & Standardisation
	•	Parsed posting dates into post_date and month
	•	Ensured numeric salary fields
	•	Filtered non-monthly salary records
	•	Flagged unrealistic salary outliers (> 50,000/month)
	•	Normalised experience and sector categories

Derived Features
	•	salary_mid (robust salary metric)
	•	salary_band (categorised salary ranges)
	•	experience_band (0–1, 2–4, 5–9, 10+ years)
	•	applications (renamed for clarity)
	•	Competition metric: applications_per_posting
	•	Freshness metric: days_since_original_post

All aggregations are performed using SQL queries via DuckDB.

⸻

4️⃣ Dashboard Design

Page 1 — Career Opportunity Radar

Bubble Chart Encoding
	•	X-axis → Hiring demand (number of postings)
	•	Y-axis → Median monthly salary
	•	Bubble size → Applications per posting (competition)
	•	Color → Salary intensity

Filters
	•	Month range
	•	Position level
	•	Sector
	•	Minimum postings threshold

Interpretation Guide
	•	Right → Higher demand
	•	Higher → Higher salary
	•	Larger bubble → Higher competition

This view allows job seekers to quickly identify high-opportunity sectors.

⸻

5️⃣ Technical Stack
	•	Streamlit — interactive web dashboard
	•	DuckDB — SQL-based analytics engine
	•	Parquet — efficient columnar data storage
	•	Plotly — interactive visualisations

Why DuckDB + Parquet:
	•	Handles large datasets efficiently
	•	Enables SQL-based aggregation
	•	Minimises memory overhead

⸻

6️⃣ How to Run

pip install -r requirements.txt
streamlit run app.py

Ensure SGJobData_enhanced.parquet is in the project directory.

⸻

7️⃣ Limitations
	•	Job postings may not fully represent total labour demand.
	•	Applications count does not measure applicant quality.
	•	Salary ranges reflect posted values, not final negotiated pay.
	•	Dataset covers a limited time window (2023 only).

⸻

📌 Summary

This project demonstrates how large-scale job posting data can be transformed into a decision-support tool for job seekers, combining scalable SQL querying with intuitive visualisation.

⸻

