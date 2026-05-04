import re

EPSILON = "epsilon"   # or "ε", "lambda" – change here if needed

def mega_parse_nfa(filename):
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

    nfa = {
        "sigma": [],
        "Q": [],
        "F": [],
        "delta": [],
        "s": []
    }

    # --- sigma ---
    if "sigma" in sections:
        for line in sections["sigma"]:
            match = re.search(r"\[(.*?)\]", line)
            if match:
                nfa["sigma"] = [x.strip() for x in match.group(1).split(",")]
        # epsilon can be present in sigma, but we will treat it specially
    else:
        raise ValueError("Missing <sigma> section.")

    # --- Q ---
    if "Q" in sections:
        for line in sections["Q"]:
            match = re.search(r"\[(.*?)\]", line)
            if match:
                nfa["Q"] = [x.strip() for x in match.group(1).split(",")]
    else:
        raise ValueError("Missing <Q> section.")

    # --- F ---
    if "F" in sections:
        nfa["F"] = [line.replace(";", "").strip() for line in sections["F"] if line]
    else:
        raise ValueError("Missing <F> section.")

    # --- s ---
    if "s" in sections:
        nfa["s"] = sections["s"][0].replace(";", "").strip() if sections["s"] else ""
    else:
        raise ValueError("Missing <s> section.")

    if "delta" in sections:
        for line in sections["delta"]:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                inner = line[1:-1]
            else:
                inner = line

            triples = re.findall(r"\[(.*?)\]", inner)
            if not triples:
                triples = [inner]

            for triple in triples:
                parts = [x.strip() for x in triple.split(',')]
                if len(parts) == 3:
                    src, sym, dst = parts
                    nfa["delta"].append([src, sym, dst])
                else:
                    raise ValueError(f"Invalid transition format: {triple} (must be [src, sym, dst])")
    else:
        raise ValueError("Missing <delta> section.")

    sigma_set = set(nfa["sigma"])
    for src, sym, dst in nfa["delta"]:
        if sym != EPSILON and sym not in sigma_set:
            raise ValueError(f"Transition symbol '{sym}' not in alphabet and is not '{EPSILON}'")

    return nfa

def epsilon_closure(states, trans):
    stack = list(states)
    closure = set(states)

    while stack:
        state = stack.pop()
        if (state, EPSILON) in trans:
            for nxt in trans[(state, EPSILON)]:
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
    return closure

def build_transition_table_nfa(dfa):
    trans = {}
    for src, sym, dst in dfa["delta"]:
        if (src, sym) not in trans:
            trans[(src, sym)] = set()
        trans[(src, sym)].add(dst)
    return trans

def simulate_nfa(dfa, input_string):
    trans = build_transition_table_nfa(dfa)

    current_states = epsilon_closure({dfa["s"]}, trans)

    input_symbols = set(dfa["sigma"]) - {EPSILON}

    for ch in input_string:
        if ch not in input_symbols:
            print(f"Warning: symbol '{ch}' not in alphabet")
            return False

        next_states = set()
        for state in current_states:
            if (state, ch) in trans:
                next_states.update(trans[(state, ch)])

        current_states = epsilon_closure(next_states, trans)

    return any(state in dfa["F"] for state in current_states)

def main():
    nfa_file = "nfa.txt"
    try:
        nfa = mega_parse_nfa(nfa_file)
        print("NFA loaded successfully.")
        print("Alphabet:", nfa["sigma"])
        print("States:", nfa["Q"])
        print("Start:", nfa["s"])
        print("Final states:", nfa["F"])
        print("Transitions:")
        for t in nfa["delta"]:
            print(f"  {t[0]} --{t[1]}--> {t[2]}")
        print()
    except Exception as e:
        print(f"Error loading NFA: {e}")
        return

    print("Input strings (empty line = quit):")
    while True:
        s = input("> ").strip()
        if not s:
            break
        accepted = simulate_nfa(nfa, s)
        print(f"'{s}' -> {'Accepted' if accepted else 'Rejected'}")

if __name__ == "__main__":
    main()