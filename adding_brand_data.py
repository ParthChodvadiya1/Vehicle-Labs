import pandas as pd
import numpy as np
import requests
# import requests.auth import HTTPBasicAuth
# import urllib3


def add(filename):
    df = pd.read_csv(filename,header=0,names=["brandname",'brandmodel'])
    # print(df.head())
    df = df.iloc[1:]
    for idx,brandname,brandmodel in df.itertuples():
        # print(brandname)
        weburl = "http://127.0.0.1:8000/api/vehiclesbrand/register/"
        myobj = {
            "brandname": brandname,
            "brandmodel":brandmodel
        }
        x = requests.post(weburl, data = myobj)
        print(x.status_code)
        # print(brandname)
    # print(data.shape)


add(filename="C:\\VL-DB-Design - Sheet7.csv")