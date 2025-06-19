-- Création de la base de données
CREATE DATABASE IF NOT EXISTS gestion_jus;
USE gestion_jus;

-- Table Client
CREATE TABLE Client (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    telephone VARCHAR(20),
    date_inscription DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Table Transaction
CREATE TABLE Transaction (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    date_transaction DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2) NOT NULL,
    adresse_livraison VARCHAR(255) NOT NULL,
    CONSTRAINT fk_transaction_client FOREIGN KEY (client_id) REFERENCES Client(client_id) ON DELETE CASCADE
);

-- Table Jus
CREATE TABLE Jus (
    jus_id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prix_unitaire DECIMAL(7, 2) NOT NULL
);

-- Table Transaction_Jus (relation N:M entre Transaction et Jus)
CREATE TABLE Transaction_Jus (
    transaction_id INT NOT NULL,
    jus_id INT NOT NULL,
    quantite INT NOT NULL CHECK (quantite > 0),
    PRIMARY KEY (transaction_id, jus_id),
    CONSTRAINT fk_transaction FOREIGN KEY (transaction_id) REFERENCES Transaction(transaction_id) ON DELETE CASCADE,
    CONSTRAINT fk_jus FOREIGN KEY (jus_id) REFERENCES Jus(jus_id) ON DELETE CASCADE
);

-- Table Ingrédient
CREATE TABLE Ingredient (
    ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL
);

-- Table Jus_Ingrédient (relation N:M entre Jus et Ingrédient)
CREATE TABLE Jus_Ingredient (
    jus_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    quantite DECIMAL(7, 2) NOT NULL CHECK (quantite > 0), -- Quantité en grammes ou millilitres
    PRIMARY KEY (jus_id, ingredient_id),
    CONSTRAINT fk_jus_compo FOREIGN KEY (jus_id) REFERENCES Jus(jus_id) ON DELETE CASCADE,
    CONSTRAINT fk_ingredient FOREIGN KEY (ingredient_id) REFERENCES Ingredient(ingredient_id) ON DELETE CASCADE
);

-- Table pour stocker les mots de passe des clients
CREATE TABLE Client_Password (
    password_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL, -- On stocke ici le hash du mot de passe, pas le mot de passe en clair
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_client_password FOREIGN KEY (client_id) REFERENCES Client(client_id) ON DELETE CASCADE
);