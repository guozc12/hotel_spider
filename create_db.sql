-- CREATE DATABASE IF NOT EXISTS hotel_spider;
DROP DATABASE IF EXISTS hotel_spider;
CREATE DATABASE hotel_spider;
USE hotel_spider;

CREATE TABLE hotels (
  id INT(10) AUTO_INCREMENT PRIMARY KEY,
  source VARCHAR(255) NOT NULL COMMENT '数据来源: meituan, ctrip, expedia',
  country VARCHAR(255) NOT NULL COMMENT '国家',
  city VARCHAR(255) NOT NULL COMMENT '酒店所在城市',
  raw_name VARCHAR(255) NOT NULL COMMENT '酒店原始名称(平台显示名称)',
  brand VARCHAR(255) NOT NULL COMMENT '酒店品牌',
  branch VARCHAR(255) NOT NULL COMMENT '分店名称/地址',
  url VARCHAR(255) NOT NULL COMMENT '酒店url',
  created_at datetime DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE rooms (
  id INT(10) AUTO_INCREMENT PRIMARY KEY,
  hotel_id INT(10) UNSIGNED,
  name VARCHAR(255) COMMENT '房间名称,比如 “高级大床房”',
  created_at datetime DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  -- FOREIGN KEY (hotel_id) REFERENCES hotels(id)
);

CREATE TABLE products (
  id INT(10) AUTO_INCREMENT PRIMARY KEY,
  hotel_id INT(10) UNSIGNED,
  room_id INT(10) UNSIGNED,
  name VARCHAR(255) COMMENT '产品名称,比如 “特惠双床房+￥15美团外卖券”',
  price INT(10) UNSIGNED COMMENT '产品价格',
  created_at datetime DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  -- FOREIGN KEY (room_id) REFERENCES rooms (id)
);