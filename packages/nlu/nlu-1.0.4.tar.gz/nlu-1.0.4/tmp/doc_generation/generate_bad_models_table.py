import pandas as pd

def generate():
    models_with_meta_csv_path = '/tmp/doc_generation/models_generated_with_meta_fullest.csv'
    df =pd.read_csv(models_with_meta_csv_path)

    print(df)

    df = df[df.nlu_predictions =='todo']
    print(df)


    df.to_csv('./tmp/doc_generation/generated_data/bad_models.csv')