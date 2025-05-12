import re

class TableExtractor:
    def __init__(self, lines):
        self.lines = lines
    
    def get_nodeID(self):
        for line in self.lines:
            search = re.search(r"Connected to (\S+) .*?MeContext=([\w-]+)", line)
            if search:
                return search.group(2)
        return None

    def extract_table(self, command):
        command_found = False
        header_found = False
        table_data = []
        skip_indicator = False 

        for line in self.lines:
            if re.match(rf"^[A-Z0-9-_]+>\s{re.escape(command)}", line):
                command_found = True
                continue

            if command_found:
                if re.match(r'^\.+', line):  
                    continue
                if re.match(r"^MO", line):  
                    if not header_found:
                        table_data.append(line)
                        header_found = True
                    else:
                        skip_indicator = True
                        
                    continue  
                
                if skip_indicator and re.match(r"^MO", line):
                    continue  
                
                if header_found:
                    if re.match(r'^\.+$', line):  
                        continue
                    if line.strip():
                        table_data.append(line)
                    else:
                        break  

        return table_data
