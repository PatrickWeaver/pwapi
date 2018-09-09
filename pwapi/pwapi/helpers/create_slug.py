import re
from . crud_instance import find_single_instance_from

def create_slug(text, slug, date, model, id):
    # Might want to update this later to include date?
    # How to deal with non unique
    if slug == "" or slug == None:
        slug = text
    sanitized_slug = sanitize_for_url(slug)
    dup_instance = find_single_instance_from(model, "slug", sanitized_slug)
    if dup_instance:
        if id != dup_instance.id:
          sanitized_slug += "-" + date.isoformat()
          sanitized_slug = sanitize_for_url(sanitized_slug)
    return sanitized_slug
  
def sanitize_for_url(slug):
    sanitized_slug = re.sub(r"[\W_]", "-", slug)
    if sanitized_slug.endswith("-"):
      sanitized_slug = sanitized_slug[:-1]
    return sanitized_slug
