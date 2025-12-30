# Imports
import json
import pandas as pd

# Load JSON data from a file
with open('NCT00830167.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    
# 1. Study overview
study_info = {
    'nct_id': data['protocolSection']['identificationModule']['nctId'],
    'brief_title': data['protocolSection']['identificationModule']['briefTitle'],
    'enrollment': data['protocolSection']['designModule']['enrollmentInfo']['count'],
    'phase': data['protocolSection']['designModule']['phases'][0],
    'arms': [arm['label'] for arm in data['protocolSection']['armsInterventionsModule']['armGroups']]
}
study_df = pd.DataFrame([study_info])
study_df.to_csv('study_overview.csv', index=False)

# 2. Baseline characteristics
baseline_measures = []
baseline_module = data['resultsSection'].get('baselineCharacteristicsModule', {})
for measure in baseline_module.get('measures', []):
    measure_title = measure.get('title', 'Unknown Measure')
    for cls in measure.get('classes', []):
        class_title = cls.get('title', 'Unknown Class')
        for cat in cls.get('categories', []):
            # Use 'title' if exists, otherwise use class_title or 'N/A'
            cat_title = cat.get('title', class_title if 'title' in cls else 'N/A')
            row = {
                'measure': measure_title, 
                'class': class_title,
                'category': cat_title
            }
            for m in cat.get('measurements', []):
                row[f"{m['groupId']}_value"] = m.get('value', '')
                row[f"{m['groupId']}_units"] = m.get('units', '')
            baseline_measures.append(row)

baseline_df = pd.DataFrame(baseline_measures)
baseline_df.to_csv('baseline_characteristics.csv', index=False)

# 3. Efficacy outcomes
outcomes = []
outcome_module = data.get('resultsSection', {}).get('outcomeMeasuresModule', {}).get('outcomeMeasures', {})
for outcome in outcome_module:
    row = {
        'outcome_type': outcome.get('type', 'Other'),
        'title': outcome.get('title', 'N/A')[:120],
        'time_frame': outcome.get('timeFrame', 'N/A')
    }
    
    # Extract from ALL found measurements
    for cls in outcome.get('classes', []):
        for cat in cls.get('categories', []):
            for m in cat.get('measurements', []):
                group_id = m['groupId']
                param_type = m.get('paramType', 'Mean')
                row[f"{group_id}_{param_type}_value"] = m.get('value', '')
                row[f"{group_id}_{param_type}_spread"] = m.get('spread', '')
                row[f"{group_id}_units"] = m.get('units', '')
                row[f"{group_id}_num_analyzed"] = m.get('numAnalyzed', '')
    outcomes.append(row)
    
outcomes_df = pd.DataFrame(outcomes)
outcomes_df.to_csv('efficacy_outcomes.csv', index=False)