import os

import pandas as pd
from IPython.display import display

from ...utils import PluginRegistry
from ..display import Displayable
from ..display import default_renderer_base, json_renderer_base
from ..display import SpecType, MimeBundleType, RendererType



#==============================================================================
# Vega 2 renderer logic
#==============================================================================


# The MIME type for Vega 2 releases.
VEGA_MIME_TYPE = 'application/vnd.vega.v2+json'  # type: str

# The entry point group that can be used by other packages to declare other
# renderers that will be auto-detected. Explicit registration is also
# allowed by the PluginRegistery API.
ENTRY_POINT_GROUP = 'altair.vega.v2.renderer'  # type: str

# The display message when rendering fails
DEFAULT_DISPLAY = """\
<Vega 2 object>

If you see this message, it means the renderer has not been properly enabled
for the frontend that you are using. For more information, see
https://altair-viz.github.io/user_guide/display.html
"""

renderers = PluginRegistry[RendererType](entry_point_group=ENTRY_POINT_GROUP)


here = os.path.dirname(os.path.realpath(__file__))


def default_renderer(spec, metadata):
    return default_renderer_base(spec, mime_type=VEGA_MIME_TYPE,
                                 str_repr=DEFAULT_DISPLAY, metadata=metadata)


def json_renderer(spec, metadata):
    return json_renderer_base(spec, str_repr=DEFAULT_DISPLAY, metadata=metadata)


renderers.register('default', default_renderer)
renderers.register('jupyterlab', default_renderer)
renderers.register('json', json_renderer)
renderers.enable('default')


class Vega(Displayable):
    """An IPython/Jupyter display class for rendering Vega 2."""

    renderers = renderers
    schema_path = os.path.join(here, 'schema', 'vega-schema.json')


def vega(spec: dict, validate=True):
    """Render and optionally validate a Vega 2 spec.

    This will use the currently enabled renderer to render the spec.

    Parameters
    ==========
    spec: dict
        A fully compliant VegaLite 1 spec, with the data portion fully processed.
    validate: bool
        Should the spec be validated against the Vega 2 schema?
    """
    display(Vega(spec, validate=validate))
