CREATE DATABASE IF NOT EXISTS ctf03;
USE ctf03;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(64) NOT NULL,
  is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO users (username, is_admin) VALUES
  ('alice', FALSE),
  ('bob', FALSE),
  ('admin', TRUE);

-- Unrelated table, never referenced by the app itself.
CREATE TABLE secrets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  flag VARCHAR(100) NOT NULL
);

INSERT INTO secrets (flag) VALUES ('FLAG{numeric_context_blind_injection_no_quotes_needed}');
