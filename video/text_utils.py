import re

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()

def wrap_words(text: str, max_chars: int = 26, max_lines: int = 4) -> list[str]:
    words = clean_text(text).split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if len(test) <= max_chars:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
        if len(lines) >= max_lines:
            break
    if line and len(lines) < max_lines:
        lines.append(line)
    return lines

def shorten_title(title: str, max_words: int = 9) -> str:
    words = clean_text(title).split()
    return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")
