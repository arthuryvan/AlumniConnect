
# README - AlumniConnect

## Présentation

AlumniConnect est une plateforme web développée avec Flask qui facilite la mise en relation entre les étudiants et les anciens élèves (alumni) d'un établissement. L'objectif principal est de favoriser le mentorat, le partage d'expérience professionnelle et l'accompagnement des étudiants dans leur parcours académique et professionnel.

## Fonctionnalités

### Authentification

* Inscription des utilisateurs
* Connexion et déconnexion sécurisées
* Gestion des rôles (Étudiant / Alumni)

### Gestion des profils

* Informations personnelles
* Filière
* Promotion
* Entreprise
* Biographie

### Mentorat

* Consultation de la liste des mentors
* Recherche de mentors
* Envoi d'une demande de mentorat
* Acceptation d'une demande de mentorat
* Refus d'une demande de mentorat
* Notifications liées aux demandes

## Technologies utilisées

### Backend

* Python
* Flask
* SQLAlchemy
* Flask-WTF

### Frontend

* HTML5
* CSS3
* Bootstrap

### Base de données

* SQLite (développement)
* MySQL (production possible)

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/votre-compte/alumniconnect.git
cd alumniconnect
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
```

### 3. Activer l'environnement virtuel

Windows :

```bash
venv\Scripts\activate
```

Linux / Mac :

```bash
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Lancer l'application

```bash
python app.py
```

L'application sera accessible à l'adresse :

```text
http://127.0.0.1:5000
```

## Structure du projet

```text
AlumniConnect/
│
├── app.py
├── models.py
├── forms.py
├── static/
│   ├── css/
│   └── images/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── mentors.html
│   ├── demandes_mentorat.html
│   └── notifications.html
│
└── instance/
    └── alumniconnect.db
```

## Utilisation

### Étudiant

1. Créer un compte.
2. Se connecter.
3. Rechercher un mentor.
4. Envoyer une demande de mentorat.
5. Consulter les notifications.

### Alumni

1. Créer un compte.
2. Se connecter.
3. Consulter les demandes reçues.
4. Accepter ou refuser une demande.
5. Accompagner les étudiants.

## Perspectives d'amélioration

* Messagerie privée
* Gestion des événements
* Publication d'opportunités de stage et d'emploi
* Système de recommandations
* Tableau de bord avancé
* Notifications en temps réel

## Auteur

ETOUKE ETOUKE Yvan

Projet académique réalisé dans le cadre de l'apprentissage du développement web avec Flask.
