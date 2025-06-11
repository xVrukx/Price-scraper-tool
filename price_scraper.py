import tkinter as tk
from tkinter import ttk, messagebox
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
from sqlalchemy import text, create_engine

# ------------------------------------------------------------------
# DATABASE CONFIGURATION
# ------------------------------------------------------------------
DB_URL = "mysql+pymysql://Yuvraj:yuvraj1234@localhost/Store"
ENGINE = create_engine(DB_URL, pool_size=5, max_overflow=0)

# ------------------------------------------------------------------
# SCRAPING HELPERS
# ------------------------------------------------------------------

def scrape_amazon(query: str) -> pd.DataFrame:
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
        }

        url = f"https://www.amazon.in/s?k={quote_plus(query)}"
        session = requests.Session()
        response = session.get(url, headers=headers)
        soup = BS(response.text, "html.parser")

        items = []
        cards = soup.select('div[data-component-type="s-search-result"]')
        for card in cards:
            title_tag = card.select_one("h2 span")
            price_tag = card.select_one("span.a-offscreen")
            if title_tag and price_tag:
                try:
                    price_cleaned = price_tag.get_text(strip=True).replace("₹", "").replace(",", "")
                    price_int = int(price_cleaned)
                    items.append({
                        "amazon_product": title_tag.get_text(strip=True),
                        "price": price_int
                    })
                except ValueError as v:
                    print(f"[Amazon Price Error]: {v}")

        return pd.DataFrame(items)
    except requests.exceptions.RequestException as e:
        print(f"[Amazon Connection Error]: {e}")
        return pd.DataFrame()

def scrape_flipkart(query: str) -> pd.DataFrame:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://www.flipkart.com/search?q={quote_plus(query)}"
        soup = BS(requests.get(url, headers=headers).text, "html.parser")

        items = []
        for card in soup.select("div.yKfJKb.row"):  # <- new card wrapper
            title = card.select_one("div.KzDlHZ")
            price = card.select_one("div.Nx9bqj._4b5DiR")

            if title and price:
                try:
                    name = title.get_text(strip=True)
                    price_cleaned = price.get_text(strip=True).replace("₹", "").replace(",", "")
                    price_int = int(price_cleaned)
                    items.append({
                        "flipkart_product": name,
                        "price": price_int
                    })
                except ValueError as v:
                    print(f"Flipkart Price Error: {v}")
        return pd.DataFrame(items)
    except requests.exceptions.RequestException as e:
        print(f"Flipkart Connection Error: {e}")
        return pd.DataFrame()

def scrape_shopsy(query: str) -> pd.DataFrame:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://www.shopsy.in/search?q={quote_plus(query)}"
        soup = BS(requests.get(url, headers=headers).text, "html.parser")

        items = []

        # Loop over each product card
        for card in soup.select("div.r-13awgt0.r-18u37iz.r-1w6e6rj.r-kzbkwu.r-ttdzmv"):
            title = card.select_one("div.sc-c50e187b-0.bkNEtl")
            price = card.select_one("div.css-146c3p1.r-cqee49.r-1vgyyaa.r-1rsjblm")

            if title and price:
                try:
                    name = title.get_text(strip=True)
                    price_cleaned = price.get_text(strip=True).replace("₹", "").replace(",", "")
                    price_int = int(price_cleaned)
                    items.append({
                        "shopshy_product": name,
                        "price": price_int
                    })
                except ValueError as v:
                    print(f"[Shopsy] Price error: {v}")
        return pd.DataFrame(items)

    except requests.exceptions.RequestException as e:
        print(f"[Shopsy] Connection error: {e}")
        return pd.DataFrame()

# ------------------------------------------------------------------
# STORAGE
# ------------------------------------------------------------------

def store_dataframe(table: str, df: pd.DataFrame, search_id: int) -> None:
    df = df.copy()
    df.insert(0, "search_id", search_id)
    df.to_sql(table, con=ENGINE, if_exists="append", index=False)

# ------------------------------------------------------------------
# MERGING
# ------------------------------------------------------------------

def merge_on_search_id(search_id: int) -> pd.DataFrame:
    ama = pd.read_sql(
        f"SELECT amazon_product AS ama_product, price AS price_amazon, search_id FROM amazon WHERE search_id={search_id}",
        ENGINE,
    )
    fli = pd.read_sql(
        f"SELECT flipkart_product AS fli_product, price AS price_flipkart, search_id FROM flipkart WHERE search_id={search_id}",
        ENGINE,
    )
    sho = pd.read_sql(
        f"SELECT shopshy_product AS sho_product, price AS price_shopshy, search_id FROM shopshy WHERE search_id={search_id}",
        ENGINE,
    )

    merged = pd.merge(pd.merge(ama, fli, on="search_id", how="outer"), sho, on="search_id", how="outer")
    return merged.fillna("N/A")

# ------------------------------------------------------------------
# GUI
# ------------------------------------------------------------------

class PriceComparerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Market Price Comparator")
        self.root.configure(bg="black")

        # --- Treeview Styling ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#333333", foreground="white", font=("Helvetica", 10, "bold"))
        style.configure("Treeview", background="black", foreground="white", rowheight=25, fieldbackground="black", font=("Helvetica", 10))
        style.map("Treeview", background=[("selected", "#444444")])

        tk.Label(self.root, text="Search term:", fg="white", bg="black").grid(row=0, column=0, padx=10, pady=20)
        self.entry = tk.Entry(self.root, width=40)
        self.entry.grid(row=0, column=1, padx=10, pady=20)

        tk.Button(self.root, text="Search & Store", command=self.handle_search, bg="grey", fg="white").grid(row=0, column=2, padx=10)
        self.root.mainloop()

    def store_search_metadata(self, search_id, keyword):
        query = text("INSERT INTO data_scraping_info (search_id, search_keyword) VALUES (:sid, :kw)")
        with ENGINE.begin() as conn:
            conn.execute(query, {"sid": search_id, "kw": keyword})

    def handle_search(self):
        query = self.entry.get().strip()
        if not query:
            return

        import datetime
        search_id = int(datetime.datetime.now().timestamp())
        self.store_search_metadata(search_id, query)

        amazon_df = scrape_amazon(query)
        flipkart_df = scrape_flipkart(query)
        shopsy_df = scrape_shopsy(query)

        store_dataframe("amazon", amazon_df, search_id)
        store_dataframe("flipkart", flipkart_df, search_id)
        store_dataframe("shopshy", shopsy_df, search_id)

        messagebox.showinfo("Done", "Data scraped and saved. Proceed to merge.")
        self.show_merge_window(search_id)

    def show_merge_window(self, search_id: int):
        merged_df = merge_on_search_id(search_id)

        top = tk.Toplevel(self.root)
        top.title("Merge Review")
        tree = ttk.Treeview(top)
        tree.pack(fill=tk.BOTH, expand=True)

        tree["columns"] = list(merged_df.columns)
        tree["show"] = "headings"
        for col in merged_df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        for _, row in merged_df.iterrows():
            tree.insert("", tk.END, values=list(row))

        btn_frame = tk.Frame(top)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Save Merge", bg="grey", fg="white", width=12,
                  command=lambda: self.save_merge(merged_df, top)).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Cancel", bg="grey", fg="white", width=12,
                  command=top.destroy).grid(row=0, column=1, padx=10)

    def save_merge(self, df: pd.DataFrame, window: tk.Toplevel):
        df.to_sql("merged_prices", con=ENGINE, if_exists="append", index=False)
        window.destroy()
        messagebox.showinfo("Saved", "Merged data committed to MySQL.")

if __name__ == "__main__":
    PriceComparerGUI()
