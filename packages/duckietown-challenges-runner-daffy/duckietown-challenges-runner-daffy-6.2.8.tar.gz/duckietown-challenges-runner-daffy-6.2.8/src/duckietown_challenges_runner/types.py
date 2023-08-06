from typing import NewType

ContainerName = NewType("ContainerName", str)
ContainerID = NewType("ContainerID", str)

from duckietown_challenges import ServiceName

_ = ServiceName
