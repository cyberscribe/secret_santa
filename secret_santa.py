# Secret Santa Cycle Generator
#
# This tool creates a Secret Santa cycle that:
# - Ensures no self-gifting.
# - Avoids reciprocal gifting.
# - Respects partnership constraints (e.g., couples cannot give to each other).
#
# Inspired by Pista Godo's two-set approach to resolving partnership constraints
# (https://www.linkedin.com/in/pistagodo/)

import argparse
import random

def partition_into_sets(participants, partners=None):
    """
    Partition participants into two balanced sets such that no partners are in the same set.
    Strategy inspired by Pista Godo.
    """
    set_a, set_b = [], []
    assigned = set()

    for p in participants:
        if p in assigned:
            continue

        if partners and p in partners:
            partner = partners[p]
            if random.random() < 0.5:
                set_a.append(p)
                set_b.append(partner)
            else:
                set_b.append(p)
                set_a.append(partner)
            assigned.add(p)
            assigned.add(partner)
        else:
            if len(set_a) <= len(set_b):
                set_a.append(p)
            else:
                set_b.append(p)
            assigned.add(p)

    return set_a, set_b

def create_secret_santa_cycle(participants, partners=None):
    """
    Create a Secret Santa cycle:
    - Partition participants into two sets.
    - Shuffle each set and ensure linkage respects constraints.
    - Combine the sets into one full directed cycle.
    """
    # Step 1: Partition participants
    set_a, set_b = partition_into_sets(participants, partners)

    # Step 2: Shuffle each set
    random.shuffle(set_a)
    random.shuffle(set_b)

    # Step 3: Resolve conflicts between sets
    if partners:
        a_last, b_first = set_a[-1], set_b[0]
        b_last, a_first = set_b[-1], set_a[0]

        # Swap participants if conflicts exist
        if a_last in partners and partners[a_last] == b_first:
            for i in range(1, len(set_b)):
                if set_b[i] != partners.get(a_last):
                    set_b[0], set_b[i] = set_b[i], set_b[0]
                    break

        if b_last in partners and partners[b_last] == a_first:
            for i in range(1, len(set_a)):
                if set_a[i] != partners.get(b_last):
                    set_a[0], set_a[i] = set_a[i], set_a[0]
                    break

    # Step 4: Create directional links within each set
    cycle_a = [(set_a[i], set_a[i + 1]) for i in range(len(set_a) - 1)]
    cycle_b = [(set_b[i], set_b[i + 1]) for i in range(len(set_b) - 1)]

    # Step 5: Link the two sets into one cycle
    cross_links = [(set_a[-1], set_b[0]), (set_b[-1], set_a[0])]

    return cycle_a + cross_links + cycle_b

def validate_and_deduplicate_inputs(participants, partners=None):
    """
    Validate and deduplicate inputs:
    - Warn and remove duplicate participants and partnerships.
    - Check participant and partnership constraints.
    """
    # Deduplicate participants
    original_participants_count = len(participants)
    participants = list(set(participants))
    if len(participants) < original_participants_count:
        print(f"Warning: Removed {original_participants_count - len(participants)} duplicate participant(s).")

    # Deduplicate partnerships
    if partners:
        original_partners_count = len(partners)
        deduplicated_partners = {}
        for p1, p2 in partners.items():
            if (p2, p1) not in deduplicated_partners.items():
                deduplicated_partners[p1] = p2
        if len(deduplicated_partners) < original_partners_count:
            print(f"Warning: Removed {original_partners_count - len(deduplicated_partners)} duplicate partnership(s).")
        partners = deduplicated_partners

    # Validate participant count
    if len(participants) <= 2:
        raise ValueError("There must be more than 2 participants for Secret Santa.")

    # Validate partnerships
    if partners:
        max_partners = len(participants) // 2
        unique_partners = set(partners.keys()) | set(partners.values())
        if len(unique_partners) > max_partners * 2:
            raise ValueError(f"Too many partnerships. Maximum allowed is {max_partners}.")
        for partner in unique_partners:
            if partner not in participants:
                raise ValueError(f"Partner '{partner}' not found in the participant list.")

    return participants, partners

def read_participants(filename):
    """Read participants from a file, one per line."""
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def read_partners(filename):
    """Read partner pairs from a file, each pair separated by a comma."""
    partners = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            p1, p2 = [x.strip() for x in line.split(',')]
            partners[p1] = p2
            partners[p2] = p1
    return partners

def main():
    """Main entry point for the command-line tool."""
    parser = argparse.ArgumentParser(description="Secret Santa Cycle Generator with Input Validation and Deduplication")
    parser.add_argument("--participants", required=True, help="File containing participants (one per line).")
    parser.add_argument("--partners", required=False, help="File containing partner pairs (comma-separated).")
    args = parser.parse_args()

    participants = read_participants(args.participants)
    partners = read_partners(args.partners) if args.partners else None

    try:
        # Validate and deduplicate inputs
        participants, partners = validate_and_deduplicate_inputs(participants, partners)

        # Generate the Secret Santa cycle
        cycle = create_secret_santa_cycle(participants, partners)
        print("Secret Santa Cycle:")
        for giver, receiver in cycle:
            print(f"{giver} -> {receiver}")

    except ValueError as e:
        print(f"Input Validation Error: {e}")

if __name__ == "__main__":
    main()
