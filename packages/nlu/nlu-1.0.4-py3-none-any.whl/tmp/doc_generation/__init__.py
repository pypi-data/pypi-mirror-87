import os
from os import path
import sys
PARENT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(PARENT_DIR)
conf_path = os.getcwd()
sys.path.append(conf_path)
sys.path.append('/home/loan/Documents/freelancework/jsl/nlu/4realnlugit/tmp/doc_generation')
# #nlu-1.0.2.tar.gz
import doc_generation.class_table_creator as class_table
import doc_generation.model_base_table_creator as model_table
import doc_generation.generate_bad_models_table  as bad_model_table



print("What do you want to do?\n"
      "1. Create Annotator Class Metadata Table(Could crash your machine, do manual runs)\n"
      "2. Generate Meta Models CSV. This can take 12-24 hours. Logs will be generated in runlogs.txt\nAssuming models will be default cached to '~/cache_pretrained'. If this not the case, configure the parameter manually (i.e. Windows) or your machine will crash\n"
      "3. Generate Bad Models CSV (CSV of all models for which no data could be generated in (2.)\n"
      "4. Exit"
      )


inp = int(input('Enter a number'))

if inp == 1 : class_table.generate()
if inp == 2:  model_table.generate(pretrained_model_cache_path = '~/cache_pretrained')
if inp == 3 : bad_model_table.generate()
if inp == 4:  exit()



