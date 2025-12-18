def slugify(text: str) -> str:
    return text.strip().casefold().replace("","-")