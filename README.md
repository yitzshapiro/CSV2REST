# CSV REST API

This project is a REST API built with FastAPI that allows you to fetch and manipulate data from a specified CSV file. The API provides endpoints for retrieving records, searching, sorting, and filtering data.

## Features

- **Dynamic Model Creation**: Automatically creates a Pydantic model based on the columns of the CSV file.
- **Pagination**: Retrieve records with pagination support.
- **Sorting and Filtering**: Sort and filter records based on specified criteria.
- **Search**: Search across all columns or within a specific column.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Pandas
- Pydantic

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```bash
   cd <project-directory>
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your CSV file in the `data` directory and update the `CSV_FILE_PATH` in `config.py` if necessary.

2. Run the application:

   ```bash
   uvicorn main:app --reload
   ```

3. Access the API documentation at `http://localhost:8000/docs`.

## Endpoints

- **GET /records**: Retrieve records with optional pagination, sorting, searching, and filtering.
- **GET /records/{record_id}**: Retrieve a single record by its index.
- **GET /columns**: Retrieve the list of column names from the CSV.
- **GET /search/{column}**: Search within a specific column.

## Configuration

- The path to the CSV file is configured in `config.py`:

  ```python
  CSV_FILE_PATH: str = "data/data.csv"
  ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
