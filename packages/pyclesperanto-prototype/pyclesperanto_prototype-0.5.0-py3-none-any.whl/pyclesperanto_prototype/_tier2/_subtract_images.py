from .._tier0 import plugin_function
from .._tier0 import Image
from .._tier1 import add_images_weighted

@plugin_function
def subtract_images(subtrahend : Image, minuend : Image, destination : Image = None):
    """Subtracts one image X from another image Y pixel wise.
    
    <pre>f(x, y) = x - y</pre> 
    
    Parameters
    ----------
    subtrahend : Image
    minuend : Image
    destination : Image
    
    Returns
    -------
    destination
    
    References
    ----------
    .. [1] https://clij.github.io/clij2-docs/reference_subtractImages
    """
    return add_images_weighted(subtrahend, minuend, destination, 1, -1)
