CREATE DATABASE IF NOT EXISTS ctf02;
USE ctf02;

CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  category VARCHAR(50) NOT NULL
);

INSERT INTO products (name, description, price, category) VALUES
  ('Widget Pro', 'A professional-grade widget.', 19.99, 'tools'),
  ('Gadget Mini', 'A compact gadget for everyday use.', 9.50, 'electronics'),
  ('Super Wrench', 'Adjustable wrench, chrome finish.', 14.25, 'tools'),
  ('Bluetooth Speaker', 'Portable speaker with 10h battery.', 39.99, 'electronics'),
  ('Garden Hose 20m', 'Reinforced garden hose.', 24.00, 'garden'),
  ('Desk Lamp LED', 'Adjustable brightness desk lamp.', 17.75, 'home');

-- Unrelated table, never referenced by the app itself. Not linked to products.
CREATE TABLE secrets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  flag VARCHAR(100) NOT NULL
);

INSERT INTO secrets (flag) VALUES ('FLAG{union_based_information_schema_enumeration}');
