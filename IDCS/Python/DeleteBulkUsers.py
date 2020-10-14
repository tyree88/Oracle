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
  #Replace URl with the URL you use in your IDCS Environment
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
  if not users:
    return 'No more Ids'
  url = "idcs-58bd1066a98f41198b51f1c4f68610ef.identity.oraclecloud.com"
  conn = http.client.HTTPSConnection(url)
  token = getToken()
  addToPayload = ''
  """
  Loop through all the userIds and create a bulk delete
  -add the userId with a force delete.
  -for the last id do not add a common
  """
  for i in range(len(users)):
    print(i)
    if i == len(users)-1:
        addToPayload += "{\r\n      \"method\": \"DELETE\",\r\n      \"path\": \"/Users/"+users[i]+"?forceDelete=true\"\r\n    }"
    else:
      addToPayload += "{\r\n      \"method\": \"DELETE\",\r\n      \"path\": \"/Users/"+users[i]+"?forceDelete=true\"\r\n    },"
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




"""
getUsers:
  Steps:
   1.gets Resource Field
   2.then grabs the id field (this will be based into delete api)
   3.then you check to see if a user is an admin
   4.return the ids for the non admin users
"""
def filterUsers():
  token = getToken()
  url = "idcs-58bd1066a98f41198b51f1c4f68610ef.identity.oraclecloud.com"
  print(f'url is {url} \n')
  conn = http.client.HTTPSConnection(url)
  payload = ''
  headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json'
  }
  """
  STEPS:
  - Do a Get to get the total Resources so we can determine how much loops we must go through
  - create a json response of user Ids that are not in group "OCI_Administrators"
  - based on the totalResults get the number of thousands and hundered to increment startIndex by
  """
  OCI_Administrators = "874fda9c517f4d85a10bc191909a2326" #group ID Number you want to enter.
  count = 1
  startIndex = str(count)
  conn.request("GET", "/admin/v1/Users?count=1000&attributes=groups&filter=groups.value+ne+%22"+OCI_Administrators+"%22+&sortBy=userName&startIndex="+startIndex, payload, headers)
  res = conn.getresponse()
  data = res.read()
  data_decoded = (data.decode("utf-8"))
  #create a json format
  json_response = json.loads(data_decoded)
  pprint(json_response)
  #get the total Results from json response
  total = json_response['totalResults']
  print(total)

  thousands = 1000*(math.floor(total / 1000))
  hundreds = total % 1000
  print(f'there are {thousands} thousand \nthere are {hundreds} hundred')
  #create the unique set for the all the users
  userIds = [x['id'] for x in json_response['Resources']]
  ids = set(userIds)
  #print(userIds)
  count = 1000
  """
  Loop through the user IDs and do a bulk delete until it is finish
  - This paginates by a thousand users per bulk delete.
  - takes the last hundered and applies to the startIndex to delete the rest.
  Prints out how many users are left.
  """
  while json_response['Resources']:
    print(count)
    payload = ''
    headers = {
      'Authorization': 'Bearer '+token,
      'Content-Type': 'application/json'
    }
    """
    While resources are not empty iterate on start index retreving 1000 users per page
    - divide a thousand by the total users then round down to find the number of thousands for start index
    - find the remainder of the number of hundred to get the start index from there.
    """

    OCI_Administrators = "874fda9c517f4d85a10bc191909a2326" #group ID Number you want to enter.
    startIndex = str(count)
    conn.request("GET", "/admin/v1/Users?count=1000&attributes=groups&filter=groups.value+ne+%22"+OCI_Administrators+"%22+&sortBy=userName&startIndex="+startIndex, payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(f'data is type {type(data)}\n')

    data_decoded = (data.decode("utf-8"))
    #print(f'data_decoded is {data_decoded}')
    json_response = json.loads(data_decoded)
    #print(type(json_response))
    #print(f'there are {thousands} thousand \nthere are {hundreds} hundred')
    userIds = [x['id'] for x in json_response['Resources']]
    print(userIds)
    ids.update(userIds)
    if count >= total:
      print(f'total ids are {len(ids)} \nAll the ids are {ids}')
      break
    if (total-count)>1000:
      print(f'{total} - {count} = {total-count}')
      count += 1000
    else:
      count = count + hundreds

  print("\n")
  print(total)
  print(f'\ntotal ids are {len(ids)}\n')
  return ids




def getGroups():
  conn = http.client.HTTPSConnection("idcs-58bd1066a98f41198b51f1c4f68610ef.identity.oraclecloud.com")
  payload = ''
  token = getToken()
  headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json'
  }
  conn.request("GET", "/admin/v1/Groups?count=1000&attributes=members,displayName", payload, headers)
  res = conn.getresponse()
  data = res.read()
  data_decoded = (data.decode("utf-8"))
  #create a json format
  json_response = json.loads(data_decoded)
  #pprint(json_response['Resources'])
  #print(type(json_response['Resources']))
  dictGroups = json_response['Resources']
  all_groups = [x['displayName'] for x in json_response['Resources']]
  all_groupIds = [x['id'] for x in json_response['Resources']]
  groupIds =set(all_groupIds)
  groups_with_members = []
  groups_with_members_ids =set()
  for group in dictGroups:
    for key, value in group.items():
      if key =="members":
        groups_with_members.append(group['displayName'])
        groups_with_members_ids.add(group['id'])
  print(f'All groups are {all_groups}\nAll groups Ids are {all_groupIds}\nThere is a total of {len(all_groups)} groups\n')
  print(f'Groups with members: {groups_with_members}\nAll group Ids of Groups with members are {groups_with_members_ids}\nThere is a total of {len(groups_with_members)} groups with members')
  #get difference of all the groups and the ones with members so we get only groups with no members
  pprint(groupIds)
  pprint(groups_with_members_ids)
  groups = (groupIds-groups_with_members_ids)
  pprint(groups)
  #return group Ids
  return groups




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
  Get the amount of users that are left. do a loop with delete.
  then check if users are left, if so loop through and delete until users are empty
  """
  users = filterUsers()
  #pprint(users)
  count = 0

  #Delete all users not in Admin group 
  while users:
    count +=1
    userIds = filterUsers()
    print(f'user Ids are:\n {userIds}\n')
    idsList = list(userIds)
    deleteUsers(idsList)
    users = filterUsers()
    print(f'This is loop {count}\nThere are these users left {users}')

  groups = list(getGroups())
  #remove AllUsersId from list (this is the All Tenet User Group and Should not be removed)
  groups.remove('AllUsersId')
  print(f'all the groupIds of groups without members are:{groups}')
  #delete all the empty groups
  deleteGroups(groups)


if __name__ == "__main__" :main()