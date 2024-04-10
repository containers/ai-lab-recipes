def test_title(model_endpoint,selenium):
    selenium.get(f"http://{model_endpoint}:8501")
    assert selenium.title == "Streamlit"
