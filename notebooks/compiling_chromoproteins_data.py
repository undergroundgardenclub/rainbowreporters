import json
import os
import pandas as pd
import requests
import requests
import matplotlib.pyplot as plt


# Schema for Proteins Dataframe:
# - name
# - seq
# - pdb_id
# - brightness
# - em_max
# - ex_max
# - states
# - tags (ex: ['fluorescentprotein', 'chromoprotein'])



# %%
# Fetch Datasets
# ... TODO: Examples from this paper? https://jbioleng.biomedcentral.com/articles/10.1186/s13036-018-0100-0
# ... PDB chromoproteins
# POST https://www.rcsb.org/search/data with this payload to search chromoproteins: 
rcsb_results = []

for i in range(10):
  pagination_start = i * 25
  pagination_end = pagination_start + 25
  rcsb_fetched_results = requests.post("https://www.rcsb.org/search/data", json={"report":"search_summary","request":{"query":{"type":"group","nodes":[{"type":"group","nodes":[{"type":"group","nodes":[{"type":"terminal","service":"full_text","parameters":{"value":"chromoprotein"}}],"logical_operator":"and"}],"logical_operator":"and","label":"full_text"}],"logical_operator":"and"},"return_type":"entry","request_options":{"paginate":{"start":pagination_start,"rows":pagination_end},"results_content_type":["experimental"],"sort":[{"sort_by":"score","direction":"desc"}],"scoring_strategy":"combined"},"request_info":{"query_id":"dc667f8c5c2de7fcf1f48461bca06296"}},"getDrilldown":False,"attributes":None})
  rcsb_fetched_results = rcsb_fetched_results.json()
  if rcsb_fetched_results.get('result_set'):
    rcsb_results.extend(rcsb_fetched_results['result_set'])
  else:
    break



# %%
# Transform data to a matching schema as FPs
# Then cycle PDB downloads via URL: https://files.rcsb.org/download/7CAO.pdb
local_data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
local_data_cps_csv = f"{local_data_dir}/chromo_proteins.csv"
cps_df = pd.DataFrame(columns=['name', 'seq', 'pdb_id', 'brightness', 'em_max', 'ex_max', 'states', 'tags'])

if not os.path.exists(local_data_cps_csv):
  for idx, result in enumerate(rcsb_results):
    rich_result_query = '''
    query structure ($id: String!) {
      entry(entry_id:$id){
        rcsb_id
        struct {
          title
        },
        polymer_entities {
          entity_poly {
            pdbx_seq_one_letter_code_can
          }
        }
      }
    }
    '''
    response = requests.post("https://data.rcsb.org/graphql", json={"query": rich_result_query, "variables": {"id": result['identifier']}})
    rich_result = response.json()['data']['entry']
    # Append new data to the DataFrame
    new_row = {
        'name': rich_result['struct']['title'],
        'pdb_id': rich_result['rcsb_id'],
        'seq': rich_result['polymer_entities'][0]['entity_poly']['pdbx_seq_one_letter_code_can'],
        'brightness': None,  # Assume values to be filled later
        'em_max': None,
        'ex_max': None,
        'states': None,
        'tags': json.dumps(['chromoprotein', 'fluorescentprotein'])
    }
    new_row_df = pd.DataFrame([new_row])  # Encapsulate the dictionary in a list to create a DataFrame
    cps_df = pd.concat([cps_df, new_row_df], ignore_index=True)
  # ... save df CSV
  cps_df.to_csv(local_data_cps_csv, index=False)
else:
  cps_df = pd.read_csv(local_data_cps_csv)


# %%
# Quick Observations
# not sure how to analyze color


# %%
# Fetch PDB files available and save to diskm
pdb_dir = f"{local_data_dir}/pdbs"
pdb_col_names = list(filter(lambda n: n.startswith("pdb"),cps_df.columns.values)) # ex: pdb, pdb.1, pdb.2, ...
pdb_ids = set()

# --- compile ids
for index, fp in cps_df.iterrows():
  pdb_ids.add(fp['pdb_id'])

# --- download (if doesn't already exist)
os.makedirs(pdb_dir, exist_ok=True)
for pdb_id in pdb_ids:
  pdb_file_path = f"{pdb_dir}/{pdb_id}.pdb"
  # ... if we haven't downloaded
  if not os.path.exists(pdb_file_path):
    pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(pdb_url)
    with open(pdb_file_path, 'wb') as file:
      file.write(response.content)
