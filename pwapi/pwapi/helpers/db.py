import sys

def find_single_instance(model, lookup_key, lookup_value):
    if lookup_key == "slug":
        lookup_value = lookup_value.lower()
    try:
        filter_dict = {lookup_key: lookup_value}
        instance = model.objects.get(**filter_dict)
        return instance
    except:
        print("Instance not found with that identifier")
        return False
      
def save_object_instance(model, instance_dict):
    object_instance = model(**instance_dict)
    try:
        object_instance.save()
        return object_instance
    except:
        print("ERROR: Can't create object.")
        print(sys.exc_info())
        return False