"""Business logic for LGBTQ+ sexual fluidity analysis."""
from __future__ import annotations

import pandas as pd
import statsmodels.api as sm
from dataclasses import dataclass, field
from datetime import datetime, timezone
from scipy.stats import levene, shapiro
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from typing import Any, Dict, List, Tuple


@dataclass(frozen=True)
class SectionDefinition:
    """Configuration for a single survey section."""

    key: str
    questions: Tuple[str, ...]
    max_score: int
    weight: float


@dataclass
class SectionScore:
    """Calculated output for a survey section."""

    raw_score: int
    max_score: int
    percentage: float
    weight: float


@dataclass
class AnalyzerResult:
    """Structured result returned by the analyzer."""

    timestamp: str
    overall_score: float
    interpretation: Dict[str, str]
    section_scores: Dict[str, SectionScore]
    insights: List[str]
    disclaimer: str
    references: List[str]


class LGBTQAnalyzer:
    """Encapsulates the scoring rules and interpretation logic."""

    def __init__(self) -> None:
        self.section_definitions: Dict[str, SectionDefinition] = {
            "media_exposure": SectionDefinition(
                key="media_exposure",
                questions=("media1", "media2"),
                max_score=8,  # 2 questions × 4 points each
                weight=0.20,
            ),
            "family_peer_support": SectionDefinition(
                key="family_peer_support",
                questions=("family1", "family2", "family3"),
                max_score=12,  # family1 (0-4) + family2 (0-4) + family3 (0-4)
                weight=0.25,
            ),
            "online_community": SectionDefinition(
                key="online_community",
                questions=("community1", "community2"),
                max_score=8,  # 2 questions × 4 points each
                weight=0.15,
            ),
            "cultural_linguistic": SectionDefinition(
                key="cultural_linguistic",
                questions=("culture1", "culture2"),
                max_score=8,  # 2 questions × 4 points each
                weight=0.15,
            ),
            "self_exploration": SectionDefinition(
                key="self_exploration",
                questions=("exploration1", "exploration2"),
                max_score=8,  # 2 questions × 4 points each
                weight=0.20,
            ),
            "school_environment": SectionDefinition(
                key="school_environment",
                questions=("school1",),
                max_score=4,  # 1 question × 4 points
                weight=0.05,
            ),
        }

        self._interpretation_ranges: Tuple[Tuple[int, int, str, str, str], ...] = (
            (0, 20, "minimal", "มีการเปิดรับและสำรวจน้อยมาก", "\U0001F319"),
            (21, 40, "low", "มีการเปิดรับและสำรวจในระดับต่ำ", "\U0001F331"),
            (41, 60, "moderate", "มีการเปิดรับและสำรวจในระดับปานกลาง", "\U0001F98B"),
            (61, 80, "high", "มีการเปิดรับและสำรวจในระดับสูง", "\U0001F308"),
            (81, 100, "very_high", "มีการเปิดรับและสำรวจในระดับสูงมาก", "\u2728"),
        )

    def analyze(self, answers: Dict[str, int]) -> AnalyzerResult:
        """Validate user input and build the result payload."""

        self._validate_input(answers)
        section_scores = self._calculate_section_scores(answers)
        overall_score = self._calculate_weighted_score(section_scores)
        interpretation = self._interpret_overall(overall_score)
        insights = self._generate_insights(section_scores, overall_score)

        return AnalyzerResult(
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_score=overall_score,
            interpretation=interpretation,
            section_scores=section_scores,
            insights=insights,
            disclaimer=self._disclaimer(),
            references=self._references(),
        )

    def _validate_input(self, answers: Dict[str, int]) -> None:
        required = {
            key
            for section in self.section_definitions.values()
            for key in section.questions
        }

        missing = required.difference(answers.keys())
        if missing:
            raise ValueError(f"Missing answers for: {', '.join(sorted(missing))}")

        for key, value in answers.items():
            if not isinstance(value, int):
                raise ValueError(f"Answer for {key} must be an integer")
            if value < 0 or value > 4:
                raise ValueError(f"Answer for {key} must be within 0-4. Received {value}")

    def _calculate_section_scores(self, answers: Dict[str, int]) -> Dict[str, SectionScore]:
        scores: Dict[str, SectionScore] = {}
        for section_key, definition in self.section_definitions.items():
            raw_score = sum(answers.get(question, 0) for question in definition.questions)
            percentage = round((raw_score / definition.max_score) * 100, 1)
            scores[section_key] = SectionScore(
                raw_score=raw_score,
                max_score=definition.max_score,
                percentage=percentage,
                weight=definition.weight,
            )
        return scores

    def _calculate_weighted_score(self, section_scores: Dict[str, SectionScore]) -> float:
        weighted_sum = sum(score.percentage * score.weight for score in section_scores.values())
        total_weight = sum(score.weight for score in section_scores.values())
        return round(weighted_sum / total_weight, 1) if total_weight else 0.0

    def _interpret_overall(self, overall_score: float) -> Dict[str, str]:
        for min_score, max_score, level, description, emoji in self._interpretation_ranges:
            if min_score <= overall_score <= max_score:
                return {
                    "level": level,
                    "description": description,
                    "emoji": emoji,
                    "range": f"{min_score}-{max_score}%",
                }
        return {
            "level": "unknown",
            "description": "Unable to interpret / ไม่สามารถแปลผลได้",
            "emoji": "\u2753",
            "range": "N/A",
        }

    def _generate_insights(self, section_scores: Dict[str, SectionScore], overall_score: float) -> List[str]:
        thai_labels = {
            "media_exposure": "การเปิดรับสื่อ",
            "family_peer_support": "การสนับสนุนจากครอบครัวและเพื่อน",
            "online_community": "การมีส่วนร่วมในชุมชนออนไลน์",
            "cultural_linguistic": "ความเข้าใจด้านวัฒนธรรมและภาษา",
            "self_exploration": "การสำรวจตัวตน",
            "school_environment": "สภาพแวดล้อมทางการศึกษา",
        }

        sorted_sections = sorted(section_scores.items(), key=lambda item: item[1].percentage, reverse=True)
        highest_key, highest_score = sorted_sections[0]
        lowest_key, lowest_score = sorted_sections[-1]

        insights: List[str] = []
        if highest_score.percentage >= 70:
            insights.append(
                f"\U0001F31F ปัจจัยที่โดดเด่นที่สุดคือ '{thai_labels[highest_key]}' ด้วยคะแนน {highest_score.percentage}%"
            )
        if lowest_score.percentage <= 30:
            insights.append(
                f"\U0001F4A1 ปัจจัยที่ควรให้ความสำคัญเพิ่มเติมคือ '{thai_labels[lowest_key]}' ด้วยคะแนน {lowest_score.percentage}%"
            )

        if overall_score >= 80:
            insights.append("\U0001F3F3\uFE0F\u200D\U0001F308 คุณเปิดกว้างและสำรวจความหลากหลายทางเพศในระดับสูง")
        elif overall_score >= 60:
            insights.append("\U0001F98B คุณกำลังอยู่ในช่วงสำรวจและเรียนรู้เกี่ยวกับตัวเอง ซึ่งเป็นเรื่องปกติและงดงาม")
        elif overall_score >= 40:
            insights.append("\U0001F331 คุณเริ่มต้นเปิดรับในบางด้าน การค้นหาตัวเองต้องใช้เวลา")
        else:
            insights.append("\U0001F319 คุณอาจยังไม่สนใจประเด็นนี้ในตอนนี้ และนั่นก็เป็นเรื่องที่ยอมรับได้")

        return insights

    @staticmethod
    def _disclaimer() -> str:
        return (
            "ผลลัพธ์นี้เป็นแนวโน้มเชิงสถิติจากการตอบแบบสอบถาม ไม่ใช่การวินิจฉัยทางการแพทย์ "
            "หรือการระบุตัวตนที่แท้จริง ไม่มีการจัดเก็บข้อมูลส่วนบุคคลใด ๆ และใช้เพื่อการศึกษาเท่านั้น"
        )

    @staticmethod
    def _references() -> List[str]:
        return [
            "Diamond, L. M. (2008). Sexual Fluidity: Understanding Women's Love and Desire. Harvard University Press.",
            "Bronfenbrenner, U. (1979). The Ecology of Human Development. Harvard University Press.",
            "Field, A. (2018). Discovering statistics using IBM SPSS statistics (5th ed.). Sage Publications.",
            "Kinsey, A. C., Pomeroy, W. B., & Martin, C. E. (1948). Sexual Behavior in the Human Male. W.B. Saunders.",
            "Add Health Study. University of North Carolina at Chapel Hill.",
            "Russell, S. T. & Fish, J. N. (2016). Mental Health in LGBT Youth. Annual Review of Clinical Psychology, 12, 465-487.",
        ]

    def analyze_two_way_anova(self, dataset: List[Dict[str, int]]) -> Dict[str, Any]:
        """
        Performs a Two-Way ANOVA analysis on a dataset of survey responses.
        """
        if len(dataset) < 10:
            return {
                "error": "Insufficient data",
                "message": f"You have {len(dataset)} survey submission(s). At least 10 submissions are required for statistical analysis.",
                "recommendation": "Complete the survey multiple times or wait for more responses to enable advanced analysis.",
                "current_count": len(dataset),
                "required_count": 10
            }

        df = self._prepare_anova_dataframe(dataset)

        # Fit the ANOVA model
        model = ols('fluidity_score ~ C(media_group) * C(social_group)', data=df).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)

        # Assumption Testing
        residuals = model.resid
        # Correctly prepare samples for Levene's test by grouping scores
        samples_for_levene = [
            group['fluidity_score'].values
            for name, group in df.groupby(['media_group', 'social_group'], observed=False)
        ]
        # Filter out empty groups which can cause errors in Levene's test
        samples_for_levene = [s for s in samples_for_levene if len(s) > 1]

        if len(samples_for_levene) > 1:
            levene_stat, levene_p = levene(*samples_for_levene)
            levene_test = {"statistic": levene_stat, "p_value": levene_p}
        else:
            # Cannot perform test with one or zero groups
            levene_test = {"statistic": float('nan'), "p_value": float('nan')}

        shapiro_test = shapiro(residuals)

        # Post-hoc Test (Tukey HSD)
        tukey_groups = df['media_group'].astype(str) + " & " + df['social_group'].astype(str)
        tukey_results = pairwise_tukeyhsd(endog=df['fluidity_score'], groups=tukey_groups, alpha=0.05)

        return {
            "anova_table": self._format_anova_table(anova_table),
            "assumption_tests": {
                "levene": levene_test,
                "shapiro": {"statistic": shapiro_test.statistic, "p_value": shapiro_test.pvalue},
            },
            "post_hoc_test": str(tukey_results),
            "sample_size_info": self._get_group_sample_sizes(df),
            "visualizations": self._prepare_visualizations(df),
        }

    def _prepare_anova_dataframe(self, dataset: List[Dict[str, int]]) -> pd.DataFrame:
        """Prepares a pandas DataFrame for ANOVA analysis."""
        df = pd.DataFrame(dataset)

        # Calculate factor scores
        df['media_score'] = df['media1'] + df['media2']
        df['social_score'] = df['family2'] + df['family3'] + df['school1']

        # Calculate overall fluidity score (dependent variable)
        df['fluidity_score'] = df.apply(lambda row: self._calculate_weighted_score(self._calculate_section_scores(row.to_dict())), axis=1)

        # Create factor groups
        df['media_group'] = pd.cut(df['media_score'], bins=[-1, 2, 4, 6], labels=['Low', 'Medium', 'High'])
        df['social_group'] = pd.cut(df['social_score'], bins=[-1, 2, 4, 6], labels=['Low', 'Medium', 'High'])

        return df

    def _format_anova_table(self, anova_table: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Formats the ANOVA table into a more JSON-friendly dictionary."""
        # Calculate eta-squared
        anova_table['eta_sq'] = anova_table[:-1]['sum_sq'] / sum(anova_table['sum_sq'])

        # Rename columns for clarity
        anova_table.rename(columns={'sum_sq': 'sum_of_squares', 'PR(>F)': 'p_value'}, inplace=True)

        return anova_table.to_dict('index')

    def _get_group_sample_sizes(self, df: pd.DataFrame) -> Dict[str, int]:
        """Gets the sample size for each group combination."""
        return df.groupby(['media_group', 'social_group'], observed=False).size().to_dict()

    def _prepare_visualizations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Prepares data for frontend visualizations."""
        interaction_plot_data = df.groupby(['media_group', 'social_group'], observed=False)['fluidity_score'].mean().unstack().to_dict('index')

        group_means_data = df.groupby('media_group', observed=False)['fluidity_score'].mean().to_dict()
        group_means_data.update(df.groupby('social_group', observed=False)['fluidity_score'].mean().to_dict())

        return {
            "interaction_plot": interaction_plot_data,
            "group_means": group_means_data
        }
