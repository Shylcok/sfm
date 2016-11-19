/*
 Navicat Premium Data Transfer

 Source Server         : javalocal
 Source Server Type    : MySQL
 Source Server Version : 50629
 Source Host           : 172.16.2.41
 Source Database       : 55haitao_dev

 Target Server Type    : MySQL
 Target Server Version : 50629
 File Encoding         : utf-8

 Date: 10/13/2016 15:30:02 PM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `sfm_credit_card`
-- ----------------------------
DROP TABLE IF EXISTS `sfm_credit_card`;
CREATE TABLE `sfm_credit_card` (
  `id` int(10) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '自增id',
  `user_id` int(10) COMMENT '用户id',
  `card_id` varchar(32) COMMENT '额度卡编号',
  `amount` int(10) COMMENT '总额度',
  `remain_amount` int(10) COMMENT '剩余额度',
  UNIQUE KEY `card_id` (`card_id`) COMMENT '额度卡编号索引',
  UNIQUE KEY `user_id` (`user_id`) COMMENT '订单索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='信用额度卡表';

SET FOREIGN_KEY_CHECKS = 1;

alter table sfm_credit_card add channel VARCHAR(50) not null DEFAULT 'sfm' COMMENT '渠道';
alter table sfm_credit_card add update_time int(11) NOT null DEFAULT unix_timestamp(now()) COMMENT '更新时间';
