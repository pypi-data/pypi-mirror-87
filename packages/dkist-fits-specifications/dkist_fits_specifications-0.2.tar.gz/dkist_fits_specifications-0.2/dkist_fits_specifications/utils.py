"""
Functions and variables common to all specifications.
"""
from typing import Any, Dict, List, Tuple, Optional, cast, Callable
from pathlib import Path
from functools import partial

import yaml

__all__ = ['raw_schema_type_hint', 'schema_type_hint', 'expand_naxis']

schema_type_hint = Dict[str, Dict[str, Any]]
"""
A type hint for a single validation schema.

As returned by `.load_spec122` and `.load_spec214`.
"""
raw_schema_type_hint = Tuple[Dict, schema_type_hint]
"""
A Type hint for a single raw schema, as loaded directly from a yaml file.

This type is returned by the `.load_raw_spec122` and `.load_raw_spec214` methods.
"""


def expand_keys(naxis: int, keys: List[str]) -> List[str]:
    naxis_range = range(1, naxis + 1)
    output_keys = []
    for key in keys:
        if "n" in key:
            output_keys += [key.replace("n", str(i)) for i in naxis_range]
        elif "i" in key:
            output_keys += [key.replace("i", str(i)) for i in naxis_range]
        elif "j" in key:
            output_keys += [key.replace("j", str(i)) for i in naxis_range]
        else:
            output_keys += [key]
    if output_keys != keys:
        return expand_keys(naxis, output_keys)
    return output_keys


def _expand_schema(
        expansion_function: Callable[[List[str]], schema_type_hint],
        schema: schema_type_hint) -> schema_type_hint:
    """
    Given an expansion function expand the schema.
    """
    expanded_schema = {}
    for key, key_schema in schema.items():
        expanded_keys = expansion_function([key])
        expanded_schema.update({k: key_schema for k in expanded_keys})
    return expanded_schema


def expand_naxis(naxis: int, schema: schema_type_hint) -> schema_type_hint:
    """
    Expand indices in the keys of the schema.

    This function takes keys in a schema with indices corresponding to the
    number of axes in the FITS file and expands the schema so that there is a
    key for each axis.

    This function is used to expand keys such as ``NAXISn`` in the 122
    specifications as 122 always has ``NAXIS = 3``. It can be used by consumers
    of the 214 schemas to expand the schema for validation or generation of
    headers corresponding to a known number of axes for the file.

    Parameters
    ----------
    naxis
        The value of ``NAXIS`` to expand the schema with.

    schema
        The schema to expand.

    Returns
    -------
    expanded_schema
        The input schema expanded with more keys as needed.
    """
    return _expand_schema(partial(expand_keys, naxis), schema)


def load_raw_spec(base_path: Path, glob: Optional[str] = None) -> Dict[str, raw_schema_type_hint]:
    """
    Load raw schemas from the yaml files in ``base_path``.

    Parameters
    ----------
    glob
        A pattern to use to match a file, without the ``.yml`` file extension.
        Can be a section name like ``'wcs'``.

    Returns
    -------
    raw_schemas
        The schemas as loaded from the yaml files.
    """
    if glob is None:
        glob = "*"

    files = Path(base_path).glob(f"{glob}.yml")

    raw_schemas = {}
    for fname in files:
        schema_name = fname.stem
        with open(fname) as fobj:
            raw_schema = tuple(yaml.load_all(fobj, Loader=yaml.SafeLoader))

        # Apply a more specific type hint to the loaded schema
        raw_schemas[schema_name] = cast(raw_schema_type_hint, raw_schema)

    return raw_schemas
