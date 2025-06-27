# 🛍️ GUI Web Scraping Tool – Amazon, Flipkart & Shopsy (Python)

A GUI-based web scraping tool that extracts product names and prices from popular Indian e-commerce platforms like Amazon, Flipkart, and Shopsy. Built using Python with a rich tech stack including BeautifulSoup, SQLAlchemy, MySQL, and Pandas.

---

## 📌 Features

- 🖥️ Graphical User Interface (Tkinter)
- 🔍 Scrapes product name and price from:
  - ✅ Amazon.in
  - ✅ Flipkart.com
  - ✅ Shopsy.in
- 🧠 Simple input form – just enter the product name
- 📦 Saves data to a MySQL database using SQLAlchemy ORM
- 📊 Exports results to CSV (optional it asks if user wants to save the data scraped or otherwise the user can click exit button)using Pandas
- 🔄 Clean modular design with error handling

---

## 🧰 Tech Stack

| Tech/Libraries       | Purpose                          |
|----------------------|----------------------------------|
| `Tkinter`            | GUI frontend                     |
| `requests`           | Fetching HTML content            |
| `BeautifulSoup`      | HTML parsing and data extraction |
| `SQLAlchemy`         | ORM for MySQL database           |
| `MySQL`              | Persistent storage               |
| `pandas`             | CSV export                       |

---

## 📦 Installation

### 1. Clone the repository
git clone https://github.com/vrukcodes/gprice-scraper-tool
cd price-scraper-tool

###2. Install dependencies
pip install requests beautifulsoup4 sqlalchemy pymysql pandas

###3. Setup MySQL
Create a database in MySQL:
CREATE DATABASE product_scraper;
Update db_config.py or .env:
---
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "your_password"
DB_NAME = "product_scraper"

4. Run the Application
python app.py

📸 GUI Overview

![1750535944715](https://github.com/user-attachments/assets/c9988539-7283-4816-9e4c-63d26230d0cb)
![1750535832620](https://github.com/user-attachments/assets/4c84751f-359e-4644-b90b-f94a22b19043)


🧠 How to Use
Launch the GUI

Write a product name 

Click “Search”

View product name and price in the UI

Optionally export data to .csv

🗃️ Database Schema (via SQLAlchemy)
products table:

id (Primary Key)

site (Amazon/Flipkart/Shopsy)

product_name

price

scraped_at (timestamp)

📂 Project Structure

📁 gui-scraper-tool/
│
├── tests
├── .gitignore
├── LICENSE
├── README.md
├── conftest.py
├── price_scraper.py
├── pytest.ini
├── version.txt 
└── scraper.ico

🚀 Future Improvements
 Multi-product batch scraping

 Proxy support for anti-bot handling

 Real-time price monitoring with email alerts

 SQLite fallback for offline use

 Theme customization for GUI

⚠️ Legal Note
This tool is intended for educational and research purposes only, the sites changes there elements after sometime so it might not work as efficiently as it works now.
Do not use it for bulk scraping or commercial use without complying with the target site's robots.txt and Terms of Service.

👨‍💻 Author
Vruk (vrukcodes)
Student | Python Developer | Automation Enthusiast
GitHub: github.com/xVrukx

👩Guide
KI my sensei guided me and helped me throught this project

📄 License
MIT License – use freely, modify as needed, give credit if shared.
