from prettytable import PrettyTable
# Pastikan untuk menginstal modul 'prettytable' jika belum terinstal
# Command untuk install: pip install prettytable
class State:
    def __init__(self, rule, dot_index, start, end, back_pointers, added_by, state_id=None):
        self.rule = rule  # (LHS, RHS)
        self.dot_index = dot_index
        self.start = start
        self.end = end
        self.back_pointers = back_pointers  # daftar objek State
        self.added_by = added_by
        self.state_id = state_id  # ID unik untuk setiap state

    def __repr__(self):
        lhs, rhs = self.rule
        dotted_production = rhs[:self.dot_index] + ["•"] + rhs[self.dot_index:]
        production = f"{lhs} → {' '.join(dotted_production)}"
        back_pointers_ids = [bp.state_id for bp in self.back_pointers]
        return f"{self.state_id}\t{production}\t[{self.start}, {self.end}]\t{back_pointers_ids}\t{self.added_by}"

    def __eq__(self, other):
        return (self.rule == other.rule and
                self.dot_index == other.dot_index and
                self.start == other.start and
                self.end == other.end)

    def __hash__(self):
        return hash((self.rule, self.dot_index, self.start, self.end))


class EarleyParser:
    def __init__(self, grammar, start_symbol):
        self.grammar = grammar
        self.start_symbol = start_symbol
        self.chart = []
        self.state_counter = 0  # Untuk memberikan ID unik pada setiap state

    def predict(self, state, chart_index):
        _, rhs = state.rule
        next_symbol = rhs[state.dot_index]
        if next_symbol in self.grammar:
            for production in self.grammar[next_symbol]:
                new_state = State((next_symbol, production), 0, chart_index, chart_index, [], "predictor")
                if new_state not in self.chart[chart_index]:
                    # Beri ID unik pada state baru
                    new_state.state_id = self.state_counter
                    self.state_counter += 1
                    self.chart[chart_index].append(new_state)
                    print(f"Predict: Added {new_state} to Chart[{chart_index}]")

    def scan(self, state, chart_index, word):
        _, rhs = state.rule
        next_symbol = rhs[state.dot_index]
        if next_symbol == word:
            new_state = State(state.rule, state.dot_index + 1, state.start, chart_index + 1, state.back_pointers, "scanner")
            if new_state not in self.chart[chart_index + 1]:
                # Beri ID unik pada state baru
                new_state.state_id = self.state_counter
                self.state_counter += 1
                self.chart[chart_index + 1].append(new_state)
                print(f"Scan: Added {new_state} to Chart[{chart_index + 1}]")

    def complete(self, state, chart_index):
        for prev_state in self.chart[state.start]:
            lhs, rhs = prev_state.rule
            if prev_state.dot_index < len(rhs):
                next_symbol = rhs[prev_state.dot_index]
                if next_symbol == state.rule[0]:
                    new_back_pointers = prev_state.back_pointers + [state]
                    new_state = State(prev_state.rule, prev_state.dot_index + 1, prev_state.start, chart_index, new_back_pointers, "completer")
                    if new_state not in self.chart[chart_index]:
                        # Beri ID unik pada state baru
                        new_state.state_id = self.state_counter
                        self.state_counter += 1
                        self.chart[chart_index].append(new_state)
                        print(f"Complete: Added {new_state} to Chart[{chart_index}]")

    def parse(self, words):
        n = len(words)
        self.chart = [[] for _ in range(n + 1)]
        initial_rule = (f"{self.start_symbol}'", [self.start_symbol])
        initial_state = State(initial_rule, 0, 0, 0, [], "seed")
        # Beri ID unik pada state awal
        initial_state.state_id = self.state_counter
        self.state_counter += 1
        self.chart[0].append(initial_state)

        self.input_string = ' '.join(words)  # Simpan input string

        for i in range(n + 1):
            print(f"\nProcessing Chart[{i}]")
            if i < n:
                print(f"Current word: {words[i]}")
            j = 0
            while j < len(self.chart[i]):
                state = self.chart[i][j]
                lhs, rhs = state.rule
                if state.dot_index < len(rhs):
                    next_symbol = rhs[state.dot_index]
                    if next_symbol in self.grammar:
                        self.predict(state, i)
                    elif i < n:
                        self.scan(state, i, words[i])
                else:
                    self.complete(state, i)
                j += 1

        # Periksa apakah input diterima
        self.accepted = False
        for state in self.chart[n]:
            if (state.rule == initial_rule and
                state.dot_index == len(initial_rule[1]) and
                state.start == 0 and state.end == n):
                self.accepted = True
                break

        return self.chart

    def display_chart(self):
        for i, states in enumerate(self.chart):
            print(f"\nChart {i}:")
            table = PrettyTable()
            table.field_names = ["ID", "Dotted Production", "Start, End", "Back Pointers", "Added by"]
            for state in states:
                lhs, rhs = state.rule
                dotted_production = rhs[:state.dot_index] + ["•"] + rhs[state.dot_index:]
                production = f"{lhs} → {' '.join(dotted_production)}"
                back_pointers_ids = [bp.state_id for bp in state.back_pointers]
                table.add_row([state.state_id, production, f"[{state.start}, {state.end}]", back_pointers_ids, state.added_by])
            print(table)

        # Tampilkan apakah input string diterima atau tidak
        if self.accepted:
            print(f'\nInput string "{self.input_string}" diterima oleh grammar.')
        else:
            print(f'\nInput string "{self.input_string}" tidak diterima oleh grammar.')



# Definisikan grammar sebagai dictionary
grammar = {
    "S": [["NP", "VP"]],
    "NP": [["N"], ["DET", "NP"], ["NP", "PP"]],
    "VP": [["V"], ["V", "NP"], ["V", "NP", "PP"]],
    "PP": [["PREP", "NP"]],
    "N": [["Chris"], ["blind"], ["bread"], ["eyes"]],
    "V": [["opened"], ["ate"]],
    "DET": [["the"], ["a"]],
    "PREP": [["of"], ["in"]]
}

# Buat parser dengan grammar dan simbol awal
parser = EarleyParser(grammar, "S")

# Parsing kalimat input
input_sentence = ["Chris", "opened", "the", "eyes"]
chart = parser.parse(input_sentence)

# Tampilkan chart yang dihasilkan
parser.display_chart()
