# Bank Transaction Data Validation Pipeline

## Project Overview

This project is a Python-based data validation pipeline for processing bank transaction CSV files.

The pipeline reads transaction data from multiple branch files, combines the data, validates it based on business rules, and generates valid, invalid, and summary output files.

## Input Data

The pipeline reads all CSV files from the `input` folder.

Example:

- BR001_20260906_TRANSACTION.csv
- BR002_20260906_TRANSACTION.csv
- BR003_20260906_TRANSACTION.csv

The pipeline automatically detects CSV files from the input folder, so new files with the same structure can be processed without changing the code.

## Required Columns

Each input CSV file must contain the following columns:

- transaction_id
- account_id
- transaction_date
- transaction_type
- amount
- currency

## Validation Rules

The pipeline validates the following rules:

1. Transaction ID must not be missing.
2. Account ID must not be missing.
3. Transaction date must be in the correct format.
4. Transaction type must be CREDIT or DEBIT.
5. Amount must be present.
6. Amount must be numeric.
7. Amount must be greater than 0.
8. Currency must be USD.
9. Transaction ID must be unique across all input files.

If a record violates multiple rules, all applicable errors are stored in the `error_reason` column.

## Output Files

The pipeline generates three files in the `output` folder:

### valid_transactions.csv

Contains records that passed all validation rules.

### invalid_transactions.csv

Contains records that failed one or more validation rules.

The `error_reason` column contains the reason or reasons why a record is invalid.

### summary.csv

Contains the total number of records, valid records, and invalid records.

## Project Structure

```text
bank-transaction-pipeline/
│
├── input/
│   ├── BR001_20260906_TRANSACTION.csv
│   ├── BR002_20260906_TRANSACTION.csv
│   └── BR003_20260906_TRANSACTION.csv
│
├── output/
│   ├── valid_transactions.csv
│   ├── invalid_transactions.csv
│   └── summary.csv
│
├── src/
│   └── pipeline.py
│
├── requirements.txt
└── README.md

Technologies Used: 
Python
Pandas
CSV
Git
GitHub

Installation:

Install the required Python package using:
     pip install -r requirements.txt

How to Run:

Run the pipeline from the project root folder using:
    python src/pipeline.py
The processed output files will be generated automatically in the output folder.

Current Output Summary:

For the provided input files:

Total Records: 24
Valid Records: 10
Invalid Records: 14


## Week 2 Testing

The pipeline was tested with different real-world input scenarios to check reliability and error handling.

Test scenarios included:

- T01: New branch file
- T02: Header-only file
- T03: Missing required column
- T04: Multiple validation errors
- T05: Cross-file duplicate transaction
- T06: Non-numeric amount
- T07: Impossible transaction date
- T08: Different column order
- T09: Rerun with the same inputs
- T10: Unexpected file

All tests passed after investigation and retesting.

During T06, the pipeline initially failed when a non-numeric amount such as ABC was provided. The issue was fixed by safely converting the amount using pd.to_numeric(..., errors="coerce"). After the fix, the pipeline was rerun successfully.

Final Test Output Summary:

Total Records: 32
Valid Records: 14
Invalid Records: 18



