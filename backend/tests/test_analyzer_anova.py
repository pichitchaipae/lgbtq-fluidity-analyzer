import pandas as pd
import pytest
from app.services.analyzer import LGBTQAnalyzer

@pytest.fixture
def analyzer():
    return LGBTQAnalyzer()

@pytest.fixture
def simulated_dataset():
    """Fixture to load the simulated dataset."""
    try:
        # Corrected path for running pytest from the 'backend' directory
        return pd.read_csv("tests/data/simulated_dataset.csv").to_dict('records')
    except FileNotFoundError:
        pytest.fail("The simulated dataset file was not found. Please run the data simulation script first.")

def test_anova_with_simulated_data(analyzer, simulated_dataset):
    """Test the Two-Way ANOVA with a large, simulated dataset."""
    results = analyzer.analyze_two_way_anova(simulated_dataset)

    assert "anova_table" in results
    assert "assumption_tests" in results
    assert "post_hoc_test" in results
    assert "sample_size_info" in results
    assert "visualizations" in results

    # Check that the ANOVA table has the correct structure
    assert "C(media_group)" in results["anova_table"]
    assert "C(social_group)" in results["anova_table"]
    assert "C(media_group):C(social_group)" in results["anova_table"]

def test_anova_small_sample_size_warning(analyzer):
    """Test that a small sample size returns a specific warning."""
    small_dataset = [{"media1": 1, "media2": 1, "family2": 1, "family3": 1, "school1": 1}] * 10
    results = analyzer.analyze_two_way_anova(small_dataset)

    assert "error" in results
    assert results["error"] == "Small sample size"

def test_anova_dataframe_preparation(analyzer, simulated_dataset):
    """Test the internal DataFrame preparation logic."""
    df = analyzer._prepare_anova_dataframe(simulated_dataset[:20]) # Use a subset for speed

    assert 'media_score' in df.columns
    assert 'social_score' in df.columns
    assert 'fluidity_score' in df.columns
    assert 'media_group' in df.columns
    assert 'social_group' in df.columns

    # Check that the fluidity score is calculated
    assert df['fluidity_score'].mean() > 0

    # Check that groups are assigned
    assert not df['media_group'].isnull().any()
    assert not df['social_group'].isnull().any()