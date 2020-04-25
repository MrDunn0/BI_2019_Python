class Dna:
    def __init__(self, sequence):
        self.sequence = str(sequence)
        if not (self.sequence and len(set(self.sequence)) == len(set(self.sequence) & {"A", "G", "T", "C"})):
            raise ValueError

    def gc_content(self):
        return (self.sequence.count("G") + self.sequence.count("C")) / len(self.sequence) * 100

    def reverse_complement(self):
        nt_dict = {"A": "T", "T": "A", "C": "G", "G": "C"}
        return "".join(nt_dict[nt] for nt in self.sequence[::-1])

    def transcribe(self):
        transcript = "".join("U" if nt == "T" else nt for nt in self.sequence)
        return Rna(transcript)


class Rna:
    def __init__(self, sequence):
        self.sequence = str(sequence)
        if not (self.sequence and len(set(self.sequence)) == len(set(self.sequence) & {"A", "G", "U", "C"})):
            raise ValueError

    def gc_content(self):
        return (self.sequence.count("G") + self.sequence.count("C")) / len(self.sequence) * 100

    def reverse_complement(self):
        nt_dict = {"A": "U", "U": "A", "C": "G", "G": "C"}
        return "".join(nt_dict[nt] for nt in self.sequence[::-1])
