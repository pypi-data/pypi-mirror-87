from extras.plugins import PluginTemplateExtension

from .models import Activity


class SiteDnsCount(PluginTemplateExtension):
    """
    Extend the DCIM site template to include content from this plugin. Specifically,
    we render the animal_count.html template with some additional context to embed
    the current number of animals on the right side of the page.
    """
    model = 'dcim.site'

    def right_page(self):
        return self.render('conectividadeapp/inc/conectividadeapp_count.html', extra_context={
            're_count': Activity.objects.count(),
        })


# PluginTemplateExtension subclasses must be packaged into an iterable named
# template_extensions to be imported by NetBox.
template_extensions = [SiteDnsCount]
