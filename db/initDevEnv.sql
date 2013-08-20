create database if not exists moneyBack;
drop user mbuser; -- 删除用户
create user mbuser identified by 'mbfighter'; -- mbfighter is pwd
grant select, insert, update, delete,create, alter on moneyBack.* to mbuser@"%" identified by "mbfighter"; -- grant the privilege to the mbuseate 
flush privileges; -- 刷新系统权限表