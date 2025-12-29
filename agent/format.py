# ✅ Fix: Strip ANSI escape sequences, with input safety
import re

def clean_output(output):
    # 1. Ensure input is a string
    if isinstance(output, bytes):
        output = output.decode("utf-8", errors="ignore")
    elif not isinstance(output, str):
        output = str(output)

    # 2. Strip ANSI escape sequences (colors)
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    output = ansi_escape.sub('', output)

    # 3. Fix "â”€" symbols (Unicode Box Drawing characters)
    # This encodes to ASCII and ignores characters that can't be represented
    # This effectively removes the lines and decorative symbols
    output = output.encode("ascii", "ignore").decode("ascii")

    return output.strip()