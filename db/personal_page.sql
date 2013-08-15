CREATE TABLE `personal_page` (
    `id` int(10) NOT NULL AUTO_INCREMENT,
    `user_id` int(10) NOT NULL,
    `merchant_id` int(10) NOT NULL,
    `visist_num` int(15) NOT NULL DEFAULT '0' COMMENT 'HOW MANY TIMES USER VISIT THE URL',
    PRIMARY KEY (`id`),
    UNIQUE KEY `user_merchant_id` (`user_id`, `merchant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
