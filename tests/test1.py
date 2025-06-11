# test1.py  ---------------------------------------------------------
import types
import pandas as pd
import requests
import price_scraper as app   # ← imports your single‑file script
                          #    (rename if your file is named differently)

# ------------------------------------------------------------------
# Helper: fake HTTP  ------------------------------------------------
class _FakeResponse:
    def __init__(self, html):
        self.text = html
        self.status_code = 200

_FAKE_AMAZON_HTML = """
<div data-component-type="s-search-result">
    <h2><span>Dummy Phone 128GB</span></h2>
    <span class="a-offscreen">₹12,345</span>
</div>
"""

def _fake_get(*_args, **_kw):
    return _FakeResponse(_FAKE_AMAZON_HTML)

def test_keyword_format(test1_keyword,test2_keyword):
    assert isinstance(test1_keyword,test2_keyword, str)
    assert isinstance(test1_keyword,test2_keyword, str)

# ------------------------------------------------------------------
# Tests  ------------------------------------------------------------
def test_scrape_amazon_single_item(monkeypatch):
    """
    The scraper should return exactly one row with
    columns: amazon_product, price
    """
    # Patch requests.Session.get to avoid hitting amazon.in
    monkeypatch.setattr(requests.Session, "get", _fake_get)

    df = app.scrape_amazon("dummy phone")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["amazon_product"] == "Dummy Phone 128GB"
    assert df.iloc[0]["price"] == 12345


def test_merge_on_search_id(monkeypatch):
    """
    merge_on_search_id() returns a DataFrame even when
    the underlying SELECTs return empty frames.
    We monkey‑patch read_sql so it always returns empty.
    """
def _empty_sql(*_a, **_k):
    # empty frame **with** expected column
    return pd.DataFrame(columns=["search_id"])

    df = app.merge_on_search_id(111222)
    # Should be empty but still a DataFrame
    assert isinstance(df, pd.DataFrame)
