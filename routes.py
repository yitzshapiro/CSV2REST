from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from utils import load_csv, create_dynamic_model
from config import CSV_FILE_PATH

router = APIRouter()

# Load CSV and create model at startup
try:
    df = load_csv(CSV_FILE_PATH)
    DynamicModel = create_dynamic_model(df)
    data = df.to_dict(orient='records')
except Exception as e:
    raise RuntimeError(f"Failed to load CSV: {e}")

@router.get("/records", response_model=List[Dict[str, Any]])
def get_records(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Records per page"),
    sort_by: Optional[str] = Query(None, description="Column to sort by"),
    sort_order: Optional[str] = Query("asc", enum=["asc", "desc"], description="Sort order"),
    search: Optional[str] = Query(None, description="Search term across all columns"),
    filters: Optional[str] = Query(None, description="Filter in format: column:value,column2:value2")
):
    """
    Retrieve records with pagination, sorting, searching, and filtering.
    """
    # Start with all records
    filtered_data = data.copy()
    
    # Apply filters if provided
    if filters:
        filter_pairs = [f.split(':') for f in filters.split(',')]
        for column, value in filter_pairs:
            if column in df.columns:
                filtered_data = [
                    record for record in filtered_data 
                    if str(record.get(column, '')).lower() == value.lower()
                ]

    # Apply search across all columns if provided
    if search:
        search = search.lower()
        filtered_data = [
            record for record in filtered_data 
            if any(
                str(value).lower().find(search) != -1 
                for value in record.values()
            )
        ]

    # Apply sorting
    if sort_by and sort_by in df.columns:
        filtered_data.sort(
            key=lambda x: str(x.get(sort_by, '')),
            reverse=(sort_order == "desc")
        )

    # Calculate pagination
    total_records = len(filtered_data)
    total_pages = (total_records + page_size - 1) // page_size
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    # Prepare response with metadata
    response_data = {
        "data": filtered_data[start_idx:end_idx],
        "metadata": {
            "total_records": total_records,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
    }

    return response_data

@router.get("/records/{record_id}", response_model=Dict[str, Any])
def get_record(record_id: int):
    """
    Retrieve a single record by its index.
    """
    if record_id < 0 or record_id >= len(data):
        raise HTTPException(status_code=404, detail="Record not found")
    return data[record_id - 1]

@router.get("/columns", response_model=List[str])
def get_columns():
    """
    Retrieve the list of column names from the CSV.
    """
    return list(df.columns)

@router.get("/search/{column}", response_model=List[Dict[str, Any]])
def search_column(
    column: str,
    query: str = Query(..., description="Search term"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results")
):
    """
    Search within a specific column.
    """
    if column not in df.columns:
        raise HTTPException(status_code=400, detail=f"Column '{column}' not found")
    
    query = query.lower()
    results = [
        record for record in data 
        if str(record.get(column, '')).lower().find(query) != -1
    ][:limit]
    
    return results