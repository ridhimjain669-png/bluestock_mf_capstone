
import pandas as pd

# Load the fund master and Day 4 scorecard CSV files.
fund_master_df = pd.read_csv(
    "/content/drive/MyDrive/Bluestock /capstone/cleaned/fund_master_cleaned.csv"
)

scorecard_df = pd.read_csv(
    "/content/drive/MyDrive/Bluestock /capstone/cleaned/fund_scorecard.csv"
)

# Keep fund names, risk categories, and Sharpe ratios.
recommender_df = fund_master_df[
    ["amfi_code", "scheme_name", "risk_category"]
].merge(
    scorecard_df[["amfi_code", "Sharpe_Ratio"]],
    on="amfi_code",
    how="inner"
)

risk_mapping = {
    "Low": ["Low"],
    "Moderate": ["Moderate", "Moderately High"],
    "High": ["High", "Very High"]
}

def recommend_funds(risk_appetite):
    risk_appetite = risk_appetite.strip().title()

    if risk_appetite not in risk_mapping:
        print("Please enter Low, Moderate, or High.")
        return

    matching_funds = recommender_df[
        recommender_df["risk_category"].isin(
            risk_mapping[risk_appetite]
        )
    ]

    recommendations = (
        matching_funds
        .dropna(subset=["Sharpe_Ratio"])
        .sort_values("Sharpe_Ratio", ascending=False)
        .head(3)
    )

    print(f"Top 3 funds for {risk_appetite} risk appetite:")

    display(
        recommendations[
            ["scheme_name", "risk_category", "Sharpe_Ratio"]
        ].reset_index(drop=True)
    )

if __name__ == "__main__":
    risk_appetite = input("Enter risk appetite (Low / Moderate / High): ")
    recommend_funds(risk_appetite)
