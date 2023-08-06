from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class AutomationInputGenerator:
    """  """

    api_url: Optional[str] = cast(None, UNSET)
    assay_run_id: Optional[str] = cast(None, UNSET)
    automation_file_config: Optional[Dict[Any, Any]] = cast(None, UNSET)
    file: Optional[Dict[Any, Any]] = cast(None, UNSET)
    id: Optional[str] = cast(None, UNSET)
    status: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        api_url = self.api_url
        assay_run_id = self.assay_run_id
        if self.automation_file_config is UNSET:
            automation_file_config = UNSET
        else:
            automation_file_config = self.automation_file_config if self.automation_file_config else None

        if self.file is UNSET:
            file = UNSET
        else:
            file = self.file if self.file else None

        id = self.id
        status = self.status

        properties: Dict[str, Any] = dict()

        if api_url is not UNSET:
            properties["apiURL"] = api_url
        if assay_run_id is not UNSET:
            properties["assayRunId"] = assay_run_id
        if automation_file_config is not UNSET:
            properties["automationFileConfig"] = automation_file_config
        if file is not UNSET:
            properties["file"] = file
        if id is not UNSET:
            properties["id"] = id
        if status is not UNSET:
            properties["status"] = status
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AutomationInputGenerator":
        api_url = d.get("apiURL")

        assay_run_id = d.get("assayRunId")

        automation_file_config = None
        if d.get("automationFileConfig") is not None:
            automation_file_config = d.get("automationFileConfig")

        file = None
        if d.get("file") is not None:
            file = d.get("file")

        id = d.get("id")

        status = d.get("status")

        return AutomationInputGenerator(
            api_url=api_url,
            assay_run_id=assay_run_id,
            automation_file_config=automation_file_config,
            file=file,
            id=id,
            status=status,
        )
