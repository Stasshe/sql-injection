CREATE DATABASE IF NOT EXISTS ctf01;
USE ctf01;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(64) NOT NULL UNIQUE,
  password VARCHAR(64) NOT NULL,
  is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO users (username, password, is_admin) VALUES
  ('admin', 'Sup3rS3cretAdm1nP@ss', TRUE),
  ('guest', 'guestpass123', FALSE);

CREATE TABLE flags (
  id INT AUTO_INCREMENT PRIMARY KEY,
  flag VARCHAR(100) NOT NULL
);

INSERT INTO flags (flag) VALUES ('FLAG{auth_bypass_tautology_1n_where_clause}');
