import re
import numpy as np
from trell_ai_util import  S3Adapter
from sklearn.feature_extraction import DictVectorizer



class GenderPrediction:
    def __init__(self):
        self.m = S3Adapter.read_from_s3_bucket(bucket='data-science-datas',
                                               sub_bucket='models/',
                                               file_name='gender_prediction.pkl')
        self.model, self.names = self.m
        self.dv = DictVectorizer()
        self.include_features()

    # Using a custom function for feature analysis
    # By Analogy most female names ends in 'A' or 'E' or has the sound of 'A'

    def features(self, name):
        name = name.lower()
        return {
            'first-letter': name[0],  # First letter
            'first2-letters': name[0:2],  # First 2 letters
            'first3-letters': name[0:3],  # First 3 letters
            'last-letter': name[-1],
            'last2-letters': name[-2:],
            'last3-letters': name[-3:]
        }

    def include_features(self):
        # Vectorize the features function
        self.features = np.vectorize(self.features)

        # Including all the training features into testing names
        df_X = self.features(self.names)
        self.dv.fit_transform(df_X)
        my_xfeatures = self.dv.transform(df_X)
        print(my_xfeatures.shape)

    def gender(self, name):
        name = re.sub("[^a-zA-Z]+", " ", name)
        name = name.strip()
        name = name.split(' ')[0]
        sample_name_eg = [name]
        transform_dv = self.dv.transform(self.features(sample_name_eg))
        vect3 = transform_dv.toarray()
        a = self.model.predict(vect3)
        gender = 'male' if (a == 1) else 'female'
        prob = self.model.predict_proba(vect3)
        attribute = {"first_name": name,
                     "gender": gender, "probability": round(float(prob[0][a][0]), 4)}
        return attribute