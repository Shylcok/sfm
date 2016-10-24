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
  `card_id` varchar(32) COMMENT '额度卡编号',
  `amount` decimal COMMENT '总额度',
  `remain_amount` decimal COMMENT '剩余额度',
  INDEX `card_id` (`card_id`) COMMENT '额度卡编号索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='信用额度卡表';

SET FOREIGN_KEY_CHECKS = 1;
