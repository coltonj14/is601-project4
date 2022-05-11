"""Test the csv upload"""

def test_csv(application, client):
    res = client.get("/transactions/upload")
    print(res.data)
    assert res.status_code == 302
    upload_res = client.post("/transactions/upload", data="/tests/csvs/transactions.csv", follow_redirects=True)
    assert upload_res.status_code == 200