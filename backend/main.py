from fastapi import FastAPI
from fastapi.responses import FileResponse
from backend.database import create_tables, get_connection
from backend.growth_analyst import generate_growth_recommendation
from backend.recommendation_agent import generate_recommendation
from backend.campaign_agent import create_campaign
from backend.action_layer import approve_campaign, reject_campaign
from backend.execution_agent import execute_campaign
from backend.measurement_agent import analyze_campaign


app = FastAPI(
    title="GrowthPilot AI",
    description="AI-powered merchant growth and agentic commerce system",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/api/growth/opportunity")
def get_growth_opportunity():
    return generate_growth_recommendation()


@app.get("/api/growth/recommendation")
def get_recommendation():
    return generate_recommendation()


@app.post("/api/campaign/create")
def create_growth_campaign():
    return create_campaign()


@app.get("/api/campaigns")
def get_campaigns():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM campaigns
        ORDER BY id DESC
    """)

    campaigns = cursor.fetchall()

    connection.close()

    return [dict(campaign) for campaign in campaigns]


@app.post("/api/campaign/{campaign_id}/approve")
def approve_growth_campaign(campaign_id: int):
    return approve_campaign(campaign_id)


@app.post("/api/campaign/{campaign_id}/reject")
def reject_growth_campaign(campaign_id: int):
    return reject_campaign(campaign_id)


@app.post("/api/campaign/{campaign_id}/execute")
def execute_growth_campaign(campaign_id: int):
    return execute_campaign(campaign_id)


@app.get("/api/campaign/{campaign_id}/analysis")
def get_campaign_analysis(campaign_id: int):
    return analyze_campaign(campaign_id)


@app.get("/api/dashboard")
def get_dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total_customers
        FROM customers
    """)
    total_customers = cursor.fetchone()["total_customers"]

    cursor.execute("""
        SELECT COUNT(*) AS total_products
        FROM products
    """)
    total_products = cursor.fetchone()["total_products"]

    cursor.execute("""
        SELECT COUNT(*) AS total_campaigns
        FROM campaigns
    """)
    total_campaigns = cursor.fetchone()["total_campaigns"]

    cursor.execute("""
        SELECT
            COALESCE(SUM(incremental_revenue), 0) AS incremental_revenue,
            COALESCE(AVG(roi), 0) AS average_roi
        FROM campaign_results
    """)
    performance = cursor.fetchone()

    connection.close()

    return {
        "total_customers": total_customers,
        "total_products": total_products,
        "total_campaigns": total_campaigns,
        "incremental_revenue": round(
            performance["incremental_revenue"], 2
        ),
        "average_roi": round(
            performance["average_roi"], 2
        )
    }