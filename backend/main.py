from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import yaml
import os
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = Path(__file__).parent.parent / "data" / "networth.yaml"

class Asset(BaseModel):
    type: str
    value: float
    description: Optional[str] = ""

class Debt(BaseModel):
    type: str
    value: float
    description: Optional[str] = ""

class NetWorthData(BaseModel):
    assets: dict
    debts: dict

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {
            "assets": {
                "real_estate": [],
                "stocks": [],
                "cash": []
            },
            "debts": {
                "credit_card": [],
                "student_loan": [],
                "mortgage": []
            }
        }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

@app.get("/api/networth")
def get_networth():
    data = load_data()
    
    total_assets = 0
    for category in data["assets"].values():
        for item in category:
            total_assets += item.get("value", 0)
    
    total_debts = 0
    for category in data["debts"].values():
        for item in category:
            total_debts += item.get("value", 0)
    
    return {
        "data": data,
        "summary": {
            "total_assets": total_assets,
            "total_debts": total_debts,
            "net_worth": total_assets - total_debts
        }
    }

@app.post("/api/assets/{category}")
def add_asset(category: str, asset: Asset):
    data = load_data()
    
    if category not in data["assets"]:
        raise HTTPException(status_code=400, detail=f"Invalid asset category: {category}")
    
    data["assets"][category].append({
        "type": asset.type,
        "value": asset.value,
        "description": asset.description
    })
    
    save_data(data)
    return {"message": "Asset added successfully"}

@app.post("/api/debts/{category}")
def add_debt(category: str, debt: Debt):
    data = load_data()
    
    if category not in data["debts"]:
        raise HTTPException(status_code=400, detail=f"Invalid debt category: {category}")
    
    data["debts"][category].append({
        "type": debt.type,
        "value": debt.value,
        "description": debt.description
    })
    
    save_data(data)
    return {"message": "Debt added successfully"}

@app.delete("/api/assets/{category}/{index}")
def delete_asset(category: str, index: int):
    data = load_data()
    
    if category not in data["assets"]:
        raise HTTPException(status_code=400, detail=f"Invalid asset category: {category}")
    
    if index < 0 or index >= len(data["assets"][category]):
        raise HTTPException(status_code=404, detail="Asset not found")
    
    data["assets"][category].pop(index)
    save_data(data)
    return {"message": "Asset deleted successfully"}

@app.delete("/api/debts/{category}/{index}")
def delete_debt(category: str, index: int):
    data = load_data()
    
    if category not in data["debts"]:
        raise HTTPException(status_code=400, detail=f"Invalid debt category: {category}")
    
    if index < 0 or index >= len(data["debts"][category]):
        raise HTTPException(status_code=404, detail="Debt not found")
    
    data["debts"][category].pop(index)
    save_data(data)
    return {"message": "Debt deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)