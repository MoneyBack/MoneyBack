use moneyBack; -- 切换到moneyBack数据库

/*电商信息表*/
DROP TABLE IF EXISTS `electric_purchaser`; 
CREATE TABLE `electric_purchaser` (
      `id` int(10) NOT NULL AUTO_INCREMENT,
      `merchant_id` int(10) NOT NULL COMMENT '电商在联盟的ID',
      `name` varchar(50) NOT NULL COMMENT 'name of electric purchaser',
      `merchant_cat_id` int(10) NOT NULL COMMENT 'category ID',
      `merchant_cat_name` varchar(50) NOT NULL COMMENT 'name of category',
      `type` tinyint(4) NOT NULL COMMENT '1电商 2团购 3精品推荐网站',
      `url` varchar(100) NOT NULL,
      `logo_url` varchar(100) NOT NULL,
      `pretty_logo` varchar(20) NOT NULL COMMENT '本地logo图片',
      `click_url` varchar(1024) NOT NULL,
      `description` varchar(2048) NOT NULL COMMENT '站点的详细描述',
      `url_source` tinyint(4) NOT NULL COMMENT '1from office 2from user',
      `rebate` tinyint(4) NOT NULL COMMENT '0不参加返利 1参加返利',
      `rebate_info` varchar(1024) NOT NULL COMMENT '返利信息',
      `collection` int(20) NOT NULL DEFAULT '0' COMMENT '被用户添加量',
      `click_rate` bigint(50) NOT NULL COMMENT '点击率',
      `sale_promotion` tinyint(4) NOT NULL COMMENT '是否有优惠活动',
      PRIMARY KEY (`id`),
      UNIQUE INDEX `index_var` (`merchant_id`, `name`) -- 唯一索引
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
