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
