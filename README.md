# My Data Base Manager

Un outils personnel pour enregistrer, rechercher et gérer vos ide=ées avec une interface graphique simple et intuitive.

### Description

Ce programme est un Gestionnaire de Bases de Données personnel pour stocker et retrouver facilement vos idées.
Il utilise une base de données SQLite pour sauvegarder toutes vos inspirations, avec des fonctionnalités de recherche par mots-clés, tags et description.

### Fonctionnalités

- ✅ Ajout d'idées avec texte, description et tags.
- 🔍 Recherche d'idées par mots-clés.
- 👀 Affichage de toutes les idées enregistrées.
- 🗑️ Suppression d'idées par ID
- 📊 Export des idées au format CSV

Prochaine Version:
- 📊 Import des idées a partir d'un CSV
- 🔄 Modifier des idées

### Installation

    1. Assurez-vous d'avoir Python 3 installé sur votre système (python3 dans un terminal une version devrait apparaitre)
    2. Clonez ce dépot sur votre machine locale
    3. Aucune dépendance externe n'est nécessaire (le programme utilise uniquement des modules standards Python)

### Utilistaion

Pour lancer l'application, exécutez dans votre terminale sur le depot de votre machine:
```
./data_base_manager.py
```
Ou si il est écrit permission non accordée:
```
python3 data_base_manager.py
```

Interface principale

L'interface se compose de:

    - **Section supérieure**: Formulaire pour ajouter de nouvelles idées et contrôles de recherche
    - **Section inférieuré**: Zone d'affichage des résultats

Ajouter une idée

    1. Remplissez le champ "idée" (obligatoire)
    2. Ajoutez une description détaillée (optionnel)
    3. Spécifiez des tags pour faciliter la recherche future (optionnel)
    4. Cliquez sur "Ajouter"

Rechercher des idées

    1. Entrez un mot-clé dans le champ de recherche
    2. Cliquez sur "Rechercher"
    3. Les résultats s'afficheront dans la zone inférieure

Autres opérations

    - **Tout afficher**: Affiche toutes les idées enregistrées
    - **Supprimer**: Entrez l'ID d'une idée et cliquez sur "Supprimer"
    - **Exporter en CSV**: Crée un fichier CSV avec toutes vos idées

### Structure technique

    - Base de données SQLite (mes_idees.db) pour le stockage persistant
    - Interface graphique avec Tkinter
    - Gestion des erreurs et validation des entrées utilisateur

### Licence
© Etienne POUILLE 2025

Tous droits réservés. POur toute demande d'utilisation, veuillez contacter:
etienne.pouille@epitech.eu
