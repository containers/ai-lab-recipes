def test_title(url,selenium):
    selenium.get(f"http://{url}:8501")
    assert selenium.title == "Streamlit"
