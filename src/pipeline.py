from pathlib import Path

import pandas as pd

INPUT_FOLDER = Path("input")

csv_files = list(INPUT_FOLDER.glob("*.csv"))

print("CSV files found:")

for file in csv_files:

    print(file)


required_columns = [
    "transaction_id",
    "account_id",
    "transaction_date",
    "transaction_type",
    "amount",
    "currency"
]

dataframes = []

for file in csv_files:

    df = pd.read_csv(file)

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print(f"\nMissing columns in {file}:")
        print(missing_columns)
    else:
        dataframes.append(df)

print("\nCSV files read successfully!")

for df in dataframes:

    print(df.shape)

combined_df = pd.concat(dataframes, ignore_index=True)

duplicate_ids = combined_df[
    combined_df["transaction_id"].duplicated(keep=False)
]

print("\nDuplicate transaction IDs:")

print(duplicate_ids)


missing_transaction_id = combined_df["transaction_id"].isna()

print("\nMissing Transaction IDs:")

print(combined_df[missing_transaction_id])

missing_account_id = combined_df["account_id"].isna()

print("\nMissing Account IDs:")

print(combined_df[missing_account_id])

missing_transaction_date = combined_df["transaction_date"].isna()

print("\nMissing Transaction Dates:")

print(combined_df[missing_transaction_date])

invalid_transaction_dates = pd.to_datetime(
    combined_df["transaction_date"],
    format="%Y-%m-%d",
    errors="coerce"
).isna()

print("\nInvalid Transaction Dates:")

print(combined_df[invalid_transaction_dates])

invalid_transaction_type = ~combined_df["transaction_type"].isin(
    ["CREDIT", "DEBIT"]
)

print("\nInvalid Transaction Types:")

print(combined_df[invalid_transaction_type])

missing_amount = combined_df["amount"].isna()

print("\nMissing Amounts:")

print(combined_df[missing_amount])

invalid_amount = combined_df["amount"].notna() & (combined_df["amount"] <= 0)

print("\nInvalid Amounts:")

print(combined_df[invalid_amount])

invalid_currency = combined_df["currency"] != "USD"

print("\nInvalid Currencies:")

print(combined_df[invalid_currency])

non_numeric_amount = pd.to_numeric(
    combined_df["amount"],
    errors="coerce"
).isna() & combined_df["amount"].notna()

print("\nNon-Numeric Amounts:")

print(combined_df[non_numeric_amount])


combined_df["error_reason"] = ""


combined_df.loc[missing_transaction_id, "error_reason"] += "Transaction ID is missing; "


duplicate_mask = combined_df["transaction_id"].duplicated(keep=False)
combined_df.loc[duplicate_mask, "error_reason"] += "Duplicate Transaction ID; "


combined_df.loc[missing_account_id, "error_reason"] += "Account ID is missing; "


combined_df.loc[invalid_transaction_dates, "error_reason"] += "Invalid transaction date; "


combined_df.loc[invalid_transaction_type, "error_reason"] += "Invalid transaction type; "


combined_df.loc[missing_amount, "error_reason"] += "Amount is missing; "
combined_df.loc[invalid_amount, "error_reason"] += "Amount must be greater than 0; "
combined_df.loc[non_numeric_amount, "error_reason"] += "Amount must be numeric; "


combined_df.loc[invalid_currency, "error_reason"] += "Invalid currency; "


combined_df["error_reason"] = combined_df["error_reason"].str.rstrip("; ")



valid_df = combined_df[combined_df["error_reason"] == ""].copy()

invalid_df = combined_df[combined_df["error_reason"] != ""].copy()

print("\nValid Records:")
print(valid_df)

print("\nInvalid Records:")
print(invalid_df)

print("\nCombined data:")

print(combined_df)



valid_df.to_csv(
    "output/valid_transactions.csv",
    index=False
)

invalid_df.to_csv(
    "output/invalid_transactions.csv",
    index=False
)

print("\nOutput files created successfully!")



summary_df = pd.DataFrame({
    "metric": [
        "Total Records",
        "Valid Records",
        "Invalid Records"
    ],
    "count": [
        len(combined_df),
        len(valid_df),
        len(invalid_df)
    ]
})



summary_df.to_csv(
    "output/summary.csv",
    index=False
)

print("\nSummary file created successfully!")
print(summary_df)