"""Unit tests for the LGBTQAnalyzer service."""
from __future__ import annotations

import pytest

from app.services.analyzer import LGBTQAnalyzer


@pytest.fixture()
def analyzer() -> LGBTQAnalyzer:
    return LGBTQAnalyzer()


def test_analyze_returns_expected_structure(analyzer: LGBTQAnalyzer) -> None:
    payload = {
        "media1": 3,
        "media2": 2,
        "family1": 1,
        "family2": 2,
        "family3": 2,
        "community1": 2,
        "community2": 2,
        "culture1": 2,
        "culture2": 2,
        "exploration1": 2,
        "exploration2": 2,
        "school1": 1,
    }

    result = analyzer.analyze(payload)

    assert result.overall_score > 0
    assert "description" in result.interpretation
    assert len(result.section_scores) == len(analyzer.section_definitions)
    assert result.references


def test_analyze_rejects_invalid_values(analyzer: LGBTQAnalyzer) -> None:
    invalid_payload = {key: 0 for key in analyzer.section_definitions["media_exposure"].questions}
    invalid_payload.update({"media1": 5})

    with pytest.raises(ValueError):
        analyzer.analyze(invalid_payload)


def test_analyze_requires_all_answers(analyzer: LGBTQAnalyzer) -> None:
    partial_payload = {"media1": 1, "media2": 1}

    with pytest.raises(ValueError):
        analyzer.analyze(partial_payload)
