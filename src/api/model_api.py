from flask import Flask, jsonify, request 
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy 
import pickle

app = Flask(__name__)
api = Api(app)

# create same class as in the dev notebook
class RawFeats:
    def __init__(self, feats):
        self.feats = feats

    def fit(self, X, y=None):
        pass


    def transform(self, X, y=None):
        return X[self.feats]

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

#load model from pickle
model = pickle.load(open('lr_model.sav', 'rb'))

# create endpoint using POST request
class Scoring(Resource):
    def post(self):
        json_data = request.get_json()
        df = pd.DataFrame(json_data.values(), index=json_data.keys()).transpose()

        #get predictions form our model
        # it is much simpler because we used pipline during dev
        #res = model.predict_proba(df)
        res = model.predict(df)
        # we cannot send numpy array as a result
        return res.tolist()

#assign endpoint to our API
api.add_resource(Scoring, '/scoring')

# create ap when run file 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)