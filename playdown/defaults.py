from mezzanine.conf import register_setting


register_setting(
    name="PAGEDOWN_SERVER_SIDE_PREVIEW",
    description="Render previews on the server using the same "
                "converter that generates the actual pages.",
    editable=False,
    default=False,
)

register_setting(
    name="PAGEDOWN_MARKDOWN_EXTENSIONS",
    description="A tuple specifying enabled python-markdown extensions.",
    editable=False,
    default=(),
)
