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


# Age Mapping

agegroup_data=[
    {
        'grp_category': 'agegroup',
        'grp_name':  x ,
        'grp_desc': '%d to %d'%(x*4,(x*4)+4)
    }
    for x in range(0,31)
]

# Race Mapping

racialgroup_data=[
    {
        'grp_category': 'race',
        'grp_name': '0',
        'grp_desc': 'All races'
    },
    {
        'grp_category': 'race',
        'grp_name': '1',
        'grp_desc': 'White alone'
    },
    {
        'grp_category': 'race',
        'grp_name': '2',
        'grp_desc': 'Black alone'
    },
    {
        'grp_category': 'race',
        'grp_name': '3',
        'grp_desc': 'American Indian and Alaska Native alone'
    },
    {
        'grp_category': 'race',
        'grp_name': '4',
        'grp_desc': 'Asian alone'
    },
    {
        'grp_category': 'race',
        'grp_name': '5',
        'grp_desc': 'Native Hawaiian and Other Pacific Islander alone'
    },
    {
        'grp_category': 'race',
        'grp_name': '6',
        'grp_desc': 'Two or more races'
    },
    {
        'grp_category': 'race',
        'grp_name': '7',
        'grp_desc': 'White alone or in combination'
    },
    {
        'grp_category': 'race',
        'grp_name': '8',
        'grp_desc': 'Black alone or in combination'
    },
    {
        'grp_category': 'race',
        'grp_name': '9',
        'grp_desc': 'American Indian and Alaska Native alone or in combination'
    },
    {
        'grp_category': 'race',
        'grp_name': '10',
        'grp_desc': 'Asian alone or in combination'
    },
    {
        'grp_category': 'race',
        'grp_name': '11',
        'grp_desc': 'Native Hawaiian and Other Pacific Islander alone or in combination'
    }
]

# Sex Mapping

sex_mapping = [
    {
        'grp_category':'sex',
        'grp_name': '0',
        'grp_desc': 'Both Sexes'
    },
    {
        'grp_category':'sex',
        'grp_name': '1',
        'grp_desc': 'Male'
    },
    {
        'grp_category':'sex',
        'grp_name': '2',
        'grp_desc': 'Female'
    }
]

# Hispanic Origin Mapping

hispanic_mapping = [
    {
        'grp_category': 'hisp',
        'grp_name': '1',
        'grp_desc': 'No Hispanic Origin'
    },
    {
        'grp_category': 'hisp',
        'grp_name': '2',
        'grp_desc': 'Hispanic Origin'
    },
    {
        'grp_category': 'hisp',
        'grp_name': '0',
        'grp_desc': 'Both Hispanic Origins'
    }
]

# State Mapping

state_mapping = [
    {
        'grp_category': 'state',
        'grp_name': '0',
        'grp_desc': 'All States'
    },
    {
        'grp_category': 'state',
        'grp_name': '1',
        'grp_desc': 'Alabama'
    },
    {
        'grp_category': 'state',
        'grp_name': '2',
        'grp_desc': 'Alaska'
    },
    {
        'grp_category': 'state',
        'grp_name': '3',
        'grp_desc': 'Arizona'
    },
    {
        'grp_category': 'state',
        'grp_name': '4',
        'grp_desc': 'Arkansas'
    },
    {
        'grp_category': 'state',
        'grp_name': '5',
        'grp_desc': 'California'
    },
    {
        'grp_category': 'state',
        'grp_name': '6',
        'grp_desc': 'Colorado'
    },
    {
        'grp_category': 'state',
        'grp_name': '7',
        'grp_desc': 'Connecticut'
    },
    {
        'grp_category': 'state',
        'grp_name': '8',
        'grp_desc': 'Delaware'
    },
    {
        'grp_category': 'state',
        'grp_name': '9',
        'grp_desc': 'Florida'
    },
    {
        'grp_category': 'state',
        'grp_name': '10',
        'grp_desc': 'Georgia'
    },
    {
        'grp_category': 'state',
        'grp_name': '11',
        'grp_desc': 'Hawaii'
    },
    {
        'grp_category': 'state',
        'grp_name': '12',
        'grp_desc': 'Idaho'
    },
    {
        'grp_category': 'state',
        'grp_name': '13',
        'grp_desc': 'Illinois'
    },
    {
        'grp_category': 'state',
        'grp_name': '14',
        'grp_desc': 'Indiana'
    },
    {
        'grp_category': 'state',
        'grp_name': '15',
        'grp_desc': 'Iowa'
    },
    {
        'grp_category': 'state',
        'grp_name': '16',
        'grp_desc': 'Kansas'
    },
    {
        'grp_category': 'state',
        'grp_name': '17',
        'grp_desc': 'Kentucky'
    },
    {
        'grp_category': 'state',
        'grp_name': '18',
        'grp_desc': 'Louisiana'
    },
    {
        'grp_category': 'state',
        'grp_name': '19',
        'grp_desc': 'Maine'
    },
    {
        'grp_category': 'state',
        'grp_name': '20',
        'grp_desc': 'Maryland'
    },
    {
        'grp_category': 'state',
        'grp_name': '21',
        'grp_desc': 'Massachusetts'
    },
    {
        'grp_category': 'state',
        'grp_name': '22',
        'grp_desc': 'Michigan'
    },
    {
        'grp_category': 'state',
        'grp_name': '23',
        'grp_desc': 'Minnesota'
    }]

# Create metadata table

metadata = pd.DataFrame.from_dict(
    agegroup_data+state_mapping+racialgroup_data+sex_mapping+hispanic_mapping , orient='columns'
)

# Write to database

metadata.to_sql('metadata_table', pg_engine, if_exists='replace', index=False)


print('Metadata table created')
