from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Code du jeu Uno (à adapter selon vos besoins)

COULEURS = ['Rouge', 'Jaune', 'Vert', 'Bleu']
VALEURS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Passe', 'Inverser', 'Plus 2']

class CarteUno:
    def __init__(self, couleur, valeur):
        self.couleur = couleur
        self.valeur = valeur

    def __str__(self):
        return f"{self.couleur} {self.valeur}"

class JeuUno:
    def __init__(self):
        self.cartes = [CarteUno(couleur, valeur) for couleur in COULEURS for valeur in VALEURS]
        self.pioche = self.cartes.copy()
        random.shuffle(self.pioche)
        self.joueur1_main = []
        self.joueur2_main = []
        self.carte_actuelle = self.piocher_carte()

    def piocher_carte(self):
        return self.pioche.pop()

    def distribuer_cartes(self):
        self.joueur1_main = [self.piocher_carte() for _ in range(7)]
        self.joueur2_main = [self.piocher_carte() for _ in range(7)]

    def jouer(self, joueur_main, carte):
        if carte.couleur == self.carte_actuelle.couleur or carte.valeur == self.carte_actuelle.valeur:
            self.carte_actuelle = carte
            joueur_main.remove(carte)
            return True
        else:
            return False

jeu_uno = JeuUno()

@app.route('/')
def index():
    return render_template('index.html', main_hand=jeu_uno.joueur1_main)

@app.route('/jouer_carte', methods=['POST'])
def jouer_carte():
    carte_index = int(request.form['carte_index'])
    carte_jouee = jeu_uno.joueur1_main[carte_index]
    if jeu_uno.jouer(jeu_uno.joueur1_main, carte_jouee):
        return redirect(url_for('index'))
    else:
        return "Carte invalide. Choisissez une autre carte."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
