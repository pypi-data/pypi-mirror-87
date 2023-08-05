import pandas as pd
import nlu

def df_to_pretty_markdown(df,max_len =  50):
    '''
    Truncates every cell content to max len and then calls .to_markdown() on the table
    Especially usefull for embeddings, which are very long.
    :param df: pandas dataframe to convert
    :param max_len: max cell len when converter to str.
    :return:
    '''

    for idx, row in df.iterrows():
        for c in df.columns:
            cell = str(df.iloc[idx][c])
            # df.loc[j][i] = str(df.loc[j][i])[:max_len] + '..]'
            if len(str(cell)) > max_len :
                # todo case dependent suffix for soecufuc datatypes>?
                df.loc[idx][c] = cell[:max_len] + ',..]'
    return df.to_markdown()
# 1. After generating pandas DF, go through every Cell and Cast it to String
# 2. If len(string(cell) > Max_len ->  cell = string(cell)[:max_len].append('..]')    # only ] if it was aray type like embeds
# #
# print("SENTENCE LEVEL :")
# df = nlu.load('sentiment',verbose=True).predict(['I hate no docs. I love the modelshub.',' I am so sad because sadness is life','I love good docs! I love good examples! I hate no docs',  ], metadata=True, positions=True, output_level='sentence', drop_irrelevant_cols=False)
# print(df_to_pretty_markdown(df))
# df = nlu.load('spam',verbose=True).predict(['I love the modelshub. I am so sad because sadness is life.','I love good docs! I love good examples! I hate no docs',  ], metadata=True, positions=True, output_level='sentence', drop_irrelevant_cols=False )
# print(df_to_pretty_markdown(df))
# df = nlu.load('questions',verbose=True).predict(['I love the modelshub. I am so sad because sadness is life.','I love good docs! I love good examples! I hate no docs',  ], metadata=True, positions=True, output_level='sentence' , drop_irrelevant_cols=False)
# print(df_to_pretty_markdown(df))
#
#
# print("DOCUMENT LEVEL :")
# df = nlu.load('emotion',verbose=True).predict(['I love the modelshub. I am so sad because sadness is life.','I love good docs! I love good examples! I hate no docs',  ], metadata=True, positions=True, output_level='document', drop_irrelevant_cols=False)
# print(df_to_pretty_markdown(df))
# df = nlu.load('spam',verbose=True).predict(['I love the modelshub. I am so sad because sadness is life.','I love good docs! I love good examples! I hate no docs',  ], metadata=True, positions=True, output_level='document', drop_irrelevant_cols=False )
# print(df_to_pretty_markdown(df))
# df = nlu.load('questions',verbose=True).predict(['I love the modelshub. I am so sad because sadness is life.','I love good docs! I love good examples! I hate no docs',  ], metadata=True, positions=True, output_level='document' , drop_irrelevant_cols=False)
# print(df_to_pretty_markdown(df))


# print("TOKEN LEVEL :")
# df = nlu.load('emotion',verbose=True).predict(['I love the modelshub. I hate bad code it is so bad and negative.','I love good docs! I love good examples! I hate no docs',  ], metadata=True, positions=True, output_level='token', drop_irrelevant_cols=False)
# print(df_to_pretty_markdown(df))
# df = nlu.load('spam',verbose=True).predict(['I love the modelshub. I hate bad code it is so bad and negative.','I love good docs! I love good examples! I hate no docs',  ], metadata=True, positions=True, output_level='token', drop_irrelevant_cols=False )
# print(df_to_pretty_markdown(df))
# df = nlu.load('questions',verbose=True).predict(['I love the modelshub. I hate bad code it is so bad and negative.','I love good docs! I love good examples! I hate no docs',  ], metadata=True, positions=True, output_level='token' , drop_irrelevant_cols=False)
# print(df_to_pretty_markdown(df))
#


#
# print("SENTENCE LEVEL META FALSE:") # BUGGY cpmfodemce
# df = nlu.load('emotion',verbose=True).predict(['I love the modelshub. I hate bad code it is so bad and negative.','I love good docs! I love good examples! I hate no docs',  ], metadata=False, positions=False, output_level='sentence', drop_irrelevant_cols=True)
# print(df_to_pretty_markdown(df))
# df = nlu.load('spam',verbose=True).predict(['I love the modelshub. I hate bad code it is so bad and negative.','I love good docs! I love good examples! I hate no docs',  ], metadata=False, positions=False, output_level='sentence', drop_irrelevant_cols=True )
# print(df_to_pretty_markdown(df))
# df = nlu.load('questions',verbose=True).predict(['I love the modelshub. I hate bad code it is so bad and negative.','I love good docs! I love good examples! I hate no docs',  ], metadata=False, positions=False, output_level='sentence' , drop_irrelevant_cols=True)
# print(df_to_pretty_markdown(df))


print("DOCUMENT LEVEL META FALSE:") # BIGGY ERRPR
df = nlu.load('emotion',verbose=True).predict(['I love the modelshub. I hate bad code it is so bad and negative.','I love good docs! I love good examples! I hate no docs',  ], metadata=False, positions=False, output_level='document', drop_irrelevant_cols=True)
print(df_to_pretty_markdown(df))
df = nlu.load('spam',verbose=True).predict(['I love the modelshub. I hate bad code it is so bad and negative.','I love good docs! I love good examples! I hate no docs',  ], metadata=False, positions=False, output_level='document', drop_irrelevant_cols=True )
print(df_to_pretty_markdown(df))
df = nlu.load('questions',verbose=True).predict(['I love the modelshub. I hate bad code it is so bad and negative.','I love good docs! I love good examples! I hate no docs',  ], metadata=False, positions=False, output_level='document' , drop_irrelevant_cols=True)
print(df_to_pretty_markdown(df))

#
# print("TOKEN LEVEL META FALSE:") # ?
# df = nlu.load('emotion',verbose=True).predict(['I love the modelshub. I hate bad code it is so bad and negative.','I love good docs! I love good examples! I hate no docs',  ], metadata=True, positions=False, output_level='token', drop_irrelevant_cols=True)
# print(df_to_pretty_markdown(df))
# df = nlu.load('spam',verbose=True).predict(['I love the modelshub. I hate bad code it is so bad and negative.','I love good docs! I love good examples! I hate no docs',  ], metadata=True, positions=False, output_level='token', drop_irrelevant_cols=True )
# print(df_to_pretty_markdown(df))
# df = nlu.load('questions',verbose=True).predict(['I love the modelshub. I hate bad code it is so bad and negative.','I love good docs! I love good examples! I hate no docs',  ], metadata=True, positions=False, output_level='token' , drop_irrelevant_cols=True)
# print(df_to_pretty_markdown(df))
