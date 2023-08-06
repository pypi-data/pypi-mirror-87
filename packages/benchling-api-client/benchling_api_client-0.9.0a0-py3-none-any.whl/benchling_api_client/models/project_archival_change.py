from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class ProjectArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of projects along with any IDs of project contents that were unarchived."""

    project_ids: Optional[List[str]] = cast(None, UNSET)
    folder_ids: Optional[List[str]] = cast(None, UNSET)
    entry_ids: Optional[List[str]] = cast(None, UNSET)
    protocol_ids: Optional[List[str]] = cast(None, UNSET)
    dna_sequence_ids: Optional[List[str]] = cast(None, UNSET)
    aa_sequence_ids: Optional[List[str]] = cast(None, UNSET)
    custom_entity_ids: Optional[List[str]] = cast(None, UNSET)
    mixture_ids: Optional[List[str]] = cast(None, UNSET)
    oligo_ids: Optional[List[str]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.project_ids is None:
            project_ids = None
        elif self.project_ids is UNSET:
            project_ids = UNSET
        else:
            project_ids = self.project_ids

        if self.folder_ids is None:
            folder_ids = None
        elif self.folder_ids is UNSET:
            folder_ids = UNSET
        else:
            folder_ids = self.folder_ids

        if self.entry_ids is None:
            entry_ids = None
        elif self.entry_ids is UNSET:
            entry_ids = UNSET
        else:
            entry_ids = self.entry_ids

        if self.protocol_ids is None:
            protocol_ids = None
        elif self.protocol_ids is UNSET:
            protocol_ids = UNSET
        else:
            protocol_ids = self.protocol_ids

        if self.dna_sequence_ids is None:
            dna_sequence_ids = None
        elif self.dna_sequence_ids is UNSET:
            dna_sequence_ids = UNSET
        else:
            dna_sequence_ids = self.dna_sequence_ids

        if self.aa_sequence_ids is None:
            aa_sequence_ids = None
        elif self.aa_sequence_ids is UNSET:
            aa_sequence_ids = UNSET
        else:
            aa_sequence_ids = self.aa_sequence_ids

        if self.custom_entity_ids is None:
            custom_entity_ids = None
        elif self.custom_entity_ids is UNSET:
            custom_entity_ids = UNSET
        else:
            custom_entity_ids = self.custom_entity_ids

        if self.mixture_ids is None:
            mixture_ids = None
        elif self.mixture_ids is UNSET:
            mixture_ids = UNSET
        else:
            mixture_ids = self.mixture_ids

        if self.oligo_ids is None:
            oligo_ids = None
        elif self.oligo_ids is UNSET:
            oligo_ids = UNSET
        else:
            oligo_ids = self.oligo_ids

        properties: Dict[str, Any] = dict()

        if project_ids is not UNSET:
            properties["projectIds"] = project_ids
        if folder_ids is not UNSET:
            properties["folderIds"] = folder_ids
        if entry_ids is not UNSET:
            properties["entryIds"] = entry_ids
        if protocol_ids is not UNSET:
            properties["protocolIds"] = protocol_ids
        if dna_sequence_ids is not UNSET:
            properties["dnaSequenceIds"] = dna_sequence_ids
        if aa_sequence_ids is not UNSET:
            properties["aaSequenceIds"] = aa_sequence_ids
        if custom_entity_ids is not UNSET:
            properties["customEntityIds"] = custom_entity_ids
        if mixture_ids is not UNSET:
            properties["mixtureIds"] = mixture_ids
        if oligo_ids is not UNSET:
            properties["oligoIds"] = oligo_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ProjectArchivalChange":
        project_ids = d.get("projectIds")

        folder_ids = d.get("folderIds")

        entry_ids = d.get("entryIds")

        protocol_ids = d.get("protocolIds")

        dna_sequence_ids = d.get("dnaSequenceIds")

        aa_sequence_ids = d.get("aaSequenceIds")

        custom_entity_ids = d.get("customEntityIds")

        mixture_ids = d.get("mixtureIds")

        oligo_ids = d.get("oligoIds")

        return ProjectArchivalChange(
            project_ids=project_ids,
            folder_ids=folder_ids,
            entry_ids=entry_ids,
            protocol_ids=protocol_ids,
            dna_sequence_ids=dna_sequence_ids,
            aa_sequence_ids=aa_sequence_ids,
            custom_entity_ids=custom_entity_ids,
            mixture_ids=mixture_ids,
            oligo_ids=oligo_ids,
        )
