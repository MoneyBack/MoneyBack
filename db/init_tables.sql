/*电商信息表*/
DROP TABLE IF EXISTS `electric_purchaser`; 
CREATE TABLE `electric_purchaser` (
      `id` int(10) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) NOT NULL COMMENT 'name of electric purchaser',
      `type` tinyint(4) NOT NULL COMMENT '1电商 2团购 3精品推荐网站',
      `url` varchar(100) NOT NULL,
      `url_source` tinyint(4) NOT NULL COMMENT '1from office 2 rom user',
      `rebate` tinyint(4) NOT NULL COMMENT '1参加返利 0不参加返利',
      `collection` int(20) NOT NULL DEFAULT '0' COMMENT '被用户添加量',
      `click_rate` bigint(50) NOT NULL COMMENT '点击率',
      `sale_promotion` tinyint(4) NOT NULL COMMENT '是否有优惠活动',
      PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*个人tab页表*/
DROP TABLE IF EXISTS `personal_page`; 
CREATE TABLE `personal_page` (
    `id` int(10) NOT NULL AUTO_INCREMENT,
    `user_id` int(10) NOT NULL,
    `merchant_id` int(10) NOT NULL,
    `visist_num` int(15) NOT NULL DEFAULT '0' COMMENT 'HOW MANY TIMES USER VISIT THE URL',
    PRIMARY KEY (`id`),
    UNIQUE KEY `user_merchant_id` (`user_id`, `merchant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*用户个人银行帐号表*/
DROP TABLE IF EXISTS `user_bank_account`; 
CREATE TABLE `user_bank_account` (
      `id` int(10) NOT NULL AUTO_INCREMENT,
      `user_id` int(10) NOT NULL,
      `account_num` varchar(30) CHARACTER SET latin1 NOT NULL COMMENT '帐号',
      `account_type` tinyint(5) NOT NULL COMMENT '1支付宝2招商3工商4人民银行5交通',
      `priority` tinyint(5) DEFAULT NULL COMMENT '帐号优先级，优先往哪个帐号返利',
      PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*用户个人注册信息表*/
DROP TABLE IF EXISTS `user_info`; 
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
