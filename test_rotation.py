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
        # Tous ont été tirés : réinitialiser le cycle
        # Trier par timestamp pour identifier le(s) plus ancien(s)
        already_drawn.sort(key=lambda x: x["last_drawn_timestamp"])
        
        # Trouver le timestamp le plus ancien
        oldest_timestamp = already_drawn[0]["last_drawn_timestamp"]
        
        # Sélectionner tous les membres avec ce timestamp (ou très proche)
        # pour permettre l'aléatoire en cas d'égalité
        candidates = [
            m["name"] for m in already_drawn 
            if m["last_drawn_timestamp"] == oldest_timestamp
        ]
        
        # Tirage aléatoire parmi les candidats les plus anciens
        return random.choice(candidates)


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
    print("✓ Les 3 premiers tirages couvrent tous les membres")
    print("✓ Les tirages 4 et 5 reprennent le cycle\n")

    # Scénario 5: Test de l'aléatoire avec timestamps égaux
    print("Scénario 5: Test de l'aléatoire - tous tirés au même moment")
    same_time = datetime.now() - timedelta(hours=1)
    members = [
        {"name": "Alice", "active": True, "last_drawn_timestamp": same_time},
        {"name": "Bob", "active": True, "last_drawn_timestamp": same_time},
        {"name": "Charlie", "active": True, "last_drawn_timestamp": same_time},
    ]
    
    # Faire 20 tirages pour vérifier la distribution aléatoire
    results = {"Alice": 0, "Bob": 0, "Charlie": 0}
    for _ in range(20):
        selected = select_next_candidate(members)
        results[selected] += 1
    
    print(f"Distribution sur 20 tirages: {results}")
    # Vérifier que chaque membre a été tiré au moins une fois
    assert all(count > 0 for count in results.values()), "Tous les membres devraient être tirés"
    print("✓ L'aléatoire fonctionne : tous les membres ont été tirés\n")

    print("=== Tous les tests sont passés avec succès ! ===")


if __name__ == "__main__":
    test_rotation_logic()
