import re
from threading import Lock

lock = Lock()

class CommandExtractor:
    @staticmethod
    def extract_command(command_file, start, end, result, key):
        extracted = []
        capture = False

        for line in command_file:
            line = line.strip()
            if re.match(fr"{start}", line):
                capture = True
                continue

            if capture:
                if re.match(fr"{end}", line):
                    capture = False
                    break
                
                if capture and not re.match(fr'{start}', line):

                    extracted.append(line)

        with lock:
            if key not in result:
                result[key] = []
            result[key].extend(extracted)

