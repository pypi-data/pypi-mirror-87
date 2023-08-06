from collections import ChainMap, OrderedDict
from logging import getLogger
from pathlib import Path
from shutil import copy as shutil_copy
from typing import Any, Dict, Optional

from yaml import safe_load as yaml_safe_load

from invoicez.exceptions import InvoicezException
from invoicez.paths import Paths


_logger = getLogger(__name__)


def get_config(paths: Paths) -> Dict[str, Any]:
    return OrderedDict(
        (k, v)
        for k, v in sorted(
            ChainMap(
                *[
                    _get_or_create_config(f, p)
                    for f, p in [
                        (paths.company_config, paths.template_company_config),
                        (paths.global_config, None),
                    ]
                ],
            ).items()
        )
    )


def _get_or_create_config(path: Path, template_path: Optional[Path]) -> Dict[str, Any]:
    if not path.is_file():
        if template_path:
            if template_path.is_file():
                shutil_copy(str(template_path), str(path), follow_symlinks=True)
                raise InvoicezException(
                    f"{path} was not found, copied {template_path} there. Please edit "
                    "it."
                )
            else:
                raise InvoicezException(
                    f"Neither {path} nor {template_path} were found. "
                    "Please create both."
                )
        else:
            raise InvoicezException(f"{path} was not found. Please create it.")
    with open(path, "r", encoding="utf8") as fh:
        return yaml_safe_load(fh)
