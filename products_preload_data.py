import csv
import random

def generate_supplier_id():
    return f"SUPL{random.randint(1, 50):03}"

def process_csv(input_file, output_file):
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = ['product_id', 'name', 'category', 'price', 'supplier_id']  # Updated field names
        
        with open(output_file, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                row['supplier_id'] = generate_supplier_id()  # Renamed 'Supplier ID' to 'supplier_id'
                new_row = {
                    'product_id': row['Uniq Id'],  # Changed 'Uniq Id' to 'product_id'
                    'name': row['Product Name'],  # Changed 'Product Name' to 'name'
                    'category': row['Category'],  # Changed 'Category' to 'category'
                    'price': row['Sale Price'],    # Changed 'Sale Price' to 'price'
                    'supplier_id': row['supplier_id']
                }
                writer.writerow(new_row)

if __name__ == "__main__":
    input_file = 'products_original.csv'
    output_file = 'products.csv' 
    process_csv(input_file, output_file)
    print("Completed")