from enum import Enum


class Type12345(str, Enum):
    LINK = "link"
    USER = "user"
    REQUEST = "request"
    ENTRY = "entry"
    STAGE_ENTRY = "stage_entry"
    PROTOCOL = "protocol"
    WORKFLOW = "workflow"
    CUSTOM_ENTITY = "custom_entity"
    AA_SEQUENCE = "aa_sequence"
    DNA_SEQUENCE = "dna_sequence"
    BATCH = "batch"
    BOX = "box"
    CONTAINER = "container"
    LOCATION = "location"
    PLATE = "plate"
