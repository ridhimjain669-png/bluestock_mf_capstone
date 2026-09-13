"""
Fetch the latest available NAV history for selected mutual fund schemes
from the MFAPI and save each scheme's data as a CSV file.
"""

import requests
import pandas as pd


# AMFI scheme codes to fetch
SCHEME_CODES = [
    125497,
    119551,
    120503,
    118632,
    119092,
    120841,
]


def fetch_nav(scheme_code):
    """Fetch NAV history for one scheme and save it as a CSV file."""
    url = f"https://api.mfapi.in/mf/{scheme_code}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        nav_df = pd.DataFrame(data["data"])
        nav_df["amfi_code"] = scheme_code
        nav_df["scheme_name"] = data["meta"]["scheme_name"]

        file_name = f"live_nav_{scheme_code}.csv"
        nav_df.to_csv(file_name, index=False)

        print(f"Saved {file_name} ({len(nav_df)} rows)")

    except requests.RequestException as error:
        print(f"Could not fetch scheme {scheme_code}: {error}")

    except (KeyError, ValueError, TypeError) as error:
        print(f"Could not process data for scheme {scheme_code}: {error}")


def main():
    """Fetch NAV history for all selected schemes."""
    for scheme_code in SCHEME_CODES:
        fetch_nav(scheme_code)

    print("NAV fetching completed.")


if __name__ == "__main__":
    main()
