import requests
import json
import time
import os
from tqdm import tqdm  # For progress bars
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.environ.get('APP_ID')
APP_KEY = os.environ.get('APP_KEY')
BASE_URL = "https://api.s24.com/v3/"
TYPE = "products"


def fetch_page(page_number, page_size=40):
    """Fetch a single page of products from the API"""
    url = f"{BASE_URL}{APP_ID}/{TYPE}"

    # Basic auth using APP_ID and APP_KEY https://developer.s24.com/api/
    auth = (APP_ID, APP_KEY)

    # Set headers for the request
    # Available headers: xml (default), json, javascript
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    params = {
        'page': page_number,
        'size': page_size
    }

    response = requests.get(url, auth=auth, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def save_products(products, output_file):
    """Append products to the output file"""
    with open(output_file, 'a') as f:
        for product in products:
            # Write each product as a separate JSON line (JSONL format)
            f.write(json.dumps(product) + '\n')


def fetch_all_products(output_file="data/products.jsonl", page_size=40):
    """Fetch all products and save them to a file"""
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Clear the output file if it exists
    open(output_file, 'w').close()

    # Track the last page we successfully processed
    progress_file = output_file + ".progress"
    start_page = 1

    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            try:
                start_page = int(f.read().strip()) + 1
            except:
                start_page = 1

    # First, fetch the initial page to get total count
    try:
        initial_data = fetch_page(1, page_size)

        # Extract total count from response
        total_products = initial_data.get('totalResults', 0)
        page_size_actual = initial_data.get('pageElements', page_size)

        if total_products == 0:
            print("No products found or couldn't determine total count")
            return

        total_pages = (total_products + page_size_actual -
                       1) // page_size_actual

        print(f"Found {total_products} products across {total_pages} pages")

        # Save the first page results since we already fetched them
        products = initial_data.get('products', [])
        save_products(products, output_file)

        # Start from page 2 if we're just beginning (page 1 is already processed above)
        # If we have a progress file, we start from the next page
        if start_page == 1:
            start_page = 2
            with open(progress_file, 'w') as f:
                f.write("1")  # Processed page 1

        print(f"Starting from page {start_page} of {total_pages}")

        # Create progress bar
        with tqdm(total=total_pages, initial=start_page-1) as pbar:
            for page in range(start_page, total_pages + 1):
                try:
                    data = fetch_page(page, page_size)
                    products = data.get('products', [])

                    # Check if end of products is reached
                    if not products:
                        print(
                            f"No more products found at page {page}, stopping")
                        break

                    save_products(products, output_file)

                    # Update the progress file
                    with open(progress_file, 'w') as f:
                        f.write(str(page))

                    # Update progress bar
                    pbar.update(1)

                    time.sleep(0.1)

                except Exception as e:
                    print(f"Error on page {page}: {e}")
                    print("Retrying in 5 seconds...")
                    time.sleep(5)

                    # Retry the current page
                    try:
                        data = fetch_page(page, page_size)
                        products = data.get('products', [])
                        save_products(products, output_file)

                        with open(progress_file, 'w') as f:
                            f.write(str(page))

                        pbar.update(1)
                    except Exception as retry_e:
                        print(f"Retry also failed: {retry_e}")
                        print("Continuing to next page...")

    except Exception as e:
        print(f"Initial fetch failed: {e}")
        print(f"Error details: {e}")

    finally:
        print(f"Completed fetching products. Check {output_file} for results.")


if __name__ == "__main__":
    fetch_all_products()
