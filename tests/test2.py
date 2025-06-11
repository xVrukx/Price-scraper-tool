# test2.py  ---------------------------------------------------------
import pandas as pd
import sqlalchemy as sa
import price_scraper as app

# ------------------------------------------------------------------
# Build a fresh in‑memory SQLite engine for each test  --------------
def _sqlite_engine():
    return sa.create_engine("sqlite:///:memory:")

# ------------------------------------------------------------------
def test_store_dataframe_inserts_correctly(monkeypatch):
    """
    Verify store_dataframe() adds the search_id column and
    really writes to the given engine.
    """
    engine = _sqlite_engine()

    # Monkey‑patch the global ENGINE *inside price_app*
    monkeypatch.setattr(app, "ENGINE", engine, raising=True)

    # Build dummy table schema (SQLite creates on first insert, so optional)
    search_id = 999
    df = pd.DataFrame({"amazon_product": ["Foo"], "price": [111]})

    app.store_dataframe("amazon", df, search_id)

    # Read back and assert
    out = pd.read_sql("SELECT * FROM amazon", engine)
    assert len(out) == 1
    assert out.loc[0, "search_id"] == search_id
    assert out.loc[0, "price"] == 111
