import os
import re
import pandas as pd
from pdfminer.high_level import extract_text ## use to convert pdf

# folder target PDFs
PDF_FOLDER = "sample" # change holder name here 

def extract_metadata(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    title = lines[0].replace('"','')
    media = ""
    date = ""
    for i in range(len(lines)):
        if re.search(r'\b(19|20)\d{2}\b', lines[i]):   # detect year, can find start from 1900
            date = lines[i]
            if i > 0:
                media = lines[i-1]
            break
    pub_type_match = re.search(r'Publication-Type:\s*(\w+)', text) # extract the type
    if pub_type_match:
        pub_type = pub_type_match.group(1)
    else:
        pub_type = "Webnews"
    return title, media, date, pub_type


def extract_body_original(lines):
    start = None
    end = len(lines)
    # locate the Body header
    for i in range(len(lines)):
        if lines[i].strip().lower() == "body":
            start = i + 1
            break

    if start is None:
        return ""

    # stop only at the Classification header
    for i in range(start, len(lines)):
        if lines[i].strip().lower() == "classification":
            end = i
            break

    body_lines = lines[start:end]

    return "\n".join(body_lines).strip()


# Return True if a line looks like menu or ad clutter.
def is_junk_line(line):
    s = line.strip()
    lower = s.lower()

    # empty
    if not s:
        return True
    # lines that are only bullets and punctuation
    if re.fullmatch(r"[\.\-\•\·\*\■\▪\▫\◦\s]+", s):
        return True

    # page markers
    if re.fullmatch(r"page \d+ of \d+", lower):
        return True

    #html residue
    if "skip-to-content" in lower:
        return True
    if 'content"class=' in lower:
        return True
    
    # headline index entries like a date with a title 
    if re.match(
    r'^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}',
    s):
        if len(s.split()) <= 15:
            return True

    # remove junk parts
    junk_exact = {
        "about", "masthead", "join", "submit", "advertise", "donate", "more",
        "facebook", "threads", "instagram", "x", "spotify", "linkedin",
        "youtube", "reddit", "email signup", "search this site",
        "submit search", "open navigation menu", "sponsored" }
    if lower in junk_exact:
        return True
    if re.match(r"^[\•\·\*\-\■\▪\▫\◦]\s*", s):
        return True

    return False

def looks_like_article_line(line):
    text = line.strip()

    # must contain letters
    if not re.search(r"[a-zA-Z]", text):
        return False
    # detect navigation lists: many capitalized words
    words = text.split()
    capital_words = sum(1 for w in words if w[0].isupper())
    if len(words) >= 5 and capital_words / len(words) > 0.6:
        return False
    # short line without any punctuation marks
    if len(text) < 28 and not re.search(r"[.,!?;:]", text):
        return False
    return True

def clean_body(body_original, title="", date=""):
    lines = [l.strip() for l in body_original.splitlines() if l.strip()]
    cleaned = []
    for line in lines:
        lower = line.lower()
        if is_junk_line(line):
            continue
        if not looks_like_article_line(line):
            continue
        if title and line.strip().strip('"') == title.strip().strip('"'):
            continue
        if date and line.strip() == date.strip():
            continue
        if lower == "end of document":
            continue
        cleaned.append(line)

    # drop leading junk until real paragraph starts
    start = 0
    for i in range(len(cleaned)):
        if looks_like_article_line(cleaned[i]):
            start = i
            break

    cleaned = cleaned[start:]

    return "\n".join(cleaned).strip()

def process_pdf(path):
    text = extract_text(path)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    title, media, date, pub_type = extract_metadata(text)
    body_original = extract_body_original(lines)
    cleaned = clean_body(body_original, title, date)
    return {
        "Title": title,
        "media_outlet": media,
        "Date": date,
        "body_original": body_original,
        "cleaned_body": cleaned,
        "type": pub_type
    }

records = []
for file in os.listdir(PDF_FOLDER):
    if file.endswith(".PDF"):
        full_path = os.path.join(PDF_FOLDER, file)
        records.append(process_pdf(full_path))

df = pd.DataFrame(records)
df.to_csv("articles.csv", index=False)
#print(df)
