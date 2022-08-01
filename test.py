import apyd
import requests

# https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY
#apyd.show_version()

client = apyd.http.HTTPClient('TOKEN')
#output = client.get_date(date='2022-08-01')
#print(output.title)
#out = client.get_spec_dates(start_date='2022-07-21', end_date='2022-07-30')
#print([i.title for i in out])
#output_random = client.get_random_img(count=1)
#print(output_random)