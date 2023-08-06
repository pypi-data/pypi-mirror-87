from typing import Any, Dict, List, Union

import attr

from ..models.aa_sequence import AaSequence
from ..models.custom_entity import CustomEntity
from ..models.dna_sequence import DnaSequence
from ..models.mixture import Mixture
from ..models.oligo import Oligo


@attr.s(auto_attribs=True)
class RegisteredEntitiesList:
    """  """

    entities: List[Union[DnaSequence, CustomEntity, AaSequence, Mixture, Oligo]]

    def to_dict(self) -> Dict[str, Any]:
        entities = []
        for entities_item_data in self.entities:
            if isinstance(entities_item_data, DnaSequence):
                entities_item = entities_item_data.to_dict()

            elif isinstance(entities_item_data, CustomEntity):
                entities_item = entities_item_data.to_dict()

            elif isinstance(entities_item_data, AaSequence):
                entities_item = entities_item_data.to_dict()

            elif isinstance(entities_item_data, Mixture):
                entities_item = entities_item_data.to_dict()

            else:
                entities_item = entities_item_data.to_dict()

            entities.append(entities_item)

        properties: Dict[str, Any] = dict()

        properties["entities"] = entities
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RegisteredEntitiesList":
        entities = []
        for entities_item_data in d["entities"]:

            def _parse_entities_item(
                data: Dict[str, Any]
            ) -> Union[DnaSequence, CustomEntity, AaSequence, Mixture, Oligo]:
                entities_item: Union[DnaSequence, CustomEntity, AaSequence, Mixture, Oligo]
                try:
                    entities_item = DnaSequence.from_dict(entities_item_data)

                    return entities_item
                except:  # noqa: E722
                    pass
                try:
                    entities_item = CustomEntity.from_dict(entities_item_data)

                    return entities_item
                except:  # noqa: E722
                    pass
                try:
                    entities_item = AaSequence.from_dict(entities_item_data)

                    return entities_item
                except:  # noqa: E722
                    pass
                try:
                    entities_item = Mixture.from_dict(entities_item_data)

                    return entities_item
                except:  # noqa: E722
                    pass
                entities_item = Oligo.from_dict(entities_item_data)

                return entities_item

            entities_item = _parse_entities_item(entities_item_data)

            entities.append(entities_item)

        return RegisteredEntitiesList(
            entities=entities,
        )
