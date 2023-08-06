from typing import Union, List

from anacreonlib.types.response_datatypes import Trait
from anacreonlib.types.scenario_info_datatypes import ScenarioInfoElement


def trait_inherits_from_trait(child_trait: Union[Trait, int], parent_trait: Union[Trait, int],
                              scninfo: List[ScenarioInfoElement]):
    """
    Checks if trait_a inherits from trait_b i.e
    trait_a extends trait_b
    trait_a inheritsFrom trait_b
    :param child_trait:
    :param parent_trait:
    :return:
    """
    try:
        childs_parent_list = next(trait.inherit_from for trait in scninfo if trait.id == child_trait or trait.id == child_trait.trait_id)
        if childs_parent_list is None:
            return False

        return parent_trait in childs_parent_list or any(
            trait_inherits_from_trait(trait, parent_trait, scninfo) for trait in childs_parent_list)
    except StopIteration as e:
        raise ValueError("child trait was not found in scenario info") from e
    except KeyError:
        return False
