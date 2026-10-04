from fastapi import FastAPI

from app.api.routes.forms import router as forms_router
from app.api.routes.simulations import router as simulations_router


app = FastAPI(
    title="Synthetic Questionnaire Simulator",
    version="0.1.0",
)


app.include_router(forms_router)
app.include_router(simulations_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }
