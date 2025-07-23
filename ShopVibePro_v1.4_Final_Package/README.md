
# 🛍️ ShopVibe Pro

ShopVibe Pro هو مشروع متجر إلكتروني احترافي مبني باستخدام Flask وMongoDB مع دعم كامل للغات متعددة (i18n) ونظام تقييم، Stripe للدفع الإلكتروني، وخدمات احترافية لعرض المنتجات.

## ✨ الميزات الرئيسية

- 🎨 تصميم احترافي متعدد الصفحات
- 🗃️ دعم MongoDB الكامل لتخزين المنتجات والطلبات والمستخدمين
- 🌐 دعم الترجمة الدولية عبر ملفات JSON
- 💳 دعم الدفع عبر Stripe (شراء حقيقي)
- 🛒 نظام سلة متكامل: إضافة - تعديل - حذف - الدفع
- 🧾 إصدار فواتير PDF وتصدير الطلبات
- ⭐ صفحة تفاصيل المنتج مع التقييمات
- 🔐 تسجيل دخول وتسجيل مستخدمين + reCAPTCHA
- 📈 صفحة إحصائيات وحسابات لوحة التحكم
- 👤 صفحة "حسابي" لعرض الطلبات
- 📂 زر تصدير Excel - PDF
- ⚙️ لوحة تحكم Admin لإدارة المنتجات والمبيعات
- 🛍️ نظام كوبونات وخصومات
- 🌍 دعم تعدد العملات حسب الدولة

## 🧪 المتطلبات

- Python 3.10+
- MongoDB Atlas
- حساب Stripe
- مكتبات: Flask, pymongo, stripe, python-dotenv, pandas, openpyxl

## 🚀 تشغيل المشروع

```bash
pip install -r requirements.txt
python seed_real_products.py  # لتعبئة المنتجات تلقائيًا
python app.py
```

## 🔑 إعداد ملف `.env`

```env
FLASK_ENV=development
SECRET_KEY=سر_خاص_بك
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/shopvibe?retryWrites=true&w=majority
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,ar,fr,de,es
```

## 📁 هيكل المشروع

```
ShopVibePro_Final_Updated/
│
├── app.py                     # الملف الرئيسي لتشغيل التطبيق
├── init.py / __init__.py     # إعداد Flask وMongoDB
├── routes/                   # مسارات Flask
├── Templates/                # ملفات HTML (products, detail, cart...)
├── Items/                    # صور المنتجات
├── seed_real_products.py     # سكريبت ملء قاعدة البيانات بمنتجات
├── .env                      # إعدادات البيئة
└── README.md                 # هذا الملف
```

## 📦 بيانات دخول التجريبية

- **Admin Panel:** `/admin`
- **User Login:** تسجيل عبر `/register` أو تسجيل دخول من `/login`

## 📸 الصور والملفات

يتم تحميل صور المنتجات من مجلد `Items/` وتخزين روابطها مباشرة في MongoDB.

## 📄 التراخيص

هذا المشروع مخصص للبيع التجاري ومهيأ للنشر على Flippa وCodeCanyon.
