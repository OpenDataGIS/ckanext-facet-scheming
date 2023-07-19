from ckan.common import config
import ckan.logic as logic
from ckanext.facet_scheming import config as fs_config
import logging
import os
import hashlib
from threading import Lock
from ckanext.dcat.utils import CONTENT_TYPES
import yaml
from yaml.loader import SafeLoader
from pathlib import Path

logger = logging.getLogger(__name__)

# No configuro estas variables al principio del todo porque no sé si luego la
# aplicación cargará otras extensiones con información que pueda necesitar.
# Configurándolas con la primera petición me aseguro que todo está en orden y
# funcionando cuando se inicien.

_facets_dict = None
_public_dirs = None
_files_hash = []
_dirs_hash = []

_facets_dict_lock = Lock()
_public_dirs_lock = Lock()


def get_facets_dict():
    '''
    Busco las etiquetas de todos los campos definidos en el fichero de scheming
    '''
    global _facets_dict
    if not _facets_dict:
        with _facets_dict_lock:
            if not _facets_dict:
                # Lo lógico sería colocar un único if tras el lock, pero en
                # esta parte del código solo se entrará la primera vez que se
                # ejecute el código al iniciar la aplicación, por lo que me ha
                # parecido más eficiente a largo plazo hacerlo así.
                _facets_dict = {}

                schema = logic.get_action('scheming_dataset_schema_show')(
                    {},
                    {'type': 'dataset'}
                    )

                for item in schema['dataset_fields']:
                    _facets_dict[item['field_name']] = item['label']

                for item in schema['resource_fields']:
                    _facets_dict[item['field_name']] = item['label']

    return _facets_dict


def get_public_dirs():
    global _public_dirs

    if not _public_dirs:
        with _public_dirs_lock:
            if not _public_dirs:
                _public_dirs = config.get('extra_public_paths', '').split(',')

    return _public_dirs


def public_file_exists(path):
    #    logger.debug("Compruebo si existe {0}".format(path))
    file_hash = hashlib.sha512(path.encode('utf-8')).hexdigest()

    if file_hash in _files_hash:
        return True

    for dir in get_public_dirs():
        #  logger.debug("Buscando en {0}".format(os.path.join(dir,path)))
        if os.path.isfile(os.path.join(dir, path)):
            _files_hash.append(file_hash)
            return True

    return False


def public_dir_exists(path):
    dir_hash = hashlib.sha512(path.encode('utf-8')).hexdigest()

    if dir_hash in _dirs_hash:
        return True

    for dir in get_public_dirs():
        if os.path.isdir(os.path.join(dir, path)):
            _dirs_hash.append(dir_hash)
            return True

    return False

def init_config():
    fs_config.data_links = _load_yaml('data_links.yaml')
    fs_config.inspire_links = _load_yaml('inspire_links.yaml')

def _load_yaml(file):
    source_path = Path(__file__).resolve(True)
    respuesta = None
    try:
        p = os.path.join(source_path.parent, file)
        with open(p,'r') as f:
            respuesta=yaml.load(f, Loader=SafeLoader )
    except FileNotFoundError:
        logger.error("El fichero {0} no existe".format(file))
    except Exception as e:
        logger.error("No ha sido posible leer la configuración de {0}: ".format(e))
    return respuesta


def get_linked_data(id):
    if fs_config.debug:
        data_links = _load_yaml('data_links.yaml')
    else:
        data_links=fs_config.data_links

    data=[]
    for name in CONTENT_TYPES:
        data.append({
            'name': name,
            'display_name': data_links.get(name,{}).get('display_name',CONTENT_TYPES[name]),
            'image_display_url': data_links.get(name,{}).get('image_display_url',None),
            'description': data_links.get(name,{}).get('description','Tipos '+CONTENT_TYPES[name]),
            'endpoint_data':{
                '_id': id,
                '_format': name,
                }
        })

    return data

def get_inspire():
    if fs_config.debug:
        inspire_links = _load_yaml('inspire_links.yaml')
    else:
        inspire_links=fs_config.inspire_links
    data=[]
    for item in inspire_links.get('inspire_formats',{}):
        data.append({
            'name': item['name'],
            'display_name': item['display_name'],
            'image_display_url': item['image_display_url'],
            'description': item['description'],
            'url': inspire_links['inspire_link'].format(schema=item['outputSchema'],id='{id}')
        })

    return data
        
        
