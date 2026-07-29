CREATE DATABASE IF NOT EXISTS ctf04;
USE ctf04;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(64) NOT NULL,
  is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO users (username, is_admin) VALUES
  ('alice', FALSE),
  ('bob', FALSE),
  ('admin', TRUE);

CREATE TABLE flags (
  id INT AUTO_INCREMENT PRIMARY KEY,
  flag VARCHAR(100) NOT NULL
);

INSERT INTO flags (flag) VALUES ('FLAG{boolean_blind_binary_search}');
