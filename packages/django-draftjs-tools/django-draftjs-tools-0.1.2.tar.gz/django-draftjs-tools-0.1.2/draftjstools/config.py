
from django.conf import settings
from draftjs_exporter.constants import ENTITY_TYPES
from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP


########################
# DRAFTJS RENDER CONFIG

# Entity Decorator Setup
ENTITY_MAP_OVERRIDES = getattr(settings, "DRAFTJS_ENTITY_MAP_OVERRIDES", None)

ENTITY_MAP = {ENTITY_TYPES.LINK: "link", ENTITY_TYPES.IMAGE: "image", ENTITY_TYPES.HORIZONTAL_RULE: "hr"}

if ENTITY_MAP_OVERRIDES:
    DRAFTJS_ENTITY_MAP = dict(ENTITY_MAP, **ENTITY_MAP_OVERRIDES)
else:
    DRAFTJS_ENTITY_MAP = ENTITY_MAP

# Block Map Setup
BLOCK_MAP_OVERRIDES = getattr(settings, "DRAFTJS_BLOCK_MAP_OVERRIDES", None)

if BLOCK_MAP_OVERRIDES:
    DRAFTJS_BLOCK_MAP = dict(BLOCK_MAP, **BLOCK_MAP_OVERRIDES)
else:
    DRAFTJS_BLOCK_MAP = BLOCK_MAP

# Style Map Setup
STYLE_MAP_OVERRIDES = getattr(settings, "DRAFTJS_STYLE_MAP_OVERRIDES", None)

if STYLE_MAP_OVERRIDES:
    DRAFTJS_STYLE_MAP = dict(STYLE_MAP, **STYLE_MAP_OVERRIDES)
else:
    DRAFTJS_STYLE_MAP = STYLE_MAP

DRAFTJS_RENDER_CONFIG = getattr(settings, "DRAFTJS_RENDER_CONFIG", {"entity_decorators": DRAFTJS_ENTITY_MAP, "block_map": DRAFTJS_BLOCK_MAP, "style_map": DRAFTJS_STYLE_MAP})     # Can be overridden wholesale if desired


# Composite Decorator Setup
COMPOSITE_DECORATORS = getattr(settings, "DRAFTJS_COMPOSITE_DECORATORS", None)

if COMPOSITE_DECORATORS:
    DRAFTJS_RENDER_CONFIG['composite_decorators'] = COMPOSITE_DECORATORS


"""
Sample Overides

Though not needed, the contstants from draftjs_exporter use a fixed set of varaibles, so less prone to typos.

---

from draftjs_exporter.constants import BLOCK_TYPES

DRAFTJS_BLOCK_MAP = dict(BLOCK_MAP, **getattr(settings, "DRAFTJS_BLOCK_MAP", {
        BLOCK_TYPES.HEADER_ONE: "h1",
        BLOCK_TYPES.HEADER_TWO: "h2",
        BLOCK_TYPES.HEADER_THREE: "h3",
        BLOCK_TYPES.HEADER_FOUR: "h4",
        BLOCK_TYPES.HEADER_FIVE: "h5",
        BLOCK_TYPES.HEADER_SIX: "h6",
        BLOCK_TYPES.ORDERED_LIST_ITEM:{
            "element": "li",
            "wrapper": "ol",
        },
        BLOCK_TYPES.UNORDERED_LIST_ITEM:{
            "element": "li",
            "wrapper": "ul",
            "wrapper_props":{
                "class": "bullet-list"
            },
        },
        BLOCK_TYPES.UNSTYLED: "div",
        BLOCK_TYPES.CODE: "code",
        BLOCK_TYPES.ATOMIC: "atomic",
        BLOCK_TYPES.BLOCKQUOTE: "blockquote",
    }))

STYLE_MAP = getattr(settings, "DRAFTJS_STYLE_MAP", {"BOLD": "strong", "ITALIC": {"element":"em", "props": {"class":"u-font-italic"}}})
"""
