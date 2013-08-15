CREATE TABLE `user_bank_account` (
      `id` int(10) NOT NULL AUTO_INCREMENT,
      `user_id` int(10) NOT NULL,
      `account_num` varchar(30) CHARACTER SET latin1 NOT NULL COMMENT '帐号',
      `account_type` tinyint(5) NOT NULL COMMENT '1支付宝2招商3工商4人民银行5交通',
      `priority` tinyint(5) DEFAULT NULL COMMENT '帐号优先级，优先往哪个帐号返利',
      PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
