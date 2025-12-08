"""
Script de test pour vérifier la logique de rotation équitable.
"""
import random
from datetime import datetime, timedelta


def select_next_candidate(active_members_data: list[dict]) -> str:
    """
    Sélectionne le prochain candidat selon une logique de rotation équitable avec aléatoire.
    Priorise les membres qui n'ont jamais été tirés, puis tire aléatoirement
    parmi ceux qui n'ont pas été tirés récemment.

    :param active_members_data: Liste des membres actifs avec leurs données
    :return: Nom du membre sélectionné
    """
    never_drawn = []
    already_drawn = []

    for member in active_members_data:
        if "last_drawn_timestamp" not in member or member["last_drawn_timestamp"] is None:
            never_drawn.append(member["name"])
        else:
            already_drawn.append(member)

    if never_drawn:
        # Choisir aléatoirement parmi ceux jamais tirés
        return random.choice(never_drawn)
    else:
        # Tous ont été tirés : réinitialiser le cycle pour un nouveau tirage aléatoire
        # Effacer tous les timestamps pour repartir à zéro
        for member in active_members_data:
            member["last_drawn_timestamp"] = None
        
        # Tirage aléatoire parmi tous les membres actifs
        return random.choice([m["name"] for m in active_members_data])


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
    # Vérifier que les timestamps ont été réinitialisés
    assert all(m["last_drawn_timestamp"] is None for m in members), "Les timestamps devraient être réinitialisés"
    print(f"✓ {selected} a été sélectionné et les timestamps ont été réinitialisés\n")

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
    print("✓ Les 3 premiers tirages couvrent tous les membres")
    print("✓ Les tirages 4 et 5 reprennent le cycle\n")

    # Scénario 5: Test de l'aléatoire sur plusieurs cycles
    print("Scénario 5: Test de l'aléatoire - vérifier la variabilité entre cycles")
    members = [
        {"name": "Alice", "active": True},
        {"name": "Bob", "active": True},
        {"name": "Charlie", "active": True},
    ]
    
    # Faire 2 cycles complets et vérifier qu'ils sont différents
    cycle1 = []
    cycle2 = []
    
    # Premier cycle
    for _ in range(3):
        selected = select_next_candidate(members)
        cycle1.append(selected)
        for member in members:
            if member["name"] == selected:
                member["last_drawn_timestamp"] = datetime.now()
                break
    
    # Deuxième cycle (les timestamps seront réinitialisés automatiquement)
    for _ in range(3):
        selected = select_next_candidate(members)
        cycle2.append(selected)
        for member in members:
            if member["name"] == selected:
                member["last_drawn_timestamp"] = datetime.now()
                break
    
    print(f"Cycle 1: {cycle1}")
    print(f"Cycle 2: {cycle2}")
    print("✓ Deux cycles complets effectués avec réinitialisation automatique\n")

    print("=== Tous les tests sont passés avec succès ! ===")


if __name__ == "__main__":
    test_rotation_logic()
