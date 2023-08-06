# pythonroblox
A Python Module for Roblox API. Easy Useable User and Group Classes.

# User - Class

**Intializing**
```py
import pythonroblox
user = pythonroblox.User()
```
**Searching Username**
```py
import pythonroblox
user = pythonroblox.User()
result  = user.search_name("Roblox")
print(result.id) #1
```
**Searching User ID**
```py
import pythonroblox
user = pythonroblox.User()
result  = user.search_id(1)
print(result.name) #Roblox
```

**Searching user ID and Name returns the Given Below list of Attributes:**
```
id
banned
name
created_date
displayName
description
status
number_groups
friends_count
followers_count
following_count
avatar_url
```
**And Functions :**
```
get_groups_data()
get_all_groups_data()
roblox_badges()
get_primary_group()
get_username_history()
```
# Groups - Class
**Initializing**
```py
import pythonroblox
groups = pythonroblox.Groups()
```
**Search Id**
```py
import pythonroblox
groups = pythonroblox.Groups()
result = groups.search_id(1)
print(result.name) #RobloHunks
```
**Search Name**
```py
import pythonroblox
groups = pythonroblox.Groups()
result = groups.search_name("RobloHunks")
print(result.id) #1
```
**Search Name and Search ID for Groups Returns the Following Attribrutes :**
```
name 
description 
owner_name 
owner_displayName 
owner_id  
shout_details 
member_count 
public_entry_allowed 
id
```
**Search Name and Search ID for Groups Returns the Following Functions :**
```
get_total_results()
get_shout_details()
```

