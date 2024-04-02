import csv
import random

def stores_data():
    locations = ['Hyderabad,TG', 'Vizag,AP', 'Banglore,KN', 'Kochi,KL', 'Chennai,TN', 'Delhi,DL', 'Mumbai,MH', 'Kolkata,WB', 'Ahmedabad,GJ', 'Lucknow,UP']
    managers = ['Krishnasairaj', 'Lasya Priya', 'Guna Varshith', 'JayaSree', 'Susritha', 'Raghvani', 'Justin', 'Niteesh', 'Shazin', 'Lalit']
    
    with open('stores.csv', 'w', newline='') as csvfile:
        fieldnames = ['store_id', 'location', 'size', 'manager']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, 11):
            store_id = "W00" + str(i)
            location = random.choice(locations)
            size = random.randrange(500, 1400)
            manager = random.choice(managers)
            locations.remove(location)
            managers.remove(manager)

            writer.writerow({'store_id': store_id, 'location': location, 'size': size, 'manager': manager})

if __name__ == "__main__":
    stores_data()
    print("Data written to stores.csv file")