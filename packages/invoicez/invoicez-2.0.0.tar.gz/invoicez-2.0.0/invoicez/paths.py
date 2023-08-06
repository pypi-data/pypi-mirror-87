from logging import getLogger
from pathlib import Path
from typing import Optional

from git import Repo
from git.exc import InvalidGitRepositoryError

from invoicez.exceptions import InvoicezException


_logger = getLogger(__name__)


class Paths:
    def __init__(self, working_dir: Path, check_depth: bool = True) -> None:
        self.working_dir = working_dir.resolve()
        self.build_dir = self.working_dir / "build"
        self.pdf_dir = self.working_dir / "pdf"
        self.assets_dir = self.git_dir / "assets"
        self.templates_dir = self.git_dir / "templates"
        self.yml_templates_dir = self.templates_dir / "yml"
        self.template_company_config = self.yml_templates_dir / "company-config.yml"
        self.template_invoice = self.yml_templates_dir / "invoice.yml"
        self.jinja2_dir = self.templates_dir / "jinja2"
        self.global_config = self.git_dir / "global-config.yml"
        self.company_config = (
            self.git_dir
            / self.working_dir.relative_to(self.git_dir).parts[0]
            / "company-config.yml"
        )

        if check_depth and not self.working_dir.relative_to(self.git_dir).match("*"):
            raise InvoicezException(
                f"Not deep enough from root {self.git_dir}. "
                "Please follow the directory hierarchy root > company and "
                "invoke this tool from the company directory."
            )

    @property
    def git_dir(self) -> Optional[Path]:
        if not hasattr(self, "_git_dir"):
            try:
                repository = Repo(str(self.working_dir), search_parent_directories=True)
            except InvalidGitRepositoryError as e:
                raise InvoicezException(
                    "Could not find the path of the current git working directory. "
                    "Are you in one?"
                ) from e
            self._git_dir = Path(repository.git.rev_parse("--show-toplevel")).resolve()
        return self._git_dir
