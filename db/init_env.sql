create database if not exists moneyBack;
grant usage on *.* to mbuser@"%"; -- drop user if not exists XX 不支持的解决方案 
drop user mbuser; -- 删除用户
create user mbuser identified by 'mbfighter'; -- mbfighter is pwd
grant select, insert, update, delete,create, alter on moneyBack.* to mbuser@"%" identified by "mbfighter"; -- grant the privilege to the mbuseate 
flush privileges; -- 刷新系统权限表