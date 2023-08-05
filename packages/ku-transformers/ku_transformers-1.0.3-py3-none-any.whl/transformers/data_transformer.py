from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
import pandas as pd

class DataTransformer(BaseEstimator, TransformerMixin):
    
    NB_PREVIOUS_RATINGS_KEY = "nb_previous_ratings"
    AVG_RATINGS_PREVIOUS_KEY = "avg_ratings_previous"
    USER_ID_KEY = "userId"
    MOVIE_ID_KEY = "movieId"
    RATING_KEY = "rating"
    TIMESTAMP_KEY = "timestamp"
    
    def __init__(self, db):
        self.db = db

    def fit(self, db):
        return self
    
    def transform(self, X, y=None):
        
        df_transformed = pd.DataFrame([],columns=[self.NB_PREVIOUS_RATINGS_KEY, self.AVG_RATINGS_PREVIOUS_KEY])
        for index, row in X.iterrows():
            
            user_id = row[self.USER_ID_KEY]
            movie_id = row[self.MOVIE_ID_KEY]
            features = self._get_features(user_id, movie_id)
            a = features[self.NB_PREVIOUS_RATINGS_KEY]
            b = features[self.AVG_RATINGS_PREVIOUS_KEY]
            s = pd.Series([a, b],index=[self.NB_PREVIOUS_RATINGS_KEY, self.AVG_RATINGS_PREVIOUS_KEY])
            df_transformed = df_transformed.append(s,ignore_index=True)
            
        return df_transformed
    
    def _get_features(self, user_id, movie_id):
        user_ratings = self.db.loc[self.db.userId == user_id]
        idx_max = user_ratings[self.NB_PREVIOUS_RATINGS_KEY].idxmax()
        return self.db.iloc[idx_max]