from pydantic import BaseModel


class GraphData(BaseModel):
    labels: list
    values: list
