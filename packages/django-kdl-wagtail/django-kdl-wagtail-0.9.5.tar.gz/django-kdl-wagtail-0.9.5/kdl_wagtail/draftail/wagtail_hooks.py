import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.core import hooks

from .rich_text import FootnoteEntityElementHandler, footnote_entity_decorator


@hooks.register("register_rich_text_features")
def register_footnote_feature(features):
    """Register the `footnote` feature, which uses the `FOOTNOTE` Draft.js entity type,
    and is stored as HTML with a `<span>` tag."""
    feature_name = "footnote"
    type_ = "FOOTNOTE"

    control = {"type": type_, "label": "✱", "description": "Footnote"}

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.EntityFeature(
            control, js=["kdl_wagtail_draftail/js/footnote.js"]
        ),
    )

    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            "from_database_format": {
                "span[data-footnote]": FootnoteEntityElementHandler(type_)
            },
            "to_database_format": {
                "entity_decorators": {type_: footnote_entity_decorator}
            },
        },
    )

    features.default_features.append(feature_name)
