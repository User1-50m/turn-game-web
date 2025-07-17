from flask import Flask, render_template, request, redirect, session, url_for
from game_logic import Character, Attack, player, enemies
import random
import copy  # To clone enemy objects

app = Flask(__name__)
app.secret_key = "replace_with_a_strong_secret_key"

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()  # This clears all stored session data (HP, stamina, enemy progress, etc.)
    return redirect(url_for('index'))  # Redirects back to the battle screen


def serialize_character(char):
    return {
        "name": char.name,
        "hp": char.hp,
        "max_hp": char.max_hp,
        "stamina": char.stamina,
        "max_stamina": char.max_stamina,
        "attacks": [{"name": atk.name, "damage": atk.damage, "stamina_cost": atk.stamina_cost} for atk in char.attacks]
    }

def deserialize_character(data):
    attacks = [Attack(a["name"], a["damage"], a["stamina_cost"]) for a in data["attacks"]]
    char = Character(data["name"], data["max_hp"], data["max_stamina"], attacks)
    char.hp = data["hp"]
    char.stamina = data["stamina"]
    return char

@app.route('/')
def index():
    if 'player' not in session or 'enemy' not in session:
        session['player'] = serialize_character(copy.deepcopy(player))
        session['enemy_index'] = 0
        session['enemy'] = serialize_character(copy.deepcopy(enemies[0]))
        session['message'] = "Battle Start! Your turn."

    return render_template('index.html',
                           player=session['player'],
                           enemy=session['enemy'],
                           message=session.get('message', ''))

# Add more routes here as needed...

if __name__ == "__main__":
    app.run(debug=True)

    from flask import request, redirect, url_for

@app.route('/attack', methods=['POST'])
def attack():
    attack_name = request.form.get('attack')
    if not attack_name:
        session['message'] = "No attack selected!"
        return redirect(url_for('index'))

    # Deserialize characters from session
    player_char = deserialize_character(session['player'])
    enemy_char = deserialize_character(session['enemy'])

    # Find the attack object the player chose
    attack = next((atk for atk in player_char.attacks if atk.name == attack_name), None)
    if not attack:
        session['message'] = "Invalid attack!"
        return redirect(url_for('index'))

    # Player performs attack on enemy
    player_char.perform_attack(enemy_char, attack)

    # Check if enemy defeated
    if enemy_char.hp <= 0:
        enemy_index = session.get('enemy_index', 0) + 1
        if enemy_index >= len(enemies):
            session['message'] = "🎉 You defeated all enemies and won the game!"
            # Optionally clear session here or mark game over
            # e.g. session.clear()
        else:
            session['enemy_index'] = enemy_index
            session['enemy'] = serialize_character(copy.deepcopy(enemies[enemy_index]))
            session['message'] = f"You defeated {enemy_char.name}! Next enemy appears!"

        # Save updated player and enemy states to session
        session['player'] = serialize_character(player_char)

        return redirect(url_for('index'))

        # If enemy still alive, enemy attacks back
    enemy_available_attacks = [atk for atk in enemy_char.attacks if enemy_char.stamina >= atk.stamina_cost]
    if enemy_available_attacks:
        enemy_attack = random.choice(enemy_available_attacks)
        enemy_char.perform_attack(player_char, enemy_attack)
        session['message'] = f"{player_char.name} used {attack.name}! {enemy_char.name} retaliated with {enemy_attack.name}!"
    else:
        session['message'] = f"{player_char.name} used {attack.name}! {enemy_char.name} is too tired and skips the turn."
    # Regenerate stamina every turn (whether attacked or skipped)
    enemy_char.regen_stamina(10)
    player_char.regen_stamina(10)

    # Save updated player and enemy states to session
    session['player'] = serialize_character(player_char)
    session['enemy'] = serialize_character(enemy_char)

    return redirect(url_for('index'))


    # If enemy still alive, enemy attacks back
    # ... (enemy attack logic here) ...

    # Save updated player and enemy states to session
    session['player'] = serialize_character(player_char)
    session['enemy'] = serialize_character(enemy_char)

    return redirect(url_for('index'))


    # Find the attack object by name
    attack_obj = next((atk for atk in player_char.attacks if atk.name == attack_name), None)
    if not attack_obj:
        session['message'] = "Invalid attack!"
        return redirect(url_for('index'))

    # Player performs attack on enemy
    player_char.perform_attack(enemy_char, attack_obj)

    # Enemy turn (simple random attack)
    enemy_available = enemy_char.get_available_attacks()
    if enemy_available:
        enemy_attack = random.choice(enemy_available)
        enemy_char.perform_attack(player_char, enemy_attack)

    # Update session
    session['player'] = serialize_character(player_char)
    session['enemy'] = serialize_character(enemy_char)

    # Message update
    if not enemy_char.is_alive(0):
        session['message'] = f"You defeated {enemy_char.name}!"
    elif not player_char.is_alive(0):
        session['message'] = "You have been defeated! Game over."
    else:
        session['message'] = f"You used {attack_name}! Enemy attacked back."

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

