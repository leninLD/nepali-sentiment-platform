import re
import unicodedata

_NOISE = (
    r'~؟॥"▬`%´•●=+÷।–][{}*"_…'
    + r"''\/"
    + ';abcdefghijklmnopqrstuvwxyz1234567890०१२३४५६७८९()-.|!?\",:—?।'
    + "'"
)

def _rm_emojis(t: str) -> str:
    cleaned = []
    for char in t:
        cp = ord(char)
        if (
            0x1F600 <= cp <= 0x1F64F or 0x1F300 <= cp <= 0x1F5FF or
            0x1F680 <= cp <= 0x1F6FF or 0x1F700 <= cp <= 0x1F77F or
            0x1F780 <= cp <= 0x1F7FF or 0x1F800 <= cp <= 0x1F8FF or
            0x1F900 <= cp <= 0x1F9FF or 0x1FA00 <= cp <= 0x1FA6F or
            0x1FA70 <= cp <= 0x1FAFF or 0x2600  <= cp <= 0x26FF  or
            0x2700  <= cp <= 0x27BF  or 0x2300  <= cp <= 0x23FF  or
            0x2B50  <= cp <= 0x2B55  or 0x25AA  <= cp <= 0x25FE  or
            0x1F1E0 <= cp <= 0x1F1FF or 0x1F100 <= cp <= 0x1F1FF or
            0x1F200 <= cp <= 0x1F2FF or 0x1F000 <= cp <= 0x1F02F or
            0x1F0A0 <= cp <= 0x1F0FF or 0xFE00  <= cp <= 0xFE0F  or
            0x1F3FB <= cp <= 0x1F3FF or 0x2702  <= cp <= 0x27B0  or
            cp in (0x200D, 0xFE0F, 0x00A9, 0x00AE, 0x2122,
                   0x3030, 0x303D, 0x3297, 0x3299) or
            unicodedata.category(char) in ('So', 'Sk')
        ):
            continue
        cleaned.append(char)
    return "".join(cleaned)

def _rm_zero_width(t: str) -> str:
    return re.sub(r'[\u200c-\u200f\u202a-\u202f\u2066-\u2069]', '', t)

def _rm_urls(t: str) -> str:
    t = re.sub(r'https?://\S+', ' ', t)
    t = re.sub(r'www\.\S+', ' ', t)
    t = re.sub(r't\.co/\S+', ' ', t)
    t = re.sub(r'\b\S+\.co\.np\S*', ' ', t)
    t = re.sub(r'\b\S+\.(com|org|net|io|gov|edu|co|info|biz|np|me|tv)\S*',
               ' ', t, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', t).strip()

def _rm_mentions(t: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'@\S*', '', t)).strip()

def _rm_hashtags(t: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'#\S*', '', t)).strip()

def _rm_noise_chars(t: str) -> str:
    t = t.lower()
    for ch in _NOISE:
        t = t.replace(ch, ' ')
    return re.sub(r'\s+', ' ', t).strip()

def _rm_special_chars(t: str) -> str:
    t = re.sub(r'[^\u0900-\u097Fa-zA-Z0-9\s]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

def clean_tweet(text: str) -> str:
    if not text or str(text).strip() in ('', 'nan'):
        return ''
    t = str(text)
    t = _rm_emojis(t)
    t = _rm_zero_width(t)
    t = _rm_urls(t)
    t = _rm_mentions(t)
    t = _rm_hashtags(t)
    t = _rm_noise_chars(t)
    t = _rm_special_chars(t)
    return t.strip()
