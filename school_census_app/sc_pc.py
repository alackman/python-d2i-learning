import streamlit as st
import pandas as pd
import zipfile
import io

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


st.title("School Census Postcode Filejoin")

postcode_files = st.file_uploader(label='Input postcode files:', accept_multiple_files=True)

df_list = []

if postcode_files:

    for file in postcode_files:
        filename = file.name.split("/")[-1].split(".")[0].split(" ")[0]
        print(filename)
        df = pd.read_csv(file)
        df['locality'] = filename
        df['postcode'] = df['Postcode'].str.replace(' ','')
        df_list.append(df[['locality', 'postcode']])
        # print(df)


    postcode_df = pd.concat(df_list)
    output_postcodes = convert_df(postcode_df)

    st.download_button(
    "Download grouped postcode file",
    output_postcodes,
    "GroupedPostcodes.csv",
    "text/csv"
    )


st.title("School Census Postcode Match")

pupil_input_file = st.file_uploader(label='Input pupil file:', accept_multiple_files=False)

new_postcode_file = st.file_uploader(label='Input postcode file with all relevant LAs:', accept_multiple_files=False)

if pupil_input_file and new_postcode_file:
    pupil_input_df = pd.read_csv(pupil_input_file)
    new_postcode_df = pd.read_csv(new_postcode_file)
    matched_df = pupil_input_df.merge(new_postcode_df, how='left', on='postcode')
    st.title('Pupils matched to locality:')
    matched_df
    
    st.download_button(
    label="Download Pupils Matched to Locality",
    data=convert_df(matched_df),
    file_name="All Pupils Matched to Postcode.csv",
    mime="text/csv"
    )

    locality_list = matched_df['locality'].dropna().unique().tolist()

    locality_dict = {}

    for locality in locality_list:
        split_local_df = matched_df[matched_df['locality'] == locality]
        locality_dict[locality] = split_local_df

    # Create an in-memory ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for key, value in locality_dict.items():
            csv_data = convert_df(value)
            zipf.writestr(f"{key}.csv", csv_data)
    
    # Provide download link for the ZIP file
    st.title('School Census files split by Locality')
    st.download_button(
        label="Download School Census Locality Files ZIP",
        data=zip_buffer.getvalue(),
        file_name="school census files.zip",
        mime="application/zip"
    )
