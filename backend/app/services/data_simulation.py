import pandas as pd
import numpy as np
import os

def generate_correlated_data(n, p, base_prob, correlated_prob, correlation_strength):
    """
    Generates correlated binary data based on a primary variable.
    """
    base_data = np.random.choice(p, size=n)
    correlated_data = np.zeros(n, dtype=int)

    for i in range(n):
        if np.random.rand() < correlation_strength:
            # Follow the correlated probability distribution
            prob = correlated_prob[base_data[i]]
        else:
            # Follow the base probability distribution
            prob = base_prob

        correlated_data[i] = np.random.choice(len(prob), p=prob)

    return base_data, correlated_data

def generate_simulated_dataset(n=300, output_path="backend/tests/data/simulated_dataset.csv"):
    """
    Generates a simulated dataset for the LGBTQ+ Sexual Fluidity Analysis Platform.

    Args:
        n (int): The number of samples to generate.
        output_path (str): The path to save the generated CSV file.
    """
    np.random.seed(42) # for reproducibility

    # Define the questions and their possible responses
    questions = {
        'media1': list(range(5)), 'media2': list(range(5)),
        'family1': list(range(3)), 'family2': list(range(3)), 'family3': list(range(3)),
        'community1': list(range(5)), 'community2': list(range(5)),
        'culture1': list(range(5)), 'culture2': list(range(5)),
        'self1': list(range(5)), 'self2': list(range(5)),
        'exploration1': list(range(5)), 'exploration2': list(range(5)),
        'school1': list(range(3)),
    }

    # Realistic distributions as per user feedback
    media_dist = [0.1, 0.2, 0.4, 0.2, 0.1] # Skewed towards moderate exposure
    social_dist = [0.2, 0.5, 0.3] # Skewed towards moderate acceptance

    # Create a DataFrame
    df = pd.DataFrame(columns=questions.keys())

    # Generate data for each question
    for question, choices in questions.items():
        if 'media' in question:
            df[question] = np.random.choice(choices, size=n, p=media_dist)
        elif question in ['family2', 'family3', 'school1']:
            # Create correlation between social acceptance factors
            if question == 'family2':
                df[question] = np.random.choice(choices, size=n, p=social_dist)
            else:
                # Correlate family3 and school1 with family2
                base_data = df['family2']
                correlated_data = np.zeros(n, dtype=int)
                for i in range(n):
                    # Adjust probabilities based on the value of family2
                    if base_data[i] == 0: # Low acceptance
                        prob = [0.6, 0.3, 0.1]
                    elif base_data[i] == 1: # Mid acceptance
                        prob = [0.2, 0.6, 0.2]
                    else: # High acceptance
                        prob = [0.1, 0.3, 0.6]
                    correlated_data[i] = np.random.choice(choices, p=prob)
                df[question] = correlated_data
        else:
            # For other questions, use a uniform distribution for simplicity
            df[question] = np.random.choice(choices, size=n)

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the DataFrame to a CSV file
    df.to_csv(output_path, index=False)
    print(f"Successfully generated and saved simulated dataset to {output_path}")

if __name__ == "__main__":
    generate_simulated_dataset()