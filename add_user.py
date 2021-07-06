import os
import pwd
import re
import grp
import crypt
import random
import string
#Open file and set it in variable with read only permission
input_file = open("list1.txt", "r")
#read all existing lines and create array
user_list = input_file.readlines()
#close file
input_file.close()
#loop through array line by line
#This variable defines lenth of the random password.
pass_len = 10
waiting_list = "waitinglist_"

#Function creats random password for user
def password_gen(length):
    # get all lowercase letter from ascii
    letters = string.ascii_lowercase
    #pick randomly characters from the list 
    result_str = ''.join(random.choice(letters) for i in range(length))
    #retern a string of characters randomly generated
    return result_str
#Function cheks if user exists
def is_user_exist(username):
    try:
        if pwd.getpwnam(username):
            return True 
    except:
        return False
#Function cheks if group exists
def is_group_exist(groupname):
    try:
        if grp.getgrnam(groupname):
            print (f"Group {groupname} already exist.")
            return True
    except:
        return False
#Function adds user
def create_user(username):
    try:
        os.system(f'useradd -p {password_gen(pass_len)} {username}')
    except:
        print("There is error in user creation")
#Function adds a new group
def create_group(groupname):
    try:
        os.system(f'groupadd {groupname}')
        print (f"Group {groupname} doesn't exist, so has created")
    except:
        print ("There is error in group creation")
#Function cheks how many users in the group
def check_users_in_group(group):
    users_number = grp.getgrnam(group)
    users_number = len(users_number.gr_mem)
    return users_number

#Function adds user in the group
def add_user_in_group(username, groupname):
    try:
        os.system(f"adduser {username} {groupname}")
    except:
        print ("There is an error in user group greation.")

#Those a few loops check requarements for user and group creation
for idx, user in enumerate(user_list):
    # ignore first two lines in the file with header and next line
    if idx < 2:
        continue
    #Split list element by spaces
    user_data = re.split("\s+", user)
    username = user_data[0]
    #Check if user exist
    if is_user_exist(username) == True:
        print (f"User {username} already exist",idx)
        continue
    else:
        #User dooesn't exist, create user
        create_user(username)
        print (f"User {username} has created.",idx)
        #Parce list in range of 1 to 7 indexes to filter groups
        user_groups = user_data[1:7]
        #Check dashes in the groups list
        for group in user_groups:
            if group == "-":
                continue
            #Check is group exist
            if is_group_exist(group) == True:
                #check is number of users less then 10
                if check_users_in_group(group) < 10:
                    #Add user in this group
                    add_user_in_group(username, group)
                else:
                    #Create report
                    full_name = (f"{user_data[7]} {user_data[8]}")
                    def report_add(file_name, username, full_name, group):
                        try:
                            if os.path.isfile(file_name) == False:
                                edit_file = open(file_name, "x")
                                edit_file.close()
                                edit_file = open(file_name, "at")
                                edit_file.write(f'{username} {full_name} {group} \n')
                                edit_file.close()
                            else:
                                edit_file = open(file_name, "at")
                                edit_file.write(f"{username} {full_name} {group} \n")
                                edit_file.close()
                        except:
                            print ("There is en error in report creation.")
                    report_add(waiting_list+group, username, full_name, group)
                    #Create waiting list group if users in the group more then 10
                    if is_group_exist(waiting_list+group) == True:
                            #Add user in existin waiting list
                            add_user_in_group(username, waiting_list+group)
                            print (f"User {username} has added in {waiting_list}{group}.")
                    else:
                        #Create new waiting list
                        create_group(waiting_list+group)
                        print(f"Group {waiting_list}{group} has created.")
                        #Add user in new created waiting list
                        add_user_in_group(username, waiting_list+group)
                        print (f"User {username} has added in {waiting_list}{group} group.")
            else:
                #Create new group
                create_group(group)
                #Add user in new group
                add_user_in_group(username, group)
