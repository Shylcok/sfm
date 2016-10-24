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
--  Table structure for `sfm_address`
-- ----------------------------
DROP TABLE IF EXISTS `sfm_address`;
CREATE TABLE `sfm_address` (
  `id` int(10) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '自增id',
  `user_id` varchar(32) NOT NULL COMMENT '用户id',
  `name` varchar(60) COMMENT '收件人',
  `mobile` varchar(32) DEFAULT '' COMMENT '联系电话',
  `address` varchar(128) DEFAULT '' COMMENT '收件地址',
  `person_number` varchar(60) DEFAULT '' COMMENT '身份证号码',
  `is_default` tinyint(4) DEFAULT 0 COMMENT '是否是默认地址'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收货人地址表';

SET FOREIGN_KEY_CHECKS = 1;
