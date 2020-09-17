import http.client
import mimetypes
import ssl 
import json
from pprint import pprint

"""
getUsers:
  Steps:
   1.gets Resource Field
   2.then grabs the id field (this will be based into delete api)
   3.then you check to see if a user is an admin 
   4.return the ids for the non admin users 
"""
def getUsers(users):
  print(f'users is type{type(users)}\n')
  pprint(users)
  print('\n\n')
  ids = set()
  dupids = []
  admins = []
  for key, value in users.items():
    if key == "Resources":
      print(f'key: {key} \n value: {value[1]} ')
      print(type(value[1]))
      #pprint(value)
      pprint(value[1])
      """Parse through fields with key values of each user"""
      for user_key in value:
        #print('user_key is:\n')
        #pprint(user_key)
        for key, value in user_key.items():
          if key == "groups":
            #print(f'value is: \n {value}\n')
            #list(filter(lambda person: person['name'] == 'Pam', people))
            dict_values = list(filter(lambda admin: admin['display'] =='OCI_Administrators', value))
            if dict_values:
              print(f'OCI_Administrators ids are : {user_key["id"]}')
              admins.append(user_key["id"])
            else:
              ids.add(user_key["id"])
              dupids.append(user_key["id"])
              #admin.append(key['id'])
            # for dict_key, dict_value in value:
            #   if dict_value['display'] == 'OCI_Administrators':
            #     print(f'id for this user is {user_key["id"]}')
          else:
            dupids.append(user_key["id"])
            ids.add(user_key["id"])

        #   user_value = user_key['idcsCreatedBy']
        #   #This get the non admins 
        #   if user_value['display'] != 'OCI_Administrators':
        #     ids.append(user_key['id'])
        
  #         #This gets admins      
  #         if user_value['display']=='idcssm':
  #           admins.append(user_key['id'])
            
  print(f'ids that are NOT created by idcs:\n {ids}\n')
  print(f'duplicate ids that are NOT created by idcs:\n {dupids}\n')
  print(f'admins created by idcs are:\n {admins}\n')
  return ids  

def getToken():
  url = "idcs-58bd1066a98f41198b51f1c4f68610ef.identity.oraclecloud.com"
  conn = http.client.HTTPSConnection(url)
  payload = 'grant_type=client_credentials&scope=urn%3Aopc%3Aidm%3A__myscopes__'
  headers = {
  'Authorization': 'Basic ZWQzYjBjMGMxNGU0NGQyZDllZTA0NDVjMGIyNjExNjc6NmZjNjY1ZGUtMGRiYS00NGY5LTljZDQtMWQ4NmU3ZDFlYTU4',
  'Content-Type': 'application/x-www-form-urlencoded'
  }
  conn.request("POST", "/oauth2/v1/token", payload, headers)
  res = conn.getresponse()
  data = res.read()
  data_decoded = data.decode("utf-8")
  json_response = json.loads(data_decoded)
  #pprint(json_response)
  #print(type(json_response))
  access_token = json_response['access_token']
  #print(f'acces_token is {access_token}')
  return access_token

"""
deleteUsers:
  Steps:
   1.gets Resource Field
   2.then grabs the id field (this will be based into delete api)
   3.then you check to see if a user is an admin  
""" 
def deleteUsers(users):
  url = "idcs-58bd1066a98f41198b51f1c4f68610ef.identity.oraclecloud.com"
  conn = http.client.HTTPSConnection(url)
  token = getToken()
  payload = ''
  headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json'
  }
  #pprint(users)
  for i in range(50):
    print(users[i])
  for user in users:
    print(user)    
    conn.request("DELETE", "/admin/v1/Users/"+user+"?forceDelete=true", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

  
  
def main(): 
  try:
    _create_unverified_https_context = ssl._create_unverified_context
  except expression as identifier:
    #Legacy python that doesnt verify HTTPS certificated by default
    pass
  else:
    # Handle target environment that doesnt support HTTPS verification 
    ssl._create_default_https_context = _create_unverified_https_context
  """
  - make sure to refresh the token whenver authorization has failed
  - change in the delete users function too
  """
  token = getToken()
  #print(f'the access token is{token}')
  url = "idcs-58bd1066a98f41198b51f1c4f68610ef.identity.oraclecloud.com"
  print(f'url is {url} \n')
  conn = http.client.HTTPSConnection(url)
  payload = ''
  headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json'
  }
  
  conn.request("GET", "/admin/v1/Users?count=1500&startIndex=0&attributes=groups", payload, headers)
  
  res = conn.getresponse()
  print(f'res is type {type(res)}\n')
  
  data = res.read()
  print(f'data is type {type(data)}\n')
  
  data_decoded = (data.decode("utf-8"))
  #print(f'data_decoded is {data_decoded}')
  
  json_response = json.loads(data_decoded)
  pprint(json_response)
  
  userIds = getUsers(json_response)
  print(f'user Ids are:\n {userIds}\n')
  idsList = list(userIds)
  deleteUsers(idsList)
  
if __name__ == "__main__" :main()