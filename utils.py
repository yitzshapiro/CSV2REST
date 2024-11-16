import pandas as pd
from typing import List, Any
from pydantic import BaseModel, create_model

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load CSV file into a pandas DataFrame.
    """
    return pd.read_csv(file_path)

def create_dynamic_model(df: pd.DataFrame) -> BaseModel:
    """
    Dynamically create a Pydantic model based on DataFrame columns.
    """
    columns = df.columns
    annotations = {col: (Any, ...) for col in columns}
    DynamicModel = create_model('DynamicModel', **annotations)
    return DynamicModel

def get_data_as_dict(df: pd.DataFrame) -> List[dict]:
    """
    Convert DataFrame rows to a list of dictionaries.
    """
    return df.to_dict(orient='records')