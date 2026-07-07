from urllib import request

from fastapi import APIRouter
from app.schemas.models import AnalysisRequest
from app.services.basic_stats import run_basic_stats
from app.services.ttest import run_ttest
from app.graph.plot_generator import generate_boxplot, generate_scatterplot
from app.exceptions import CalculationError
from app.services.correlation import run_correlation
from app.graph.plot_generator import generate_boxplot, generate_scatterplot, generate_heatmap
from app.services.regression import run_regression
from app.graph.plot_generator import generate_boxplot, generate_scatterplot, generate_heatmap, generate_regression_plot
from app.services.regression import run_regression, run_multiple_regression
from app.graph.plot_generator import (
    generate_boxplot, generate_scatterplot, generate_heatmap,
    generate_regression_plot, generate_prediction_plot,
)
from app.services.anova import run_anova

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
        return {"status": "error", "errorCode": "CALCULATION_ERROR", "message": str(e)}


@router.post("/internal/stats/ttest")
def ttest_endpoint(request: AnalysisRequest):
    try:
        result = run_ttest(request.groups, request.options)
        boxplot = generate_boxplot(request.groups)
        scatter = generate_scatterplot(request.groups)
        return {
            "status": "success",
            "method": "ttest",
            "result": result,
            "graphs": {
                "boxplot": {"format": "png", "base64": boxplot},
                "scatter": {"format": "png", "base64": scatter},
            },
        }
    except CalculationError as e:
        return {"status": "error", "errorCode": "CALCULATION_ERROR", "message": str(e)}
    except Exception as e:
        return {"status": "error", "errorCode": "CALCULATION_ERROR", "message": str(e)}
    
@router.post("/internal/stats/correlation")
def correlation_endpoint(request: AnalysisRequest):
    try:
        result = run_correlation(request.groups)
        heatmap = generate_heatmap(result["correlation"], result["labels"])
        return {
            "status": "success",
            "method": "correlation",
            "result": result,
            "graphs": {"heatmap": {"format": "png", "base64": heatmap}},
        }
    except CalculationError as e:
        return {"status": "error", "errorCode": "CALCULATION_ERROR", "message": str(e)}
    except Exception as e:
        return {"status": "error", "errorCode": "CALCULATION_ERROR", "message": str(e)}
    
@router.post("/internal/stats/regression")
def regression_endpoint(request: AnalysisRequest):
    try:
        result = run_regression(request.groups)
        graph = generate_regression_plot(request.groups, result)
        return {
            "status": "success",
            "method": "regression",
            "result": result,
            "graphs": {"regression": {"format": "png", "base64": graph}},
        }
    except CalculationError as e:
        return {"status": "error", "errorCode": "CALCULATION_ERROR", "message": str(e)}
    except Exception as e:
        return {"status": "error", "errorCode": "CALCULATION_ERROR", "message": str(e)}
    
@router.post("/internal/stats/multiple_regression")
def multiple_regression_endpoint(request: AnalysisRequest):
    try:
        result = run_multiple_regression(request.groups, request.options)
        graph = generate_prediction_plot(result["predicted"], result["actual"])
        return {
            "status": "success",
            "method": "multiple_regression",
            "result": result,
            "graphs": {"prediction": {"format": "png", "base64": graph}},
        }
    except CalculationError as e:
        return {"status": "error", "errorCode": "CALCULATION_ERROR", "message": str(e)}
    except Exception as e:
        return {"status": "error", "errorCode": "CALCULATION_ERROR", "message": str(e)}
    
@router.post("/internal/stats/anova")
def anova_endpoint(request: AnalysisRequest):
    try:
        result = run_anova(request.groups)
        boxplot = generate_boxplot(request.groups)
        scatter = generate_scatterplot(request.groups)
        return {
            "status": "success",
            "method": "anova",
            "result": result,
            "graphs": {
                "boxplot": {"format": "png", "base64": boxplot},
                "scatter": {"format": "png", "base64": scatter},
            },
        }
    except CalculationError as e:
        return {"status": "error", "errorCode": "CALCULATION_ERROR", "message": str(e)}
    except Exception as e:
        return {"status": "error", "errorCode": "CALCULATION_ERROR", "message": str(e)}