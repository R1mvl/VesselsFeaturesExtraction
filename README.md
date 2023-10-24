# VesselsFeaturesExtraction

Ce projet est un ensemble de scripts Python permettant d'extraire des caractéristiques des vaisseaux sanguins à partir d'images médicales.

## Installation

```python
pip install -r requirements.txt
```

## Description des fichiers

python

dataset.py: Ce fichier charge le dataset d'images médicales.<br />
skeletization.py: Ce fichier effectue la skeletisation des vaisseaux sanguins a partir de la matrice des données.<br />
topology.py: Ce fichier calcule la topologie des vaisseaux sanguins. extremitées, intersection, ...<br />
featureExtract.py: Ce fichier extrait les caractéristiques des edges du graph.<br />
branchAssignement.py: Ce fichier extrait les features des points en les assignant a leurs edges<br />
refinement.py: Ce fichier améliore les caractéristiques des vaisseaux sanguins en enlevant les asperitées<br />
utils.py: Ce fichier contient des fonctions utiles à tous les fichiers