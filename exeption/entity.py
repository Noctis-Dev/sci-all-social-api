class EntityNotFoundException(Exception):
    def __init__(self, entity_name, entity_id):
        self.entity_name = entity_name
        self.entity_id = entity_id
