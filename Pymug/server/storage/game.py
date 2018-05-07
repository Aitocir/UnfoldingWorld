import rethinkdb as r

class GameDAO:
    def __init__(self, host='localhost', port=28015, db='game'):
        self._conn = r.connect(host=host, port=port, db=db)
    #
    #  get a Component of an Entity
    #  -> document
    def get_component_for_entity(self, component_name, entity_name):
        if isinstance(component_name, str) and isinstance(entity_name, str):
            try:
                result = r.table(component_name).get(entity_name).run(self._conn)
            except:
                raise
            return result
        else:
            raise ValueError('component_name and entity_name must be strings')
    #
    #  set a Component of an Entity
    #  -> bool (success)
    def set_component_for_entity(self, component_name, component_value, entity_name):
        if isinstance(component_name, str) and isinstance(component_value, dict):
            try:
                component_value['entity'] = entity_name
                result = r.table(component_name).insert(
                    component_value,
                    conflict = 'replace'
                    ).run(self._conn)
            except:
                raise
            return True
        else:
            raise ValueError('component_name and entity_name must be strings, component_value must be a dict')
    #
    #  update a Component of an Entity
    #  -> bool (success)
    def update_component_for_entity(self, component_name, component_value, entity_name):
        if isinstance(component_name, str) and isinstance(component_value, dict):
            try:
                component_value['entity'] = entity_name
                result = r.table(component_name).get(entity_name).update(
                    component_value
                    ).run(self._conn)
            except:
                raise
            return True
        else:
            raise ValueError('component_name and entity_name must be strings, component_value must be a dict')
    #
    #  delete a Component of an Entity
    #  -> bool (success)
    def delete_component_for_entity(self, component_name, entity_name):
        if isinstance(component_name, str) and isinstance(entity_name, str):
            try:
                result = r.table(component_name).get(entity_name).delete().run(self._conn)
            except:
                raise
            return True
        else:
            raise ValueError('component_name and entity_name must be strings')
    
    #
    #  get all Entities matching provided value
    #  -> [document]
    def get_matching_entities(self, component_name, component_value):
        if isinstance(component_name, str) and isinstance(component_value, dict):
            try:
                results = r.table(component_name).filter(component_value).run(self._conn)
                entities = [x['entity'] for x in results]
            except:
                raise
            return entities
        else:
            raise ValueError('component_name must be a string, and component_value must be a dict')
    #
    #  get all Components matching provided value
    #  -> [document]
    def get_matching_components(self, component_name, component_value):
        if isinstance(component_name, str) and isinstance(component_value, dict):
            try:
                results = r.table(component_name).filter(component_value).run(self._conn)
            except:
                raise
            return results
        else:
            raise ValueError('component_name must be a string, and component_value must be a dict')
    #
    #  get all Components matching provided predicates
    #  -> [document]
    def get_components_matching_predicates(self, component_name, predicates):
        if isinstance(component_name, str) and isinstance(predicates, list):
            try:
                tmp = r.table(component_name)
                for pred in predicates:
                    include_missing = False
                    if len(pred) > 3:
                        if pred[3] == True:
                            include_missing = True
                        else:
                            raise ValueError('Only valid value for fourth predicate elemet is True to indicate inclusion of objects with missing field')
                    if pred[1] == '<':
                        tmp = tmp.filter(r.row[pred[0]] < pred[2], default=include_missing)
                    elif pred[1] == '<=':
                        tmp = tmp.filter(r.row[pred[0]] <= pred[2], default=include_missing)
                    elif pred[1] == '>':
                        tmp = tmp.filter(r.row[pred[0]] > pred[2], default=include_missing)
                    elif pred[1] == '>=':
                        tmp = tmp.filter(r.row[pred[0]] >= pred[2], default=include_missing)
                    elif pred[1] == '==':
                        tmp = tmp.filter(r.row[pred[0]] == pred[2], default=include_missing)
                    elif pred[1] == '!=':
                        tmp = tmp.filter(r.row[pred[0]] != pred[2], default=include_missing)
                results = tmp.run(self._conn)
            except:
                raise
            return results
        else:
            raise ValueError('component_name must be a string, and predicates must be a list of 3-tuples')
    #
    #  get all Entities for Component
    #  -> [document]
    def get_all_entities(self, component_name):
        if isinstance(component_name, str):
            try:
                results = r.table(component_name).run(self._conn)
                entities = [x['entity'] for x in results]
            except:
                raise ValueError('The component "{0}" wasn\'t found in the database'.format(component_name))
            return entities
        else:
            raise ValueError('component_name must be a string')
    #
    #  get all Components for Component
    #  -> [document]
    def get_all_components(self, component_name):
        if isinstance(component_name, str):
            try:
                results = r.table(component_name).run(self._conn)
            except:
                raise ValueError('The component "{0}" wasn\'t found in the database'.format(component_name))
            return results
        else:
            raise ValueError('component_name must be a string')