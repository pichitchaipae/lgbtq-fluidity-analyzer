import { jStat } from 'jstat';
import type { AnalysisRequest, AnalysisV2Response } from '../types';

// Helper to calculate the overall score for a single survey response
const calculateOverallScore = (answers: AnalysisRequest): number => {
    // This is a simplified version of the backend's weighted scoring
    const sections = {
        media_exposure: (answers.media1 + answers.media2) / 6 * 0.20,
        family_peer_support: (answers.family1 + answers.family2 + answers.family3) / 6 * 0.25,
        online_community: (answers.community1 + answers.community2) / 4 * 0.15,
        cultural_linguistic: (answers.culture1 + answers.culture2) / 5 * 0.15,
        self_exploration: (answers.exploration1 + answers.exploration2) / 4 * 0.20,
        school_environment: answers.school1 / 2 * 0.05,
    };
    const totalScore = Object.values(sections).reduce((sum, score) => sum + score, 0);
    const totalWeight = 0.20 + 0.25 + 0.15 + 0.15 + 0.20 + 0.05;
    return (totalScore / totalWeight) * 100;
};


export const calculateLocalTwoWayAnova = (dataset: AnalysisRequest[]): AnalysisV2Response => {
    const data = dataset.map(answers => {
        const media_score = answers.media1 + answers.media2;
        const social_score = answers.family2 + answers.family3 + answers.school1;
        const fluidity_score = calculateOverallScore(answers);

        let media_group: 'Low' | 'Medium' | 'High' = 'Low';
        if (media_score > 4) media_group = 'High';
        else if (media_score > 2) media_group = 'Medium';

        let social_group: 'Low' | 'Medium' | 'High' = 'Low';
        if (social_score > 4) social_group = 'High';
        else if (social_score > 2) social_group = 'Medium';

        return { media_group, social_group, fluidity_score };
    });

    const groups = {};
    data.forEach(d => {
        const key = `${d.media_group}-${d.social_group}`;
        if (!groups[key]) groups[key] = [];
        groups[key].push(d.fluidity_score);
    });

    // Prepare visualization data
    const interaction_plot = {};
    Object.keys(groups).forEach(key => {
        const [media, social] = key.split('-');
        if (!interaction_plot[media]) interaction_plot[media] = {};
        interaction_plot[media][social] = jStat.mean(groups[key]);
    });

    return {
        anova_results: {
            "Info": {
                "sum_of_squares": 0, "df": 0, "F": 0, "p_value": 0,
                "note": "Local calculation does not perform a full ANOVA. Use AI Insights for detailed statistics."
            }
        },
        ai_interpretation: "Local analysis provides a visual overview of how different factors interact. For a full statistical breakdown (including p-values and effect sizes), please use the 'Get AI Insights' option.",
        visualizations: {
            interaction_plot,
            group_means: {}, // Simplified; not calculating separate group means
        },
        privacy_notice: "Analysis performed entirely in your browser. No data was sent to any server.",
    };
};