
import requests
import pandas as pd

# Required AMFI scheme codes
scheme_codes = [
    125497,
    119551,
    120503,
    118632,
    119092,
    120841
]

for scheme_code in scheme_codes:

    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        # Convert NAV data to DataFrame
        nav_df = pd.DataFrame(data["data"])

        # Add scheme information
        nav_df["amfi_code"] = scheme_code
        nav_df["scheme_name"] = data["meta"]["scheme_name"]

        # Save as CSV
        file_name = f"live_nav_{scheme_code}.csv"
        nav_df.to_csv(file_name, index=False)

        print(f"Successfully fetched AMFI Code: {scheme_code}")
        print(f"Scheme Name: {data['meta']['scheme_name']}")
        print(f"Rows fetched: {len(nav_df)}")
        print("-" * 50)

    else:
        print(f"Failed to fetch AMFI Code: {scheme_code}")
        print(f"Status Code: {response.status_code}")

print("Live NAV fetching completed!")
