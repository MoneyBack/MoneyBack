create user mbuser identified by 'mbfighter'; -- mbfighter is pwd
create database moneyBack;
grant select, insert, update, delete,create, alter on moneyBack.* to mbuser@"%" identified by "mbfighter"; -- grant the privilege to the mbuseate 
