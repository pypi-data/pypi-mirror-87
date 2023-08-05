# this runs after python code has been generated nd converts the py code to Scala code

# 1. Convert " to '
# 2. Add val in the beginning of each line that has a =
# 3. Add 'new' after each = which is NOT created .pretrained()
# 4. Remove \
# 5. Convert py arrays [] to scalla Array in pipe.setTages()
# 6 New Fit/Transform sufix
# 7. New imports

#convert the generated Python Spark NLP code into runnable Scala Code for Scala Notebooks (i.e Databricks)

#1. Imports
def translate_imports_pretrained(imports_py):pass

def translate_imports_model(imports_py):pass

def underscore_to_camelcase():pass
# make all strings LEFT from the = camelcase


#2. Annotator Definitions
# def translate_pipe_annotators(pipe_py):pass

def translate_pipe_annotators_pretrained(pipe_py): pass

def translate_pipe_annotators_model(pipe_py):
    annos_scala = []
    anno_start = True
    cur_anno = []
    for l in pipe_py :
        if 'nlp_pipe' in l :
            annos_scala.append(['val nlpPipe =' + l.split('=')[1]])
            break
        if '=' in l :
            annos_scala.append(cur_anno)
            cur_anno = []
            l = 'val ' + l
            # l = underscore_to_camelcase(l)
            if '.pretrained()' not in l : # non-ppretraineda nnotators are created with new keyword
                l = l.replace('=', ' = new ')

        # Make True/False params lowercase
        if 'True' in l : l = l.replace('True','true')
        if 'False' in l : l = l.replace('False','false')

        # Any Python arrays [] must become scala Array()
        if ']' in l : l = l.replace(']',')')
        if '[' in l : l = l.replace('[','Array(')

        # For special case [] in inut/output cols with just One param, we can remove the []
        # When we have [] with just 1 Ele, we can ommit the Array

        l = l.replace('\\','') # remove python \ for multi-line code
        l = l.replace("'",'"') # replace single qoutes with double quoutes
        cur_anno.append(l)

    print('translates py pipe to : ')
    print(annos_scala)
    res = ['\n'.join(c) for c in annos_scala]
    print(res)
    print('\n'.join(res))
    return annos_scala


# 3. Pipe Object Construction (only for model?)\
# def translate_pipe_construction_model(suffix_py):pass

# 4. add fit_transform_df suffix
def translate_fit_transform_suffix(suffix_py) : pass

def parse_py_pipe_to_pieces(py_code):
    #segment py code into parts
    # 1. imports (beginning until first '=' is imports
    # 2. pipe definition
    # 3. suffix
    # 4. and classifies wether it is a pretrained pipeline or Model stack
    import_code = []
    pipe_code = []
    suffix_code = []
    code_type = ''
    on_imports = True
    on_pipe = False
    for l in  py_code.split('\n'):
        if '=' in l  and (on_pipe or on_imports):
            on_imports = False
            on_pipe = True
        if 'text =' in l : #if true then we are in suffix
            on_pipe, on_imports = False, False
        if on_imports : import_code.append(l)
        if on_pipe : pipe_code.append(l)
        if not on_imports and not on_pipe : suffix_code.append(l)

    return import_code, pipe_code, suffix_code, code_type

def join_scala_snippets(imports_scala,pipe_definition_scala,suffix_scala) : pass

def translate_python_pipe_to_scala(py_code) :
    print('got code', py_code)
    imports_py,pipe_definition_py, suffix_py, code_type =  parse_py_pipe_to_pieces(py_code)
    imports_scala,pipe_definition_scala, suffix_scala = [],[],[]
    print('hp')
    code_type = 'model'
    if code_type =='model':
        # imports_scala = translate_imports_pretrained(imports_py)
        pipe_definition_scala = translate_pipe_annotators_model(pipe_definition_py)
        suffix_scala = translate_fit_transform_suffix(suffix_py)

    else : #pipe
        imports_scala = translate_imports_model(imports_py)
        pipe_definition_scala = translate_pipe_annotators_pretrained(pipe_definition_py)
        suffix_scala = translate_fit_transform_suffix(suffix_py)


    result_code = join_scala_snippets(imports_scala,pipe_definition_scala,suffix_scala)




if __name__ == "__main__":
    import pandas as pd

    print('___________________PIPE TEST ___________________________-')
    py_pipe_path = '/home/loan/Documents/freelancework/jsl/nlu/4realnlugit/tmp/doc_generation/generated_data/latest_models_generated_with_meta.csv'
    df = pd.read_csv(py_pipe_path)

    for idx ,row in df.iterrows():
        py_code = row.nlp_pipeline_code
        if 'todo' in py_code : continue
        scala_code = translate_python_pipe_to_scala(py_code)
        df.at[idx, 'scala_code'] = scala_code

