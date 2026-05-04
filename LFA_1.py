"""
cum definim DFA orice automat lab 1
(sigma, Q, F, delta, s)

sigma = alfabetul nostru {0, 1}
Q = {q0, q1, q2}
F = {q2}
delta etse o functie delta(q,s) = q
s = {q0}

delta putem sa l exprimam ca un tabel
q0,1 --> q1 etc.
"""

# def sigma (f):
#     for line in readlines(f):
#         if line == "<sigma>":
#             lang = 1;
#     if lang != 1:
#         raise ValueError("Cannot decode the languege you want to use for this section.")
#     for line in readlines(f):
#         section_contents = line.strip().split(" ,=")
# f.close()
#definesc variabilele ce le folosesc in dfa
lang = []
states = []
start = 9999
final = 0
delta_function = []

#definesc initial state pentru a testa daca fisierul are structura care trebuie:

#verificam daca fisierul are formatul cerut
# verificam daca fisierul are formatul cerut
def format_checking(filename):
    language_existance = False
    states_existance = False
    final_state_existance = False
    jumping_existance = False
    initial_state_existance = False

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line == "<sigma>":
                language_existance = True
            elif line == "<Q>":
                states_existance = True
            elif line == "<F>":
                final_state_existance = True
            elif line == "<delta>":
                jumping_existance = True
            elif line == "<s>":
                initial_state_existance = True

    if (language_existance and states_existance and jumping_existance
        and final_state_existance and initial_state_existance):
        return True
    else:
        raise ValueError(
            "This file does not have the correct format. "
            "Required sections: sigma, Q, F, delta, s"
        )
#extragem alfabetul
def language_extractor(filename):
    lang = []

    if format_checking(filename):
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()

                if len(parts) >= 4 and parts[0] == "define" and parts[1] == "lang":
                    start = line.find("[")
                    end = line.find("]")

                    if start != -1 and end != -1:
                        content = line[start + 1:end]
                        items = content.split(",")

                        for item in items:
                            item = item.strip()
                            if item:
                                lang.append(int(item))

    for x in lang:
        print(x)

    return lang


def initial_state_extractor(filename):
    start = None
    in_s_section = False

    if format_checking(filename):
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if line == "<s>":
                    in_s_section = True
                    continue
                elif line == "<end_s>":
                    in_s_section = False
                    continue

                if in_s_section:
                    # remove trailing semicolon if present
                    state = line.rstrip(";").strip()
                    if state:
                        start = state
                        break  # only one initial state

    print(start)
    return start

def final_state_extractor(filename):
    final = None
    in_F_section = False

    if format_checking(filename):
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if line == "<F>":
                    in_F_section = True
                    continue
                elif line == "<end_F>":
                    in_F_section = False
                    continue

                if in_F_section:
                    state = line.rstrip(";").strip()
                    if state:
                        final = state
                        break
    print(final)
    return final

def number_of_states_extractor(filename):
    states = []
    in_Q_section = False

    if format_checking(filename):
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if line == "<Q>":
                    in_Q_section = True
                    continue
                elif line == "<end_Q>":
                    in_Q_section = False
                    continue

                if in_Q_section:
                    parts = line.strip().split()

                    if len(parts) >= 4 and parts[0] == "define" and parts[1] == "states":
                        start = line.find("[")
                        end = line.find("]")

                        if start != -1 and end != -1:
                            content = line[start + 1:end]
                            items = content.split(",")

                            for item in items:
                                item = item.strip()
                                if item:
                                    states.append(item)

    print(states)
    return states




def delta_extractor(filename):
    delta = []
    in_delta_section = False

    if format_checking(filename):
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if line == "<delta>":
                    in_delta_section = True
                    continue
                elif line == "<end_delta>":
                    in_delta_section = False
                    continue

                if in_delta_section:
                    parts = line.strip().split()

                    if len(parts) >= 4 and parts[0] == "define" and parts[1] == "delta_function":
                        start1 = line.find("[")
                        end1 = line.rfind("]")

                        if start1 != -1 and end1 != -1:
                            content_in_matrix = line[start1 + 1:end1]
                            items = content_in_matrix.split(",")

                            for item in items:
                                item = item.strip()
                                if item:
                                    delta.append(item)

                            # for item in items:
                            #     start2 = line.find("[")
                            #     end2 = line.rfind("]")


                                # if start2 != -1 and end2 != -1:
                                #     content_in_list = line[start2 + 1:end2]
                                #     ytems = content_in_list.split(",")
                                #
                                #     for ytem in ytems: aici e problema ca pune de fiecare data cand gaseste in interior
                                #         ytem = ytem.strip()
                                #         if ytem:
                                #             delta.append(ytem)  nu merge, se duce la infinit ca intra in bucla

    print (delta)
    return delta


#checking all functions
format_checking("dfa.txt")
language_extractor("dfa.txt")
number_of_states_extractor("dfa.txt")
initial_state_extractor("dfa.txt")
final_state_extractor("dfa.txt")
delta_extractor("dfa.txt")

#sticking everything together ca sa arate mai bine ca e jale mare

def working_file(filename):
    if format_checking(filename):
        if language_extractor(filename):
            if number_of_states_extractor(filename):
                if delta_extractor(filename):
                    if initial_state_extractor(filename):
                        if final_state_extractor(filename):

                            language = language_extractor(filename)
                            number_of_states = number_of_states_extractor(filename)
                            initial_state = initial_state_extractor(filename)
                            final_state = final_state_extractor(filename)
                            delta_function = delta_extractor(filename)

                        else:
                            raise ValueError("You do not have a final state. Please reconsider!")
                    else:
                        raise ValueError("You do not have an initial state. Please reconsider!")
                else:
                    raise ValueError("You do not have a delta function. Please reconsider!")
            else:
                raise ValueError("You do not have a defined list of states. Please reconsider!")
        else:
            raise ValueError("You do not have a defined language. Please reconsider!")

    return language, number_of_states, initial_state, final_state, delta_function
    print(language, number_of_states, initial_state, final_state, delta_function)

working_file("dfa.txt")