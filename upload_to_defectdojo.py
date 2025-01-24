import os
import requests

# DefectDojo settings
DEFECTDOJO_URL = os.getenv("DEFECTDOJO_URL")  # Fetch from environment variables
API_KEY = os.getenv("DEFECTDOJO_API_KEY")  # Fetch from environment variables
print(f"API_KEY: {API_KEY}")  # Debugging output
PRODUCT_NAME = "Automated Product"  # Name of the product to use or create
PRODUCT_TYPE_NAME = "Automated Product Type"  # Name of the product type to use or create
ENGAGEMENT_NAME = "Automated Engagement"
SCAN_TYPE = "Anchore Grype"  # Scan type matching the tool used
SCAN_FILE_PATH = os.getenv("SCAN_FILE_PATH")

# Headers
HEADERS = {
    "Authorization": f"Token {API_KEY}",
}


try:
    with open(SCAN_FILE_PATH, "r") as file:
        file_contents = file.read()
        print(f"Contents of the scan file:\n{file_contents}")
except Exception as e:
    print(f"Error reading file {SCAN_FILE_PATH}: {e}")




def get_or_create_product_type():
    """
    Ensures a product type exists and returns its ID.
    """
    # Check for existing product type
    response = requests.get(f"{DEFECTDOJO_URL}/api/v2/product_types/", headers=HEADERS)
    if response.status_code == 200:
        product_types = response.json()["results"]
        for product_type in product_types:
            if product_type["name"] == PRODUCT_TYPE_NAME:
                print(f"Found product type: {PRODUCT_TYPE_NAME} with ID {product_type['id']}")
                return product_type["id"]

    # Create product type if not found
    print(f"Product type {PRODUCT_TYPE_NAME} not found. Creating it.")
    url = f"{DEFECTDOJO_URL}/api/v2/product_types/"
    data = {"name": PRODUCT_TYPE_NAME, "description": "Created for automated scans"}
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 201:
        product_type_id = response.json()["id"]
        print(f"Product type created with ID: {product_type_id}")
        return product_type_id
    else:
        print("Failed to create product type.")
        print(response.json())
        return None

def get_or_create_product():
    """
    Ensures a product exists, creating it if necessary, and returns its ID.
    """
    # Get or create the product type
    product_type_id = get_or_create_product_type()
    if not product_type_id:
        return None

    # Check for existing product
    response = requests.get(f"{DEFECTDOJO_URL}/api/v2/products/", headers=HEADERS)
    if response.status_code == 200:
        products = response.json()["results"]
        for product in products:
            if product["name"] == PRODUCT_NAME:
                print(f"Found product: {PRODUCT_NAME} with ID {product['id']}")
                return product["id"]

    # Create product if not found
    print(f"Product {PRODUCT_NAME} not found. Creating it.")
    url = f"{DEFECTDOJO_URL}/api/v2/products/"
    data = {
        "name": PRODUCT_NAME,
        "description": "Created for automated scans",
        "prod_type": product_type_id,  # Include the required product type ID
    }
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 201:
        product_id = response.json()["id"]
        print(f"Product created with ID: {product_id}")
        return product_id
    else:
        print("Failed to create product.")
        print(response.json())
        return None

def create_engagement(product_id):
    """
    Creates an engagement in DefectDojo and returns its ID.
    """
    url = f"{DEFECTDOJO_URL}/api/v2/engagements/"
    data = {
        "name": ENGAGEMENT_NAME,
        "product": product_id,
        "target_start": "2024-01-01",
        "target_end": "2024-12-31",
        "status": "In Progress",
        "engagement_type": "CI/CD",
    }

    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 201:
        engagement_id = response.json()["id"]
        print(f"Engagement created with ID: {engagement_id}")
        return engagement_id
    else:
        print("Failed to create engagement.")
        print(response.json())
        return None

def upload_scan(engagement_id):
    """
    Uploads the scan result to DefectDojo.
    """
    url = f"{DEFECTDOJO_URL}/api/v2/import-scan/"
    with open(SCAN_FILE_PATH, "rb") as scan_file:
        files = {"file": scan_file}
        data = {
            "engagement": engagement_id,
            "scan_type": SCAN_TYPE,
            "active": True,
            "verified": True,
        }
        response = requests.post(url, headers=HEADERS, files=files, data=data)
        if response.status_code == 201:
            print("Scan successfully uploaded to DefectDojo.")
        else:
            print("Failed to upload scan.")
            print(response.json())

# Main workflow
def main():
    product_id = get_or_create_product()
    if product_id:
        engagement_id = create_engagement(product_id)
        if engagement_id:
            upload_scan(engagement_id)

if __name__ == "__main__":
    main()
