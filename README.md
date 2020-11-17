
# Oracle
To help whoever needs to do a bulk delete of users in IDCS
link for all IDCS API documentation: https://docs.oracle.com/en/cloud/paas/identity-cloud/rest-api/index.html


# IDCS 
the file in the IDCS folder contains a [bulk delete users](https://github.com/tyree88/Oracle/blob/master/IDCS/Python/DeleteBulkUsers.py)python script, [bulk delete groups](https://github.com/tyree88/Oracle/blob/master/IDCS/Python/DeleteBulkGroups.py) python script, [bulk delete users and groups](https://github.com/tyree88/Oracle/blob/master/IDCS/Python/DeleteBulkUsers%26Groups.py) python script

## Bulk Delete users and Groups
- 
- 1 . This script grabs the users in group OCI_Administrators
- 2 . Filters out the ids for each user in this group into an admins array
- 3 . Passes the rest of the users in a set array so only unique values are entered
- 4 . returns the set array into a delete function that do a total removal from all resources in the tenancy

# Requirements
Do these below to adjust the script to fit your environment
-
- 1.Getting the Access Token to use the IDCS API. Follow The tutorial below. 
  - https://www.oracle.com/webfolder/technetwork/tutorials/obe/cloud/idcs/idcs_rest_postman_obe/rest_postman.html
  
    - Here are the instructions for the images below^ 
    - These will help you set up the Environment Variables in Postman, get Access token, and provide an environment to test the APIs you are using in the code.
    ![Create the Application in IDCS](https://github.com/tyree88/Oracle/blob/master/IDCS/Images/Screen%20Shot%202020-10-22%20at%201.07.06%20PM.png?raw=true)
    
    ![Postman Setup](https://github.com/tyree88/Oracle/blob/master/IDCS/Images/Screen%20Shot%202020-10-22%20at%201.07.46%20PM.png?raw=true)
    
    ![Import the Postman Collection](https://github.com/tyree88/Oracle/blob/master/IDCS/Images/Screen%20Shot%202020-10-22%20at%201.08.14%20PM.png?raw=true)
    
    ![Request the Access Token](https://github.com/tyree88/Oracle/blob/master/IDCS/Images/Screen%20Shot%202020-10-22%20at%201.08.31%20PM.png?raw=true)
    
  
- 2.Change the URLs variables
![Change the urls](https://github.com/tyree88/Oracle/blob/master/IDCS/Images/Change%20URLs.png?raw=true)
 
 
 -2. Change the Group ID Variable
 ![Find each Group Variable and Change it to the right id number]
 
 ![you get the Id number you are looking for by searching on postman](https://github.com/tyree88/Oracle/blob/master/IDCS/Images/Screen%20Shot%202020-11-17%20at%2010.15.37%20AM.png?raw=true)

# BULK Delete 
The Bulk delete script uses the IDCS API. This is how to navigate through it
- 
1. getToken function gets an access token that is refresehed every api call and passed into a variable to process the GET pull.

2. First there is a GET pull from the search all Users Api. 
  - 2a. there are added params to get a count of user input variable and the attribute groups 
    - 2aa. the count variable will be used to determine how many items per page are allowed for the pull. 
    - 2ab. this is important because it will determnine how many ids will be returned. So if you do not pull enough pages it will not delete all the users desired-   - 2b. pass json response to a get users function

3. the getUsers function parses through the returned API to get the "groups" of each user. 
 -  3a. group returns a dict that has the key "display" - shows the group names associated with the user 
 -  3b. the value of the key "display" is the name of the group in IDCS
 -  3c. if the users are in group 'OCI_Administrators' append to the admins list
 -  3d. else add to the set array 'ids'. Return this array to the main function and into delete users
 
4. deleteUsers gets an access token from getToken() and does DELETE request for each id in the id array
 -  4a. the DELETE request takes in a user inside a for loop that does a 'forceDelete' so it removes all instances with the user


