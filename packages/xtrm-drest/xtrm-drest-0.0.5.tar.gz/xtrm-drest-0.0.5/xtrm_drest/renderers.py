"""This module contains custom renderer classes."""
from rest_framework.renderers import BrowsableAPIRenderer


class DynamicBrowsableAPIRenderer(BrowsableAPIRenderer):
    """Renderer class that adds directory support to the Browsable API."""

    template = 'xtrm_drest/api.html'

    def get_context(self, data, media_type, context):
        from xtrm_drest.routers import get_directory

        context = super(DynamicBrowsableAPIRenderer, self).get_context(
            data,
            media_type,
            context
        )
        request = context['request']
        context['directory'] = get_directory(request)
        return context
