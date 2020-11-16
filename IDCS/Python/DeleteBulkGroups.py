import http.client
import mimetypes
import ssl
import json
import math
from pprint import pprint

"""
GetToken
- Get the token that will be used in the other functions for the Access Token in the Authoritzation String
- for any new user enter in a new url
"""
def getToken():
  #url 1 that you must change
  url = "idcs-58bd1066a98f41198b51f1c4f68610ef.identity.oraclecloud.com"
  conn = http.client.HTTPSConnection(url)
  payload = 'grant_type=client_credentials&scope=urn%3Aopc%3Aidm%3A__myscopes__'
  #change the Auth from the test code in Postman
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





def deleteGroups(groups):
  if not groups:
    return "No empty groups"
  url = "idcs-58bd1066a98f41198b51f1c4f68610ef.identity.oraclecloud.com"
  conn = http.client.HTTPSConnection(url)
  token = getToken()
  addToPayload = ''
  """
  Loop through all the userIds and create a bulk delete
  -add the userId with a force delete.
  -for the last id do not add a common
  """
  for i in range(len(groups)):
    print(i)
    if i == len(groups)-1:
        addToPayload += "{\r\n      \"method\": \"DELETE\",\r\n      \"path\": \"/Groups/"+groups[i]+"\"\r\n    }"
    else:
      addToPayload += "{\r\n      \"method\": \"DELETE\",\r\n      \"path\": \"/Groups/"+groups[i]+"\"\r\n    },"
  #print(addToPayload)
  payload =\
  "{\r\n  \"schemas\":\
      [\r\n\
      \"urn:ietf:params:scim:api:messages:2.0:BulkRequest\"\
      \r\n  ],\
  \r\n  \"Operations\": \
      [\r\n\
        "+addToPayload+"\r\n  \
      ]\r\n\
    }"
  headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json'
  }
  conn.request("POST", "/admin/v1/Bulk", payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))


def getGroups():
  conn = http.client.HTTPSConnection("idcs-58bd1066a98f41198b51f1c4f68610ef.identity.oraclecloud.com")
  payload = ''
  token = getToken()
  headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json'
  }
  conn.request("GET", "/admin/v1/Groups?count=1000&attributes=members,displayName&filter=not(members+pr)", payload, headers)
  res = conn.getresponse()
  data = res.read()
  data_decoded = (data.decode("utf-8"))
  #create a json format
  json_response = json.loads(data_decoded)
  pprint(json_response)
  #print(type(json_response['Resources']))
  dictGroups = json_response['Resources']
  '''
    Below does:
      - a list comprehnsion to gather all the group names of groups without members
        - this is for testing purposes to make sure the groups you have are correct
      - a list comprehnsion to gather all the group IDs of groups without members
      - puts all the groupIds in a set because all groups are unique

  '''
  all_groups = [x['displayName'] for x in json_response['Resources']]
  all_groupIds = [x['id'] for x in json_response['Resources']]
  groupIds =set(all_groupIds)
  print(f'All groups are {all_groups}\nAll groups Ids are {all_groupIds}\nThere is a total of {len(all_groups)} groups\n')
  #get difference of all the groups and the ones with members so we get only groups with no members
  pprint(groupIds)

  pprint(f'the total numbers of groups are {len(groupIds)}')
  return groupIds
  #return groups


def main():
  try:
    _create_unverified_https_context = ssl._create_unverified_context
  except expression as identifier:
    #Legacy python that doesnt verify HTTPS certificated by default
    pass
  else:
    # Handle target environment that doesnt support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

  groups = list(getGroups())
  #remove AllUsersId from list (this is the All Tenet User Group and Should not be removed)
  groups.remove('AllUsersId')
  print(f'all the groupIds of groups without All Tenet User Group are:{groups}')
  print(f'length all the groupIds of groups without All Tenet User Group are:{len(groups)}')

  #delete all the empty groups
  deleteGroups(groups)
  groups = list(getGroups())
  print(f'all the groupIds of groups without members are:{groups}')
  print(f'len all the groupIds of groups without members are:{len(groups)}')
  if len(groups)> 1:
    groups.remove('AllUsersId')
    deleteGroups(groups)



if __name__ == "__main__" :main()