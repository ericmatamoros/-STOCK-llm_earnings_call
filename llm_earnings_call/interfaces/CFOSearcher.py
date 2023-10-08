"""Class to search for CFO interventions on the earnings call."""
import pandas as pd
import numpy as np
import spacy
import multiprocessing
import concurrent.futures

N_THREADS = multiprocessing.cpu_count() - 2

def process_row(row, earnings_col, nlp):
    return CFOSearcher.get_cfo_name(row[earnings_col], nlp)

class CFOSearcher:
    def __init__(self, df: pd.DataFrame, earnings_col: str) -> None:
        self._df = df
        self._earnings_col = earnings_col
        self._nlp = spacy.load('en_core_web_sm')


    def get_cfo_name(text: str, nlp):

            if len(text.split("Chief Financial Officer")) > 1:
                min_lower = min(len(text.split("Chief Financial Officer")[0].split(" ")) , 10)
                min_upper = min(len(text.split("Chief Financial Officer")[1].split(" ")) , 10)
                text_pre = nlp(' '.join(text.split("Chief Financial Officer")[0].split(" ")[-min_lower:-1]))
                text_post = nlp(' '.join(text.split("Chief Financial Officer")[1].split(" ")[0:min_upper]))
                min_lower = min(min_lower, 5)
                min_upper = min(min_upper, 5)
                between = nlp(' '.join(text.split("Chief Financial Officer")[0].split(" ")[-min_lower:-1]) + " Chief Financial Officer " + ' '.join(text.split("Chief Financial Officer")[1].split(" ")[0:min_upper]))      

            elif len(text.split("CFO")) > 1:
                min_lower = min(len(text.split("CFO")[0].split(" ")) , 10)
                min_upper = min(len(text.split("CFO")[1].split(" ")) , 10)
                text_pre = nlp(' '.join(text.split("CFO")[0].split(" ")[-min_lower:-1]))
                text_post = nlp(' '.join(text.split("CFO")[1].split(" ")[0:min_upper]))
                min_lower = min(min_lower, 5)
                min_upper = min(min_upper, 5)
                between = nlp(' '.join(text.split("CFO")[0].split(" ")[-min_lower:-1]) + " CFO " + ' '.join(text.split("CFO")[1].split(" ")[0:min_upper]))      

            else:
                text_pre = []
                text_post = []
                between = []

            if len(text_pre) == 0:
                return []
            
            element_list = []
            label_list = []
            for word in text_pre.ents:
                element_list.append(word.text)
                label_list.append(word.label_)


            for word in text_post.ents:
                element_list.append(word.text)
                label_list.append(word.label_)

            for word in between.ents:
                element_list.append(word.text)
                label_list.append(word.label_)

            df = pd.DataFrame({'element': element_list, 'label': label_list})
            df['count'] = 1

            # Times names appear in dataframe
            df['count'] = df.groupby(['element'])['count'].transform(np.sum)

            # Count of words & letters
            thr_letter = 6

            if df.shape[0] == 0:
                return []

            for i in range(0, df.shape[0]):
                df.loc[i, 'n_words'] = len(df['element'][i].split(' '))
                df.loc[i, 'n_letters'] = len(df['element'][i])

            df.sort_values('count', inplace = True, ascending=False)
            
            if df.loc[(df['label'] == 'PERSON') & (df['n_letters'] >= thr_letter),].shape[0] == 0:
                return []

            return np.array(df.loc[(df['label'] == 'PERSON') & (df['n_letters'] >= thr_letter), 'element'])[0]


    def get_cfo_info(self):
        df_nlp = self._df
        df_nlp['cfo'] = df_nlp.apply(lambda row: process_row(row, self._earnings_col, self._nlp),axis = 1)

        self._df = df_nlp

    # Get CFO interventions
    def get_full_cfo_interventions(self):
        def get_cfo_intervention(df: pd.DataFrame, earnings_col: str, cfo_name: str = 'cfo') -> pd.DataFrame:
            cfo = np.array(df[cfo_name])[0]
            text = np.array(df[earnings_col])[0]
            splitted_text = text.split("\n")
            
            if len(cfo) == 0:
                df['cfo_interventions'] = ''
                return df

            complete_cfo = []

            for i in range(0, len(splitted_text)):
                not_found = False
                if len(splitted_text[i].split(cfo + ":")) > 1:
                    not_found = True
                    
                if not_found == True:
                    complete_cfo.append(splitted_text[i])
                        
            df['cfo_interventions'] = ' '.join(complete_cfo)
                        
            return df

        with concurrent.futures.ProcessPoolExecutor(max_workers=N_THREADS) as executor:
            df = self._df.groupby(['ticker', 'date']).apply(lambda x: get_cfo_intervention(x, self._earnings_col, 'cfo'))

        return df