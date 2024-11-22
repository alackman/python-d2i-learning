import pandas as pd
import glob
import os



# def postcode_finder(postcode_list):
#     import urllib3
#     postcode_locality_dict = {}

#     for postcode in postcode_list:
        
#         http = urllib3.PoolManager()
#         url = f'https://www.doogal.co.uk/GetPostcode/{postcode}?output=json'
#         output = http.request("GET", url=url)
#         postcode_data = output.json()
#         postcode_district = postcode_data['district']
#         postcode_locality_dict[f'{postcode}'] = postcode_district
    
#     return postcode_locality_dict



all_files = glob.glob("/workspaces/python-d2i-learning/school_census_app/postcode files/*.csv")

df_list = []

for file in all_files:
    filename = file.split("/")[-1].split(".")[0].split(" ")[0]
    print(filename)
    df = pd.read_csv(file)
    df['Locality'] = filename
    df_list.append(df[['Locality', 'Postcode']])
    # print(df)


print(df_list[1])

final_df = pd.concat(df_list)

final_df.to_csv("./workspaces/python-d2i-learning/school_census_app")
