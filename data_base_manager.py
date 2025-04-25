#!/usr/bin/env python3
"""
Etienne POUILLE PROJECT, 2025
Mon moteur de recherche personnel pour idées
"""

import sqlite3
from datetime import datetime
import csv
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from contextlib import contextmanager


class BaseDeDonnees:
    """
    Gestion de la base de données des idées
    """

    def __init__(self, db_file='mes_idees.db'):
        self.db_file = db_file
        self.initialiser_db()
    
    @contextmanager
    def connexion(self):
        """
        Gestionnaire de contexte pour la connexion à la base de données
        """

        conn = sqlite3.connect(self.db_file)
        try:
            yield conn
        finally:
            conn.close()
    
    def initialiser_db(self):
        """
        Crée ou met à jour la structure de la table
        """

        with self.connexion() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(idees)")
            colonnes = [col[1] for col in cursor.fetchall()]
            
            if not colonnes:
                cursor.execute('''CREATE TABLE idees 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        texte TEXT NOT NULL, 
                        description TEXT, 
                        tags TEXT, 
                        date TEXT)''')
            elif "description" not in colonnes:
                cursor.execute("ALTER TABLE idees ADD COLUMN description TEXT")
            conn.commit()
    
    def ajouter_idee(self, texte, description, tags=""):
        """
        Ajoute une nouvelle idée à la base de données
        """

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.connexion() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO idees (texte, description, tags, date) VALUES (?, ?, ?, ?)", 
                (texte, description, tags, date))
            conn.commit()
            return True
    
    def rechercher_idee(self, mot_cle):
        """
        Recherche des idées contenant le mot-clé
        """

        with self.connexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM idees 
                    WHERE texte LIKE ? OR tags LIKE ? OR description LIKE ?""", 
                    (f"%{mot_cle}%", f"%{mot_cle}%", f"%{mot_cle}%"))
            return cursor.fetchall()
    
    def afficher_toutes_idees(self):
        """
        Récupère toutes les idées de la base de données
        """

        with self.connexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM idees")
            return cursor.fetchall()
    
    def supprimer_idee(self, id_idee):
        """
        Supprime une idée par son ID
        """

        with self.connexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM idees WHERE id = ?", (id_idee,))
            supprime = cursor.rowcount > 0
            conn.commit()
            return supprime
    
    def exporter_idees(self, nom_fichier='mes_idees_export.csv'):
        """
        Exporte les idées vers un fichier CSV
        """

        try:
            with self.connexion() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM idees")
                idees = cursor.fetchall()

            with open(nom_fichier, 'w', newline='', encoding='utf-8') as fichier:
                writer = csv.writer(fichier)
                writer.writerow(['ID', 'Texte', 'Description', 'Tags', 'Date'])
                writer.writerows(idees)
            return True
        except Exception:
            return False

class MoteurIdeesApp:
    """
    Interface graphique pour le moteur de recherche d'idées
    """

    def __init__(self, root):
        self.root = root
        self.db = BaseDeDonnees()
        self.configurer_interface()

    def configurer_interface(self):
        """
        Configure l'interface utilisateur
        """

        self.root.title("Moteur de recherche pour mes idées")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Configuration du redimensionnement
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Création et configuration des cadres
        self.creer_cadre_entree()
        self.creer_cadre_resultats()

    def creer_cadre_entree(self):
        """
        Crée le cadre supérieur avec les contrôles d'entrée
        """

        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky="ew")
        frame.grid_columnconfigure(1, weight=1)

        # Formulaire d'ajout
        ttk.Label(frame, text="Idée :").grid(row=0, column=0, sticky="w")
        self.texte_entry = ttk.Entry(frame, width=50)
        self.texte_entry.grid(row=0, column=1, columnspan=2, pady=5, sticky="ew")

        ttk.Label(frame, text="Description :").grid(row=1, column=0, sticky="w")
        self.desc_entry = ttk.Entry(frame, width=50)
        self.desc_entry.grid(row=1, column=1, columnspan=2, pady=5, sticky="ew")

        ttk.Label(frame, text="Tags :").grid(row=2, column=0, sticky="w")
        self.tags_entry = ttk.Entry(frame, width=50)
        self.tags_entry.grid(row=2, column=1, columnspan=2, pady=5, sticky="ew")

        # Boutons d'actions principales
        boutons_frame = ttk.Frame(frame)
        boutons_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")
        boutons_frame.columnconfigure(tuple(range(4)), weight=1)

        ttk.Button(boutons_frame, text="Ajouter", command=self.ajouter).grid(row=0, column=0, padx=5)
        ttk.Button(boutons_frame, text="Tout afficher", command=self.tout_afficher).grid(row=0, column=1, padx=5)
        ttk.Button(boutons_frame, text="Exporter en CSV", command=self.exporter).grid(row=0, column=2, padx=5)

        # Recherche
        rech_frame = ttk.LabelFrame(frame, text="Recherche")
        rech_frame.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")
        rech_frame.columnconfigure(1, weight=1)

        ttk.Label(rech_frame, text="Mot-clé :").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.recherche_entry = ttk.Entry(rech_frame)
        self.recherche_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(rech_frame, text="Rechercher", command=self.rechercher).grid(row=0, column=2, padx=5, pady=5)

        # Suppression
        suppr_frame = ttk.LabelFrame(frame, text="Suppression")
        suppr_frame.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")
        suppr_frame.columnconfigure(1, weight=1)

        ttk.Label(suppr_frame, text="ID :").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.id_entry = ttk.Entry(suppr_frame, width=10)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(suppr_frame, text="Supprimer", command=self.supprimer).grid(row=0, column=2, padx=5, pady=5)

    def creer_cadre_resultats(self):
        """
        Crée le cadre des résultats
        """

        frame = ttk.LabelFrame(self.root, text="Résultats")
        frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.resultats_text = scrolledtext.ScrolledText(frame)
        self.resultats_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.resultats_text.config(wrap=tk.WORD)

    def ajouter(self):
        """
        Ajoute une nouvelle idée
        """

        texte = self.texte_entry.get().strip()
        description = self.desc_entry.get().strip()
        tags = self.tags_entry.get().strip()

        if not texte:
            messagebox.showwarning("Attention", "Le champ 'Idée' est obligatoire.")
            return

        try:
            if self.db.ajouter_idee(texte, description, tags):
                messagebox.showinfo("Succès", "Idée ajoutée avec succès !")
                self.texte_entry.delete(0, tk.END)
                self.desc_entry.delete(0, tk.END)
                self.tags_entry.delete(0, tk.END)
                self.tout_afficher()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ajouter l'idée : {str(e)}")

    def rechercher(self):
        """
        Recherche des idées par mot-clé
        """

        mot_cle = self.recherche_entry.get().strip()
        if not mot_cle:
            messagebox.showwarning("Attention", "Veuillez entrer un mot-clé pour rechercher.")
            return

        try:
            resultats = self.db.rechercher_idee(mot_cle)
            self.afficher_resultats(resultats, f"Recherche : '{mot_cle}'")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche : {str(e)}")

    def tout_afficher(self):
        """
        Affiche toutes les idées
        """

        try:
            resultats = self.db.afficher_toutes_idees()
            self.afficher_resultats(resultats, "Toutes les idées")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage : {str(e)}")

    def afficher_resultats(self, resultats, titre="Résultats"):
        """
        Affiche les résultats dans la zone de texte
        """

        self.resultats_text.delete(1.0, tk.END)
        self.resultats_text.insert(tk.END, f"=== {titre} ===\n\n")

        if resultats:
            for idee in resultats:
                self.resultats_text.insert(tk.END, 
                    f"ID: {idee[0]}\n"
                    f"Texte: {idee[1]}\n"
                    f"Description: {idee[2] or 'N/A'}\n"
                    f"Tags: {idee[3] or 'N/A'}\n"
                    f"Date: {idee[4]}\n"
                    f"{'-' * 40}\n"
                )
        else:
            self.resultats_text.insert(tk.END, "Aucune idée trouvée.\n")
    
    def supprimer(self):
        """
        Supprime une idée par son ID
        """

        id_str = self.id_entry.get().strip()
        if not id_str or not id_str.isdigit():
            messagebox.showwarning("Attention", "Veuillez entrer un ID valide (nombre entier).")
            return

        id_idee = int(id_str)
        try:
            if self.db.supprimer_idee(id_idee):
                messagebox.showinfo("Succès", f"Idée avec ID {id_idee} supprimée.")
                self.id_entry.delete(0, tk.END)
                self.tout_afficher()
            else:
                messagebox.showwarning("Attention", f"Aucune idée trouvée avec l'ID {id_idee}.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression : {str(e)}")

    def exporter(self):
        """
        Exporte les idées vers un fichier CSV
        """

        try:
            if self.db.exporter_idees():
                messagebox.showinfo("Succès", "Idées exportées dans mes_idees_export.csv")
            else:
                messagebox.showwarning("Attention", "Erreur lors de l'exportation.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exportation : {str(e)}")

def main():
    """
    Point d'entrée principal de l'application
    """

    root = tk.Tk()
    app = MoteurIdeesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
