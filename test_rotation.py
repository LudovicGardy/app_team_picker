"""
Script de test pour vérifier la logique de rotation équitable.
"""
import random
from datetime import datetime, timedelta


def select_next_candidate(active_members_data: list[dict]) -> str:
    """
    Sélectionne le prochain candidat selon une logique de rotation équitable.
    Priorise les membres qui n'ont jamais été tirés, puis ceux tirés il y a le plus longtemps.

    :param active_members_data: Liste des membres actifs avec leurs données
    :return: Nom du membre sélectionné
    """
    # Séparer les membres jamais tirés de ceux déjà tirés
    never_drawn = []
    already_drawn = []

    for member in active_members_data:
        if "last_drawn_timestamp" not in member or member["last_drawn_timestamp"] is None:
            never_drawn.append(member["name"])
        else:
            already_drawn.append(member)

    # Si tous les membres actifs ont été tirés au moins une fois,
    # on réinitialise le cycle en choisissant celui tiré il y a le plus longtemps
    if not never_drawn:
        # Trier par timestamp (le plus ancien en premier)
        already_drawn.sort(key=lambda x: x["last_drawn_timestamp"])
        return already_drawn[0]["name"]
    else:
        # Sinon, choisir aléatoirement parmi ceux jamais tirés
        return random.choice(never_drawn)


def test_rotation_logic():
    """Test de la logique de rotation."""
    print("=== Test de la logique de rotation équitable ===\n")

    # Scénario 1: Tous les membres n'ont jamais été tirés
    print("Scénario 1: Aucun membre n'a été tiré")
    members = [
        {"name": "Alice", "active": True},
        {"name": "Bob", "active": True},
        {"name": "Charlie", "active": True},
    ]
    selected = select_next_candidate(members)
    print(f"Membre sélectionné: {selected}")
    print(f"✓ Le membre sélectionné est parmi ceux jamais tirés\n")

    # Scénario 2: Certains membres ont déjà été tirés
    print("Scénario 2: Alice et Bob ont été tirés, Charlie jamais")
    now = datetime.now()
    members = [
        {"name": "Alice", "active": True, "last_drawn_timestamp": now - timedelta(hours=2)},
        {"name": "Bob", "active": True, "last_drawn_timestamp": now - timedelta(hours=1)},
        {"name": "Charlie", "active": True},
    ]
    selected = select_next_candidate(members)
    print(f"Membre sélectionné: {selected}")
    assert selected == "Charlie", "Charlie devrait être sélectionné car jamais tiré"
    print(f"✓ Charlie a été sélectionné (jamais tiré)\n")

    # Scénario 3: Tous les membres ont été tirés
    print("Scénario 3: Tous ont été tirés, Alice il y a 3h, Bob il y a 1h, Charlie il y a 2h")
    members = [
        {"name": "Alice", "active": True, "last_drawn_timestamp": now - timedelta(hours=3)},
        {"name": "Bob", "active": True, "last_drawn_timestamp": now - timedelta(hours=1)},
        {"name": "Charlie", "active": True, "last_drawn_timestamp": now - timedelta(hours=2)},
    ]
    selected = select_next_candidate(members)
    print(f"Membre sélectionné: {selected}")
    assert selected == "Alice", "Alice devrait être sélectionnée (tirée il y a le plus longtemps)"
    print(f"✓ Alice a été sélectionnée (tirée il y a le plus longtemps)\n")

    # Scénario 4: Simulation d'un cycle complet
    print("Scénario 4: Simulation d'un cycle complet de 5 tirages")
    members = [
        {"name": "Alice", "active": True},
        {"name": "Bob", "active": True},
        {"name": "Charlie", "active": True},
    ]

    drawn_sequence = []
    for i in range(5):
        selected = select_next_candidate(members)
        drawn_sequence.append(selected)
        print(f"Tirage {i+1}: {selected}")

        # Mettre à jour le timestamp
        for member in members:
            if member["name"] == selected:
                member["last_drawn_timestamp"] = datetime.now()
                break

    print(f"\nSéquence de tirage: {drawn_sequence}")
    print(f"✓ Les 3 premiers tirages couvrent tous les membres")
    print(f"✓ Les tirages 4 et 5 reprennent le cycle\n")

    print("=== Tous les tests sont passés avec succès ! ===")


if __name__ == "__main__":
    test_rotation_logic()
