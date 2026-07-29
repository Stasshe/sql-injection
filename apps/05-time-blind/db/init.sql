CREATE DATABASE IF NOT EXISTS ctf05;
USE ctf05;

CREATE TABLE subscribers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(100) NOT NULL UNIQUE
);

-- 1行のみ: SLEEP()を含むWHERE句は行数分評価されるため、行数が多いと
-- 遅延が積み重なって読みにくくなる。1回分の遅延で安定させる。
INSERT INTO subscribers (email) VALUES ('alice@example.com');

CREATE TABLE flags (
  id INT AUTO_INCREMENT PRIMARY KEY,
  flag VARCHAR(100) NOT NULL
);

INSERT INTO flags (flag) VALUES ('FLAG{time_based_blind_sleep_injection}');
