import requests
import json
import time

def fetch_employee_data():
    """Fetch employee data from the dummy API"""
    url = "https://dummy.restapiexample.com/api/v1/employees"
    
    # Add headers to avoid 406 error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1} to fetch data...")
            response = requests.get(url, headers=headers)
            
            if response.status_code == 429:  # Too Many Requests
                print(f"Rate limited. Waiting {retry_delay} seconds before retry...")
                time.sleep(retry_delay)
                continue
            elif response.status_code == 406:  # Not Acceptable
                print("Request not acceptable. Trying with different headers...")
                # Try with a simpler header set
                simple_headers = {
                    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
                    'Accept': '*/*'
                }
                response = requests.get(url, headers=simple_headers)
            else:
                response.raise_for_status()  # Raises an HTTPError for bad responses
            
            # Parse the JSON response
            data = response.json()
            
            # Print the data in a formatted way
            print("Employee Data:")
            print(json.dumps(data, indent=2))
            
            # Save the data to a file
            with open('employees.json', 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"\nSuccessfully fetched {len(data.get('data', []))} employees")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print(f"Waiting {retry_delay} seconds before retry...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Failed to fetch data.")
                return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            return None

if __name__ == "__main__":
    fetch_employee_data()