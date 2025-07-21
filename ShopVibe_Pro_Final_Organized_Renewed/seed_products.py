
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["shopvibepro"]
products = db["products"]

sample_data = [
{'name': 'Wireless Headphones', 'price': 89.99, 'image': 'headphones.jpg', 'description': 'High-quality wireless headphones.'},
{'name': 'Smart Watch', 'price': 149.99, 'image': 'watch.jpg', 'description': 'Track your fitness and notifications.'},
{'name': 'Gaming Mouse', 'price': 59.99, 'image': 'mouse.jpg', 'description': 'Ergonomic mouse with RGB lighting.'},
{'name': 'Bluetooth Speaker', 'price': 39.99, 'image': 'speaker.jpg', 'description': 'Portable speaker with deep bass.'},
{'name': '4K Monitor', 'price': 299.99, 'image': 'monitor.jpg', 'description': 'Ultra HD 27-inch monitor.'},
{'name': 'USB-C Hub', 'price': 29.99, 'image': 'hub.jpg', 'description': 'Multi-port USB-C hub for laptops.'}
]

products.insert_many(sample_data)
print("Sample products inserted successfully.")
