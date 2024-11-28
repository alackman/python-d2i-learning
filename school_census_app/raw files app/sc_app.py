import streamlit as st
import pandas as pd



st.title('School Census File Joiner')



def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


def attendance_file_processor(file, source):
    filename = file.name.split("_")[-1].split(".")[0]
    if filename == 'pupilonroll':
        df = pd.read_csv(file)
        df = df[['pupilonrolltableid', 'upn', 'forename', 'surname', 'dob', 'sex']]
    elif filename == 'termlysessiondetailsonroll':
        df = pd.read_csv(file)
        df = df[['termlysessiondetailsonrolltableid', 'pupilonrolltableid', 'sessions', 'attendancereason']]
        df['attendancereason'] = df['attendancereason'].replace("/", "AM")
        df['attendancereason'] = df['attendancereason'].replace("\\", "PM")
    elif filename == 'addresses':
        df = pd.read_csv(file)
        df = df[['pupilonrolltableid', 'postcode']]
    filename = f'{source}_{filename}'
    return filename, df

#--- File inputs
term_file = st.file_uploader(label='Input pupilonroll file(s) for term', accept_multiple_files=True)

la_attendance_files = st.file_uploader(label='For LA files: Input pupilonroll, termlysessiondetailsonroll, and addresses', accept_multiple_files=True)

academy_attendance_files = st.file_uploader(label='For Academy files: Input pupilonroll, termlysessiondetailsonroll, and addresses', accept_multiple_files=True)

#--- Reading files to Dataframes

# dict for all dataframes after processing
attendance_data_dict = {}

if term_file and (la_attendance_files or academy_attendance_files):
    
    la_check = False
    ac_check = False

    if len(term_file) > 1:
        term_df = pd.concat(term_file)
    elif len(term_file) == 1:
        term_df = pd.read_csv(term_file[0])
    term_df = term_df[['pupilonrolltableid','upn']]

    if la_attendance_files:
        if len(la_attendance_files) == 3:
            for file in la_attendance_files:
                output = attendance_file_processor(file=file, source="LA")
                attendance_data_dict[output[0]] = output[1]
            la_address_merge = pd.merge(attendance_data_dict['LA_pupilonroll'],
                                        attendance_data_dict['LA_addresses'],
                                        on='pupilonrolltableid')
            la_address_merge['source'] = 'Local Authority'
            la_pupils = la_address_merge[['source',
                                        'pupilonrolltableid',
                                       'upn',
                                       'forename',
                                       'surname',
                                       'dob',
                                       'postcode']]
            la_attendance_pivot = attendance_data_dict['LA_termlysessiondetailsonroll'].pivot(index=['termlysessiondetailsonrolltableid', 'pupilonrolltableid'], 
                                                                                              columns='attendancereason', 
                                                                                              values='sessions').reset_index()
            la_attendance_pivot = la_attendance_pivot.groupby(['pupilonrolltableid'], as_index=False).sum()
            la_result = pd.merge(la_pupils, la_attendance_pivot, how='left', on='pupilonrolltableid')
            la_result['postcode'] = la_result['postcode'].str.replace(' ','')
            la_check = True
        else:
            st.write("Not all  LA attendance files are present. Restart process")


    if academy_attendance_files:
        if len(academy_attendance_files) == 3:
            for file in academy_attendance_files:
                output = attendance_file_processor(file=file, source="AC")
                attendance_data_dict[output[0]] = output[1]
            ac_address_merge = pd.merge(attendance_data_dict['AC_pupilonroll'],
                                        attendance_data_dict['AC_addresses'],
                                        on='pupilonrolltableid')
            ac_address_merge['source'] = 'Academy'
            ac_pupils = ac_address_merge[['source',
                                        'pupilonrolltableid',
                                       'upn',
                                       'forename',
                                       'surname',
                                       'dob',
                                       'postcode']]
            ac_attendance_pivot = attendance_data_dict['AC_termlysessiondetailsonroll'].pivot(index=['termlysessiondetailsonrolltableid', 'pupilonrolltableid'], 
                                                                                              columns='attendancereason', 
                                                                                              values='sessions').reset_index()
            ac_attendance_pivot = ac_attendance_pivot.groupby(['pupilonrolltableid'], as_index=False).sum()
            ac_result = pd.merge(ac_pupils, ac_attendance_pivot, how='left', on='pupilonrolltableid')
            ac_result['postcode'] = ac_result['postcode'].str.replace(' ','')
            ac_check = True
        else:
            st.write("Not all Academy attendance files are present. Restart process")

    if la_check and ac_check:
        result_df = pd.concat([la_result, ac_result])
    elif la_check and ac_check == False:
        result_df = la_result
    elif ac_check and la_check == False:
        result_df = ac_result

    final_df = result_df[result_df['upn'].isin(term_df['upn'])]
    
    output_postcodes = convert_df(final_df['postcode'])
    output_final = convert_df(final_df)

    

    postcode_list = final_df['postcode'].unique().tolist()


    st.download_button(
        "Download final output of pupils",
        output_final,
        "Final Pupil Output.csv",
        "text/csv"
    )







