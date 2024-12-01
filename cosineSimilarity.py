from sklearn.impute import SimpleImputer
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity

def handler(event,context):
    schemeData="https://storage-abhiyan.s3.ap-south-1.amazonaws.com/schemes-data/schemes_data+-+Sheet1.csv"
    userData=pd.DataFrame({"id":[event.get("id")],"state":[event.get("state")],"describe":[event.get("describe")]})
    #userData=pd.DataFrame({"id":[3],"state":["central"],"describe":["farmers"]})
    return scheme_preprocess(userData.values,pd.read_csv(schemeData).values)

def scheme_preprocess(user_data,scheme_data):
    #user=user_data.reshape(1,-1)
    concatenation=np.concatenate((user_data,scheme_data[:,0:3]))
    ct=ColumnTransformer(transformers=[('encoder',OneHotEncoder(),[1,2])],remainder='passthrough')
    encoded_data=ct.fit_transform(concatenation)
    #print(encoded_data)
    similarity_id=pd.DataFrame({"id":[],"similarity":[]})
    #print(scheme_data)

    similarity=cosine_similarity(encoded_data[0].reshape(1,-1),encoded_data[1:])

    similarity_id["id"]=scheme_data[:,0]
    similarity_id["name"]=scheme_data[:,3]
    similarity_id["link"]=scheme_data[:,4]
    similarity_id["similarity"]=similarity[0]

    #sorts the dataframe in descending order and returns. Specify the number of rows to be returned
    top=similarity_id.sort_values(by="similarity",ascending=False,inplace=False)
    return {
        "scheme1":{"id":top.iloc[0,0],"scheme_name":top.iloc[0,2],"scheme_link":top.iloc[0,3]},
        "scheme2":{"id":top.iloc[1,0],"scheme_name":top.iloc[1,2],"scheme_link":top.iloc[1,3]},
        "scheme3":{"id":top.iloc[2,0],"scheme_name":top.iloc[2,2],"scheme_link":top.iloc[2,3]},
        "scheme4":{"id":top.iloc[3,0],"scheme_name":top.iloc[3,2],"scheme_link":top.iloc[3,3]},
        "scheme5":{"id":top.iloc[4,0],"scheme_name":top.iloc[4,2],"scheme_link":top.iloc[4,3]}
    }

#print(handler(4,5))
