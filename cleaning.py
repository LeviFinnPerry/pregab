import pandas as pd

# Function to print a brief overview of a dataframe
def print_overview(df):
    print("Overview:")
    print(df.head())
    #print(df.info())
    #print(df.describe())
    print(df.dtypes)


# Study overview

# Read csv file
study_df = pd.read_csv('study_overview.csv')

print_overview(study_df)

# Baseline characteristics
baseline_df = pd.read_csv('baseline_characteristics.csv')


# Rename columns for groups
baseline_df.rename(columns={'BG000_value':'n_placebo',
                            'BG001_value':'n_pregab',
                            'BG002_value':'n_total'}, inplace=True)

print_overview(baseline_df)

# Efficacy outcomes
outcomes_df = pd.read_csv('efficacy_outcomes.csv')

# Rename columns for groups
outcomes_df.rename(columns={'OG000_Mean_value':'placebo_mean_change',
                            'OG001_Mean_value':'pregab_mean_change',
                            'OG000_Mean_spread':'placebo_sd',
                            'OG001_Mean_spread':'pregab_sd'}, inplace=True)

# Calculate difference in means
outcomes_df['mean_difference'] = outcomes_df['pregab_mean'] - outcomes_df['placebo_mean']
# Calculate pooled standard deviation
outcomes_df['pooled_sd'] = ((outcomes_df['placebo_sd'] ** 2 + outcomes_df['pregab_sd'] ** 2) / 2) ** 0.5
# Calculate effect size (Cohen's d)
outcomes_df['effect_size'] = outcomes_df['mean_difference'] / outcomes_df['pooled_sd']
# Calculate relative difference
outcomes_df['relative_difference'] = outcomes_df['mean_difference'] / outcomes_df['placebo_mean']


print_overview(outcomes_df)


# Participant flow
flow_df = pd.read_csv('participant_flow.csv')

print_overview(flow_df)


# Adverse events
adverse_df = pd.read_csv('adverse_events.csv')

# Rename columns for groups
adverse_df.rename(columns={'EG000_affected':'n_placebo_affected',
                            'EG000_at_risk':'n_placebo_at_risk',
                            'EG001_affected':'n_pregab_affected',
                            'EG001_at_risk':'n_pregab_at_risk'}, inplace=True)

# Calculate risk
adverse_df['risk_placebo'] = adverse_df['n_placebo_affected'] / adverse_df['n_placebo_at_risk']
adverse_df['risk_pregab'] = adverse_df['n_pregab_affected'] / adverse_df['n_pregab_at_risk']
# Calculate risk difference
adverse_df['risk_difference'] = adverse_df['risk_pregab'] - adverse_df['risk_placebo']
# Calculate relative risk
adverse_df['relative_risk'] = adverse_df['risk_pregab'] / adverse_df['risk_placebo']
# Calculate odds ratio
adverse_df['odds_placebo'] = adverse_df['n_placebo_affected'] / (adverse_df['n_placebo_at_risk'] - adverse_df['n_placebo_affected'])
adverse_df['odds_pregab'] = adverse_df['n_pregab_affected'] / (adverse_df['n_pregab_at_risk'] - adverse_df['n_pregab_affected'])
adverse_df['odds_ratio'] = adverse_df['odds_pregab'] / adverse_df['odds_placebo']

print_overview(adverse_df)

