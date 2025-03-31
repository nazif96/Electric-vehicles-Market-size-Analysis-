# 🚗 Electric-vehicles-Market-Size-Analysis 2025

## Contexte 
L'analyse de la taille du marché est un aspect crucial des études de marché. Elle permet de déterminer le volume de ventes potentiel d'un marché donné. Elle aide les entreprises à comprendre l'ampleur de la demande, à évaluer les niveaux de saturation du marché et à identifier les opportunités de croissance.

## 🎯 Objectif 

Ce projet vise à analyser la taille du marché des véhicules électriques aux Etats Unis.

L'objectif principal de cette analyse est d'exploiter les données historiques d'immatriculation des véhicules électriques afin de comprendre leur pénétration actuelle sur le marché, de prédire leur croissance future et d'identifier les principales tendances et facteurs d'expansion. 

[L'analyse complete de la taille du marché des VE](https://github.com/nazif96/Electric-vehicles-Market-Size-Analysis/blob/main/Vehicles_electric_market_Analysis.html)

## 🏗️ Structure du projet 

```
Electric-vehicles-Market-Size-Analysis/
│
├── app.py                                   #  L’application principale Streamlit
├── Electric_Vehicle_Data_2025.csv.gz        # Données compressées
├── requirements.txt                         # Dépendances
├── README.md                                # Documentation
├── LICENSE                                  # Licence du projet
├── .gitignore                               # Fichiers ignorés par Git
├── Notebooks/                               # Dossier pour analyses du marché des VE .Jupyter
└── Vehicles_electric_market_Analysis.html   # Analyse complète en html  
``` 

 
## Application 

Une application interactive développée avec **Streamlit** pour explorer, analyser et visualiser les données sur les véhicules électriques immatriculés dans l'État de Washington (USA). Ce projet a pour objectif d'assister les décideurs, analystes et passionnés d'énergie verte dans l’exploration du marché actuel des véhicules électriques (VE).

[Application url](https://nazif96-electric-vehicles-market-size-analysis--app-qlrsye.streamlit.app/)
---

## 📊 Fonctionnalités principales

### 🏠 Accueil
- Présentation générale du projet
- Aperçu des données sources

### 📈 Analyses
- Filtrage par année modèle
- Indicateurs clés (nombre de véhicules, modèles, marques)
- Top 10 des marques les plus représentées
- Répartition des types de VE (BEV, PHEV, etc.)

### 🚘 Profils Véhicules VE
- Filtres dynamiques (marque, modèle, année, type)
- **Boxplot** : Autonomie par marque
- **Barplot** : Prix moyen par modèle
- **Histogramme** : Répartition des autonomies
- **📄 Génération de rapport PDF personnalisé** avec les graphiques et données sélectionnées

---

## 📁 Données utilisées

- Source : [Electric Vehicle Population Data (WA)](https://catalog.data.gov/dataset/electric-vehicle-population-data)
- Format : CSV compressé
- Colonnes clés : `Make`, `Model`, `Model Year`, `Electric Range`, `Base MSRP`, `Vehicle Type`, `Location`, etc.

---

## ⚙️ Installation

### Prérequis
- Python 3.8+
- pip

### Installation des dépendances

```bash
pip install -r requirements.txt

``` 

# 🚀 Lancement de l’application

```bash
streamlit run app.py

``` 

## 👨‍💻 Auteur

**AFOLABI Nazifou**

- **Datascientist | Machine Learning & Modeling** 
- Passionné par les sciences de données et l'intelligence artificielle.
- **Email** : [afolabinazif96@gmail.com](mailto.afolabinazif96@gmail.com)
- **LinkedIn** : [Nazifou AFOLABI](https://www.linkedin.com/in/nazifou-afolabi-10544729b/)

Projet pédagogique et analytique sur les données ouvertes liées aux véhicules électriques.
