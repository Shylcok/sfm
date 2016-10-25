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
--  Table structure for `sfm_cart` 购物车
-- ----------------------------
DROP TABLE IF EXISTS `sfm_cart`;
CREATE TABLE `sfm_cart` (
  `id` int(10) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '自增id',
  `user_id` varchar(32) COMMENT '用户id',
  `sku_id` varchar(32) COMMENT '商品sku_id',
  `sku_count` int(10) COMMENT '该sku数量',
  `time` int(11) COMMENT '更新时间',
  UNIQUE index `user_id` (`user_id`, `sku_id`) COMMENT '用户id skuid索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='购物车表';

SET FOREIGN_KEY_CHECKS = 1;
