from ckanext.facet_scheming.tests.config import fake_context

def create_fake_context(**kwargs):
    respuesta=dict(fake_context)
    for clave in kwargs:
        respuesta[clave]=kwargs[clave]
    
    return respuesta