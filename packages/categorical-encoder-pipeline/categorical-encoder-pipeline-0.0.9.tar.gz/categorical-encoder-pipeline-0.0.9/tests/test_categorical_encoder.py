from categorical_encoder import CategoricalEncoder
import unittest
import pandas as pd
import numpy as np

class TestCategoricalEncoder(unittest.TestCase):
    
    def test_basic(self):
        df = [
            {'col1':'papa', 'col2':'pepe'},
            {'col1':'pepe', 'col2':'papa'},
            {'col1':'pipi', 'col2':'pipi'},
            {'col1':'papa', 'col2':'popo'},
        ]

        df = pd.DataFrame(df)
        enc = CategoricalEncoder(columns=['col1', 'col2'])
        res = enc.fit_transform(df)
        self.assertEquals(list(res['col1']), [0, 1, 2, 0])

    def test_missings_replace(self):
        df1 = [
            {'col1':'papa', 'col2':'pepe'},
            {'col1':'pepe', 'col2':'papa'},
            {'col1':'pipi', 'col2':'pipi'},
            {'col1':np.nan, 'col2':'popo'},
        ]

        df2 = [
            {'col1':'papa', 'col2':np.nan},
            {'col1':'popp', 'col2':np.nan},
            {'col1': np.nan, 'col2':np.nan},
        ]

        # replace strategy
        enc = CategoricalEncoder(columns=['col1', 'col2'], missing_value=-1, null_strategy='replace')
        res1 = enc.fit_transform(pd.DataFrame(df1))
        res2 = enc.transform(pd.DataFrame(df2))

        self.assertEquals(list(res1['col1']), [0, 1, 2, -1])
        self.assertEquals(list(res2['col1']), [0, -1, -1])
        self.assertEquals(list(res2['col2']), [-1, -1, -1])

    def test_missings_ignore(self):
        df1 = [
            {'col1':'papa', 'col2':'pepe'},
            {'col1':'pepe', 'col2':'papa'},
            {'col1':'pipi', 'col2':'pipi'},
            {'col1':np.nan, 'col2':'popo'},
        ]

        df2 = [
            {'col1':'papa', 'col2':np.nan},
            {'col1':'popp', 'col2':np.nan},
            {'col1': np.nan, 'col2':np.nan},
        ]

        enc = CategoricalEncoder(columns=['col1', 'col2'], missing_value=-1, null_strategy='ignore')
        res1 = enc.fit_transform(pd.DataFrame(df1))
        res2 = enc.transform(pd.DataFrame(df2))

        assert(pd.isnull(list(res1['col1'])[-1]))
        assert(all([pd.isnull(el) for el in list(res2['col1'])[2:] ]))
        assert(all([pd.isnull(el) for el in list(res2['col2']) ]))


        
        
