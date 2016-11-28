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
--  Table structure for `sfm_auth` 实名认证
-- ----------------------------
DROP TABLE IF EXISTS `sfm_auth`;
CREATE TABLE `sfm_auth` (
  `id` int(10) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '自增id',
  `user_id` VARCHAR(32) COMMENT 'user_id',
  `real_name` varchar(32) COMMENT '真实姓名',
  `id_code` VARCHAR(32) COMMENT '身份证号码',
  `id_card_up` varchar(100) COMMENT '身份证正面',
  `id_card_down` varchar(100) COMMENT '身份证反面',
  `time` int(11) COMMENT '更新时间',
  `pass` int(4) COMMENT '是否认证通过',
  `note` VARCHAR(500) COMMENT '认证失败的原因',
  UNIQUE index `user_id` (`user_id`) COMMENT '用户id索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='实名认证表';

SET FOREIGN_KEY_CHECKS = 1;
