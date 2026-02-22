from django import template

register = template.Library()


@register.filter(name='lifespan')
def lifespan(artist):
    """Returns the artist's lifespan as a formatted string."""
    return artist.get_lifespan()


@register.filter(name='artwork_count')
def artwork_count(artist):
    """Returns how many artworks are linked to this artist."""
    return artist.get_artwork_count()


@register.filter 
def nationality_badge(nationality):
    """Renders a Bootstrap badge colour based on nationality."""
    colours = {
        'American': 'primary',
        'British': 'danger',
        'French': 'info',
        'German': 'warning',
        'Italian': 'success',
        'Spanish': 'secondary',
        'Dutch': 'warning',
        'Japanese': 'danger',
        'Chinese': 'danger',
        'Russian': 'dark',
    }
    return colours.get(nationality, 'secondary')
