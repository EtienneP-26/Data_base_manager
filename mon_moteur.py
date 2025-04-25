##
## Etienne POUILLE PROJECT, 2025
## mon_moteur_de_recherche
## File description:
## mon_moteur
##


import sqlite3
from datetime import datetime
import csv
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

conn = sqlite3.connect('mes_idees.db')
c = conn.cursor()

def mettre_a_jour_table():
    c.execute("PRAGMA table_info(idees)")
    colonnes = [col[1] for col in c.fetchall()]
    if not colonnes:
        c.execute('''CREATE TABLE idees 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                texte TEXT NOT NULL, 
                description TEXT, 
                tags TEXT, 
                date TEXT)''')
    elif "description" not in colonnes:
        c.execute("ALTER TABLE idees ADD COLUMN description TEXT")
    conn.commit()

mettre_a_jour_table()

def ajouter_idee(texte, description, tags=""):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO idees (texte, description, tags, date) VALUES (?, ?, ?, ?)", 
        (texte, description, tags, date))
    conn.commit()
    return True

def rechercher_idee(mot_cle):
    c.execute("SELECT * FROM idees WHERE texte LIKE ? OR tags LIKE ? OR description LIKE ?", 
        (f"%{mot_cle}%", f"%{mot_cle}%", f"%{mot_cle}%"))
    return c.fetchall()

def afficher_toutes_idees():
    c.execute("SELECT * FROM idees")
    return c.fetchall()

def supprimer_idee(id):
    c.execute("DELETE FROM idees WHERE id = ?", (id,))
    conn.commit()
    return True

def exporter_idees():
    c.execute("SELECT * FROM idees")
    idees = c.fetchall()
    with open('mes_idees_export.csv', 'w', newline='', encoding='utf-8') as fichier:
        writer = csv.writer(fichier)
        writer.writerow(['ID', 'Texte', 'Description', 'Tags', 'Date'])
        writer.writerows(idees)
    return True

class MoteurIdeesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Moteur de recherche pour mes idées")
        self.root.geometry("800x600")

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky="ew")

        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(frame, text="Idée :").grid(row=0, column=0, sticky="w")
        self.texte_entry = ttk.Entry(frame, width=50)
        self.texte_entry.grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(frame, text="Description :").grid(row=1, column=0, sticky="w")
        self.desc_entry = ttk.Entry(frame, width=50)
        self.desc_entry.grid(row=1, column=1, pady=5, sticky="ew")

        ttk.Label(frame, text="Tags (séparés par des virgules) :").grid(row=2, column=0, sticky="w")
        self.tags_entry = ttk.Entry(frame, width=50)
        self.tags_entry.grid(row=2, column=1, pady=5, sticky="ew")

        ttk.Button(frame, text="Ajouter", command=self.ajouter).grid(row=3, column=0, pady=5)
        ttk.Button(frame, text="Rechercher", command=self.rechercher).grid(row=6, column=2, pady=5)
        ttk.Button(frame, text="Tout afficher", command=self.tout_afficher).grid(row=4, column=0, pady=5)
        ttk.Button(frame, text="Exporter en CSV", command=self.exporter).grid(row=4, column=1, pady=5)

        ttk.Label(frame, text="ID à supprimer :").grid(row=5, column=0, sticky="w")
        self.id_entry = ttk.Entry(frame, width=10)
        self.id_entry.grid(row=5, column=1, sticky="w", pady=5)
        ttk.Button(frame, text="Supprimer", command=self.supprimer).grid(row=5, column=1, pady=5, padx=5)

        self.resultats_text = scrolledtext.ScrolledText(root)
        self.resultats_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # "nsew" pour s'étendre dans toutes les directions

        ttk.Label(frame, text="Mot-clé :").grid(row=6, column=0, sticky="w")
        self.recherche_entry = ttk.Entry(frame, width=30)
        self.recherche_entry.grid(row=6, column=1, pady=5, sticky="ew")

    def ajouter(self):
        texte = self.texte_entry.get()
        description = self.desc_entry.get()
        tags = self.tags_entry.get()
        if texte:
            if ajouter_idee(texte, description, tags):
                messagebox.showinfo("Succès", "Idée ajoutée avec succès !")
                self.texte_entry.delete(0, tk.END)
                self.desc_entry.delete(0, tk.END)
                self.tags_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Erreur", "Le champ 'Idée' est obligatoire.")

    def rechercher(self):
        mot_cle = self.recherche_entry.get()
        if mot_cle:
            resultats = rechercher_idee(mot_cle)
            self.resultats_text.delete(1.0, tk.END)
            if resultats:
                for idee in resultats:
                    self.resultats_text.insert(tk.END, f"ID: {idee[0]} | Texte: {idee[1]} | "
                        f"Description: {idee[2]} | Tags: {idee[3]} | "
                        f"Date: {idee[4]}\n")
            else:
                self.resultats_text.insert(tk.END, "Aucune idée trouvée.\n")
        else:
            messagebox.showwarning("Erreur", "Entre un mot-clé pour rechercher.")

    def tout_afficher(self):
        resultats = afficher_toutes_idees()
        self.resultats_text.delete(1.0, tk.END)
        if resultats:
            for idee in resultats:
                self.resultats_text.insert(tk.END, f"ID: {idee[0]} | Texte: {idee[1]} | "
                    f"Description: {idee[2]} | Tags: {idee[3]} | "
                    f"Date: {idee[4]}\n")
        else:
            self.resultats_text.insert(tk.END, "Aucune idée enregistrée.\n")

    def supprimer(self):
        id = self.id_entry.get()
        if id and id.isdigit():
            if supprimer_idee(int(id)):
                messagebox.showinfo("Succès", f"Idée avec ID {id} supprimée.")
                self.id_entry.delete(0, tk.END)
                self.tout_afficher()
            else:
                messagebox.showwarning("Erreur", "ID non trouvé.")
        else:
            messagebox.showwarning("Erreur", "Entre un ID valide.")

    def exporter(self):
        if exporter_idees():
            messagebox.showinfo("Succès", "Idées exportées dans mes_idees_export.csv")
        else:
            messagebox.showwarning("Erreur", "Erreur lors de l'exportation.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MoteurIdeesApp(root)
    root.mainloop()
    conn.close()
