from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineEntityElementHandler,
)


def footnote_entity_decorator(props):
    return DOM.create_element(
        "span",
        {"class": "footnote", "data-footnote": props["footnote"]},
        props["children"],
    )


class FootnoteEntityElementHandler(InlineEntityElementHandler):
    mutability = "IMMUTABLE"

    def get_attribute_data(self, attrs):
        """
        Take the ``stock`` value from the ``data-stock`` HTML attribute.
        """
        return {"footnote": attrs["data-footnote"]}
