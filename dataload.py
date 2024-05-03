# Packages Imported
import requests
import os
import pandas as pd
from sqlalchemy import create_engine
import logging

# API Key
CENSUS_API_KEY = os.environ.get('CENSUS_API_KEY')

# PostgreSQL Connection Details
PG_HOST = os.environ.get('PG_HOST')
PG_PORT = os.environ.get('PG_PORT')
PG_DATABASE = os.environ.get('PG_DATABASE')
PG_USER = os.environ.get('PG_USER')
PG_PASSWORD = os.environ.get('PG_PASSWORD')

# PostgreSQL Connection
pg_engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Helper Functions
def ParseCensusAPIRespToDF(respOP):
    '''parses census api response to dataframe'''
    try:
        data = respOP[1:-1].replace('"', '').split('\n')
        cols = data[0][1:-2].split(',')
        data[-1] = data[-1] + ','
        dataRows = [x[1:-2].split(',') for x in data[1:]]
        df = pd.DataFrame(columns=cols, data=dataRows)
        return df
    except Exception as E:
        raise Exception('Failed Parsing The Output. The exact error is ' + str(E))

def ExtractDataFromCensusAPI(uri, key):
    '''extracts data from census api'''
    try:
        resp = requests.get(uri,timeout=300)
        if resp.status_code == 200:
            return ParseCensusAPIRespToDF(resp.text)
        else:
            raise Exception('Failed to Extract Data. The status code is ' + str(resp.status_code))
    except Exception as E:
        raise Exception('Failed to Extract Data. The exact error is ' + str(E))

def load_df_to_postgres(df, year, table_name, pg_engine):
    """
    Load a DataFrame to a PostgreSQL table.

    Args:
        df (pandas.DataFrame): The DataFrame to be loaded.
        year (int): The year for which the data is being loaded.
        table_name (str): The name of the table to create/replace in the database.
        pg_engine (sqlalchemy.engine.Engine): The SQLAlchemy engine for the PostgreSQL database.

    Returns:
        dict: A dictionary with the status of the operation.
    """
    try:
        # Rename columns to lowercase and replace spaces with underscores
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        # Add 'year' column
        df['year'] = year

        # Convert 'pop' column to integer
        df['pop'] = df['pop'].astype(float)
        
        # Define primary key columns
        primary_key_cols = ['year', 'state', 'agegroup', 'race', 'sex','hisp']

        df[primary_key_cols+['pop']].to_sql(table_name,
                    pg_engine,
                    if_exists='append',
                    index=False,
                    index_label=primary_key_cols)
        
        logging.info(f"Data for year {year} loaded successfully into {table_name} table.")
        return {'status': "data loaded successfully"}
    
    except Exception as e:
        logging.error(f"Error loading data for year {year} into {table_name} table: {str(e)}")
        return {'status': f"error loading data: {str(e)}"}
    
    
# Loading 2010 data
demo_uri_2010 = 'https://api.census.gov/data/2000/pep/int_charagegroups?get=AGEGROUP,RACE,SEX,HISP,POP&for=state:*&DATE_=12'

demography_2010_df = ExtractDataFromCensusAPI(demo_uri_2010, CENSUS_API_KEY)

load_df_to_postgres(demography_2010_df,2010,'demography', pg_engine)

# Loading 2011 data

demo_uri_2011 = 'https://api.census.gov/data/2013/pep/stchar6?get=POP,RACE6,SEX,HISP,AGE&for=state:*&DATE_=4'

demography_2011_df = ExtractDataFromCensusAPI(demo_uri_2011, CENSUS_API_KEY)

demography_2011_df.rename(columns={'RACE6':'RACE',"AGE":"AGEGROUP"}, inplace=True)

load_df_to_postgres(demography_2011_df,2011,'demography', pg_engine)

# Loading 2012 data

demo_uri_2012 = 'https://api.census.gov/data/2013/pep/stchar6?get=POP,RACE6,SEX,HISP,AGE&for=state:*&DATE_=5'

demography_2012_df = ExtractDataFromCensusAPI(demo_uri_2012, CENSUS_API_KEY)

demography_2012_df.rename(columns={'RACE6':'RACE',"AGE":"AGEGROUP"}, inplace=True)

load_df_to_postgres(demography_2012_df,2012,'demography', pg_engine)



# Loading 2013 data

demo_uri_2013 = 'https://api.census.gov/data/2013/pep/stchar6?get=POP,RACE6,SEX,HISP,AGE&for=state:*&DATE_=6'

demography_2013_df = ExtractDataFromCensusAPI(demo_uri_2013, CENSUS_API_KEY)

demography_2013_df.rename(columns={'RACE6':'RACE',"AGE":"AGEGROUP"}, inplace=True)

load_df_to_postgres(demography_2013_df,2013,'demography', pg_engine)

Loading 2014 data

demo_uri_2014 = 'https://api.census.gov/data/2016/pep/charagegroups?get=AGEGROUP,SEX,RACE,POP,HISP&for=state:*&DATE_=7'

demography_2014_df = ExtractDataFromCensusAPI(demo_uri_2014, CENSUS_API_KEY)

load_df_to_postgres(demography_2014_df,2014,'demography', pg_engine)

# Loading 2015 data

demo_uri_2015 = 'https://api.census.gov/data/2016/pep/charagegroups?get=AGEGROUP,SEX,RACE,POP,HISP&for=state:*&DATE_=8'

demography_2015_df = ExtractDataFromCensusAPI(demo_uri_2015, CENSUS_API_KEY)

load_df_to_postgres(demography_2015_df,2015,'demography', pg_engine)

# Loading 2016 data

demo_uri_2016 = 'https://api.census.gov/data/2016/pep/charagegroups?get=AGEGROUP,SEX,RACE,POP,HISP&for=state:*&DATE_=9'

demography_2016_df = ExtractDataFromCensusAPI(demo_uri_2016, CENSUS_API_KEY)

load_df_to_postgres(demography_2016_df,2016,'demography', pg_engine)

# Loading 2017 data

demo_uri_2017 = 'https://api.census.gov/data/2019/pep/charagegroups?get=AGEGROUP,SEX,RACE,POP,HISP&for=state:*&DATE_CODE=10'

demography_2017_df = ExtractDataFromCensusAPI(demo_uri_2017, CENSUS_API_KEY)

load_df_to_postgres(demography_2017_df,2017,'demography', pg_engine)

# Loading 2018 data

demo_uri_2018 = 'https://api.census.gov/data/2019/pep/charagegroups?get=AGEGROUP,SEX,RACE,POP,HISP&for=state:*&DATE_CODE=11'

demography_2018_df = ExtractDataFromCensusAPI(demo_uri_2018, CENSUS_API_KEY)

load_df_to_postgres(demography_2018_df,2018,'demography', pg_engine)


# Loading 2019 data

demo_uri_2019 = 'https://api.census.gov/data/2019/pep/charagegroups?get=AGEGROUP,SEX,RACE,POP,HISP&for=state:*&DATE_CODE=12'

demography_2019_df = ExtractDataFromCensusAPI(demo_uri_2019, CENSUS_API_KEY)

load_df_to_postgres(demography_2019_df,2019,'demography', pg_engine)


logging.info("Data loaded successfully for years 2011 to 2019")