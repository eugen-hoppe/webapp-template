from pydantic import BaseModel, ConfigDict


class BaseORM(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
