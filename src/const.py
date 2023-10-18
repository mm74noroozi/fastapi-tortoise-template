from enum import Enum


class OrderStatusEnum(Enum):
    REGISTERED = 1
    PAID = 2
    DELIVERED = 3
    FINISHED = 4
    CANCELED = 5
