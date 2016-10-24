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
--  Table structure for `sfm_pay`
-- ----------------------------
DROP TABLE IF EXISTS `sfm_pay`;
CREATE TABLE `sfm_pay` (
  `id` int(10) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '自增id',
  `water_id` varchar(32) COMMENT '流水号',
  `channel_id` int(10) COMMENT '付款方式 0 微信，1支付宝，3额度卡',
  `channel_water_id` varchar(32) COMMENT '三方流水号',
  `account` varchar(60) COMMENT '付款账户',
  `amount` decimal COMMENT '支付金额',
  `order_id` varchar(32) COMMENT '支付对应的订单号',
  `time` int(11) COMMENT '支付时间',
  UNIQUE KEY `water_id` (`water_id`) COMMENT '支付流水索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='支付表';

SET FOREIGN_KEY_CHECKS = 1;
