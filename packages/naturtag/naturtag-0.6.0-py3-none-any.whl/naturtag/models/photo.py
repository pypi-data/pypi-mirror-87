import attr
from pathlib import Path
from typing import List, Tuple

from naturtag.constants import CC_LICENSES, PHOTO_BASE_URL, PHOTO_INFO_BASE_URL, PHOTO_SIZES
from naturtag.models import BaseModel, kwarg
from naturtag.validation import format_const, format_dimensions


@attr.s
class Photo(BaseModel):
    """A data class containing information about a photo"""

    attribution: str = kwarg
    flags: List = attr.ib(factory=list)
    license_code: str = attr.ib(converter=format_const, default=None)  # Enum
    original_dimensions: Tuple[int, int] = attr.ib(converter=format_dimensions, factory=dict)

    # URLs
    large_url: str = kwarg
    medium_url: str = kwarg
    original_url: str = kwarg
    small_url: str = kwarg
    square_url: str = kwarg
    thumbnail_url: str = kwarg
    url: str = kwarg

    def __attrs_post_init__(self):
        has_url = bool(self.url)
        self.url = f'{PHOTO_INFO_BASE_URL}/{self.id}'
        if not has_url:
            return

        # Get a URL format string to get different photo sizes
        path = Path(self.url.rsplit('?', 1)[0])
        _url_format = f'{PHOTO_BASE_URL}/{self.id}/{{size}}{path.suffix}'

        # Manually construct any URLs missing from the response (only works for iNat-hosted photos)
        for size in PHOTO_SIZES:
            if not getattr(self, f'{size}_url') and 'inaturalist.org' in self.url:
                setattr(self, f'{size}_url', _url_format.format(size=size))
        self.thumbnail_url = self.square_url

        # Point default URL to info page instead of thumbnail

    @property
    def has_cc_license(self) -> bool:
        """Determine if this photo has a Creative Commons license"""
        return self.license_code in CC_LICENSES
