import pytest

import pandas as pd
'''
This takes the model_meta_generated.csv which should have the nlu_references from the 
model_base_table_creator.py

It will load every nlu reference and infer all possible metadata
It needs to be a pytest, so we can leverage the memory resets between tests and we dont OOM ourselves

'''

'''

'''
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
                df.loc[idx][c] = cell[:max_len] + '..]'
    return df.to_markdown()


models_df = pd.read_csv('../generated_data/models_generated.csv')
models = []
models_df['model_class'] = 'TODO'
models_df['model_upstream_deps'] = 'TODO'
models_df['model_dataset'] = 'TODO'
models_df['labels'] = 'TODO'
# models_df['type'] = 'handled by previous method' #  model or pipe
models_df['consists_of'] = 'TODO' #if pipe, list of nlp references to the components or class references or so
models_df['can_be_satisfied_with_classes'] = 'TODO' # list of NLP annotator classes that must be resent in pipeline to get outputs
models_df['input_prediction_sample'] = 'TODO' # some data to feed the annotator to get sample results
models_df['output_schema'] = 'TODO' #df.printSchema()
models_df['result_selection'] = 'TODO' # df.select('something').show()
models_df['reference_url'] = 'TODO'
models_df['model_author'] = 'TODO'
models_df['model_repo'] = 'TODO'
models_df['nlu_type'] = 'TODO' # the embelishment NLU uses, useful for tags and seo
models_df['nlu_input_columns'] = 'todo'
models_df['nlu_output_columns'] = 'todo'
models_df['nlp_input_columns'] = 'todo'
models_df['nlp_output_columns'] = 'todo'
models_df['nlu_predictions'] = 'todo'
models_df['nlu_predictions_markdown'] = 'todo'

#setup list of parameters we want to call
for idx, row in models_df.iterrows():models.append((row['nlu_ref'],idx))


print(models_df.columns)

models_df.to_csv('./models_generated_with_meta.csv',index=False)

del models_df

# to_skip = 15 # 16,17 bad because portugese bert not public

# BAD : 167,
# None existend PT bert, NER
to_skip = 10

import multiprocessing as mp
import resource



def run_component(nlu_reference, id):
    import nlu
    import gc
    id = int(id)
    # if 'embed' in nlu_reference : return
    # if id <= to_skip or id %2 == 0 : return
    print('testing', nlu_reference)
    if 'NOT FOUND' in nlu_reference :
        print('PASSING NLU REFERENCE FOR IDX', id)
        return

    # string_to_predict = 'John Snow Labs ofers over 300 models in over 40 languages to solve a variety of NLP problems while keeping the highest accuracy.'
    #
    # models_df = pd.read_csv('generated_data/models_generated_with_meta.csv')

    #TODO add temporary model cleanup in /tmp
    print(f'Test NLU_REF={nlu_reference}')
    # if id < skip_to_test : return
    # nlu_pipe = nlu.load(nlu_ref)
    #get component
    # nlu.load('tokenize',verbose=True)
    nlu_component_pipe = nlu.load(nlu_reference,verbose=True)

    # ## TODO, lemma and other model-free annotators have no model attribute and cause crahes (?)
    # nlu_component = nlu.parse_component_data_from_name_query(nlu_reference)
    # if type (nlu_component ) is type([]):
    #     #pipe handling
    #     models_df.at[id, 'model_class'] =  'PretrainedPipeline'
    #     models_df.at[id, 'model_upstream_deps'] = [c.model.extractParamMap()[c.model.storageRef] for c in nlu_component_pipe.pipe_components if any ([ 'storageRef' in str(d) for d in c.model.extractParamMap().keys() ] ) ] # [c.model.extractParamMap()[c.model.storageRef] for c in nlu_component_pipe.pipe_components] #'Pipe storage dependencies already met']
    #     models_df.at[id, 'consists_of'] = [m.model.__class__.name for m in nlu_component]
    #     models_df.at[id, 'can_be_satisfied_with_classes'] = [c.model.__class__.name for c in nlu_component_pipe.pipe_components]
    #     models_df.at[id, 'type'] = 'pipeline'
    #     models_df.at[id, 'nlu_type'] = 'pipeline'
    #     models_df.at[id, 'nlu_input_columns'] = [c.component_info.inputs for c in nlu_component_pipe.pipe_components]
    #     models_df.at[id, 'nlu_output_columns'] = [c.component_info.outputs for c in nlu_component_pipe.pipe_components]
    #     models_df.at[id, 'nlp_input_columns'] = [c.component_info.spark_input_column_names for c in nlu_component_pipe.pipe_components]
    #     models_df.at[id, 'nlp_output_columns'] =  [c.component_info.spark_output_column_names for c in nlu_component_pipe.pipe_components]
    #     models_df.at[id, 'nlu_predictions'] = nlu_component_pipe.predict(string_to_predict, metadata=True, positions=True, output_level='document', drop_irrelevant_cols=False)
    #     models_df.at[id, 'nlu_predictions_markdown'] = df_to_pretty_markdown(nlu_component_pipe.predict(string_to_predict, metadata=True, positions=True, output_level='document', drop_irrelevant_cols=False))
    #
    # else :
    #     # get metdata for single model
    #     models_df.at[id, 'model_class'] =  nlu_component.model.__class__.name
    #
    #     if any ([ 'storageRef' in str(d) for d in nlu_component.model.extractParamMap().keys() ] ) : models_df.at[id, 'model_upstream_deps'] = nlu_component.model.extractParamMap()[nlu_component.model.storageRef]
    #     else : models_df.at[id, 'model_upstream_deps'] = "Has no upstream dependencies"
    #     models_df.at[id, 'consists_of'] =  nlu_component.model.__class__.name
    #     models_df.at[id, 'can_be_satisfied_with_classes'] =  [c.model.__class__.name for c in nlu_component_pipe.pipe_components]
    #     models_df.at[id, 'type'] = 'model'
    #     models_df.at[id, 'nlu_type'] = nlu_component.component_info.type
    #     models_df.at[id, 'nlu_input_columns'] = nlu_component.component_info.inputs
    #     models_df.at[id, 'nlu_output_columns'] = nlu_component.component_info.outputs
    #     models_df.at[id, 'nlp_input_columns'] = nlu_component.component_info.spark_input_column_names
    #     models_df.at[id, 'nlp_output_columns'] = nlu_component.component_info.spark_output_column_names
    #     models_df.at[id, 'nlu_predictions'] = nlu_component_pipe.predict(string_to_predict,metadata=True, positions=True, output_level='document', drop_irrelevant_cols=False)
    #     models_df.at[id, 'nlu_predictions_markdown'] = df_to_pretty_markdown(nlu_component_pipe.predict(string_to_predict,metadata=True, positions=True, output_level='document', drop_irrelevant_cols=False))
    #
    #
    # models_df.to_csv('./models_generated_with_meta.csv',index=False)
    # nlu.spark.stop()
    # nlu.sparknlp.SparkSession._instantiatedContext = None
    # nlu.sparknlp.SparkSession._instantiatedSession = None


    for c in nlu_component_pipe.pipe_components : del c
    nlu_component_pipe.pipe_components.clear()
    nlu_component_pipe.clear()
    nlu.active_pipes.clear()
    del nlu
    # del nlu_component_pipe.spark_estimator_pipe
    # del nlu_component_pipe.spark_transformer_pipe
    # # nlu.clear() implement clean up method that deletes all pipes? basically clears dict and pipe list
    # print("DONE GOING TO NEXT MODLE")
    # del nlu_component
    # del models_df
    gc.collect()

    print('TESTING DONE FOR NLU REFERENCE : ', nlu_reference)
    import sys
    # sys.modules[__name__].__dict__.clear()



for mod in models :
    proc = mp.Process(target=run_component(mod[0], mod[1]))
    proc.start()
    proc.join()
    proc.terminate()
