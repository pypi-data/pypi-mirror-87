# creates the base table with NLU references
# each nlu references will be run later to generate model_meta
def generate_base():

    # 1. create meta file for all classes
    # 2. Create meta file for all open source models
    # 3. create meta file for all licenced classes
    # 4. create meta file for all licenced models
    import nlu
    import sparknlp
    sparknlp.start()
    import pandas as pd


    data = {
        'model_name':[],
        'model_lang':[],
        'model_upstream_deps':[],
        'model_class':[],
        'model_dataset':[],
        'labels':[],
        'reference_url':[],
        'model_author':[],
        'model_repo':[],
        'nlu_ref':[],
        'nlu_reference_aliases':[],
        'type':[], # model or pipe
        'consists_of':[], #if pipe, list of nlp references to the components or class references or so
        'satisfied_with_classes': [], # list of NLP annotator classes that must be resent in pipeline to get outputs
    }
    # I could get the printSchema() output
    # I could also get predictions output


    # raw_s3_path= './tmp/doc_generation/input_data/models_metadata_s3_raw.csv'
    # raw_s3_path = 'tmp/doc_generation/input_data/models_metadata_s3_raw.csv'
    raw_s3_path = './input_data/models_metadata_s3_raw.csv'
    model_df = pd.read_csv(raw_s3_path)
    model_df_copy = model_df.copy()
    print(model_df)
    model_df['nlu_ref'] =''
    import gc

    not_found_count = 0
    for  row in model_df_copy.itertuples():
        del nlu
        import nlu

        nlu.active_pipes.clear()
        gc.collect()
        found=False
        idx = row.Index
        model_df.iloc[idx]['nlu_ref'] = ''
        nlp_ref_target = row.name
        lang = row.language
        is_model = False
        is_pipe = False
        nlp_version = model_df.iloc[idx]['compatibility']
        # check models
        if lang in nlu.namespace.NameSpace.pretrained_models_references.keys():
            for nlu_ref, nlp_ref in nlu.namespace.NameSpace.pretrained_models_references[lang].items():
                if nlp_ref == nlp_ref_target:
                    model_df.at[idx, 'nlu_ref'] = nlu_ref
                    # model_df.iloc[idx]['nlu_ref'] = nlu_ref
                    found = True
                    is_model = True

        # check pipes
        if found == False and lang in nlu.namespace.NameSpace.pretrained_pipe_references.keys():
            for nlu_ref, nlp_ref in nlu.namespace.NameSpace.pretrained_pipe_references[lang].items():
                if nlp_ref == nlp_ref_target:
                    model_df.at[idx, 'nlu_ref'] = nlu_ref
                    # model_df.iloc[idx]['nlu_ref'] = nlu_ref
                    found = True
                    is_pipe = True

        if found == False :
            not_found_count +=1
            if nlp_version== '2.6.2': model_df.at[idx, 'nlu_ref'] = '<<<<NOT FOUND BECAUSE V2.6.2>>>>'
            else :  model_df.at[idx, 'nlu_ref'] = '<<<<NOT FOUND >>>>'
            print(f"Could not find nlu ref for nlp_ref_target = {nlp_ref_target}  for lang = {lang} , not found count sofar = {not_found_count}")
        else :
            # we will download the model or pipe via NLU
            if is_pipe: pass
            elif is_model:
                # nlu_pipe = nlu.load(nlu_ref)
                model_class = ''
                model_stor_ref = ''
                model_dataset = ''
                labels = ''
                type ='model'
                consists_of = []
                can_be_satisfied_with_classes = []
                nlu.active_pipes.clear()
                # del nlu_pipe

    print(model_df.columns)
    print(model_df_copy.columns)

    model_df.to_csv('./generated_data/models_base_generated.csv')

def generate_model_meta_base_table():
    import pandas as pd
    print("GENERATING BASE NESTED")
    generate_base()
    print("DONE BASE NESTED")

    models_df = pd.read_csv('./generated_data/models_base_generated.csv')
    models_df['model_class'] = 'TODO'
    models_df['model_upstream_deps'] = 'TODO'
    models_df['model_dataset'] = 'TODO'
    models_df['labels'] = 'TODO'
    # models_df['type'] = 'handled by previous method' #  model or pipe
    models_df['consists_of'] = 'TODO'  # if pipe, list of nlp references to the components or class references or so
    models_df[
        'can_be_satisfied_with_classes'] = 'TODO'  # list of NLP annotator classes that must be resent in pipeline to get outputs
    models_df['input_prediction_sample'] = 'TODO'  # some data to feed the annotator to get sample results
    models_df['output_schema'] = 'TODO'  # df.printSchema()
    models_df['result_selection'] = 'TODO'  # df.select('something').show()
    models_df['reference_url'] = 'TODO'
    models_df['model_author'] = 'TODO'
    models_df['model_repo'] = 'TODO'
    models_df['nlu_type'] = 'TODO'  # the embelishment NLU uses, useful for tags and seo
    models_df['nlu_input_columns'] = 'todo'
    models_df['nlu_output_columns'] = 'todo'
    models_df['nlp_input_columns'] = 'todo'
    models_df['nlp_output_columns'] = 'todo'
    models_df['nlu_predictions'] = 'todo'
    models_df['nlu_predictions_markdown'] = 'todo'
    models_df['nlp_pipeline_code'] = 'todo'

    models_df.to_csv('./generated_data/models_generated_with_meta.csv',index=False)

def gen_model_generation_params_file(pretrained_model_cache_path = '/home/loan/cache_pretrained'):
    # call initially once to generate parameters for the sh file
    import pandas as pd
    models_df = pd.read_csv('./generated_data/models_base_generated.csv')
    models = []
    for idx, row in models_df.iterrows():models.append((row['nlu_ref'],idx))

    with open('./generated_data/model_gen_params.txt', 'w') as file:
        for mod in models :
            file.write(str(mod[0] )+ ' ' + str(mod[1]) + ' ' + pretrained_model_cache_path)
            file.write('\n')
        file.close()
def generate(pretrained_model_cache_path = '/home/loan/cache_pretrained'):
    print('STARTING WITH BASE META')
    generate_model_meta_base_table()
    print('DONE WITH BASE META')
    print('STARTING WITH PARAMS FILE  AND SH JOBS')
    gen_model_generation_params_file(pretrained_model_cache_path)
    import os
    print("STARTING SH JOB")
    cmd = 'sh gen_docs.sh'# &> big_run.txt'
    os.system(cmd)