# Demographic Data Visualization - United States of America

This project aims to visualize demographic data for the United States of America using data from the US Census Bureau API. It includes scripts to fetch data from the API, load it into a PostgreSQL database, and create a Streamlit dashboard for interactive data visualization.

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.x
- PostgreSQL database

## Installation

1. Clone the repository:

```
git clone https://github.com/KavyaGuram/AnalyticsOnUSDemography.git
```

2. Create a virtual environment and activate it:

```
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

3. Install the required Python packages:

```
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file in the project root directory and add the following variables:

```
CENSUS_API_KEY=your_census_api_key
PG_HOST=your_postgres_host
PG_PORT=your_postgres_port
PG_DATABASE=your_postgres_database
PG_USER=your_postgres_user
PG_PASSWORD=your_postgres_password
```

Replace the placeholders with your actual values.

## Usage

1. Load data from the Census API and store it in the PostgreSQL database:

```
python dataload.py
```

This script will fetch demographic data from the Census API for the years 2010-2019 and load it into the `demography` table in the PostgreSQL database.

2. Create the metadata table:

```
python set_metadata.py
```

This script will create a `metadata_table` in the PostgreSQL database, which contains descriptions for the various demographic groups (age, race, sex, Hispanic origin, and state).

3. Run the Streamlit dashboard:

```
streamlit run dashboard.py
```

This will launch the Streamlit dashboard, where you can interactively visualize the demographic data using various filters and chart types.

## Project Structure

- `dataload.py`: Script to fetch demographic data from the Census API and load it into the PostgreSQL database.
- `set_metadata.py`: Script to create the metadata table in the PostgreSQL database.
- `dashboard.py`: Streamlit app for interactive data visualization.
- `requirements.txt`: List of required Python packages.
- `.env`: Environment variables file (not included in the repository).

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
```

This README file provides an overview of the project, instructions for installation and usage, a description of the project structure, and information about contributing and licensing.