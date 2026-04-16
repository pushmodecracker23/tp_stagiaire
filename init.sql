-- Création de la base de données
CREATE DATABASE IF NOT EXISTS db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE db;

-- Table des clients
CREATE TABLE IF NOT EXISTS client (
    id           VARCHAR(10)    PRIMARY KEY,
    name         VARCHAR(100)   NOT NULL,
    balance      DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    account_type VARCHAR(20)    NOT NULL
);

-- Table des produits
CREATE TABLE IF NOT EXISTS product (
    id    VARCHAR(10)    PRIMARY KEY,
    name  VARCHAR(100)   NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT            NOT NULL DEFAULT 0
);

-- Insertion des clients
INSERT INTO client (id, name, balance, account_type) VALUES
    ('C001', 'Marie Dupont',        15234.50,  'Standard'),
    ('C002', 'Jean-Pierre Martin',  87650.00,  'Premium'),
    ('C003', 'Sophie Leclerc',     250000.00,  'VIP');

-- Insertion des produits
INSERT INTO product (id, name, price, stock) VALUES
    ('P001', 'Laptop Pro 15"',                1299.99, 12),
    ('P002', 'Souris ergonomique sans fil',     49.99, 45),
    ('P003', 'Bureau standing électrique',     799.00,  8),
    ('P004', 'Chaise de bureau ergonomique',   349.00, 20),
    ('P005', 'Casque audio premium',           249.99, 30);
