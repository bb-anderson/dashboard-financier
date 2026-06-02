# Dashboard Financier Interactif

Application web d'analyse financière en temps réel permettant d'analyser la performance, le risque et les indicateurs techniques de n'importe quelle action cotée en bourse. Conçu pour reproduire les outils d'analyse utilisés en gestion d'actifs et risk management.

## Demo en ligne

https://dashboard-financier-zpmgawujpmtmgeha2zbb78.streamlit.app

## Contexte et motivation

Les indicateurs financiers classiques (Sharpe, Sortino, Drawdown, Beta) sont au cœur du métier de gestionnaire de portefeuille et d'analyste quantitatif. Ce projet les implémente from scratch en Python et les expose dans une interface interactive accessible à tout utilisateur, sans nécessiter de compétences techniques.

## Fonctionnalités

**Sélection et navigation**
- Menus déroulants organisés par secteur : Tech, Finance, Santé, Energie, Industrie, Europe, Asie, ETF
- Comparaison de deux actions sur la même période, normalisées en base 100 pour une comparaison équitable
- Choix de la période d'analyse : 1 mois, 3 mois, 6 mois, 1 an, 2 ans, 5 ans

**Visualisation**
- Graphique du cours de clôture avec Moyenne Mobile 50 jours (MA50)
- Graphique du Drawdown historique synchronisé avec le cours
- Résumé d'analyse automatique en langage naturel

**Indicateurs financiers calculés**
- Rendement total sur la période sélectionnée
- Volatilité annualisée (écart-type des rendements journaliers * sqrt(252))
- Ratio de Sharpe : rendement excédentaire par unité de risque total
- Ratio de Sortino : rendement excédentaire par unité de risque négatif uniquement
- Maximum Drawdown : perte maximale historique du sommet au creux
- Beta vs S&P 500 (SPY) : sensibilité de l'action par rapport au marché
- Top 5 des pires journées sur la période avec date et performance

## Stack technique

- Python 3.11
- Streamlit — interface web interactive
- yfinance — récupération des données Yahoo Finance en temps réel
- Pandas — manipulation et calcul des séries temporelles
- NumPy — calculs mathématiques (annualisation, covariance, beta)
- Matplotlib — visualisation des graphiques

## Lancer en local

```bash
git clone https://github.com/bb-anderson/dashboard-financier.git
cd dashboard-financier
pip install -r requirements.txt
streamlit run dashboard.py
```

## Structure du projet

dashboard-financier/
├── dashboard.py        # Application principale
├── requirements.txt    # Dépendances Python
└── README.md

## Auteur

Bilel Bencherif — 
Projet réalisé dans le cadre d'un parcours autodidacte/développement de compétences en Machine Learning appliqué à la Finance.
