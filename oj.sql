/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 50650
 Source Host           : localhost:3306
 Source Schema         : oj

 Target Server Type    : MySQL
 Target Server Version : 50650
 File Encoding         : 65001

 Date: 26/05/2024 20:17:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for problem
-- ----------------------------
DROP TABLE IF EXISTS `problem`;
CREATE TABLE `problem`  (
  `pid` int(8) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `flag` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `example` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `tips` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `create_date` date NULL DEFAULT NULL,
  `pass_rate` float NULL DEFAULT NULL,
  `difficulty` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`pid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of problem
-- ----------------------------
INSERT INTO `problem` VALUES (1, '两数之和', '给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target  的那 两个 整数，并返回它们的数组下标。\r\n\r\n你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。\r\n\r\n你可以按任意顺序返回答案。', NULL, '{\r\n	\"1\": [\"输入：nums = [2,7,11,15], target = 9\", \"输出：[0,1]\", \"解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。\"],\r\n	\"2\": [\"输入：nums = [3,2,4], target = 6\", \"输出：[1,2]\", \"\"],\r\n	\"3\": [\"输入：nums = [3,3], target = 6\", \"输出：[0,1]\"]\r\n}', '{\r\n	\"1\":  \"2 <= nums.length <= 10^4\",\r\n	\"2\":  \"-10^9 <= nums[i] <= 10^9\",\r\n	\"3\":  \"-10^9 <= target <= 10^9\",\r\n    \"4\": \"只会存在一个有效答案\"\r\n}', '2024-05-26', 0, '简单');
INSERT INTO `problem` VALUES (2, '两数相加', '给你两个 非空 的链表，表示两个非负的整数。它们每位数字都是按照 逆序 的方式存储的，并且每个节点只能存储 一位 数字。\r\n\r\n请你将两个数相加，并以相同形式返回一个表示和的链表。\r\n\r\n你可以假设除了数字 0 之外，这两个数都不会以 0 开头。', NULL, '{\r\n	\"1\": [\"输入：l1 = [2,4,3], l2 = [5,6,4]\", \"输出：[7,0,8]\", \"解释：342 + 465 = 807\"],\r\n	\"2\": [\"输入：l1 = [0], l2 = [0]\", \"输出：[0]\"],\r\n	\"3\": [\"输入：l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]\", \"输出：[8,9,9,9,0,0,0,1]\"]\r\n}', '{\r\n	\"1\":  \"每个链表中的节点数在范围 [1, 100] 内\",\r\n	\"2\":  \"0 <= Node.val <= 9\",\r\n	\"3\":  \"题目数据保证列表表示的数字不含前导零\"\r\n}', '2024-05-26', 0, '中等');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(9) NOT NULL AUTO_INCREMENT,
  `username` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(13) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (2, 'test', '123456');
INSERT INTO `user` VALUES (3, 'test2', '123456');

SET FOREIGN_KEY_CHECKS = 1;
