"""Implementing the DFA - determinist finite automata"""

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
            if current_section:
                sections[current_section].append(line)

    dfa = {
        "sigma": [],
        "Q": [],
        "F": [],
        "delta": [],
        "s": []
    }

    if "sigma" in sections:
        for line in sections["sigma"]:
            match = re.search(r"\[(.*?)\]", line)
            if match:
                dfa["sigma"] = [x.strip() for x in match.group(1).split(",")]
    else:
        raise ValueError("Missing <sigma> section.")


    if "Q" in sections:
        for line in sections["Q"]:
            match = re.search(r"\[(.*?)\]", line)
            if match:
                dfa["Q"] = [x.strip() for x in match.group(1).split(",")]
    else:
        raise ValueError("Missing <Q> section.")


    if "F" in sections:
        dfa["F"] = [line.replace(";", "").strip() for line in sections["F"] if line]
    else:
        raise ValueError("Missing <F> section.")


    if "s" in sections:
        dfa["s"] = sections["s"][0].replace(";", "").strip() if sections["s"] else ""
    else:
        raise ValueError("Missing <s> section.")

    # tranzitii prin delta
    if "delta" in sections:
        for line in sections["delta"]:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                inner = line[1:-1]
            else:
                inner = line
            pairs = re.findall(r"\[(.*?)\]", inner)
            if not pairs:
                parts = [x.strip() for x in inner.split(',')]
                if len(parts) == 2:
                    src, dst = parts
                    for sym in dfa["sigma"]:
                        dfa["delta"].append([src, sym, dst])
                elif len(parts) == 3:
                    dfa["delta"].append(parts)
            else:
                for p in pairs:
                    parts = [x.strip() for x in p.split(',')]
                    if len(parts) == 2:
                        src, dst = parts
                        for sym in dfa["sigma"]:
                            dfa["delta"].append([src, sym, dst])
                    elif len(parts) == 3:
                        dfa["delta"].append(parts)
                    else:
                        raise ValueError(f"Invalid transition format: {p}")
    else:
        raise ValueError("Missing <delta> section.")

    return dfa

def build_transition_table(dfa):
    trans = {}
    for src, sym, dst in dfa["delta"]:
        trans[(src, sym)] = dst
    return trans

def simulate_dfa(dfa, input_string):
    trans = build_transition_table(dfa)
    current_state = dfa["s"]
    sigma = set(dfa["sigma"])

    for ch in input_string:
        if ch not in sigma:
            print(f"Warning: symbol '{ch}' not in alphabet")
            return False
        if (current_state, ch) not in trans:
            return False
        current_state = trans[(current_state, ch)]

    return current_state in dfa["F"]

def main():
    dfa_file = "dfa.txt"
    try:
        dfa = mega_parse_dfa(dfa_file)
        print("DFA loaded cu succes.")
        print("Alphabet:", dfa["sigma"])
        print("States:", dfa["Q"])
        print("Start:", dfa["s"])
        print("Final states:", dfa["F"])
        print("Transitions (expanded):")
        for t in dfa["delta"]:
            print(f"  {t[0]} --{t[1]}--> {t[2]}")
        print()
    except Exception as e:
        print(f"Eroare loading DFA: {e}")
        return

    print("stringuri de 1 si 0 pt test: (empty line = quit):")
    while True:
        s = input("> ").strip()
        if not s:
            break
        accepted = simulate_dfa(dfa, s)
        print(f"'{s}' -> {'Accepted' if accepted else 'Rejected'}")

if __name__ == "__main__":
    main()