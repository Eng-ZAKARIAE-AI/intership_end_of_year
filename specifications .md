# Détails des Phases du Projet

## Projet

**Conception et Développement d'un Système Intelligent de Maintenance Informatique basé sur l'IA Générative et le Retrieval-Augmented Generation (RAG)**

---

# Phase 1 — Analyse & Conception

**Période :** 22/07/2026 → 28/07/2026

## Objectifs

- Comprendre les besoins métier.
- Définir les fonctionnalités du système.
- Concevoir l'architecture globale.
- Choisir les technologies.
- Préparer le planning du projet.

## Tâches

### Analyse

- Étude des besoins.
- Identification des utilisateurs.
- Analyse des systèmes existants.
- Définition des cas d'utilisation.

### Conception

- Architecture globale.
- Architecture Backend.
- Architecture Frontend.
- Architecture IA.
- Architecture RAG.

### Modélisation

- Diagramme UML.
- Diagramme de classes.
- Diagramme de séquence.
- Diagramme de déploiement.

### Choix techniques

- Python
- FastAPI
- React
- PostgreSQL
- InfluxDB
- ChromaDB
- LangChain
- Ollama / OpenAI

## Livrables

- Cahier des charges
- Architecture technique
- Diagrammes UML
- Planning

---

# Phase 2 — Backend & Agent de Collecte

**Période :** 29/07/2026 → 11/08/2026

## Objectifs

Construire l'infrastructure permettant de récupérer les données des équipements.

## Développement de l'Agent

Collecte de :

- CPU
- RAM
- Température
- SMART
- Bad Sectors
- Event Viewer
- Services Windows
- Processus
- Informations système

### Protocoles

- WMI
- PowerShell
- SNMP
- Windows Event Logs

## Backend

Développement de :

- API REST FastAPI
- Authentification JWT
- CRUD des équipements
- Gestion des utilisateurs
- Gestion des alertes

## Base de données

Création des tables :

- Users
- Devices
- Metrics
- Logs
- Alerts
- Recommendations

## Livrables

- Backend opérationnel
- Agent de collecte
- Base PostgreSQL
- API REST documentée

---

# Phase 3 — IA Prédictive & Système RAG

**Période :** 12/08/2026 → 25/08/2026

## Objectifs

Développer le moteur intelligent.

## Machine Learning

Détection :

- anomalies CPU
- anomalies RAM
- anomalies Disque
- anomalies réseau

Modèles possibles :

- Isolation Forest
- XGBoost
- LSTM

## Maintenance Prédictive

Prédire :

- panne disque
- panne mémoire
- surcharge serveur
- crash système

## Base de connaissances

Indexation de :

- PDF
- DOCX
- FAQ
- Documentation interne
- Guides Microsoft
- Documentation Constructeurs

## Base vectorielle

- ChromaDB

ou

- FAISS

## Embeddings

- BGE
- Sentence Transformers

## Pipeline RAG

Étapes :

1. Chargement des documents
2. Découpage des documents
3. Création des embeddings
4. Indexation
5. Recherche sémantique
6. Génération de réponse

## Assistant IA

Fonctionnalités :

- Répondre aux questions
- Expliquer une erreur Windows
- Conseiller une solution
- Générer un rapport
- Résumer un log

## Livrables

- Pipeline RAG
- Base vectorielle
- Modèle IA
- Assistant conversationnel

---

# Phase 4 — Dashboard & Assistant IA

**Période :** 26/08/2026 → 08/09/2026

## Objectifs

Créer l'interface utilisateur.

## Dashboard

Pages :

- Login
- Dashboard
- Parc informatique
- Équipements
- Alertes
- Historique
- Paramètres

## Visualisations

- CPU
- RAM
- Température
- SMART
- Disponibilité
- Historique

## Chat IA

Fonctionnalités

- Poser une question
- Obtenir une explication
- Générer un rapport
- Recherche documentaire

## Notifications

- Email
- Alertes Dashboard

## Livrables

- Interface React
- Dashboard
- Assistant IA intégré

---

# Phase 5 — Tests & Documentation

**Période :** 09/09/2026 → 22/09/2026

## Tests

### Tests Backend

- API
- Authentification
- Sécurité

### Tests Frontend

- Navigation
- Responsive

### Tests IA

- Qualité des réponses
- Recherche RAG
- Temps de réponse

### Tests Fonctionnels

- Collecte
- Alertes
- Dashboard
- Chat IA

## Optimisation

- Performance Backend
- Performance Frontend
- Optimisation des requêtes SQL
- Optimisation des recherches vectorielles

## Documentation

- Guide d'installation
- Manuel utilisateur
- Documentation API
- Documentation technique
- Guide développeur

## Préparation de la soutenance

- Démonstration
- Slides
- Rapport final

## Livrables

- Version finale
- Documentation complète
- Rapport
- Présentation

---

# Architecture Finale

```
                +----------------------+
                |    React Dashboard   |
                +----------+-----------+
                           |
                    FastAPI REST API
                           |
      +--------------------+--------------------+
      |                    |                    |
      |                    |                    |
 Agent Collecte      IA Prédictive         RAG Engine
(WMI/SNMP/SMART)    (ML Models)     (LangChain + ChromaDB)
      |                    |                    |
      +----------+---------+--------------------+
                 |
          PostgreSQL / InfluxDB
                 |
        Logs • Metrics • Alerts
```

---

# Technologies

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic

## Frontend

- React
- TypeScript
- TailwindCSS
- Chart.js

## IA

- LangChain
- Ollama
- OpenAI
- HuggingFace

## Machine Learning

- Scikit-Learn
- XGBoost
- TensorFlow
- LSTM

## Base de données

- PostgreSQL
- InfluxDB

## Base Vectorielle

- ChromaDB

## Outils

- Docker
- Git
- GitHub
- Postman
- VS Code

---

# Livrable Final

À la fin du projet, la plateforme devra être capable de :

- Superviser automatiquement un parc informatique.
- Collecter les métriques des équipements.
- Détecter les anomalies.
- Prédire les défaillances.
- Interroger une base documentaire via le RAG.
- Répondre aux questions des techniciens avec un assistant IA.
- Générer des recommandations de maintenance.
- Centraliser toutes les informations dans un Dashboard moderne.
