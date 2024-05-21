from fastapi import FastAPI
from fastapi.responses import FileResponse, ORJSONResponse
import os
import pandas as pd
import uvicorn

app = FastAPI(default_response_class=ORJSONResponse) # 'NaN' in the dataset throws errs in fastapi response
data_dir = os.path.join(os.path.dirname(__file__), "..", "data")


# ROUTES
@app.get("/proteins")
async def get_proteins():
    # fetch data
    cps_df = pd.read_csv(f"{data_dir}/chromo_proteins.csv")
    fps_df = pd.read_csv(f"{data_dir}/fluorescent_proteins.csv")
    cps_dict = cps_df[['name', 'pdb_id', 'seq', 'brightness', 'em_max', 'ex_max', 'states', 'tags']].to_dict(orient="records")
    fps_dict = fps_df[['name', 'pdb_id', 'seq', 'brightness', 'em_max', 'ex_max', 'states', 'tags']].to_dict(orient="records")
    # merge, sort by pdb_id, & return
    return sorted(cps_dict + fps_dict, key=lambda x: str(x['pdb_id']))

@app.get("/proteins/pdb/{pdb_id}")
async def get_protein_pdb(pdb_id: str):
    pdb_dir = f"{data_dir}/pdbs"
    pdb_file = f"{pdb_dir}/{pdb_id}.pdb"
    # send file from local dir
    return FileResponse(pdb_file)


# SERVE
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
