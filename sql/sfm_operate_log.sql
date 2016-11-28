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
DROP TABLE IF EXISTS `sfm_operate_log`;
CREATE TABLE `sfm_operate_log` (
  `id` int(10) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '自增id',
  `user_id` varchar(32) COMMENT '用户id',
  `target_id` varchar(32) COMMENT '目标id',
  `target_type` VARCHAR(32) COMMENT '目标类型',
  `log` varchar(200) COMMENT '操作日志',
  `time` int(11) COMMENT '操作时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志';

SET FOREIGN_KEY_CHECKS = 1;
