import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os


# PostgreSQL Connection Details
PG_HOST = os.environ.get("PG_HOST")
PG_PORT = os.environ.get("PG_PORT")
PG_DATABASE = os.environ.get("PG_DATABASE")
PG_USER = os.environ.get("PG_USER")
PG_PASSWORD = os.environ.get("PG_PASSWORD")

# PostgreSQL Connection
pg_engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}')

# Load data from the database
@st.cache_data
def load_data():
    demography_data = pd.read_sql_table('demography', pg_engine)
    metadata = pd.read_sql_table('metadata_table', pg_engine)
    return demography_data, metadata

# Streamlit app
def main():

    st.set_page_config(page_title='Demographic Analysis - United States of America', page_icon='🗺️', layout='wide')
    st.title("Demographic Data Visualization - Unites States Of America")

    # Load data
    demography_data, metadata = load_data()

    

    print('count of records:',len(demography_data))

    demography_data['year'] = demography_data['year'].astype(int)
    demography_data['agegroup'] = demography_data['agegroup'].astype(int)
    demography_data['sex'] = demography_data['sex'].astype(int)
    demography_data['race'] = demography_data['race'].astype(int)
    demography_data['hisp'] = demography_data['hisp'].astype(int)
    demography_data['state'] = demography_data['state'].astype(int)

    metadata['grp_name']=metadata['grp_name'].astype(int)

    metadata=metadata.loc[metadata['grp_name']!=0]

    age_maps={
        x:metadata.loc[(metadata['grp_name']==x)&
                       (metadata['grp_category']=='agegroup')]['grp_desc'].values[0] for x in range(1,31)
    }

    sex_maps={
        x:metadata.loc[(metadata['grp_name']==x)&
                       (metadata['grp_category']=='sex')]['grp_desc'].values[0] for x in range(1,3)
        }
    
    race_maps={
        x:metadata.loc[(metadata['grp_name']==x)&
                       (metadata['grp_category']=='race')]['grp_desc'].values[0] for x in range(1,12)
                            }
    
    hisp_maps={
        x:metadata.loc[(metadata['grp_name']==x)&
                           (metadata['grp_category']=='hisp')]['grp_desc'].values[0] for x in range(1,3)

                            }
    
    state_maps={
        x:metadata.loc[(metadata['grp_name']==x)&
                       (metadata['grp_category']=='state')]['grp_desc'].values[0] for x in range(1,24)
                            }
    
    # age_maps = {value: key for key, value in age_maps.items()}
    # sex_maps = {value: key for key, value in sex_maps.items()}
    # race_maps = {value: key for key, value in race_maps.items()}
    # hisp_maps = {value: key for key, value in hisp_maps.items()}
    # state_maps = {value: key for key, value in state_maps.items()}

    demography_data['agegroup'] = demography_data['agegroup'].map(age_maps)
    demography_data['sex'] = demography_data['sex'].map(sex_maps)
    demography_data['race'] = demography_data['race'].map(race_maps)
    demography_data['hisp'] = demography_data['hisp'].map(hisp_maps)
    demography_data['state'] = demography_data['state'].map(state_maps)


    print(demography_data.head(10))


    
    # Create a dictionary of the demographic data
    demography_dict = {
        'agegroup': demography_data['agegroup'].values,
       'sex': demography_data['sex'].values,
        'race': demography_data['race'].values,
        'hisp': demography_data['hisp'].values,
       'state': demography_data['state'].values,
        'year': demography_data['year'].values,
    }

    # Filter options
    year = st.sidebar.slider("Select Year", min_value=2010, max_value=2019, value=2013)
    state = st.sidebar.multiselect("Select State", 
                                   metadata[metadata['grp_category'] == 'state']['grp_desc'].unique())
    age_group = st.sidebar.multiselect("Select Age Group", 
                                       metadata[metadata['grp_category'] == 'agegroup']['grp_desc'].unique())
    race = st.sidebar.multiselect("Select Race", 
                                  metadata[metadata['grp_category'] == 'race']['grp_desc'].unique())
    sex = st.sidebar.multiselect("Select Sex", 
                                 metadata[metadata['grp_category'] == 'sex']['grp_desc'].unique())
    hispanic_origin = st.sidebar.multiselect("Select Hispanic Origin", 
                                             metadata[metadata['grp_category'] == 'hisp']['grp_desc'].unique())

    # Set default values if none selected
    if not state:
        state = metadata[metadata['grp_category'] == 'state']['grp_desc'].unique()
    if not age_group:
        age_group = metadata[metadata['grp_category'] == 'agegroup']['grp_desc'].unique()
    if not race:
        race = metadata[metadata['grp_category'] == 'race']['grp_desc'].unique()
    if not sex:
        sex = metadata[metadata['grp_category'] == 'sex']['grp_desc'].unique()
    if not hispanic_origin:
        hispanic_origin = metadata[metadata['grp_category'] == 'hisp']['grp_desc'].unique()

    # print(demography_data.head(20))

    # print(demography_data.dtypes)

    # print('Selected Options:', state, age_group, race, sex, hispanic_origin,year)

    # print('state maps:',[state_maps[x] for x in state])

    # print(demography_data.loc[demography_data['year']==2013])

    # print([x for x in list(demography_data.year.unique())])
    # Filter data based on selected options
    filtered_data = demography_data.loc[
        (demography_data['year'] == year) &
        (demography_data['state'].isin(state)) &
        (demography_data['agegroup'].isin(age_group)) &
        (demography_data['race'].isin(race)) &
        (demography_data['sex'].isin(sex)) &
        (demography_data['hisp'].isin(hispanic_origin))
    ]

    print('Number Of Records: ', filtered_data.shape[0])
    # Visualization

    col1, col2 =st.columns(2)

    with col1:    
        
        fig = px.bar(filtered_data, x='state', 
                     y='pop', 
                     color='race', 
                     title='Statewise Population by Race',
                     barmode='group')
        st.plotly_chart(fig)
    
    with col2:
        fig = px.bar(filtered_data, 
                     x='state', 
                     y='pop', color='sex', 
                     barmode='group',title='Statewise Population by Gender')
        st.plotly_chart(fig)
    
    # Time line based charts

    filtered_data_2 = demography_data.loc[
        (demography_data['year'] <= year) &
        (demography_data['state'].isin(state)) &
        (demography_data['agegroup'].isin(age_group)) &
        (demography_data['race'].isin(race)) &
        (demography_data['sex'].isin(sex)) &
        (demography_data['hisp'].isin(hispanic_origin))
    ]

    

    col3, col4 =st.columns(2)

    with col3:
        fig = px.bar(filtered_data_2,
                    x='year',
                    y='pop',
                    color='race',
                    title='Population over time grouped by race',
                    barmode='group')
        st.plotly_chart(fig)

        


    with col4:
        fig = px.bar(filtered_data_2,
                    x='year',
                    y='pop',
                    color='sex',
                    title='Population over time grouped by gender',
                    barmode='group')
        st.plotly_chart(fig)
    

    col5, col6 =st.columns(2)

    with col5:
        fig = px.pie(filtered_data_2, values='pop', names='race', title='Population by Race')
        st.plotly_chart(fig)
    
    with col6:
        fig = px.pie(filtered_data_2, values='pop', names='sex', title='Population by Gender')
        st.plotly_chart(fig)
        

if __name__ == "__main__":
    main()
