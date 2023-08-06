import os
from typing import *

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.v1.seismic_service_messages_pb2 import (
        CreatePartitionRequest,
        SearchPartitionsRequest,
        EditPartitionRequest,
    )
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import Partition, SearchSpec, Identifier
else:
    from cognite.seismic._api.shims import Identifier


MaybeString = Optional[str]
Metadata = Dict[str, str]
LineRange = Union[Tuple[int, int], Tuple[int, int, int]]


def get_identifier(id: Optional[int] = None, external_id: MaybeString = None) -> Identifier:
    """Turn an id or external id into a v1.Identifier.
    
    Returns:
        Identifier: The created Identifier
    """
    if (id is not None) and (external_id is not None):
        raise Exception("You should only specify one of: id, external_id")
    if id is not None:
        return Identifier(id=id)
    elif external_id is not None:
        return Identifier(external_id=external_id)
    raise Exception("You must specify at least one of: id, external_id")


def get_search_spec(
    id: Optional[int] = None,
    external_id: MaybeString = None,
    external_id_substring: MaybeString = None,
    name: MaybeString = None,
    name_substring: MaybeString = None,
):
    """Turns kwargs into a SearchSpec.

    Returns:
        SearchSpec: The created SearchSpec.
    """
    spec = SearchSpec()
    if id is not None:
        spec.id = id
    if external_id is not None:
        spec.external_id = external_id
    if external_id_substring is not None:
        spec.external_id_substring = external_id_substring
    if name is not None:
        spec.name = name
    if name_substring is not None:
        spec.name_substring = name_substring
    return spec
