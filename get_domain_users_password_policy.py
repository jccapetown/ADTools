import subprocess

proc = subprocess.Popen(['net', 'user','/domain'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        shell=False)
stdout_value = proc.communicate()[0]

records = stdout_value.split('\r')
userlist = []
for users in records:
    if (not users.replace('\r','').strip() == '') and \
    (not '---' in users) and \
    (not "complete" in users) and \
    (not "The " in users)and \
    (not "User accounts" in users):  
        for user in users.split():
            userlist.append(user)

#we now have all the users
#print userlist
#save userlist
f = open('domainusers.txt', 'w')            
for user in userlist:
    f.write('%s \n' % user)
f.close()


#now lets get the use password config
f = open('passwordinfo.txt', 'w')

for user in userlist:
    print "Checking user : %s" % user
    proc = subprocess.Popen(['net', 'user',user,'/domain'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        shell=False)
    stdout_value = proc.communicate()[0]
    #print stdout_value
    
    records = stdout_value.split('\r')
    attriblist = []
    for attribs in records:
        if (not "complete" in attribs) and \
        (not "The " in attribs):  
            attriblist.append(attribs.strip())
            if ("Account active" in attribs) or \
               ("Account expires" in attribs)or \
               ("Password last set" in attribs)or \
               ("Password expires" in attribs)or \
               ("Password required" in attribs)or \
               ("User may change password" in attribs)or \
               ("Workstations allowed" in attribs)or \
               ("Last logon" in attribs)or \
               ("Logon hours allowed" in attribs)or\
               ("Global Group memberships" in attribs):
                print user,'->', attribs.strip()
                f.write('%s-> %s \n' % (user,attribs.strip())  )
f.close()
    

