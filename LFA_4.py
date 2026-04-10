"""
Laboratorul 4 LFA 9/04/26

Creating a small text-based game using DFA
"""

import re


def mega_parse_dfa(filename):
    sections = {}
    current_section = None

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line in ["<sigma>", "<Q>", "<F>", "<delta>", "<s>"]:
                current_section = line[1:-1]
                sections[current_section] = []
                continue

            if line.startswith("<end_"):
                current_section = None
                continue

            if current_section and line:
                sections[current_section].append(line)

    dfa = {
        "sigma": [],
        "Q": [],
        "F": [],
        "delta": [],
        "s": ""
    }

    if "sigma" in sections:
        for line in sections["sigma"]:
            if line.startswith("[") and line.endswith("]"):
                content = line[1:-1]
                dfa["sigma"] = [x.strip() for x in content.split(",")]
            else:
                dfa["sigma"] = [x.strip() for x in line.split(",")]
    else:
        raise ValueError("Missing <sigma> section")

    if "Q" in sections:
        for line in sections["Q"]:
            if line.startswith("[") and line.endswith("]"):
                content = line[1:-1]
                dfa["Q"] = [x.strip() for x in content.split(",")]
            else:
                dfa["Q"] = [x.strip() for x in line.split(",")]
    else:
        raise ValueError("Missing <Q> section")

    if "F" in sections:
        for line in sections["F"]:
            if line.startswith("[") and line.endswith("]"):
                content = line[1:-1]
                content = content.replace(";", "")
                dfa["F"] = [x.strip() for x in content.split(",")]
            else:
                dfa["F"] = [x.strip() for x in line.split(",")]
    else:
        raise ValueError("Missing <F> section")

    if "s" in sections:
        dfa["s"] = sections["s"][0].replace(";", "").strip()
    else:
        raise ValueError("Missing <s> section")

    if "delta" in sections:
        for line in sections["delta"]:
            if line.startswith('[') and line.endswith(']'):
                line = line[1:-1]

            parts = [x.strip() for x in line.split(',')]

            if len(parts) == 3:
                dfa["delta"].append(parts)
            else:
                raise ValueError(f"Invalid transition format: {line}")
    else:
        raise ValueError("Missing <delta> section")

    return dfa


def build_transition_table(dfa):
    trans = {}
    for src, sym, dst in dfa["delta"]:
        trans[(src, sym)] = dst
    return trans


def play_game(dfa):
    trans = build_transition_table(dfa)
    current_state = dfa["s"]

    print("DFA loaded successfully.")
    print("Available commands:", dfa["sigma"])
    print("Type 'exit' to quit.")

    while True:
        room = current_state.split("_")[0]
        status = "hasPotion" if "hasPotion" in current_state else "noPotion"
        print(f"\nCurrent location: {room} ({status})")

        if current_state in dfa["F"]:
            if "Heaven" in current_state:
                print("You reached Heaven. Game won.")
            else:
                print("You reached Hell. Game over.")
            break

        available = [sym for (state, sym) in trans if state == current_state]
        print("Available moves:", available)

        cmd = input("Enter command: ").strip().upper()

        if cmd == "EXIT":
            print("Exiting game.")
            break

        if cmd not in dfa["sigma"]:
            print("Invalid command.")
            continue

        if (current_state, cmd) not in trans:
            print("No transition defined for this move.")
            continue

        current_state = trans[(current_state, cmd)]


def main():
    dfa_file = "text_game.txt"

    try:
        dfa = mega_parse_dfa(dfa_file)

        print("Alphabet:", dfa["sigma"])
        print("States:", dfa["Q"])
        print("Start state:", dfa["s"])
        print("Final states:", dfa["F"])
        print("\nTransitions:")
        for t in dfa["delta"]:
            print(f"{t[0]} --{t[1]}--> {t[2]}")

        print("\nStarting game...\n")
        play_game(dfa)

    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()