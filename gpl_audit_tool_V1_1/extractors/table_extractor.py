import re
from collections import OrderedDict

class TableExtractor:
    def __init__(self, lines):
        self.lines = lines

    def get_nodeID(self):
        for line in self.lines:
            search = re.search(r"MeContext=([\w-]+)", line)
            if search:
                return search.group(1)

    def parse_tables(self, command):
        tables = []
        current_header = []
        command_found = False

        for line in self.lines:
            line = line.strip()

            if not command_found:
                if re.match(rf"^[A-Z0-9-_]+>\s{re.escape(command)}", line):
                    command_found = True
                continue
            elif re.match(r"^[A-Z0-9-_]+>", line):
                break
                
            if not line or line.startswith("."):
                continue

            if line.startswith("MO"):
                current_header = [col.strip() for col in line.split(";")]
                continue

            if current_header:
                row = [cell.strip() for cell in line.split(";")]
                tables.append((current_header, row))

        return tables

    def extract_table(self, command):
        parsed_rows = self.parse_tables(command)
        all_headers = OrderedDict()

        for header, _ in parsed_rows:
            for h in header:
                all_headers[h] = None

        merged = []
        for header, row in parsed_rows:
            row_dict = dict(zip(header, row))
            full_row = [row_dict.get(h, "") for h in all_headers]
            merged.append(";".join(full_row))

        return [";".join(all_headers)] + merged