
"""
Recommend up to three mutual funds based on the user's risk appetite.

Recommendations are ranked by Sharpe Ratio within the selected risk category.
"""

import pandas as pd


FUND_MASTER_PATH = (
    "/content/drive/MyDrive/Bluestock /capstone/cleaned/"
    "fund_master_cleaned.csv"
)
SCORECARD_PATH = (
    "/content/drive/MyDrive/Bluestock /capstone/cleaned/"
    "fund_scorecard.csv"
)

RISK_MAPPING = {
    "Low": ["Low"],
    "Moderate": ["Moderate", "Moderately High"],
    "High": ["High", "Very High"],
}


def load_recommender_data():
    """Load fund details and Sharpe Ratios, then combine them."""
    fund_master_df = pd.read_csv(FUND_MASTER_PATH)
    scorecard_df = pd.read_csv(SCORECARD_PATH)

    return fund_master_df[
        ["amfi_code", "scheme_name", "risk_category"]
    ].merge(
        scorecard_df[["amfi_code", "Sharpe_Ratio"]],
        on="amfi_code",
        how="inner",
    )


def recommend_funds(risk_appetite, recommender_df):
    """Return up to three funds matching the requested risk appetite."""
    risk_appetite = risk_appetite.strip().title()

    if risk_appetite not in RISK_MAPPING:
        print("Please enter Low, Moderate, or High.")
        return

    recommendations = (
        recommender_df[
            recommender_df["risk_category"].isin(
                RISK_MAPPING[risk_appetite]
            )
        ]
        .dropna(subset=["Sharpe_Ratio"])
        .sort_values("Sharpe_Ratio", ascending=False)
        .head(3)
    )

    if recommendations.empty:
        print(f"No matching funds found for {risk_appetite} risk appetite.")
        return

    print(f"Top 3 funds for {risk_appetite} risk appetite:")
    print(
        recommendations[
            ["scheme_name", "risk_category", "Sharpe_Ratio"]
        ].to_string(index=False)
    )


def main():
    """Load the data and ask the user for a risk appetite."""
    recommender_df = load_recommender_data()
    risk_appetite = input("Enter risk appetite (Low / Moderate / High): ")
    recommend_funds(risk_appetite, recommender_df)


if __name__ == "__main__":
    main()
