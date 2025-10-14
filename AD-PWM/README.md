# Projet : Mélodie avec Buzzer et Potentiomètre

Ce projet consiste à générer une mélodie en utilisant un buzzer et à contrôler le volume à l'aide d'un potentiomètre. 

# Bonus

Un bouton poussoir permet de changer la mélodie entre deux morceaux célèbres : "Joyeux anniversaire" et "Marche turque".

## Matériel utilisé

- **Raspberry Pi Pico W**
- **Buzzer passif** (connecté à la broche GP28)
- **Potentiomètre** (connecté à la broche GP27)
- **Bouton poussoir** (connecté à la broche GP16)
- **LED** (connectée à la broche GP18)

## Fonctionnalités

- **Changement de mélodie** : Appuyez sur le bouton poussoir pour alterner entre deux mélodies : "Joyeux anniversaire" et "Marche turque".
- **Volume dynamique** : Le volume du buzzer est contrôlé par le potentiomètre. Le son est coupé si la valeur est trop faible (résistance interne) ou trop élevée (saturation).
- **LED d'indication** : La LED clignote en rythme avec la musique (toutes les 0,5 seconde).
- **Utilisation de boucle rapide** : Le code s'exécute dans une boucle infinie mais à l'intérieur se cache des boucles qui tournent très vite (10 ms et 500 ms) pour éviter de bloquer le thread.
- **Anti-rebond** : Utilisation d'une résistance de pull-up pour éviter le rebond du bouton.