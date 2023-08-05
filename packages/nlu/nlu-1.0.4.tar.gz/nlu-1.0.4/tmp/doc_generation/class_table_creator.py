




def generate_class_metadata_table(nlu_pipe, ):
    '''
    Print out information about every component currently loaded in the pipe and their configurable parameters
    :return: None
    '''

    import  nlu

    all_outputs = []
    final_df = {}

    for i, component_key in enumerate(nlu_pipe.keys()) :


        # get comp info of model
        c_info = None
        for c in nlu_pipe.pipe_components:
            if c.component_info.name == component_key :
                c_info = c.component_info
                break
        if c_info == None : print('CCOULD NOT FIND INFO FOR ', component_key)

        final_df[component_key] = {
            'model_class' : type(nlu_pipe[component_key]).__name__,
            'class_description' : 'TODO',
            'inputs' : c_info.inputs,
            'outputs' : c_info.outputs,
            # 'label' : [], only for approaches
            'class_parameters' : [],
            'class_license' : c_info.license,
            'dataset_schema' : 'TODO',
            'class_annotation_sample' : 'TODO',
        }

        print(component_key)
        p_map = nlu_pipe[component_key].extractParamMap()
        all_param_dicts ={}

        # get all param info
        for key in p_map.keys():
            if 'lazyAnnotator' in key.name: continue

            param_dict = {}
            param_dict['param_name'] = key.name
            param_dict['param_description'] = key.doc
            param_dict['param_default_value'] = str(p_map[key])
            param_dict['param_setter_method'] = 'TODO'
            param_dict['param_getter_method'] = 'TODO'

            if type(p_map[key]) == str :
                s1 = "model.set"+ str( key.name[0].capitalize())+ key.name[1:]+"('"+str(p_map[key])+"')"
            else :
                s1 = "model.set"+ str( key.name[0].capitalize())+ key.name[1:]+"("+str(p_map[key])+")"


            if type(p_map[key]) == str :
                s2 = "model.get"+ str( key.name[0].capitalize())+ key.name[1:]+"()"
            else :
                s2 = "model.get"+ str( key.name[0].capitalize())+ key.name[1:]+"()"


            param_dict['param_setter_method'] = s1
            param_dict['param_getter_method'] = s2
            final_df[component_key]['class_parameters'].append(param_dict)



    return final_df

def make_nlu_pipe_with_every_class():
    import  nlu
    from nlu.components import chunker
    nlu_components = []
    #
    #all chunker trained classses
    nlu_components.append( nlu.chunker.Chunker('default_chunker'))
    nlu_components.append( nlu.chunker.Chunker('ngram'))

    #all classifier trained classes

    nlu_components.append(nlu.components.classifier.Classifier('classifier_dl') )
    nlu_components.append(nlu.components.classifier.Classifier('e2e') )
    nlu_components.append(nlu.components.classifier.Classifier(nlp_ref='sentimentdl') )
    nlu_components.append(nlu.components.classifier.Classifier('vivekn') )
    nlu_components.append(nlu.components.classifier.Classifier('yake') )
    nlu_components.append(nlu.components.classifier.Classifier('wiki_') )
    nlu_components.append(nlu.components.classifier.Classifier('ner') )
    nlu_components.append(nlu.components.classifier.Classifier('pos') )


    # Dep typed and untyped
    nlu_components.append(UnlabeledDependencyParser())
    nlu_components.append(LabeledDependencyParser())

    # embeddings
    nlu_components.append(nlu.Embeddings('bert'))
    nlu_components.append(nlu.Embeddings('albert'))
    nlu_components.append(nlu.Embeddings('glove'))
    nlu_components.append(nlu.Embeddings('use'))

    nlu_components.append(nlu.Embeddings(annotator_class='embed_sentence', component_type='embedding', nlp_ref='sent_small_bert_L2_128'))
    nlu_components.append(nlu.Embeddings('elmo'))
    nlu_components.append(nlu.Embeddings('xlnet'))


    nlu_components.append(nlu.Matcher('text'))
    nlu_components.append(nlu.Matcher('date'))
    nlu_components.append(nlu.Matcher('regex'))
    nlu_components.append(nlu.Normalizer())
    nlu_components.append(nlu.NLUSentenceDetector('deep_sentence_detector'))
    nlu_components.append(nlu.NLUSentenceDetector('pragmatic_sentence_detector'))

    nlu_components.append(nlu.SpellChecker('context_spell'))
    nlu_components.append(nlu.SpellChecker('norvig_spell'))
    nlu_components.append(nlu.SpellChecker('context_spell'))
    nlu_components.append(nlu.Stemmer())
    nlu_components.append(nlu.StopWordsCleaner(get_default=True))
    nlu_components.append(nlu.Lemmatizer(get_default=True))

    pipe = nlu.NLUPipeline()
    for c in nlu_components : pipe.add(c)

    return pipe

def generate():
    import nlu
    import pandas as pd
    from nlu.components.classifier import Classifier
    from nlu.components.unlabeled_dependency_parser import UnlabeledDependencyParser
    from nlu.components.labeled_dependency_parser import LabeledDependencyParser
    import sparknlp
    sparknlp.start()
    import sparknlp
    pipe = make_nlu_pipe_with_every_class()
    model_df = pd.DataFrame(generate_class_metadata_table(pipe))
    model_df = model_df.T
    print(model_df)
    model_df.to_csv('./doc_generation/generated_data/classes_generated.csv',index=False)

# class_parameter col is a list of Dictionaries.
# Each dict  in the class_parameter list describes a param with the following values :
# - param_name
# - param_description
# - param_default_value
# - param_setter_method
# - param_getter_method

#Meta class ideas :
# wikipedia links
# NER CRF IS MISSING FROM CLASSES BCZ IT SUCXX
# Pragmatic Sentence also missing

# For every 'classification' tag add an invisible 'classifier tag' and add those generated to
    # add generated tags to SEO column, tags that are hidden or that we dont show but google should pick up
    # Also add python ner, scala ner etc.. as keywords
    # Inlcude detectION/classificatION/parsing/ and generate detectOR/classificaIER/parSER
    # For every 'Word" occurence generate 'token' in hidden Tags , i.e. Word/Token embeds, Vanilla has word, generated has token
    # For every "Embedding" occurence generate'Vetor" i.e. 'Word Vector'
    # For every "Deep Learning" add "neural Network"
    # Every "Universal Sentence Encoder" -> "USE"
    # Every 'match' -> 'matchER'
    # Every 'match' -> 'parser' ?
    # Every 'classifier' -> tagger
    # reference_links, paper_links, scala_doc_links, scala_source_links are WHITESPACE SEPERATED
    # paper abstract auto generate!
    # post process _> upercase every tag word
    # should generate how to get <xzy>


# - We should add a 'NLP TERM WIKI/ WIKIPEDIA' to dominate with our presence


# code generation schema should follow <class>.pretrained(<model_name>.<lang>)
# .setInputCols([<col1>,<colN>]
# .setOutputCols([<col1>])
# .setLabelCol('label') | for approaches! !

# Meta model ideas
 # -for languages generate keyword 'ner english' m 'ner chinese', etc..
 #-


# [‘detector’ ‘Deep Learning’,’sentence detector’, ‘sentence boundary detector’]

# all the lists with tags are written by hand straight into excel.
#  So there might still be syntax errors when loading in Python as list, I will make sure they have correct syntax in 2 hours

