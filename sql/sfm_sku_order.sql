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
--  Table structure for `sfm_sku_order` 订单中的商品表
-- ----------------------------
DROP TABLE IF EXISTS `sfm_sku_order`;
CREATE TABLE `sfm_sku_order` (
  `id` int(10) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '自增id',
  `order_id` varchar(32) NOT NULL COMMENT '订单号',
  `sku_id` varchar(32) NOT NULL COMMENT '商品sku_id',
  `sku_count` int(10) NOT NULL COMMENT '商品数量',
  `sku_weight` float(10) COMMENT '商品重量',
  `sku_amount` int(10) COMMENT '商品单价',
  `sku_name` varchar(200) COMMENT '商品名称',
  `sku_image_url` varchar(500) COMMENT '商品图片地址',
  `first_price` int(10) DEFAULT 0 COMMENT '商品选择的首付价格',
  INDEX `order_id` (`order_id`) COMMENT '订单索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单中的商品表';

SET FOREIGN_KEY_CHECKS = 1;
