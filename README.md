# fKwyk

fKwyk est un outil dont l'objectif est d'assister l'utilisateur dans la rélisation de DM sur kwyk

## Installation

### Terminal

Il est util d'avoir une console capable d'afficher les charactères unicodes. Pour Windows 10 et au delà, je recomande le [Windows Terminal (WT)](https://www.microsoft.com/store/productid/9N0DX20HK701?ocid=pdpshare)

### Python

Vous avez besoin d'avoir [python 3.10](https://www.python.org/downloads/release/python-3100/) au moins installé sur votre système pour pouvoir utilisé fKwyk.\
Il faut aussi les modules suivant :

- selenium
- sympy
- latex2sympy

Que vous pouvez installer de la manière suivante:

```shell
pip install selenium
pip install sympy
pip install latex2sympy
```

## Utilisation

### Lancement

Ouvrez une console (WT sous windows), naviguez jusqu'au dossier où vous avez déposer les fichiers de fKwyk puis lancer l'application avec:

```shell
py ./main.py
```

Attendez quelques instants et ensuite suivez les instructions (n° du DM, n° de la question intial) du programme jusqu'à l'ouverture d'une fenêtre chrome.\
Vous renseignerez ensuite vous identifiant et mot de passe Mon Bureau Numérique de manière à vous identifier sur le sîte en question.\
Le prgramme continuera ensuite et vous mènera vers le sîte kwyk quand tout cela cesse de changer, vous serez libre de selectionner le DM que vous souhaiter faire (le même que vous avez renseigné au lancement de fKwyk).\
Vous naviguerez ensuite jusqu'à la question par laquelle vous souhaité commencer.

Vous êtes prêt à utiliser fKwyk

### commen répondre à des questions ?

Une fois le programme lancé, vous trouverez ce type d'interface:

```(bash)
>>
```

vous pouvez ici entrer des commandes, elles se présentent sous deux formes:

- du code python, beaucoup de fonction python peuvent être utilisé, notamment celles provenant de sympy
- des commandes spécifiques, elles commencent avec le préfixe "$" : par exemple `$w` ou bien `$s`.
