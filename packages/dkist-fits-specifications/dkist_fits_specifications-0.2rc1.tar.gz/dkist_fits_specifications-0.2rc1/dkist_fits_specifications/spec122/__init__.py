"""
Functions and schemas relating to specification 122, the level 0 FITS files.

The 122 schemas have a singular variant, they are all NAXIS=3.
However, the yaml files still are written with the indices corresponding to NAXIS (``n, i, j``).
These indices are expanded by the loading function so the returned schema always has ``NAXIS = 3``.

The yamls are written with the indices, to reduce duplication and to make it
easier for 214 to use the raw (unprocessed) schemas.
"""
from typing import Any, Dict, List, Tuple, Optional
from pathlib import Path

import copy
import yamale  # type: ignore
import yaml

from dkist_fits_specifications import validation_schema
from dkist_fits_specifications.utils import (expand_naxis, load_raw_spec,
                                             raw_schema_type_hint,
                                             schema_type_hint,)

__all__ = ['load_raw_spec122', 'load_spec122']


base_path = Path(__file__).parent / "schemas"


def preprocess_schema(schema: schema_type_hint) -> schema_type_hint:
    """
    Convert the loaded raw schemas to the 122 schema.

    Parameters
    ----------
    raw_schema
        The loaded version of a single yaml file.

    Returns
    -------
    schema
        The body of a schema, updated as needed from the yaml files.
    """
    header, raw_schemas = schema
    header = copy.deepcopy(header)["spec122"]

    header.pop("section")

    # 122 always has 3 axes, but we encode the yamls independent of the number,
    # to match 214 which might have a variable number of axes.
    schema = expand_naxis(3, raw_schemas)
    for key, key_schema in schema.items():
        updated_schema = {key: {**header, **key_schema}}
        # Rather than put expected in all the files, default it to required
        updated_schema[key]["expected"] = key_schema.get("expected",
                                                key_schema["required"])
        schema.update(updated_schema)
    return schema



def load_raw_spec122(glob: Optional[str] = None) -> Dict[str, raw_schema_type_hint]:
    """
    Load the raw 122 schemas from the yaml files.

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
    return load_raw_spec(base_path, glob)


def load_spec122(glob: Optional[str] = None) -> Dict[str, schema_type_hint]:
    """
    Return the loaded schemas for DKIST Specification 122

    Parameters
    ----------
    glob
        A pattern to use to match a file, without the ``.yml`` file extension.
        Can be a section name like ``'wcs'``.
    """

    raw_schemas = load_raw_spec122(glob=glob)
    schemas = {}
    for schema_name, raw_schema in raw_schemas.items():
        # 122 only uses the second document
        schema = preprocess_schema(raw_schema)
        yamale.validate(validation_schema, [(schema, None)])
        schemas[schema_name] = schema

    return schemas
