from trident.backend.common import *
_session = get_session()
_backend = _session.backend
from  trident.reinforcement.utils import *
if _backend == 'pytorch':
    import trident.reinforcement.pytorch_policies

elif _backend == 'tensorflow':
    pass
