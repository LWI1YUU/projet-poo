import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("Connexion à MySQL réussie")
    except Error as e:
        print(f"L'erreur '{e}' est survenue")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Base de données créée avec succès")
    except Error as e:
        print(f"L'erreur '{e}' est survenue")

def create_table(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Table créée avec succès")
    except Error as e:
        print(f"L'erreur '{e}' est survenue")

connection = create_connection("localhost", "root", "")  # Remplacez 'root' et '' par votre utilisateur et mot de passe MySQL

# Créer la base de données
create_database(connection, "CREATE DATABASE IF NOT EXISTS clinique")

# Connecter à la base de données créée
connection.database = 'clinique'

# Créer les tables
create_table(connection, """
CREATE TABLE IF NOT EXISTS patient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    date_naissance DATE NOT NULL
)
""")

create_table(connection, """
CREATE TABLE IF NOT EXISTS medecin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    specialite VARCHAR(255) NOT NULL,
    available TINYINT NOT NULL
)
""")

create_table(connection, """
CREATE TABLE IF NOT EXISTS dossier_medical (
    id INT AUTO_INCREMENT PRIMARY KEY,
    maladie VARCHAR(255) NOT NULL,
    id_patient INT,
    medicament_attribue VARCHAR(255),
    FOREIGN KEY (id_patient) REFERENCES patient(id)
)
""")

create_table(connection, """
CREATE TABLE IF NOT EXISTS rendez_vous (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_rendez_vous DATE NOT NULL,
    id_patient INT,
    id_medecin INT,
    FOREIGN KEY (id_patient) REFERENCES patient(id),
    FOREIGN KEY (id_medecin) REFERENCES medecin(id)
)
""")

# Fermer la connexion
connection.close()
