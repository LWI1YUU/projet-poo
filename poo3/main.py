import mysql.connector
from mysql.connector import Error
import getpass

def create_connection():
    """ Crée et retourne une connexion à la base de données MySQL. """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='',
            database='clinique'
        )
        print("Connexion à MySQL réussie")
        return connection
    except Error as e:
        print(f"L'erreur '{e}' est survenue")
        return None

def login_medecin():
    """ Permet au médecin de se connecter en vérifiant ses identifiants. """
    username = input("Entrez votre nom d'utilisateur : ")
    password = getpass.getpass("Entrez votre mot de passe : ")
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM medecin WHERE nom = %s AND password = %s"
        cursor.execute(query, (username, password))
        if cursor.fetchone():
            print("Connexion réussie.")
            doctor_menu()  # Appeler le menu du docteur après une connexion réussie
        else:
            print("Nom d'utilisateur ou mot de passe incorrect.")
        connection.close()

def sign_up_medecin():
    """ Permet au médecin de créer un compte. """
    username = input("Choisissez un nom d'utilisateur : ")
    password = getpass.getpass("Choisissez un mot de passe : ")
    specialite = input("Entrez votre spécialité : ")
    available = input("Êtes-vous disponible ? (1 pour oui, 0 pour non) : ")

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "INSERT INTO medecin (nom, specialite, password, available) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(query, (username, specialite, password, available))
            connection.commit()
            print("Inscription réussie. Bienvenue !")
        except Error as e:
            print(f"L'erreur '{e}' est survenue lors de l'inscription.")
        finally:
            connection.close()
def doctor_menu():
    """ Affiche le menu du docteur et gère les choix. """
    while True:
        print("\nMenu du Docteur")
        print("1. Enregistrer un patient")
        print("2. Voir les patients")
        print("3. Éditer les infos du patient")
        print("4. Supprimer un patient")
        print("5. Remplir le dossier médical")
        print("6. Enregistrer un rendez-vous")
        print("7. Voir et gérer les rendez-vous")
        print("8. Quitter")
        choix = input("Entrez votre choix (1-8): ")

        if choix == '1':
            register_patient()
        elif choix == '2':
            check_patients()
        elif choix == '3':
            edit_patient_info()
        elif choix == '4':
            delete_patient()
        elif choix == '5':
            fill_medical_record()
        elif choix == '6':
            schedule_appointment()
        elif choix == '7':
            view_and_manage_appointments()
        elif choix == '8':
            print("Déconnexion réussie.")
            break
        else:
            print("Choix invalide, veuillez réessayer.")



# Fonctions pour gérer les patients (à intégrer dans le code)
def register_patient():
    """ Enregistre un nouveau patient dans la base de données. """
    nom = input("Nom du patient : ")
    date_naissance = input("Date de naissance (YYYY-MM-DD) : ")
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "INSERT INTO patient (nom, date_naissance) VALUES (%s, %s)"
        try:
            cursor.execute(query, (nom, date_naissance))
            connection.commit()
            print("Patient enregistré avec succès.")
        except Error as e:
            print(f"L'erreur '{e}' est survenue lors de l'enregistrement.")
        finally:
            connection.close()


def check_patients():
    """ Affiche tous les patients enregistrés. """
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT id, nom, date_naissance FROM patient"
        cursor.execute(query)
        results = cursor.fetchall()
        print("Liste des patients :")
        for patient in results:
            print(f"ID: {patient[0]}, Nom: {patient[1]}, Date de Naissance: {patient[2]}")
        connection.close()


def edit_patient_info():
    """ Modifie les informations d'un patient spécifique. """
    patient_id = input("Entrez l'ID du patient à éditer : ")
    nouveau_nom = input("Nouveau nom (laissez vide si inchangé) : ")
    nouvelle_date = input("Nouvelle date de naissance (YYYY-MM-DD, laissez vide si inchangé) : ")
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "UPDATE patient SET nom = %s, date_naissance = %s WHERE id = %s"
        cursor.execute(query, (nouveau_nom or None, nouvelle_date or None, patient_id))
        connection.commit()
        print("Informations du patient mises à jour.")
        connection.close()

def delete_patient():
    """ Supprime un patient de la base de données après avoir supprimé tous les dossiers médicaux liés. """
    patient_id = input("Entrez l'ID du patient à supprimer : ")
    try:
        patient_id = int(patient_id)  # Assure que l'ID est un entier
    except ValueError:
        print("L'ID doit être un nombre entier.")
        return

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # D'abord, supprimer les dossiers médicaux liés
            delete_dossiers_query = "DELETE FROM dossier_medical WHERE id_patient = %s"
            cursor.execute(delete_dossiers_query, (patient_id,))

            # Ensuite, supprimer le patient
            delete_patient_query = "DELETE FROM patient WHERE id = %s"
            cursor.execute(delete_patient_query, (patient_id,))
            if cursor.rowcount > 0:
                connection.commit()
                print("Patient et dossiers médicaux liés supprimés avec succès.")
            else:
                print("Aucun patient trouvé avec cet ID.")
        except Error as e:
            print(f"L'erreur '{e}' est survenue lors de la suppression du patient.")
            connection.rollback()  # Annule les modifications en cas d'erreur
        finally:
            connection.close()




def fill_medical_record():
    """ Remplit ou met à jour le dossier médical d'un patient. """
    patient_id = input("Entrez l'ID du patient : ")
    maladie = input("Entrez la maladie diagnostiquée : ")
    medicament = input("Entrez le médicament attribué : ")
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "INSERT INTO dossier_medical (maladie, id_patient, medicament_attribue) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (maladie, patient_id, medicament))
            connection.commit()
            print("Dossier médical mis à jour avec succès.")
        except Error as e:
            print(f"L'erreur '{e}' est survenue lors de la mise à jour du dossier.")
        finally:
            connection.close()
def schedule_appointment():
    """ Enregistre un rendez-vous dans la base de données. """
    id_patient = input("Entrez l'ID du patient : ")
    id_medecin = input("Entrez l'ID du médecin : ")
    date_rendez_vous = input("Entrez la date du rendez-vous (YYYY-MM-DD) : ")
    
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "INSERT INTO rendez_vous (date_rendez_vous, id_patient, id_medecin) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (date_rendez_vous, id_patient, id_medecin))
            connection.commit()
            print("Rendez-vous enregistré avec succès.")
        except Error as e:
            print(f"L'erreur '{e}' est survenue lors de l'enregistrement du rendez-vous.")
        finally:
            connection.close()
def view_and_manage_appointments():
    """ Affiche les rendez-vous et permet de les supprimer. """
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT id, date_rendez_vous, id_patient, id_medecin FROM rendez_vous"
        cursor.execute(query)
        results = cursor.fetchall()
        print("Liste des rendez-vous :")
        for appointment in results:
            print(f"ID: {appointment[0]}, Date: {appointment[1]}, ID Patient: {appointment[2]}, ID Médecin: {appointment[3]}")

        delete_choice = input("Souhaitez-vous supprimer un rendez-vous ? (oui/non) : ")
        if delete_choice.lower() == 'oui':
            appointment_id = input("Entrez l'ID du rendez-vous à supprimer : ")
            delete_query = "DELETE FROM rendez_vous WHERE id = %s"
            cursor.execute(delete_query, (appointment_id,))
            connection.commit()
            print("Rendez-vous supprimé avec succès.")
        connection.close()            


def menu():
    """ Affiche le menu principal et gère les choix de l'utilisateur. """
    while True:
        print("\nMenu Principal")
        print("1. Se connecter")
        print("2. S'inscrire")
        print("3. Quitter")
        choix = input("Entrez votre choix (1-3): ")

        if choix == '1':
            login_medecin()
        elif choix == '2':
            sign_up_medecin()
        elif choix == '3':
            print("Merci d'avoir utilisé notre système. À bientôt!")
            break
        else:
            print("Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    menu()
