
def df_to_pretty_markdown(df,max_len =  50):
    '''
    Truncates every cell content to max len and then calls .to_markdown() on the table
    Especially usefull for embeddings, which are very long.
    :param df: pandas dataframe to convert
    :param max_len: max cell len when converter to str.
    :return:
    '''
    print('wring Markdown!')
    for idx, row in df.iterrows():
        for c in df.columns:
            cell = str(df.iloc[idx][c])
            if len(str(cell)) > max_len :
                df.loc[idx][c] = cell[:max_len] + '..]'
    md = df.to_markdown()
    print('wring Markdown!',md)
    return md

# models_df = pd.read_csv('generated_data/models_generated_with_meta.csv')
def test_every_default_component(nlu_reference, id,pretrained_model_cache_path = '/home/loan/cache_pretrained'):
    import os
    from os import path
    import pandas as pd


    # __file__ should be defined in this case
    PARENT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.append(PARENT_DIR)
    conf_path = os.getcwd()
    sys.path.append(conf_path)
    #rm  old models to safe us from full hdd
    PARENT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.append(PARENT_DIR)
    conf_path = os.getcwd()
    sys.path.append(conf_path)
    sys.path.append('/home/loan/Documents/freelancework/jsl/nlu/4realnlugit/tmp/doc_generation')
    if path.exists (os.path.expanduser(pretrained_model_cache_path)): os.system('rm -r ' + pretrained_model_cache_path)

    import generate_pipe_code as pipe_code_generator
    import nlu

    import gc
    id = int(id)
    print('testing', nlu_reference)
    if 'NOT FOUND' in nlu_reference :
        print('Skipping for nlu ref with id ', id)
        return

    string_to_predict = 'John Snow Labs offers over 300 models in over 40 languages to solve a variety of NLP problems while keeping the highest accuracy.'

    models_df = pd.read_csv('./tmp/doc_generation/generated_data/models_generated_with_meta.csv')

    print(f'Test NLU_REF={nlu_reference}')
    nlu_component_pipe = nlu.load(nlu_reference,verbose=True)
    nlu_component = nlu.parse_component_data_from_name_query(nlu_reference)
    if type (nlu_component ) is type([]):
        #pipe handling
        models_df.at[id, 'model_class'] =  'PretrainedPipeline'
        models_df.at[id, 'model_upstream_deps'] = [c.model.extractParamMap()[c.model.storageRef] for c in nlu_component_pipe.pipe_components if any ([ 'storageRef' in str(d) for d in c.model.extractParamMap().keys() ] ) ] # [c.model.extractParamMap()[c.model.storageRef] for c in nlu_component_pipe.pipe_components] #'Pipe storage dependencies already met']
        models_df.at[id, 'consists_of'] = [m.model.__class__.name for m in nlu_component]
        models_df.at[id, 'can_be_satisfied_with_classes'] = [c.model.__class__.name for c in nlu_component_pipe.pipe_components]
        models_df.at[id, 'type'] = 'pipeline'
        models_df.at[id, 'nlu_type'] = 'pipeline'
        models_df.at[id, 'nlu_input_columns'] = [c.component_info.inputs for c in nlu_component_pipe.pipe_components]
        models_df.at[id, 'nlu_output_columns'] = [c.component_info.outputs for c in nlu_component_pipe.pipe_components]
        models_df.at[id, 'nlp_input_columns'] = [c.component_info.spark_input_column_names for c in nlu_component_pipe.pipe_components]
        models_df.at[id, 'nlp_output_columns'] =  [c.component_info.spark_output_column_names for c in nlu_component_pipe.pipe_components]
        models_df.at[id, 'nlu_predictions'] = nlu_component_pipe.predict(string_to_predict, metadata=True, positions=True, output_level='document', drop_irrelevant_cols=False)
        models_df.at[id, 'nlu_predictions_markdown'] = df_to_pretty_markdown(nlu_component_pipe.predict(string_to_predict, metadata=True, positions=True, output_level='document', drop_irrelevant_cols=False))
        models_df.at[id, 'nlp_pipeline_code'] = pipe_code_generator.generate_py_code_for_nlu_ref_or_pipe(nlu_ref,nlu_component_pipe)

    else :
        # get metdata for single model
        models_df.at[id, 'model_class'] =  nlu_component.model.__class__.name
        if any ([ 'storageRef' in str(d) for d in nlu_component.model.extractParamMap().keys() ] ) : models_df.at[id, 'model_upstream_deps'] = nlu_component.model.extractParamMap()[nlu_component.model.storageRef]
        else : models_df.at[id, 'model_upstream_deps'] = "Has no upstream dependencies"
        models_df.at[id, 'consists_of'] =  nlu_component.model.__class__.name
        models_df.at[id, 'can_be_satisfied_with_classes'] =  [c.model.__class__.name for c in nlu_component_pipe.pipe_components]
        models_df.at[id, 'type'] = 'model'
        models_df.at[id, 'nlu_type'] = nlu_component.component_info.type
        models_df.at[id, 'nlu_input_columns'] = nlu_component.component_info.inputs
        models_df.at[id, 'nlu_output_columns'] = nlu_component.component_info.outputs
        models_df.at[id, 'nlp_input_columns'] = nlu_component.component_info.spark_input_column_names
        models_df.at[id, 'nlp_output_columns'] = nlu_component.component_info.spark_output_column_names
        models_df.at[id, 'nlu_predictions'] = nlu_component_pipe.predict(string_to_predict,metadata=True, positions=True, output_level='document', drop_irrelevant_cols=False)
        models_df.at[id, 'nlu_predictions_markdown'] = df_to_pretty_markdown(nlu_component_pipe.predict(string_to_predict,metadata=True, positions=True, output_level='document', drop_irrelevant_cols=False))
        models_df.at[id, 'nlp_pipeline_code'] = pipe_code_generator.generate_py_code_for_nlu_ref_or_pipe(nlu_ref,nlu_component_pipe)


    models_df.to_csv('./tmp/doc_generation/generated_data/models_generated_with_meta.csv',index=False)

    print('TESTING DONE FOR NLU REFERENCE : ', nlu_reference)







import sys
print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))
nlu_ref = sys.argv[1]
id = sys.argv[2]
pretrained_model_cache_path =  sys.argv[3]
test_every_default_component(nlu_ref,id,pretrained_model_cache_path)
