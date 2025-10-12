"""Quick test to verify percentage calculations are fixed"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.analyzer import LGBTQAnalyzer

# Test data - all questions answered with max value (4)
test_answers = {
    "media1": 4,
    "media2": 4,
    "family1": 4,
    "family2": 4,
    "family3": 4,
    "community1": 4,
    "community2": 4,
    "culture1": 4,
    "culture2": 4,
    "exploration1": 4,
    "exploration2": 4,
    "school1": 4,
}

analyzer = LGBTQAnalyzer()
result = analyzer.analyze(test_answers)

print("\n" + "="*60)
print("📊 PERCENTAGE CALCULATION TEST")
print("="*60)
print("\nTest: All questions answered with maximum value (4)")
print("\n✅ Expected: All sections should show 100%")
print("❌ Before fix: Some showed >100% (e.g., 200%, 133%)\n")

print("Section Scores:")
print("-"*60)
for section_key, score in result.section_scores.items():
    status = "✅" if score.percentage == 100.0 else "❌"
    print(f"{status} {section_key:25} {score.raw_score:2}/{score.max_score:2} = {score.percentage:5.1f}%")

print("-"*60)
print(f"\n📈 Overall Score: {result.overall_score}%")
print(f"📊 Interpretation: {result.interpretation['level']}")
print(f"🎯 Description: {result.interpretation['description']}")

# Verify all are 100%
all_correct = all(score.percentage == 100.0 for score in result.section_scores.values())
if all_correct:
    print("\n🎉 SUCCESS! All percentages are now correct!")
else:
    print("\n❌ FAILED! Some percentages are still wrong")
    sys.exit(1)
