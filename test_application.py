import pytest
import requests

BASE_URL = "http://pra5-env-1.eba-mxwmqe2x.us-east-2.elasticbeanstalk.com"


def lower_response(response):
    return response.lower()

def test_index():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.text == "Your Flask App Works! V1.0"


def test_predict_no_text():
    response = requests.post(f"{BASE_URL}/predict", json={})
    assert response.status_code == 400
    assert 'No text provided' in response.json().get('error', '')

def test_predict_fake_news_1():
    response = requests.post(f"{BASE_URL}/predict", json={'text': 'my cat can eat a dinansour'})
    assert response.status_code == 200
    data = response.json()
    assert 'prediction' in data
    assert lower_response(data['prediction']) == 'fake'

def test_predict_fake_news_2():
    response = requests.post(f"{BASE_URL}/predict", json={'text': 'garlic prevent cancers.'})
    assert response.status_code == 200
    data = response.json()
    assert 'prediction' in data
    assert lower_response(data['prediction']) == 'fake'

def test_predict_real_news_1():
    response = requests.post(f"{BASE_URL}/predict", json={'text': 'UofT is a University'})
    assert response.status_code == 200
    data = response.json()
    assert 'prediction' in data
    assert lower_response(data['prediction']) == 'real'

def test_predict_real_news_2():
    response = requests.post(f"{BASE_URL}/predict", json={'text': 'printer prints things'})
    assert response.status_code == 200
    data = response.json()
    assert 'prediction' in data
    assert lower_response(data['prediction']) == 'real'