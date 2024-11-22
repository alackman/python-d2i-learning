import requests
import urllib3




def postcode_finder(postcode_list):
    postcode_locality_dict = {}

    for postcode in postcode_list:
        url = f'https://www.doogal.co.uk/GetPostcode/{postcode}?output=json'
        output = requests.get(url=url)
        postcode_data = output.json()
        postcode_district = postcode_data['district']
        postcode_locality_dict[f'{postcode}'] = postcode_district
    
    return postcode_locality_dict


postcode_list = ['BB112QS']

print(postcode_finder(postcode_list))

