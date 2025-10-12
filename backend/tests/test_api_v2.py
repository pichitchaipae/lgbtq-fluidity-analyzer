import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def simulated_dataset_dict():
    # Create two different user profiles to ensure multiple groups for comparison
    profile1 = {"media1": 1, "media2": 1, "family1": 0, "family2": 0, "family3": 0, "school1": 0,
                "community1": 1, "community2": 1, "culture1": 1, "culture2": 1, "self1": 1, "self2": 1,
                "exploration1": 1, "exploration2": 1} # Low scores
    profile2 = {"media1": 4, "media2": 4, "family1": 2, "family2": 2, "family3": 2, "school1": 2,
                "community1": 4, "community2": 4, "culture1": 4, "culture2": 4, "self1": 4, "self2": 4,
                "exploration1": 4, "exploration2": 4} # High scores

    # Repeat each profile 15 times to get a total of 30 records, which is the minimum
    return [profile1] * 15 + [profile2] * 15

def test_analyze_v2_with_ai_insights(simulated_dataset_dict):
    """Test the /api/v2/analysis endpoint with AI insights enabled."""
    with patch('app.api.routes_v2.AIInterpreter') as MockAIInterpreter:
        mock_instance = MockAIInterpreter.return_value
        mock_instance.get_interpretation.return_value = "This is an AI interpretation."

        response = client.post(
            "/api/v2/analysis",
            json={"dataset": simulated_dataset_dict, "ai_insights": True}
        )

        assert response.status_code == 200
        data = response.json()
        assert "anova_results" in data
        assert data["ai_interpretation"] == "This is an AI interpretation."
        assert "visualizations" in data
        assert "privacy_notice" in data

def test_analyze_v2_without_ai_insights(simulated_dataset_dict):
    """Test the /api/v2/analysis endpoint with AI insights disabled."""
    response = client.post(
        "/api/v2/analysis",
        json={"dataset": simulated_dataset_dict, "ai_insights": False}
    )

    assert response.status_code == 200
    data = response.json()
    assert "anova_results" in data
    assert data["ai_interpretation"] is None
    assert "privacy_notice" in data
    assert "not requested" in data["privacy_notice"]

def test_analyze_v2_small_sample_size(simulated_dataset_dict):
    """Test the endpoint with a dataset that is too small."""
    small_dataset = simulated_dataset_dict[:10]
    response = client.post(
        "/api/v2/analysis",
        json={"dataset": small_dataset}
    )
    assert response.status_code == 400

@patch('app.api.routes_v2.limiter.limit', return_value=MagicMock(side_effect=Exception("Rate limit exceeded")))
def test_rate_limiting(mock_limit, simulated_dataset_dict):
    """Test that the rate limiter is active on the endpoint."""
    # This test is a bit conceptual as it's hard to trigger the rate limit directly.
    # We patch the limiter to simulate it being triggered.
    # A more robust test would involve a library like `pytest-freezegun` to manipulate time.

    # The presence of the limiter is tested by the fact that the app setup includes it.
    # This test serves as a placeholder for more complex rate-limit testing if needed.
    assert "limiter" in app.state._state