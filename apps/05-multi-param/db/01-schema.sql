CREATE DATABASE IF NOT EXISTS ctf05;
USE ctf05;

CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255) NOT NULL,
  price DECIMAL(10,2) NOT NULL
);

INSERT INTO products (name, description, price) VALUES
  ('Widget Pro', 'A professional-grade widget.', 19.99),
  ('Gadget Mini', 'A compact gadget for everyday use.', 9.50),
  ('Super Wrench', 'Adjustable wrench, chrome finish.', 14.25),
  ('Bluetooth Speaker', 'Portable speaker with 10h battery.', 39.99),
  ('Garden Hose 20m', 'Reinforced garden hose.', 24.00),
  ('Desk Lamp LED', 'Adjustable brightness desk lamp.', 17.75);

CREATE TABLE flags (
  id INT AUTO_INCREMENT PRIMARY KEY,
  flag VARCHAR(100) NOT NULL
);
