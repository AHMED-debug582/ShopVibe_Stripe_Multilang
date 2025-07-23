from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# الاتصال بقاعدة البيانات من .env
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(mongo_uri)
db = client["shopvibe"]
products = db["products"]

# بيانات تجريبية
sample_products = [
    {
        "name": "سماعات بلوتوث",
        "description": "سماعات لاسلكية بجودة صوت عالية وعزل ضوضاء.",
        "price": 299,
        "image": "https://via.placeholder.com/300x200?text=Bluetooth+Headphones",
        "category": "إلكترونيات",
        "rating": 4.5,
        "stock": 15
    },
    {
        "name": "ساعة ذكية",
        "description": "ساعة متعددة الوظائف تراقب نشاطك وصحتك.",
        "price": 450,
        "image": "https://via.placeholder.com/300x200?text=Smart+Watch",
        "category": "إكسسوارات",
        "rating": 4.2,
        "stock": 20
    },
    {
        "name": "لوحة مفاتيح ميكانيكية",
        "description": "لوحة مفاتيح بإضاءة RGB مثالية للألعاب والبرمجة.",
        "price": 399,
        "image": "https://via.placeholder.com/300x200?text=Mechanical+Keyboard",
        "category": "كمبيوتر",
        "rating": 4.8,
        "stock": 10
    }
]

# حذف القديم وإضافة الجديد
products.delete_many({})
products.insert_many(sample_products)

print("✅ تم إدخال المنتجات التجريبية بنجاح.")
