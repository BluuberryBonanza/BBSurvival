"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Dict, Any, TypeVar, Type

BBJSONSerializableType = TypeVar('BBJSONSerializableType', bound="BBJSONSerializable")


class BBJSONSerializable:
    """BBJSONSerializable()

    Inherit this class to indicate a class is serializable into JSON.

    """

    def serialize(self: BBJSONSerializableType) -> Dict[str, Any]:
        """serialize()

        Serialize the class into a format JSON can parse.

        :return: A dictionary of data that can be output by JSON.
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError()

    @classmethod
    def deserialize(cls: Type[BBJSONSerializableType], serialized_data: Dict[str, Any]) -> 'BBJSONSerializableType':
        """deserialize(serialized_data)

        Deserialize data into a BBJSONSerializable instance.

        :param serialized_data: JSON serialized data.
        :type serialized_data: Dict[str, Any]
        :return: An instance of this class.
        :rtype: BBJSONSerializable
        """
        raise NotImplementedError()
