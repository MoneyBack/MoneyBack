#1. execute the initDevEnv.sql
#2. execute other sql file to create tables
    ###import table sql to the database directory + fileName
    eg: source /home/aaron/Workspace/eletric_purchaser.sql 


#PROBLEMS:

###if you can't connect to the host of databse, you should type follow cmd to let your db host accept all con to the 3306 port of db
iptables -I INPUT -p TCP --dport 3306 -j ACCEPT 

