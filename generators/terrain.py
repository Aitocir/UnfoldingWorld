import opensimplex as os

def _norm(x):
    n = (1.0 + (x*(1/0.866))) / 2
    return min(1.0,(max(0.0,n)))

def _scale(x, lower, upper):
    r = upper-lower
    return lower + (r * x)

def generate_tile(x, y, seed=0):
    tile_entity = '{0};{1}'.format(x,y)
    tile = {'entity': tile_entity}
    #
    #  TODO: make these cached and configurable
    m_lower_min = 0.8
    m_lower_max = 1.2
    m_upper_min = 0.0
    m_upper_max = 0.0
    t_lower_min = 0.2
    t_lower_max = 1.0
    t_upper_min = 0.0
    t_upper_max = 0.2
    #
    #  terrain type
    #  TODO: cache OpenSimplex() objects instead of re-creating for each tile call
    elevation = _norm(os.OpenSimplex(seed+1).noise2d(x,y))
    moisture = _norm(os.OpenSimplex(seed+2).noise2d(x,y))
    m_lower = _scale(moisture, m_lower_min, m_lower_max)
    m_upper = _scale(moisture, m_upper_min, m_upper_max)
    moisture = _scale(moisture, m_lower, m_upper)
    temperature = _norm(os.OpenSimplex(seed+3).noise2d(x,y))
    t_lower = _scale(temperature, t_lower_min, t_lower_max)
    t_upper = _scale(temperature, t_upper_min, t_upper_max)
    temperature = _scale(temperature, t_lower, t_upper)
    #  TODO: dynamically load plant definitions from elsewhere and loop through them or something
    plants = []
    if 0.2 < temperature < 0.6 and 0.2 < moisture < 0.8:
        plants.append({
            'entity': tile_entity+';apple tree',
            'growth_rate': 10,
            'growth': 100,
            'max_quantity': 10,
            'plant': 'apple tree', 
            'resource': 'apples'
        })
    if 0.5 < temperature < 1.0 and 0.0 < moisture < 0.5:
        plants.append({
            'entity': tile_entity+';fire berry bush',
            'growth_rate': 4,
            'growth': 100,
            'max_quantity': 25,
            'plant': 'fire berry bush', 
            'resource': 'fire berries'
        })
    tile['plants'] = [x['plant'] for x in plants]
    return tile, plants