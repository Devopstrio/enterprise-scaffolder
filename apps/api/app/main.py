import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("enterprise-scaffolder-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="Enterprise Scaffolder API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/templates")
def get_templates():
    return [
        {"id": "go-ms-v1", "name": "Go Microservice (Standard)", "category": "Microservices", "maturity": "GOLDEN"},
        {"id": "py-api-fastapi", "name": "FastAPI Accelerator", "category": "APIs", "maturity": "GOLDEN"},
        {"id": "react-vite-app", "name": "React Vite Frontend", "category": "Apps", "maturity": "SILVER"},
        {"id": "tf-module-v3", "name": "Standard Terraform Module", "category": "Infrastructure", "maturity": "GOLDEN"}
    ]

@app.post("/generate/project")
def generate_project(template_id: str, project_name: str, team_id: str):
    logger.info(f"Generating project {project_name} from {template_id} for {team_id}")
    return {"status": "GENERATING", "job_id": f"gen_{int(time.time())}", "repo_url": f"https://github.com/Org/{project_name}"}

@app.get("/history")
def get_generation_history():
    return [
        {"id": "gen_1", "project": "finance-api", "template": "go-ms-v1", "status": "COMPLETED", "date": "2026-04-20"},
        {"id": "gen_2", "project": "customer-web", "template": "react-vite-app", "status": "COMPLETED", "date": "2026-04-22"},
        {"id": "gen_3", "project": "data-lake-v2", "template": "tf-module-v3", "status": "FAILED", "date": "2026-04-25"}
    ]

@app.get("/scores/summary")
def get_scores_summary():
    return {
        "factory_maturity": 0.96,
        "developer_productivity_index": 0.92,
        "standardization_score": 0.98,
        "automation_coverage": "94%"
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_generations": 12450,
        "active_blueprints": 142,
        "avg_time_to_code": "45s",
        "factory_status": "READY"
    }

@app.get("/reports/export")
def export_report(report_type: str = "productivity"):
    return {"status": "GENERATING", "download_url": "/downloads/report_productivity_2026.pdf"}
