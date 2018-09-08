import re

def create_slug(text, slug, date):
    # Might want to update this later to include date?
    # How to deal with non unique
    if slug == "" or slug == None:
        slug = text
    sanitized_slug = re.sub(r"[\W_]", "-", slug)
    if sanitized_slug.endswith("-"):
      sanitized_slug = sanitized_slug[:-1]
    return sanitized_slug
