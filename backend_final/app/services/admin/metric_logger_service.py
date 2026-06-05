from sqlalchemy.orm import Session

from app.models.metric import Metric


def store_metric(
    db: Session,
    user_id: int,
    session_id: str,
    ai_module: str,
    pipeline_used: str,
    latency: float,
    estimated_cost: float,
    cache_used: bool,
):

    metric = Metric(
        user_id=user_id,
        session_id=session_id,
        ai_module=ai_module,
        pipeline_used=pipeline_used,
        latency=latency,
        estimated_cost=estimated_cost,
        cache_used=cache_used,
        ping_ms=0.0,
    )

    db.add(metric)
    db.commit()
    db.refresh(metric)

    return metric
