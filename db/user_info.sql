CREATE TABLE `user_info`(
    `id` int(10) NOT NULL AUTO_INCREMENT,
    `user_name` varchar(50) NOT NULL,
    `nick_name` varchar(50) NOT NULL,
    `email` varchar(40) DEFAULT NULL,
    `phone` varchar(30) DEFAULT NULL,
    `salt` varchar(30) NOT NULL COMMENT 'random num for encrypt pwd',
    `passwd` varchar(30) NOT NULL COMMENT 'encrypted content',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
