from pydantic import BaseModel


class GenericBase(BaseModel):
    def db(model_or_dict: BaseModel | dict) -> dict:
        if isinstance(model_or_dict, BaseModel):
            return model_or_dict.model_dump()
        if isinstance(model_or_dict, dict):
            return model_or_dict
        raise TypeError("Is not a Pydantic-Model/Python-Dictionary")
