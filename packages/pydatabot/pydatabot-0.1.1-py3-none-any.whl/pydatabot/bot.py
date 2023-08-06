import dialogflow_v2 as dialogflow
import os
import sys
import numpy as np
import inspect
sys.path.append('../') #/Users/xinsun/Dev_env/Py_databot/pydatabot/
from . import templates_pandas
from . import templates_spark
from . import manipulation_rec_similarity_pypi as manip

'''
print("sys.path[0] = ", sys.path[0])
print("sys.argv[0] = ", sys.argv[0])
print("__file__ = ", __file__)
print("os.path.abspath(__file__) = ", os.path.abspath(__file__))
print("os.path.realpath(__file__) = ", os.path.realpath(__file__))
print("os.path.dirname(os.path.realpath(__file__)) = ", 
       os.path.dirname(os.path.realpath(__file__)))
print("os.path.split(os.path.realpath(__file__)) = ", 
       os.path.split(os.path.realpath(__file__)))
print("os.path.split(os.path.realpath(__file__))[0] = ", 
       os.path.split(os.path.realpath(__file__))[0])
print("os.getcwd() = ", os.getcwd())
'''


credentials_file = os.path.dirname(os.path.realpath(__file__)) + '/devbot-eayuea-91f036b58a20.json'  
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_file

def detect_intent_entity(project_id, text_to_be_analyzed):
    DIALOGFLOW_PROJECT_ID = project_id
    DIALOGFLOW_LANGUAGE_CODE = 'en'
    SESSION_ID = '1'  #SESSION_ID

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    #text_to_be_analyzed = "transfer money"
    text_to_be_analyzed = text_to_be_analyzed #"set alarm"

    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)

    intent, entity = False, False

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        #print(response)
        intent = response.query_result.intent.display_name
        #print(intent)
    except:  #InvalidArgument:
        print('No intent found!')
        pass

    try:
        entity = {}
        entity_res = response.query_result.parameters.fields
        for i in entity_res:
            #entity[i] = entity_res[i].string_value.strip("\'").replace(' and', ',') if entity_res[i].string_value else None
            entity[i] = entity_res[i].string_value.strip("\'").strip('\"').replace(' and', ',') if entity_res[i].string_value else None
        #print('entity: ', entity, type(entity))

    except:  #InvalidArgument:
        print('No entity found!')
        pass

    if intent and entity: return intent, entity, response
    elif intent: return intent, None, response
    elif entity: return None, entity, response



def code_template(templates, intent, entity, user_history_query):
    required_parameters = inspect.getfullargspec(getattr(templates, intent)).args  # this function can tell us all required parameters of request function
    #print('required parameters is: ', required_parameters)
    resolved_parameters, further_parameter = [], []
    
    if required_parameters and entity:
        #print('further')
        for para in required_parameters:
            #print('para type: ', type(para))
            #print('para: ', para)
            if str(para) in entity.keys():
                resolved_parameters.append(entity[para])
            else:resolved_parameters.append(None)

        further_parameter = list(set(required_parameters) - set(entity.keys()))
    else:
        pass
    
    #result = getattr(templates, intent)() if len(required_parameters) == 0 and intent != 'recommendation' else getattr(templates, intent)(*resolved_parameters)
    
    if len(required_parameters) == 0 and intent != 'recommendation':
        result = getattr(templates, intent)()
    elif intent == 'recommendation': 
        pass #result = getattr(templates, intent)(user_history_query) 
    else:
        result = getattr(templates, intent)(*resolved_parameters)
    
    return further_parameter, result




def code(text_to_be_analyzed):
    '''
    credentials_file = '/Users/xinsun/Dev_env/Py_devbot/pydevbotdevbot-eayuea-91f036b58a20.json'  
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_file
    '''

    project_id = 'devbot-eayuea'
    message_texts = None   #'delete the value'
    #text_to_be_analyzed = sys.argv[1]   #'please give me data'
    user_history_query = '' #sys.argv[2]
    #print(user_history_query)

    intent, entity, response = detect_intent_entity(project_id, text_to_be_analyzed)
    print('Intent is:', intent)
    print('Entity is:', entity)
    
    if 'framework_type' in entity.keys() and intent != 'recommendation':
        further_parameter, result = code_template(templates_spark, intent, entity, user_history_query.split(','))
    elif 'framework_type' not in entity.keys() and intent != 'recommendation':
        further_parameter, result = code_template(templates_pandas, intent, entity, user_history_query.split(','))

    #print('further_parameter is: ', further_parameter)
    #print('result code is: ', result)
    print('\n') 
    print('The code is: ', result)     


def transformation(manip_record, specific_phase):

    
    sim_matrix = np.load(os.path.dirname(os.path.realpath(__file__)) + '/emb_similarity.npy', allow_pickle=True).item()
    
    os.path.dirname(os.path.realpath(__file__))
    
    #sim_matrix = np.load('/Users/xinsun/Desktop/test_copy/codes/Embeddings/emb_similarity.npy', allow_pickle=True).item()
    result = manip.deepwalk_sim(sim_matrix, manip_record, specific_phase)

    print('The recommended transformations are: ', result) 



if __name__ == "__main__":
    pass

    '''
    text_to_be_analyzed = sys.argv[1]
    code(text_to_be_analyzed)
    transformation(['load_data', 'dataset_shape', 'fill_na'], "preprocessing")
    '''