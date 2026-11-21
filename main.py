from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="EcoCampus 4.0 API")

# السماح للواجهة الأمامية بالتواصل مع الخادم
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

VALID_MATERIALS = ["Plastic", "Metal", "Glass", "Paper"]

THRESHOLD = 75
MARGIN = 15


class Prediction(BaseModel):
    material: str
    confidence: float = Field(ge=0, le=100)
    second_confidence: float = Field(ge=0, le=100)


@app.get("/")
def home():
    return {
        "project": "EcoCampus 4.0",
        "status": "Backend is running"
    }


@app.get("/health")
def health():
    return {"status": "OK"}


@app.post("/predict")
def predict(data: Prediction):

    if data.material not in VALID_MATERIALS:
        return {
            "status": "error",
            "decision": "Unknown material",
            "message": "Unknown material"
        }

    gap = data.confidence - data.second_confidence

    if data.confidence < THRESHOLD or gap < MARGIN:
        return {
            "status": "manual_check",
            "material": data.material,
            "confidence": data.confidence,
            "second_confidence": data.second_confidence,
            "gap": gap,
            "decision": "Manual verification required"
        }

    return {
        "status": "success",
        "material": data.material,
        "confidence": data.confidence,
        "second_confidence": data.second_confidence,
        "gap": gap,
        "decision": "Material classified"
    }