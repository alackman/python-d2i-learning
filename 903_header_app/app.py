import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def data_cleaner(df):
    '''
    Cleans 903 header and adds an AGE column based on DOB.

    Arguments:
        df -> DataFrame of 903 header data to be cleaned
    
    Returns:
        df -> DataFrame of 903 data with SEX correctly mapped and AGE added.
        Selects only SEX, AGE, ETHNIC
    '''
    df['SEX'] = df['SEX'].map({1:'Male',
                               2:'Female'})
    df['DOB'] = pd.to_datetime(df['DOB'], format="%d/%m/%Y", errors='coerce')
    # Normalize changes it to midnight rather than the time it was run!!!
    df['AGE'] = pd.to_datetime('today').normalize() - df['DOB']
    df['AGE'] = (df['AGE'] / np.timedelta64(1, 'Y')).astype('int')

    df = df[['SEX', 'AGE', 'ETHNIC']]

    return df

# Plotting functions
def age_bar(df):
    fig = px.histogram(df, 
                       x='SEX',
                       title='Breakdown by gender of 903 data',
                       labels={'SEX':'Sex of Children'},
                       color='ETHNIC')

    return fig

def ethnicity_pie(df):
    ethnic_count = df.groupby('ETHNIC')['ETHNIC'].count().reset_index(name='count')

    pie_fig = px.pie(ethnic_count, 
                     values='count',
                     names='ETHNIC',
                     title='Breakdown of 903 by ethnicity')
    return pie_fig

st.title('903 header analysis tool')

upload = st.file_uploader('Please upload 903 header as a .csv')

if upload is not None:
    st.write('File successfully uploaded')

    df_upload = pd.read_csv(upload)
    df_clean = data_cleaner(df_upload)
    st.dataframe(df_clean)
    age_bar_fig = age_bar(df_clean)
    st.plotly_chart(age_bar_fig)
    
    ethnic_pie_count = ethnicity_pie(df_clean)
    st.plotly_chart(ethnic_pie_count)