# securegate
Mini-chaîne DevSecOps locale avec contrôle bloquant
# SecureGate

Mini-chaîne DevSecOps locale avec contrôle bloquant 

**Équipe :** BENJELLOUN Abdelkrim, CHOUIEKH Ahmed Mouataz  
**Encadrant :** Abdellah OUAGUID

## Objectif
Dans une petite équipe qui livre souvent de nouvelles versions, des défauts élémentaires (une fonction
cassée, un mot de passe écrit dans le code, une requête SQL non protégée) passent en production alors
qu'un simple contrôle avant la livraison les aurait arrêtés.

SecureGate est une mini-chaîne DevSecOps locale : avant chaque livraison, elle exécute automatiquement
des tests fonctionnels et des contrôles de sécurité ciblés. Si l'un d'eux échoue, la chaîne s'arrête,
explique clairement la cause (fichier, ligne, règle, correctif) et renvoie un code d'erreur : la
livraison est bloquée jusqu'à correction.


## Démarrage rapide
    git clone https://github.com/krimobenji/securegate.git
    cd securegate
    make setup
    make test

## Prérequis
- Linux, macOS ou Windows avec WSL
- Git, Python 3.11 ou plus, Make

## Commandes disponibles
(Lancez `make` et recopiez la liste.)

## État d'avancement
- [x] Sprint 1 : socle (application /health, tests, Makefile)
- [x] Sprint 2 : application complète
- [ ] Sprint 3 : contrôles de sécurité
- [ ] Sprint 4 : orchestrateur et blocage
- [ ] Sprint 5 : lancement en deux étapes et recette
- [ ] Sprint 6 : extensions et soutenance

## API de l'application cible
| Route | Rôle | Codes |
|---|---|---|
| GET /health | État et version | 200 |
| POST /register | Créer un compte (mot de passe haché PBKDF2) | 201, 400, 409 |
| POST /login | Se connecter | 200, 401 |
| GET /users?name=... | Rechercher des utilisateurs | 200, 400 |

Couverture de code : `make coverage` (seuil bloquant à 80 %).
