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
