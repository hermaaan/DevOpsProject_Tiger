import os
import pytest
from app import app

# Ställ in en testkonfiguration för Flask
@pytest.fixture
def client():
    # Flask-testklient används för att simulera HTTP-anrop
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_missing_api_key(client, monkeypatch):
    """Testar att '/'-endpointen returnerar rätt meddelande när API-nyckeln saknas."""
    # Simulera att API_KEY saknas i miljövariabler
    monkeypatch.delenv("API_KEY", raising=False)

    response = client.get('/')
    assert response.status_code == 200
    assert b"API key is missing or incorrect in .env file" in response.data

def test_home_invalid_api_key(client, monkeypatch):
    """Testar '/'-endpointen med en felaktig API-nyckel för att se om rätt felmeddelande returneras."""
    # Simulera en felaktig API-nyckel
    monkeypatch.setenv("API_KEY", "invalid_key")

    response = client.get('/')
    assert response.status_code != 200  # Förväntar oss att statuskoden inte är 200
    assert b"Error:" in response.data