import re


def clean_for_speech(text):

    if not text:
        return ""

    # Remove code blocks
    text = re.sub(
        r"```.*?```",
        "",
        text,
        flags=re.DOTALL
    )

    # Remove inline code markers
    text = text.replace("`", "")

    # Remove Markdown bold/italic markers
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("*", "")
    text = text.replace("_", "")

    # Remove Markdown headings
    text = re.sub(
        r"^\s*#+\s*",
        "",
        text,
        flags=re.MULTILINE
    )

    # Convert Markdown links to their visible text
    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text
    )

    # Remove excessive whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()