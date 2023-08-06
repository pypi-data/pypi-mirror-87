from PIL import Image
import warnings
import numpy as np
import pandas as pd
import math
import time
import json
import numpy as np
import base64
import requests
import os



class Image_Model:

    def build_model(self, api_key=None, class_names=None, example_folders=None, model_name=None):
        '''
        --------------------------
        Create an Image Model.
        --------------------------
        Params:

          - api_key (string):
              The api key for your clevrML developer account.

          - class_names (list):
              The name of the classes / labels that you want to classify new 
              inputs with. Ex) "Dog" or "Cat"
          
          - example_folders (list):
              List of the folder directories that have the reference images. 
          
          - model_name (string):
              The name you want to give your image classification model.
          
        --------------------------
        Example:
          classes = ['cat', 'dog', 'fish']
          examples = ['cat_examples', 'dog_examples', 'fish_examples']

          img_model = Image_Model()
          img_model.build_model(classes, examples, 'my_model')

          OR 

          img_model = Image_Model()

          img_model.build_model(
               ['cat', 'dog', 'fish'], 
               ['cat_examples', 'dog_examples', 'fish_examples'], 
              'my_model',
            )

        *NOTE*: Make sure classes and example folder indexes match up to avoid
        model inaccuracies.  
        
        '''

        if api_key == None:
            raise Exception('Please enter your api key to create a model.')
        
        if class_names == None:
            raise Exception('To create an image model, you need to input a list of your class names ( ex. ["dog", "cat"] )')

        if example_folders == None:
            raise Exception('To create an image model, you need to pass the names of your folders that have the example images as a list to the parameter "example_folders"    (ex. ["/dog_examples/", "/cat_examples/"]')

        if model_name == None:
            raise Exception('Please pass your model name to the parameter "model_name"')
        
        else:
            model_object = {}
            print('Creating model, this may take up to a couple of minutes....')
            
            counter = 0

            for folder in example_folders:
                tmp = []
                
                for image_file in os.listdir(folder):
                    path = folder +  '/' + image_file
                    with open(path, 'rb') as f:
                        meta = f.read()
                        byte_data = base64.encodebytes(meta).decode("utf-8")
                        tmp.append(byte_data)
                
                model_object[class_names[counter]] = tmp
                counter += 1
 
        url = 'https://y3aexhkrea.execute-api.us-east-2.amazonaws.com/image-model-build'

        payload = {
            'api_key':  api_key,
            'references': model_object,
            'model_name': model_name
        }
        
        r = requests.post(url, data=json.dumps(payload))
        response = json.loads(r.text)

        try:
            if response['status'] == 'Success':
                print('Your model has been created!\n\nDetails:')
                print('-' * 20)
                print(
                    'Model Name: ' + model_name + '\n' +
                    'Deployed: True\n' + 
                    'Status: Complete'
                )
                
                print('-' * 20)
                print(
                    'JSON:' +
                    '\n{\n' +
                    '   Model_name: ' + model_name + '\n'
                    '   Deployed: True\n' + 
                    '   Status: Complete\n}'
                )

            else:
                print(response)
        except:
            raise Exception('Server timeout, please try again.')

  
            
    


    def predict(self, api_key=None, model_name=None, image_file_path=None):
        '''
        -------------------------
        Make a single prediction with an image model, returns class of the 
        prediction as a string.
        -------------------------
        Params:

          - api_key (string):
              The api key for your clevrML developer account.

          - image_file_name (string):
              Path to either image or text file that you want to get a 
              prediction for.

          - model_name (string):
              The name of a created image model.

        -------------------------
        Example:

          model = Image_Model()

          model.prediction(
            api_key="1234", 
            image_file_name="dog_pic.jpg",
            model_name="dogModel"
          )

        '''
        
        if model_name == None:
            raise Exception('To make a prediction, you need to pass the name of the Image model you want to use through the "model_name" parameter.')
        
        if image_file_path == None:
            raise Exception('No image file path was passed through the "image_file_path" parameter.')

        else:
            image_data = []

            with open(image_file_path, 'rb') as f:
                meta = f.read()
                image_data.append(base64.encodebytes(meta).decode("utf-8"))
            
            url = "https://8nqfrxpxxg.execute-api.us-east-2.amazonaws.com/image-model-prediction"

            payload = {
                'api_key':  api_key,
                'inference_image': image_data[0],
                'model_name': model_name,
            }
        
            r = requests.post(url, data=json.dumps(payload))

            response = json.loads(r.text)

            try:
                if response['status'] == 'Success':
                    print('Prediction:', response['prediction'][0])
    
                    print('-' * 20)
                    print(
                        'Model Name: ' + model_name + '\n' +
                        'Prediction: ' +  response['prediction'][0] + '\n' +
                        'Status: Success'
                    )
                    
                    print('-' * 20)
                    print(
                        'JSON:' +
                        '\n{\n' +
                        '   Model_name: ' + model_name + '\n'
                        '   Prediction:' + response['prediction'][0] + '\n' +
                        '   Status: Success\n}'
                    )
                    return response['prediction'][0], round(response['prediction'][1], 2)
                
                else:
                    print(response)
            except:
                  raise Exception('Server timeout. Please try again.')
    
    

    def edit_model(self, api_key=None, class_names=None, example_folders=None, model_name=None):
        '''
        -------------------------
        Edit an existing image model.
        -------------------------
        Params:

          - api_key (string):
              The api key for your clevrML developer account.
          
          - class_names (list):
              This is the list of classes you either want to add or, the image data
              you will add to existing classes.
          
          - example_folders (list):
              The list of the folders that contain the corresponding images to your 
              classes.

          - model_name (string):
              The name of the model that you want to edit.
        
        -------------------------
        Example:

          model = Image_Model()

          model.edit_model(
            api_key='1234',
            class_names=["dog", "cat"],
            example_folders=["/folder/cat/", "/folder/dog/"],
            model_name="Image_Model_1"
          )

        '''
        if api_key == None:
            raise Exception('Please enter your api key to create a model.')
        
        if class_names == None:
            raise Exception('To create an image model, you need to input a list of your class names ( ex. ["dog", "cat"] )')

        if example_folders == None:
            raise Exception('To create an image model, you need to pass the names of your folders that have the example images as a list to the parameter "example_folders"    (ex. ["/dog_examples/", "/cat_examples/"]')

        if model_name == None:
            raise Exception('Please pass your model name to the parameter "model_name"')

        else:
            
            print('Editing model, this may take up to a couple of minutes....')
            model_object = {}
            
            counter = 0

            for folder in example_folders:
                tmp = []
                
                for image_file in os.listdir(folder):
                    path = folder +  '/' + image_file
                    with open(path, 'rb') as f:
                        meta = f.read()
                        byte_data = base64.encodebytes(meta).decode("utf-8")
                        tmp.append(byte_data)
                
                model_object[class_names[counter]] = tmp
                counter += 1

            url = "https://6b6ypchja8.execute-api.us-east-2.amazonaws.com/image-model-edit"

            payload = {
                'api_key':  api_key,
                'references': model_object,
                'model_name': model_name
            }
            
            r = requests.post(url, data=json.dumps(payload))
            response = json.loads(r.text)

            try:
                if response['status'] == 'Success':
                    print('Your Model has succesfully been updated!')
                    print('-' * 20)
                    print(
                        'Model Name: ' + model_name + '\n' +
                        'Deployed: True\n' + 
                        'Status: Complete'
                    )
                    
                    print('-' * 20)
                    print(
                        'JSON:' +
                        '\n{\n' +
                        '   Model_name: ' + model_name + '\n'
                        '   Deployed: True\n' + 
                        '   Status: Complete\n}'
                    )
                else:
                    print(response)
            except:
                raise Exception('Server timeout. Please try again.')





class Forecasting_Model:
    
    def build_model(self, api_key=None, independent=None, dependent=None, reference_path=None, model_name=None):
        '''
        -------------------------
        Build a new Forecasting Model
        -------------------------
        Params:

          api_key (string):
            The api key for your clevrML developer account
          
          indepedent (string):
            The name of your independent variable (see official clevrML documentation
            for further explanation.)

          dependent (string):
            The name of your dependent variable (see official clevrML documentation
            for further explanation.)

          reference_path (string):
            The path that contains your .csv file of references for your forecasting model.

          model_name (string):
            The name of the model that is being created.
          
          -------------------------
          Example:

            model = Forecasting_Model()

            model.build_model(
              api_key='1234',
              independent='Customers',
              dependent='Sales',
              reference_path='historical_sales.csv',
              model_name='new_forecasting_model'
            )

        '''

        if api_key == None:
            raise Exception('Please enter your api key to create a model.')
        
        if reference_path == None:
            raise Exception('To create a Forecasting model, you need to input ')

        if independent == None or dependent == None:
            raise Exception('To create a Forecasting model, you need to pass the name of your independent and dependent variable names.')

        if model_name == None:
            raise Exception('Please pass your model name to the parameter "model_name"')
        
        else:
            print('Creating model, this may take up to a couple of minutes....')
            independent_values = []
            dependent_values = []
            references = pd.read_csv(reference_path)

            for i in range(len(references[independent])):
                open_val = references[independent][i]
                close_val = references[dependent][i]

                if math.isnan(open_val):
                    i += 1
                else:
                    independent_values.append(round(references[independent][i], 2))
                    dependent_values.append(round(references[dependent][i],2))

            if len(independent_values) != len(dependent_values):
                if len(independent_values) > len(dependent_values):
                    raise Exception('There are more independent variable values than dependent variable values. \
                    To make a Forecasting model, these need to be equal.')
                
                else:
                    raise Exception('There are more dependent variable values than independent variable values. \
                    To make a Forecasting model, these need to be equal.')
        

            url = "https://9qc5r1lma5.execute-api.us-east-2.amazonaws.com/forecasting-model-build"

            payload = {
                'api_key': api_key,
                'independent': independent_values,
                'dependent': dependent_values,
                'variable_names': [independent, dependent],
                'model_name': model_name
            }

            r = requests.post(url, data=json.dumps(payload))
            response = json.loads(r.text)

            try:
                if response['status'] == 'Success':
                    print('Your model has been created!\n\nDetails:')
                    print('-' * 20)
                    print(
                        'Model Name: ' + model_name + '\n' +
                        'Deployed: True\n' + 
                        'Status: Complete'
                    )
                    
                    print('-' * 20)
                    print(
                        'JSON:' +
                        '\n{\n' +
                        '   Model_name: ' + model_name + '\n'
                        '   Deployed: True\n' + 
                        '   Status: Complete\n}'
                    )

                else:
                    print(response)
            except:
                raise Exception('Server timeout. Please try again.')


    
    def predict(self, api_key=None, input_value=None, model_name=None):
        '''
        -------------------------
        Make a prediction with a built Forecasting Model
        -------------------------
        Params:

          api_key (string):
            The api key for your clevrML developer account.
          
          input_value (integer or float):
            The numeric value used to make a prediction.
          
          model_name (string):
            The name of the model being used for the prediction.

        -------------------------
        Example:

          model = Forecasting_Model()

          model.predict(
            api_key='1234',
            input_value=42,
            model_name="forecasting_model3"
          )

        '''

        if api_key == None:
            raise Exception('Please enter your api key to run model predictions.')
        
        if input_value == None:
            raise Exception('No input value found! Please pass an input value to the "input_value" parameter')

        if model_name == None:
            raise Exception('Please enter the model name to run a prediction.')
        
        else:
            prediction_object = {
                'api_key': api_key,
                'input_value': input_value,
                'model_name': model_name 
            }

            url = 'https://wgzoiy5dlg.execute-api.us-east-2.amazonaws.com/forecasting-model-prediction'

            r = requests.post(url, data=json.dumps(prediction_object))
            response = json.loads(r.text)

            try:
                if response['status'] == 'Success':
                    print('Prediction:', response['prediction'])
    
                    print('-' * 20)
                    print(
                        'Model Name: ' + model_name + '\n' +
                        'Prediction: ' +  response['prediction'][0] + '\n' +
                        'Status: Success'
                    )
                    
                    print('-' * 20)
                    print(
                        'JSON:' +
                        '\n{\n' +
                        '   Model_name: ' + model_name + '\n'
                        '   Prediction:' + response['prediction'][0] + '\n' +
                        '   Status: Success\n}'
                    )
                    return response['prediction']
                else:
                    print(response)
            except:
                raise Exception('Server timeout. Please try again.')



    def edit_model(self, api_key=None, independent=None, dependent=None, reference_path=None, model_name=None):
        '''
        -------------------------
        Edit a Forecasting Model that has been created
        -------------------------
        Params:

          api_key (string):
            The api key for your clevrML developer account
          
          indepedent (string):
            The name of your independent variable (see official clevrML documentation
            for further explanation.)

          dependent (string):
            The name of your dependent variable (see official clevrML documentation
            for further explanation.)

          reference_path (string):
            The path that contains your .csv file of references for your forecasting model.
            These will be added as extra data for your model.

          model_name (string):
            The name of the model that is being edited.
          

        -------------------------
        Example:

          model = Forecasting_Model()

          model.edit_model(
              api_key='1234',
              independent='Customers',
              dependent='Sales',
              reference_path='new_sales.csv',
              model_name='new_forecasting_model'
            )


        '''
        
        if api_key == None:
            raise Exception('Please enter your api key to create a model.')
        
        if reference_path == None:
            raise Exception('To create a Forecasting model, you need to input ')

        if independent == None or dependent == None:
            raise Exception('To create a Forecasting model, you need to pass the name of your independent and dependent variable names.')

        if model_name == None:
            raise Exception('Please pass your model name to the parameter "model_name"')
        
        else:
            print('Creating model, this may take up to a couple of minutes....')
            independent_values = []
            dependent_values = []
            references = pd.read_csv(reference_path)

            for i in range(len(references[independent])):
                open_val = references[independent][i]
                close_val = references[dependent][i]

                if math.isnan(open_val):
                    i += 1
                else:
                    independent_values.append(round(references[independent][i], 2))
                    dependent_values.append(round(references[dependent][i],2))

            if len(independent_values) != len(dependent_values):
                if len(independent_values) > len(dependent_values):
                    raise Exception('There are more independent variable values than dependent variable values. \
                    To make a Forecasting model, these need to be equal.')
                
                else:
                    raise Exception('There are more dependent variable values than independent variable values. \
                    To make a Forecasting model, these need to be equal.')
        

            url = "https://8lhwmtvqf1.execute-api.us-east-2.amazonaws.com/forecasting-model-edit"

            payload = {
                'api_key': api_key,
                'independent': independent_values,
                'dependent': dependent_values,
                'variable_names': [independent, dependent],
                'model_name': model_name
            }

            r = requests.post(url, data=json.dumps(payload))
            response = json.loads(r.text)

            try:
                if response['status'] == 'Success':
                    print('Your model has been updated!\n\nDetails:')
                    print('-' * 20)
                    print(
                        'Model Name: ' + model_name + '\n' +
                        'Deployed: True\n' + 
                        'Status: Complete'
                    )
                    
                    print('-' * 20)
                    print(
                        'JSON:' +
                        '\n{\n' +
                        '   Model_name: ' + model_name + '\n'
                        '   Deployed: True\n' + 
                        '   Status: Complete\n}'
                    )
                else:
                    print(response)
            except:
                raise Exception('Server timeout. Please try again.')



class Text_Model:

    def build_model(self, api_key=None, references_path=None, model_name=None):
        '''
        -------------------------
        Create a new Text Classification Model.
        -------------------------
        Param:

          api_key (string):
            The api key for your clevrML developer account
          
          references_path (string):
            The path to your references file (.txt) for your Text Model.
          
          model_name (string):
            The name of the model that will be created.
        
        -------------------------
        Example:

          model = Text_Model()

          model.build_model(
            api_key='1234',
            references_path='myReference_values.txt',
            model_name='Text_Model_1'
          )

        '''

        if api_key == None:
            raise Exception('Please enter your api key to create a text model')
        
        if model_name == None:
            raise Exception('Please pass your model name to the parameter "model_name"')
        
        else:
            print('Creating model, this may take up to a couple of minutes....')
            text_model_request = {}

            with open(references_path) as f:
                ref = f.read()
                data = ref.split('\n')

                for j in data:
                    find_comma = j.find(',')
                    example = j[find_comma+1:]
                    class_name = j[:find_comma]
                    
                    if class_name in text_model_request:
                        reference_examples = text_model_request[class_name]
                        reference_examples.append(example)
                    else:
                        text_model_request[class_name] = [example]

            payload = {
                'api_key': api_key,
                'model_request': text_model_request,
                'model_name': model_name
            }

            url = "https://31avk51512.execute-api.us-east-2.amazonaws.com/text-model-build"
            r = requests.post(url, data=json.dumps(payload))
            response = json.loads(r.text)

            try:
                if response['status'] == 'Success':
                    print('Your model has been created!\n\nDetails:')
                    print('-' * 20)
                    print(
                        'Model Name: ' + model_name + '\n' +
                        'Deployed: True\n' + 
                        'Status: Complete'
                    )
                    
                    print('-' * 20)
                    print(
                        'JSON:' +
                        '\n{\n' +
                        '   Model_name: ' + model_name + '\n'
                        '   Deployed: True\n' + 
                        '   Status: Complete\n}'
                    )
                else:
                    print(response)
            except:
                raise Exception('Server timeout. Please try again.')



    def predict(self, api_key=None, input_sentence=None, model_name=None):
        '''
        -------------------------
        Make a prediction with a built Text Model.
        -------------------------
        Params:

          api_key (string):
            The api key for your clevrML developer account
          
          input_sentence (string):
            The sentence to get a prediction for
          
          model_name (string):
            The name of the model that you want to use
        -------------------------
        Example:

          model = Text_Model()

          model.predict(
            api_key='1234',
            input_sentence='This is a test sentence!',
            model_name='aTextModel'
          )
        '''
        if api_key == None:
            raise Exception('Please enter your api key to run predictions.')
        
        if model_name == None:
            raise Exception('Please pass your model name to the parameter "model_name"')
        
        if input_sentence == None:
            raise Exception('To make a preiction, please pass a sentence through the "input_sentence" paramter.')
        
        payload = {
            'api_key': api_key,
            'inference': input_sentence,
            'model_name': model_name,
        }

        url = "https://zgkojasf0f.execute-api.us-east-2.amazonaws.com/text-model-prediction"
        r = requests.post(url, data=json.dumps(payload))
        response = json.loads(r.text)

        try:
            if response['status'] == 'Success':
                print('Prediction:', response['prediction'])
                print('-' * 20)
                print(
                    'Model Name: ' + model_name + '\n' +
                    'Prediction: ' +  response['prediction'][0] + '\n' +
                    'Status: Success'
                )
                
                print('-' * 20)
                print(
                    'JSON:' +
                    '\n{\n' +
                    '   Model_name: ' + model_name + '\n'
                    '   Prediction:' + response['prediction'][0] + '\n' +
                    '   Status: Success\n}'
                )
                return response['prediction']
            else:
                print(response)
        except:
            raise Exception('Server timeout. Please try again.')



    def edit_model(self, api_key=None, references_path=None, model_name=None):
        '''
        -------------------------
        Edit an existing Text Classification Model.
        -------------------------
        Param:

          api_key (string):
            The api key for your clevrML developer account
          
          references_path (string):
            The path to your references file (.txt) for your Text Model. These references
            and classes will either be added or newly created to your model.
          
          model_name (string):
            The name of the model that will be edited.
        
        -------------------------
        Example:

          model = Text_Model()

          model.edit_model(
            api_key='1234',
            references_path='my_new_Reference_values.txt',
            model_name='Text_Model_1'
          )

        '''
        if api_key == None:
            raise Exception('Please enter your api key to create a text model')
        
        if model_name == None:
            raise Exception('Please pass your model name to the parameter "model_name"')
        
        else:
            print('Editing model, this may take up to a couple of minutes....')
            text_model_request = {}

            with open(references_path) as f:
                ref = f.read()
                data = ref.split('\n')

                for j in data:
                    find_comma = j.find(',')
                    example = j[find_comma+1:]
                    class_name = j[:find_comma]
                    
                    if class_name in text_model_request:
                        reference_examples = text_model_request[class_name]
                        reference_examples.append(example)
                    else:
                        text_model_request[class_name] = [example]

            payload = {
                'api_key': api_key,
                'model_request': text_model_request,
                'model_name': model_name

            }

            
            url = "https://nw2d63wb99.execute-api.us-east-2.amazonaws.com/text-model-edit"
            r = requests.post(url, data=json.dumps(payload))
            response = json.loads(r.text)

            try:
                if response['status'] == 'Success':
                    print('Your model has been updated!\n\nDetails:')
                    print('-' * 20)
                    print(
                        'Model Name: ' + model_name + '\n' +
                        'Deployed: True\n' + 
                        'Status: Complete'
                    )
                    
                    print('-' * 20)
                    print(
                        'JSON:' +
                        '\n{\n' +
                        '   Model_name: ' + model_name + '\n'
                        '   Deployed: True\n' + 
                        '   Status: Complete\n}'
                    )
                
                else:
                    print(response)
            except:
                raise Exception('Server timeout. Please try again.')