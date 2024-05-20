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
    fps_df = pd.read_csv(f"{data_dir}/fluorescent_proteins.csv")
    fps_df = fps_df[fps_df['pdb.0'].notnull()] # Filter rows with non-null 'pdb.0' values
    fps_dict = fps_df[['uuid', 'pdb.0', 'seq', 'slug', 'states.0.brightness', 'states.0.em_max', 'states.0.ex_max']].rename(columns={"states.0.brightness": "brightness", "states.0.em_max": "em_max", "states.0.ex_max": "ex_max"}).to_dict(orient="records")
    return fps_dict

@app.get("/proteins/pdb/{pdb_id}")
async def get_protein_pdb(pdb_id: str):
    pdb_dir = f"{data_dir}/pdbs"
    pdb_file = f"{pdb_dir}/{pdb_id}.pdb"
    # send file from local dir
    return FileResponse(pdb_file)


# SERVE
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
