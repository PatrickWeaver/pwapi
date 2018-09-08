def create_slug(text, slug, date):
    # Might want to update this later to include date?
    # How to deal with non unique
    if slug == "":
        slug = text.replace(' ', '-').lower()
    return slug
