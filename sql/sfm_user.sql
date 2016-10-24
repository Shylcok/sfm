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
--  Table structure for `sfm_user`
-- ----------------------------
DROP TABLE IF EXISTS `sfm_user`;
CREATE TABLE `sfm_user` (
  `id` int(10) unsigned NOT NULL auto_increment COMMENT '用户id',
  `mobile` varchar(32) NOT NULL COMMENT '手机号',
  `pwd_md5` VARCHAR(32) NOT NULL COMMENT 'pwd md5',
  `user_name` varchar(32) NOT NULL COMMENT '用户名',
  `email` varchar(32) DEFAULT '' COMMENT '邮箱',
  `head_img` varchar(255) DEFAULT '' COMMENT '头像',
  `register_dt` int(11) NOT NULL COMMENT '注册时间',
  `lastlogin` int(11) NOT NULL DEFAULT '0' COMMENT '最后登录时间',
  `lastloginip` varchar(15) NOT NULL DEFAULT '' COMMENT '最后登录ip',
  `nick_name` varchar(32) DEFAULT '' COMMENT '昵称',
  `signature` varchar(128) DEFAULT '' COMMENT '个性签名',
  `sex` tinyint(1) DEFAULT '0' COMMENT '性别,0是男',
  `location` varchar(128) DEFAULT '' COMMENT '用户所属地区',
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `user_name` (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

SET FOREIGN_KEY_CHECKS = 1;
