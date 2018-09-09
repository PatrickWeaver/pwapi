# Default function for unmodified instance dicts
def unmodified(instance):
  return instance

def remove_hidden_func(field):
  
    def closure(instance):
      if instance[field] == True:
          return None
      return instance
    
    return closure