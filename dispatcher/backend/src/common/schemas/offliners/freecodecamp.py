from marshmallow import fields, validate

from common.schemas import LongString, SerializableSchema, String, StringEnum
from common.schemas.fields import (
    validate_output,
    validate_zim_description,
    validate_zim_filename,
    validate_zim_longdescription,
)

FCC_LANG_MAP = {
    "ara": "arabic",
    "cmn": "chinese",
    "lzh": "chinese-traditional",
    "eng": "english",
    "spa": "espanol",
    "deu": "german",
    "ita": "italian",
    "jpn": "japanese",
    "por": "portuguese",
    "ukr": "ukranian",
}


class FreeCodeCampFlagsSchema(SerializableSchema):
    class Meta:
        ordered = True

    course = String(
        metadata={
            "label": "Course(s)",
            "description": "Course or course list (separated by commas)",
        },
        required=True,
    )

    language = StringEnum(
        metadata={
            "label": "Language",
            "description": "Language of zim file and curriculum. One of "
            + ", ".join([f"'{key}' ({desc})" for key, desc in FCC_LANG_MAP.items()])
            + ".",
        },
        required=True,
        validate=validate.OneOf(list(FCC_LANG_MAP.keys())),
    )

    name = String(
        metadata={
            "label": "Name",
            "description": "ZIM name",
        },
        required=True,
    )

    title = String(
        metadata={
            "label": "Title",
            "description": "ZIM title",
        },
        required=True,
    )

    description = String(
        metadata={
            "label": "Description",
            "description": "Description for your ZIM",
        },
        required=True,
        validate=validate_zim_description,
    )

    long_description = LongString(
        metadata={
            "label": "Long description",
            "description": "Optional long description for your ZIM",
        },
        validate=validate_zim_longdescription,
        data_key="long-description",
    )

    creator = String(
        metadata={
            "label": "Content Creator",
            "description": "Name of content creator. “freeCodeCamp” otherwise",
        }
    )

    publisher = String(
        metadata={
            "label": "Publisher",
            "description": "Custom publisher name (ZIM metadata). “OpenZIM” otherwise",
        }
    )

    debug = fields.Boolean(
        truthy=[True],
        falsy=[False],
        metadata={"label": "Debug", "description": "Enable verbose output"},
    )

    output_dir = String(
        metadata={
            "label": "Output folder",
            "placeholder": "/output",
            "description": "Output folder for ZIM file(s). Leave it as `/output`",
        },
        load_default="/output",
        dump_default="/output",
        data_key="output-dir",
        validate=validate_output,
    )

    zim_file = String(
        metadata={
            "label": "ZIM filename",
            "description": "ZIM file name (based on --name if not provided). "
            "Include {period} to insert date period dynamically",
        },
        data_key="zim-file",
        validate=validate_zim_filename,
    )
