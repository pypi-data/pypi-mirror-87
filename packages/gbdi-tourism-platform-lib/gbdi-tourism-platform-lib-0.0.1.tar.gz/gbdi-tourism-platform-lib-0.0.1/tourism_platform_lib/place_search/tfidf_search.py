import pandas as pd
import string
import numpy as np
from pythainlp.tokenize import word_tokenize
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from scipy import sparse

class TfidfScore():
    def __init__(self,all_attraction=None):
        # attractions = pandas dataframe which contains 'title' and 'article' columns to tokenize
        self.all_attraction = all_attraction
        if type(self.all_attraction) != type(None):
            self.all_attraction['_id'] = all_attraction['_id'].astype(str)
            self.all_attraction.reset_index(drop=True, inplace=True)

        
        #change to import from file or db
        self.stopwords = list(string.punctuation) + ['1','2','3','4','5','6','7','8','9','0'] + ['๑','๒','๓','๔','๕','๖','๗','๘','๙','๐']

        
        
    def prep(self):
        # take dataframe then tokenize and filter some tokens
        # weight title more than detail
        self.all_attraction['token'] = self.all_attraction['title'] + ' '  + self.all_attraction['title'] + ' ' + self.all_attraction['info']
        self.all_attraction['token'] = self.all_attraction['token'].astype(str)
        self.all_attraction['token'] = list(map(self.get_token,self.all_attraction['token']))
        
        
        self.all_attraction['token_bi'] = [self.get_n_gram(token,2) for token in self.all_attraction['token']]
        self.all_attraction['token_all'] = self.all_attraction['token'] + self.all_attraction['token_bi']

        
        
        # filter out short tokens
        self.all_attraction = self.all_attraction[[True if len(row) >= 4 else False for row in self.all_attraction['token']]]
        self.all_attraction = self.all_attraction[[True if len(str(row)) >= 4 else False for row in self.all_attraction['info']]]
        self.all_attraction = self.all_attraction[[True if len(str(row)) >= 4 else False for row in self.all_attraction['title']]]
        self.all_attraction = self.all_attraction.reset_index(drop=True)

        
        
        # tfidf vector function
        #indentation fixed
        tfidf_vectorizer = TfidfVectorizer(
        analyzer='word',
        tokenizer=lambda x: x,
        preprocessor=lambda x: x,
        token_pattern=None,
        use_idf=True)  

        
        
        docs = list(self.all_attraction['token_all'])
        tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(docs)
        tfidf_word = tfidf_vectorizer.get_feature_names()
        tfidf_word_dict = dict(zip(tfidf_word,range(len(tfidf_word))))

        
        
        # filter low tfidf score
        tfidf_filter = tfidf_vectorizer_vectors
        tfidf_filter.data = np.where(tfidf_filter.data < 0.1, 0, tfidf_filter.data)

        #
        
        #new store object values
        # id reference
        self.all_attraction_id_ref = pd.DataFrame({'_id':list(self.all_attraction['_id'])}).reset_index(drop=True)
        self.all_attraction_id_ref['_id'] = self.all_attraction_id_ref['_id'].astype(str)
        self.tfidf_word_dict = tfidf_word_dict
        self.tfidf_filter = tfidf_filter   
        
        
    def save_model(self, filename):
        #save tfidf_filter
        #np.savez(filename+'_tfidf_filter.npz', data=self.tfidf_filter.data, indices=self.tfidf_filter.indices,
        #         indptr=self.tfidf_filter.indptr, shape=self.tfidf_filter.shape)
        sparse.save_npz(filename+'_tfidf_filter.npz', self.tfidf_filter)
        
        
        #save tfidf_word_dict
        with open(filename + "_tfidf_word_dict.pkl","wb") as f:
            pickle.dump(self.tfidf_word_dict,f)
            f.close()
            
        self.all_attraction_id_ref.to_json(filename+"_all_attraction_id_ref.json", orient='split')
        
        self.all_attraction.to_json(filename+"_all_attraction.json", orient='split')
        
        return None
        
        

    def load_model(self, filename):
        self.tfidf_filter = sparse.load_npz(filename+'_tfidf_filter.npz')
        
        with open(filename+'_tfidf_word_dict.pkl', 'rb') as f:
            self.tfidf_word_dict = pickle.load(f)
        
        self.all_attraction_id_ref = pd.read_json(filename+'_all_attraction_id_ref.json', orient='split').reset_index(drop=True)
        self.all_attraction_id_ref['_id'] = self.all_attraction_id_ref['_id'].astype(str)
        
        self.all_attraction = pd.read_json(filename+"_all_attraction.json", orient='split').reset_index(drop=True)
        self.all_attraction['_id'] = self.all_attraction['_id'].astype(str)
        
        return None

    def clean_text(self,text):
        list_char = list(text)
        list_clean = [char for char in list_char if char not in self.stopwords]
        text_clean = ''.join(list_clean)
        text_clean = ' '.join(text_clean.split())
        return text_clean

    def get_token(self,text):
        text = self.clean_text(text)
        text_token = word_tokenize(text)
        text_token = list(filter(lambda lst: lst != ' ', text_token))
        text_token = [word.strip() for word in text_token]
        return text_token

    def get_n_gram(self,list_text,n):
        return [''.join(pair_text) for pair_text in list(nltk.ngrams(list_text, n))]

    def get_tfidf_score(self,list_token,tfidf_dict,tfidf_vec):
        # get dict id
        token_id = list(map(tfidf_dict.get,list_token))
        # keep only unique element and remove 'None'
        token_id = [x for x in list(set(token_id)) if x is not None]
        if len(token_id) > 0:
            # sum score
            tfidf_score = 0
            for each_id in token_id:
                tfidf_score = tfidf_score + tfidf_vec[:,each_id]
            tfidf_score = tfidf_score.tocoo()
            tfidf_score = dict(zip(tfidf_score.row,tfidf_score.data))    
            tfidf_score = pd.DataFrame(tfidf_score.items())
            tfidf_score.columns = ['id', 'score']
            # make top score as 1
            tfidf_score['score'] = tfidf_score['score']/tfidf_score['score'].max()
            return tfidf_score
        # there is no index that match
        else:
            return pd.DataFrame({'id':[],'score':[]})  

    def get_exact_match_score(self,text,list_to_match):
        # in case of None
        list_to_match = list(map(str, list_to_match))
        # get index of string in list_to_match
        match_index = [i for i,val in enumerate(list_to_match) if text in val]
        # find attraction ids with their score
        if len(match_index) > 0:
            match_dict = dict(zip(match_index,[1]*len(match_index)))
            match_table = pd.DataFrame(match_dict.items())
            match_table.columns = ['id', 'score']
            return match_table
        # there is no index that match
        else:
            return pd.DataFrame({'id':[],'score':[]})  

    def smart_search(self,attraction_data_input,search_input):
        self.attraction_data_input = attraction_data_input
        self.search_input = search_input
        
        # token string
        text_clean = self.clean_text(self.search_input)
        list_token = [text_clean] + self.get_token(text_clean)
        # tfidf
        tfidf = self.get_tfidf_score(list_token, self.tfidf_word_dict, self.tfidf_filter)
        tfidf['score'] = tfidf['score']*0.2
        # exact match
        exact_title = self.get_exact_match_score(list_token[0],list(self.all_attraction['title']))
        exact_title['score'] = exact_title['score']*0.5
        exact_info = self.get_exact_match_score(list_token[0],list(self.all_attraction['info']))
        exact_info['score'] = exact_info['score']*0.3
        # final result
        result = pd.concat([tfidf,exact_title,exact_info])
        result = result.groupby(['id']).sum()

        result_join_ref = pd.merge(self.all_attraction_id_ref,result, right_on = 'id', left_index = True)
        result_join_ref = pd.DataFrame(result_join_ref.to_records())
        result_join_input = pd.merge(self.attraction_data_input,result_join_ref, how = 'left', on = '_id').sort_values("score",ascending=False)
        del result_join_input['id']
        return result_join_input