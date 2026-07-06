from fastapi import APIRouter
from app.schemas.models import AnalysisRequest
from app.services.basic_stats import run_basic_stats
from app.graph.plot_generator import generate_boxplot, generate_scatterplot

router = APIRouter()


@router.post("/internal/stats/basic")
def basic_stats_endpoint(request: AnalysisRequest):
    try:
        result = run_basic_stats(request.groups)
        boxplot = generate_boxplot(request.groups)
        scatter = generate_scatterplot(request.groups)
        return {
            "status": "success",
            "method": "basic",
            "result": result,
            "graphs": {
                "boxplot": {"format": "png", "base64": boxplot},
                "scatter": {"format": "png", "base64": scatter},
            },
        }
    except Exception as e:
        return {
            "status": "error",
            "errorCode": "CALCULATION_ERROR",
            "message": str(e),
        }