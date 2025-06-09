# google_search_api_template.py

from googleapiclient.discovery import build
import pandas as pd
import time

# Your API credentials here
API_KEY = "AIzaSyD519E62SdcuC8IstbRijgE7q_kUoMqBsU"
CSE_ID = "4415af1f7d77e4cc2"

# Function to search Google API
def google_search(query, api_key, cse_id, num_results=5):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, num=num_results).execute()
    return res.get('items', [])

# List of real company names (example) → You can replace this list with your own
company_list = [
    
    "Tata Consultancy Services (TCS)",
    "Infosys",
    "Tech Mahindra",
    "Wipro",
    "Accenture",
    "Capgemini",
    "IBM",
    "Google",
    "Microsoft",
    "Amazon",
    "Zoho",
    "Salesforce",
    "Intel",
    "NVIDIA",
    "Dell Technologies",
    "Cisco",
    "Oracle",
    "Adobe",
    "Siemens",
    "Bosch",
    "Deloitte",
    "EY (Ernst & Young)",
    "KPMG",
    "PwC (PricewaterhouseCoopers)",
    "SAP",
    "Atlassian",
    "Flipkart",
    "Paytm",
    "Ola",
    "Uber",
    "Samsung",
    "HCL Technologies",
    "Cognizant",
    "JP Morgan Chase",
    "Goldman Sachs",
    "Morgan Stanley",
    "Qualcomm",
    "ABB",
    "VMware",
    "Schneider Electric",
    "HP",
    "Unilever",
    "ITC Limited",
    "Asian Paints",
    "Mahindra & Mahindra",
    "L&T",
    "Reliance Industries",
    "Aditya Birla Group",
    "HDFC Bank",
    "ICICI Bank"
]

# Prepare empty list to store results
results_data = []

# Loop through companies
for company in company_list:
    print(f"Searching for: {company}")
    query = f'site:internshala.com "internship" "{company}"'  # You can change site or leave it open
    try:
        search_results = google_search(query, API_KEY, CSE_ID, num_results=3)
        
        if search_results:
            for result in search_results:
                results_data.append({
                    "name": company,
                    "job_description": result.get("snippet", ""),
                    "website_url": result.get("link", ""),
                    "label": 1  # Real internship
                })
        else:
            print(f"No results found for {company}")
        
        # Pause between API calls to avoid hitting rate limits
        time.sleep(1)
        
    except Exception as e:
        print(f"Error searching for {company}: {e}")

# Convert results to DataFrame
df = pd.DataFrame(results_data)

# Add empty email_domain column for manual entry later
df["email_domain"] = ""

# Save to CSV
df.to_csv("real_internship_dataset.csv", index=False)

print("✅ Real internship dataset saved to 'real_internship_dataset.csv'")
