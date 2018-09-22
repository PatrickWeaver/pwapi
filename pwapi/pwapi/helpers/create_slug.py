import re
import uuid
from . db import find_single_instance

def create_slug(model, id, *args):
    # args are passed in priority order
    # Get first arg that is not blank as slug
    slug = False
    for text in args:
        if type(text) == str and text != "":
            slug = text
            break
    
    if not slug:
        slug = str(uuid.uuid4())
    
    sanitized_slug = sanitize_for_url(slug)
    # True for admin because this is not exposed to user input
    dup_instance = find_single_instance(model, "slug", sanitized_slug, True)
    if dup_instance:
        if id != dup_instance.id:
          sanitized_slug += "-" + str(uuid.uuid4())
          sanitized_slug = sanitize_for_url(sanitized_slug)
    return sanitized_slug
  
def sanitize_for_url(slug):
    sanitized_slug = re.sub(r"[\W_]", "-", slug)
    sanitized_slug = re.sub(r"--", "-", sanitized_slug).lower()
    if sanitized_slug.endswith("-"):
      sanitized_slug = sanitized_slug[:-1]
    print("SLUG:", sanitized_slug)
    if "--" in sanitized_slug:
        return sanitize_for_url(sanitized_slug)
    return sanitized_slug
