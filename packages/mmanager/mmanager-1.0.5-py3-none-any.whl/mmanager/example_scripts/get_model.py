from mmanager.mmanager import Model

secret_key = "Secret-Key"

url = 'http://modelmanager.ai/'

model_id = 'model_id' #use model id
#for data
try:
    Model(secret_key,url).get_model(model_id)
except ConnectionResetError as e:
    print(str(e))

