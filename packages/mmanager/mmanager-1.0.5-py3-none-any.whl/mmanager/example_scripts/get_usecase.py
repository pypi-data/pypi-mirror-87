from mmanager.mmanager import Usecase


secret_key = "Secret-key"

url = 'http://modelmanager.ai/'

usecase_id = 'Usecase_id' #use usecase id
#for data
try:
    Usecase(secret_key,url).get_usecase(usecase_id)
except ConnectionResetError as e:
    print(str(e))

