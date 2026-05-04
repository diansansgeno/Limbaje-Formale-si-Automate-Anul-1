"""
Eficientizare pentru LFA_1
(sa deschid fisierul de fiecare data nu e o idee buna de loc -> neeficient
din cauza asta.)
Metode pentru return sectiuni si return contents ca sa fie totul ok-ish-er
"""
import re

def mega_parse_dfa(filename):
    dfa = {
        "sigma": [],
        "Q": [],
        "F": [],
        "delta": [],
        "s": []
    }

    current_section = None


    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            #detect inceputul sectiunii
            if line in ["<sigma>", "<Q>", "<F>", "<delta>", "<s>"]:
                current_section = line[1:-1]
                continue

            #detect end of section
            if line.startswith("<end_"):
                current_section = None
                continue

            if not current_section:
                continue

            if current_section == "sigma":
                match = re.search(r"\[(.*?)\]", line)
                if match:
                    dfa["sigma"] = [x.strip() for x in match.group(1).split(",")]

            elif current_section == "Q":
                match = re.search(r"\[(.*?)\]", line)
                if match:
                    dfa["Q"] = [x.strip() for x in match.group(1).split(",")]

            elif current_section == "F":
                dfa["F"] = [line.replace(";", "").strip()]

            elif current_section == "s":
                dfa["s"] = line.replace(";", "").strip()

            elif current_section == "delta":
                pairs = re.findall(r"\[(.*?)\]", line)
                for p in pairs:
                    dfa["delta"].append([x.strip() for x in p.split(",")])

    #format checking
    # for key in dfa:
    #     if not dfa[key]:
    #         raise ValueError("Section {key} is missing its components. Please reconsider.")


    return dfa

dfa = mega_parse_dfa("dfa.txt")

print("Alphabet:", dfa["sigma"])
print("States:", dfa["Q"])
print("Start:", dfa["s"])
print("Final:", dfa["F"])
print("Delta:", dfa["delta"])
