from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.metric import Metric


def get_ai_metrics(db: Session):

    metrics = db.query(Metric).all()
    response = {}
    modules = ["VOICE_AI", "TEXT_AI", "IMAGE_AI"]

    for module in modules:
        module_metrics = [m for m in metrics if m.ai_module == module]
        count = len(module_metrics)

        avg_latency = 0
        avg_cost = 0

        if count > 0:

            avg_latency = round(sum(m.latency for m in module_metrics) / count, 2)
            avg_cost = round(sum(m.estimated_cost for m in module_metrics) / count, 4)
        response[module.lower()] = {
            "requests": count,
            "average_latency": avg_latency,
            "average_cost": avg_cost,
            "graph_data": {
                "labels": ["Requests", "Latency", "Cost"],
                "values": [count, avg_latency, avg_cost],
            },
        }

    return response
