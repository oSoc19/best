from constants import CSV_HEADER


class CSVWriter:
    def __init__(self, path):
        self.output = open(path, 'w')
        self.output.write(','.join(CSV_HEADER) + '\n')

    def write_address(self, address):
        out = []
        for el in CSV_HEADER:
            if el in address:
                out.append(address[el])
            else:
                out.append('')
        self.output.write(','.join(out) + '\n')
