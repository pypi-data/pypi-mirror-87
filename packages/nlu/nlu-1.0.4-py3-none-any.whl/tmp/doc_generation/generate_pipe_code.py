import os
import nlu
# use the generate_py_code_for_nlu_ref() method to convert a nlu_reference into a Spark NLP pipe


#every annotator class is accompanied with a component_infos.json
# in the same dir as the component_info there will be a .py
# Then just get the code inside of get_pretrained_model() and gg! (Basically just remove"return" and white spaces, gg?
# need to add parameters to .get_pretrained_model(name, language)
# need to update input/outut cols
# Some annotators dont have pretrained models and thus they have no get_pretrained_model() method. In these cases, we will inject the get_default_model() code and update no params
def generate_py_code_for_nlu_ref_or_pipe(nlu_ref = 'pos', pipe=None):
    pipe_code = []
    if pipe == None: pipe = nlu.load(nlu_ref)
    is_pretrained_pipe = None
    component_kind, nlp_ref,lang = get_component_metadata(nlu_ref)
    print(    pipe.predict('hello my name is fred'))
    if component_kind=='pipe' :
        pipe_code = make_pretrained_pipe_code(nlp_ref, lang,nlu_ref)
    else :
        for c in pipe.pipe_components:
            source_path = get_nlu_py_file_path_for_nlu_component(c)
            if check_if_has_pretrained(source_path) :
                pipe_code.append(extract_get_pretrained_source_code(source_path))
            else:
                pipe_code.append(extract_get_default_source_code(source_path))
        pipe_code = make_model_pipe_code_pretty(pipe_code,pipe, lang, nlp_ref,nlu_ref)
    print_py_pipe_code(pipe_code)
    return py_pipe_code_to_str(pipe_code)

def print_py_pipe_code(pipe_code):
    if isinstance(pipe_code[0],str): print('\n'.join(pipe_code))
    else:
        for l in pipe_code: print(''.join(l))

def py_pipe_code_to_str(pipe_code):
    if isinstance(pipe_code[0],str): return '\n'.join(pipe_code)
    else:
        return ''.join([item for sublist in pipe_code for item in sublist])
        #  return ''.join([l  for l in pipe_code])
        # for l in pipe_code: return ''.join(l)

def get_nlu_py_file_path_for_nlu_component(c):
# for a given NLU component, find source file that creates the Spark NLP annotators

    c_folder = c.component_path
    candidates = os.listdir(c_folder)
    py_file = ''
    for can in candidates:
        if'.py' in can and '__init__' not in can: py_file=can
    return c_folder + py_file


def check_if_has_pretrained(source_path):
    f = open(source_path, 'r')

    # check for a py file if it has a pretrained method or not
    for l in f : # check if annotator has .pretrained()
        if '.pretrained()' in l : return True
    return  False

def extract_get_default_source_code(source_path):
    #extract get_default() method source code
    f = open(source_path, 'r')
    source_lines = []
    func_start = False
    for l in f :
        if func_start and 'def' in l or l =='\n' and func_start : break # func we want to extract has ended
        if func_start: source_lines.append(clean_line(l))
        if 'get_default_model' in l : func_start = True
    return  source_lines

def extract_get_pretrained_source_code( source_path ):
    #extract get_pretrained() method source code

    f = open(source_path, 'r')

    source_lines = []
    func_start = False
    for l in f :
        if func_start and 'def' in l or l =='\n' and func_start: break # func we want to extract has ended
        if func_start: source_lines.append(clean_line(l))
        if 'get_pretrained_model' in l : func_start = True

    # todo remove \t of the FIRST line only!
    source_lines[0].replace('\t','')
    return  source_lines

def define_annotator_variable_names(pipe_code):
    # set left side of equality for variable name
    new_pipe = []
    var_names = []

    for anno in pipe_code:
        first_line = anno[0]
        class_name = first_line.split('=')[1].split('.')[0]\
            .replace(' ','').replace('\\','').\
            replace('(','').replace(')','')\
            .replace('name','').replace('language','')\
            .replace('\n', '')

        var_name = camel_case_to_underscore(class_name)
        var_names.append(var_name)
        new_pipe.append([anno[0].replace('annotator_name',var_name)] + anno[1:])
    return new_pipe,var_names

def camel_case_to_underscore(string):
    new_s = ''
    new_pipe =[]

    for i, s in enumerate(string):
        if i == 0 : new_s = s.lower()
        elif s.islower(): new_s = new_s+s
        else : new_s = new_s+ '_' +s.lower()
    return  new_s

def get_nlp_reference_for_nlu_reference(nlu_ref):
    # for NLU reference, search namesapce for matchng NLP eference
    pass

def configure_indentation(pipe_code):
    # first line should be  0 tab, all following lines should be 1  tab
    new_pipe =  []
    for anno in pipe_code:
        rem_white = lambda x : x.lstrip()
        prepend_indent = lambda x : '	' +x #we could use \t but it would not be renderd by jekyll(?)
        new_pipe.append( [anno[0].lstrip()] + list(map(prepend_indent,map(rem_white, anno[1:]))))

    return new_pipe

def configure_input_output_cols(pipe_code, nlu_pipeline):
    #inject paramets for input/output column into code base on what they are configured to in nlu pipeline
    new_pipe_code = []
    for i,anno in enumerate(pipe_code):
        input_col = nlu_pipeline.pipe_components[i].component_info.spark_input_column_names
        output_col = nlu_pipeline.pipe_components[i].component_info.spark_output_column_names
        new_anno_code = []
        for l in anno:
            new_l = ''
            if 'setOutputCols' in l:
                new_l = l[:l.find('(')+1] + str(output_col) +   l[l.find(')'): ] # ')'
            elif 'setOutputCol' in l:
                new_l = l[:l.find('(')+1] + str(output_col).replace('[','').replace(']','') +  l[l.find(')'): ] #  ')'
            elif 'setInputCols' in l:
                new_l = l[:l.find('(')+1] + str(input_col) +  l[l.find(')'): ] # ')'
            elif 'setInputCol' in l:
                new_l = l[:l.find('(')+1]+ str(input_col).replace('[','').replace(']','')  +  l[l.find(')'): ]
            else: new_l = l
            new_anno_code.append(new_l)

        new_pipe_code.append(new_anno_code)
    return new_pipe_code

def get_embedding_parameters(lang, nlp_storage_ref):
    #iterate over namespace and see if embed exist for that lang. if not, it must be multi lang embed
    # if embeddings do not exist in specific lang and xx space, it has to be en embedding..

    for k,v in nlu.NameSpace.pretrained_models_references[lang].items():
        if v == nlp_storage_ref : return lang, nlp_storage_ref

    for k,v in nlu.NameSpace.pretrained_models_references['xx'].items():
        if v == nlp_storage_ref : return 'xx', nlp_storage_ref

    for k,v in nlu.NameSpace.pretrained_models_references['en'].items():
        if v == nlp_storage_ref : return 'en', nlp_storage_ref

    print("EXCEPTION COULD NOT FIND CORRECT EMBED PARAMETERS FOR ", lang, nlp_storage_ref)
    return '???????', nlp_storage_ref

def get_pretrained_model_parameters(lang, nlu_model_ref):
    #iterate over namespace and see if embed exist for that lang. if not, it must be multi lang embed
    # if embeddings do not exist in specific lang and xx space, it has to be en embedding..

    for k,v in nlu.NameSpace.pretrained_models_references[lang].items():
        if k == nlu_model_ref : return lang, v

    for k,v in nlu.NameSpace.pretrained_models_references['xx'].items():
        if k == nlu_model_ref : return 'xx', v

    for k,v in nlu.NameSpace.pretrained_models_references['en'].items():
        if k == nlu_model_ref : return 'en', v

    print("EXCEPTION COULD NOT FIND CORRECT MODEL PARAMETERS FOR ", lang, nlu_model_ref)
    return '???????', nlu_model_ref


def configure_pretrained(pipe_code, nlu_pipeline, lang, nlp_ref, nlu_ref):
    #configure .pretrained parameters and also takes the embeddings into acound
    # We iterate in reverse, first will be classifier then model
    parameters_set_count = 0
    new_pipe_code = []
    for i,anno in enumerate(reversed(pipe_code)):

        if 'pretrained' in anno[0] and parameters_set_count != 0:
            storage_refs = [c.model.extractParamMap()[c.model.storageRef] for c in nlu_pipeline.pipe_components if any ([ 'storageRef' in str(d) for d in c.model.extractParamMap().keys() ] ) ]
            p_lang,p_name = get_embedding_parameters(lang,storage_refs[0])

            new_l = anno[0][:anno[0].find('(') + 1] +"'"+ p_name +"'"+  ', ' +"'"+  p_lang +"'"+ anno[0][anno[0].find(')'):]
            parameters_set_count =+1
            new_pipe_code.append([new_l] + anno[1:])

        elif 'pretrained' in anno[0] and parameters_set_count== 0:
            p_name, p_lang = get_pretrained_model_parameters(lang,nlu_ref)
            parameters_set_count = 1
            new_l = anno[0][:anno[0].find('(') + 1] +"'"+ p_name +"'"+ ', ' +"'"+  p_lang +"'"+ anno[0][anno[0].find(')'):]
            new_pipe_code.append([new_l] + anno[1:])
        else:
            new_pipe_code.append(anno)

    if parameters_set_count > 2 : print("CONFIGURED MROE THAn 2 PARAMS FOR ", nlu_ref,nlp_ref, nlu_pipeline, pipe_code)
    new_pipe_code.reverse()
    return  new_pipe_code

def configure_annotator_parameters(pipe_code, nlu_pipeline, lang, nlp_ref,nlu_ref):
    # 1. inject parameters  of input/output cols, based on what NLU has currently configured them to
    # 2. If .pretrained(name,lang) in first line, inject name/lang
    # (2.) occurs only for NON pretrained pipelines. We also need to check if the model uses embeddings and if so, we must configure .pretraiend() of the embeddings aswell
    pipe_code = configure_input_output_cols(pipe_code, nlu_pipeline)
    pipe_code = configure_pretrained(pipe_code, nlu_pipeline, lang, nlp_ref,nlu_ref)
    return pipe_code



def clean_line(l): return l.replace('return','annotator_name = ').replace('\t\t','\t')


def make_model_pipe_code_pretty(pipe_code, nlu_pipeline, lang, nlp_ref,nlu_ref):
    # pipe code consist of list of lists. each outer list contains one Annotator Source code. Each inner element of a list is a list with strings that represent the source code
    # we replace annotator_name with a more meaningful name
    # also we fix tabs
    # inject parameters aswell input/output cols and .pretrained(name,lang)
    pipe_code,var_names = define_annotator_variable_names(pipe_code)
    pipe_code = configure_indentation(pipe_code)

    # set input/output cols and .pretrained() parameters
    pipe_code = configure_annotator_parameters(pipe_code, nlu_pipeline, lang, nlp_ref,nlu_ref)

    #pipeline with stages definition
    pipe_code.append(get_spark_pipe_definition(var_names))
    pipe_code.insert(0,[add_pretrained_model_imports()])
    # fit_transform and dataframe definition
    pipe_code.append([get_fit_transform_df_suffix()])



    print("DONE MAKING PRETTY")

    return pipe_code
def make_pretrained_pipe_code(nlp_ref, lang,nlu_ref):
    pipe_code = []
    pipe_code.append(add_pretrained_model_imports())
    pipe_code.append(add_pretrained_pipe_definition(nlp_ref,lang))
    pipe_code.append(get_fit_transform_df_suffix())
    return pipe_code



def add_pretrained_pipe_imports(): return 'import sparknlp \nfrom sparknlp.pretrained\nimport PretrainedPipeline\n'
def add_pretrained_model_imports(): return 'import sparknlp \nfrom sparknlp.annotator import *\nfrom pyspark.ml import Pipeline\n'

def add_pretrained_pipe_definition(nlp_ref,lang): return f"pipeline = PretrainedPipeline('{nlp_ref}', lang='{lang}')\n"


def get_spark_pipe_definition(var_names):
    # summarize all annotators in a Spark pipeline  and add it as new line to the list
    #var_name is a list of what the annotator variable namesa re in the code

    pre = "nlp_pipe = Pipeline(stages=["
    stages = ','.join(var_names)
    post = "])\n"
    return pre+stages+post


#todo add get_sample_df
def get_fit_transform_df_suffix():
    # after we have the full model/pretraine pipe code and the 'pipe' variable, we can always add the same suffix!
    l1 = "text = 'John Snow Labs offers over 300 models in over 40 languages to solve a variety of NLP problems while keeping the highest accuracy.'\n"
    l2 = "df = spark.createDataFrame([[text]]).toDF('text')\n"
    return l1+l2+'predictions = nlp_pipe.fit(df).transform(df)\npredictions.printSchema()\npredictions.show()'


def get_component_metadata(nlu_reference):
# get nlp_ref and wheter it is pretrained pipe or just a prertained mdoel(component kind)
    from nlu import all_components_info
    infos = nlu_reference.split('.')
    language = ''
    component_type = ''
    dataset = ''
    component_embeddings = ''
    component_pipe = []
    if len(infos) == 0: 1+1
    elif len(infos) == 1:
        # if we only have 1 split result, it must a a NLU action reference or an alias
        language = 'en'
        if infos[0] in all_components_info.all_components or all_components_info.all_nlu_actions:
            component_type = infos[0]
    #  check if it is any query of style #<lang>.<class>.<dataset>.<embeddings>
    elif infos[0] in all_components_info.all_languages:
        language = infos[0]
        component_type = infos[1]

        if len(infos) == 3:  # dataset specified
            dataset = infos[2]
        if len(infos) == 4:  # embeddings specified
            component_embeddings = infos[3]

    # passing embed_sentence can have format embed_sentence.lang.embedding or embed_sentence.embedding
    # i.e. embed_sentence.bert
    # fr.embed_sentence.bert will automatically select french bert thus no embed_sentence.en.bert or simmilar is required
    # embed_sentence.bert or en.embed_sentence.bert
    # name does not start with a language
    # so query has format <class>.<dataset>
    elif len(infos) == 2:
        language = 'en'
        component_type = infos[0]
        dataset = infos[1]
    # query has format <class>.<dataset>.<embeddings>
    elif len(infos) == 3:
        language = 'en'
        component_type = infos[0]
        dataset = infos[1]
        component_embeddings = infos[1]

    resolved_component = resolve_component_from_parsed_query_data(language, component_type, dataset,
                                                                  component_embeddings, nlu_reference)

    return resolved_component
def resolve_component_from_parsed_query_data(language, component_type, dataset, component_embeddings, nlu_ref):
    from nlu import NameSpace
    component_kind = ''  # either model or pipe or auto_pipe
    nlp_ref = ''
    resolved = False
    # 1. check if pipeline references for resolution
    if resolved == False and language in NameSpace.pretrained_pipe_references.keys():
        if nlu_ref in NameSpace.pretrained_pipe_references[language].keys():
            component_kind = 'pipe'
            nlp_ref = NameSpace.pretrained_pipe_references[language][nlu_ref]
            resolved = True

    # 2. check if model references for resolution
    if resolved == False and language in NameSpace.pretrained_models_references.keys():
        if nlu_ref in NameSpace.pretrained_models_references[language].keys():
            component_kind = 'model'
            nlp_ref = NameSpace.pretrained_models_references[language][nlu_ref]
            resolved = True

    return (component_kind, nlp_ref,language)


if __name__ == "__main__":
    print('___________________PIPE TEST ___________________________-')
    pipe_code = generate_py_code_for_nlu_ref_or_pipe('albert')
    print("DONE CODE : ", pipe_code)
    # print(pipe_code)

    print('___________________COMPONENT TEST ___________________________-')
    # should proeprly set .pretrained prameters of embdeddings and model
    pipe_code = generate_py_code_for_nlu_ref_or_pipe('nl.ner.wikiner.glove.6B_100')
    print("DONE CODE : ", pipe_code)

#todo
def generate_jupyter_notebook():

    pass