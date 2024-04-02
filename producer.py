import csv
import json
import random
import time
from google.cloud import pubsub_v1
from datetime import datetime, timedelta

publisher = pubsub_v1.PublisherClient()

project_id = "walmartsalesanalysis"
sales_topic_name = "Salesrecord"
inventory_topic_name = "Inventorydata"
sales_topic_path = publisher.topic_path(project_id, sales_topic_name)
inventory_topic_path = publisher.topic_path(project_id, inventory_topic_name)

# Load product_ids and store_ids from CSV files
def load_ids_from_csv(file_path, id_key):
    ids = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ids.append(row[id_key])
    return ids

product_ids = load_ids_from_csv('products.csv', 'product_id')
store_ids = load_ids_from_csv('stores.csv', 'store_id')

def sales_transaction():
    transaction_id = "T" + str(random.randint(1, 10000))
    product_id = random.choice(product_ids)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    quantity = random.randint(1, 24)
    unit_price = random.randint(200, 100000)
    store_id = random.choice(store_ids)
    
    return {
        "transaction_id": transaction_id,
        "product_id": product_id,
        "timestamp": timestamp,
        "quantity": quantity,
        "unit_price": unit_price,
        "store_id": store_id
    }

def inventory_updates(product_id, quantity, store_id):
    timestamp = (datetime.now() - timedelta(days=(random.randint(7, 20)))).strftime('%Y-%m-%d %H:%M:%S')
    quantity_change = -quantity
    
    return {
        "product_id": product_id,
        "timestamp": timestamp,
        "quantity_change": quantity_change,
        "store_id": store_id
    }

def callback(future):#Future is an asynchronous operation
    try:
        message_id = future.result()
        # print(f"Published message with ID: {message_id}\n")
    except Exception as e:
        print(f"Error publishing message: {e}\n")

temp = 0
while True:
    if temp == 500:
        break
    try:
        temp += 1
        sales_data = sales_transaction()
        product_id = sales_data['product_id']
        quantity = sales_data['quantity']
        store_id = sales_data['store_id']
        inventory_data = inventory_updates(product_id, quantity, store_id)
        json_sales_data = json.dumps(sales_data).encode('utf-8')
        json_inventory_data = json.dumps(inventory_data).encode('utf-8')
        sales_publish = publisher.publish(sales_topic_path, data=json_sales_data)
        sales_publish.add_done_callback(callback)
        sales_publish.result()
        print(f"Sales Data: {sales_data}\n")
        inventory_publish = publisher.publish(inventory_topic_path, data=json_inventory_data)
        inventory_publish.add_done_callback(callback)#It calls the callback function when object is added to topic
        inventory_publish.result()#It holds the block of code execution until the result of asynchornous operation is returned
        print(f"Inventory Update Data: {inventory_data}\n")
        time.sleep(5)
    except Exception as e:
        print(f"Error occurred: {e}")
        