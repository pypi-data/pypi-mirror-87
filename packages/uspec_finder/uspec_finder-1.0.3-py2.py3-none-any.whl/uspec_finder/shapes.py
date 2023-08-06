from ginga.util import wcs
from ginga.canvas.types.all import Polygon


class CCDWin(Polygon):
    def __init__(self, ra_ll_deg, dec_ll_deg, xs, ys,
                 image, **params):
        """
        Shape for drawing ccd window

        Parameters
        ----------
        ra_ll_deg : float
            lower left coordinate in ra (deg)
        dec_ll_deg : float
            lower left y coord in dec (deg)
        xs : float
            x size in degrees
        ys : float
            y size in degrees
        image : `~ginga.AstroImage`
            image to plot Window on
        """
        points_wcs = (
            (ra_ll_deg, dec_ll_deg),
            wcs.add_offset_radec(ra_ll_deg, dec_ll_deg, xs, 0.0),
            wcs.add_offset_radec(ra_ll_deg, dec_ll_deg, xs, ys),
            wcs.add_offset_radec(ra_ll_deg, dec_ll_deg, 0.0, ys)
        )
        self.points = [image.radectopix(ra, dec) for (ra, dec) in points_wcs]
        super(CCDWin, self).__init__(self.points, **params)
        self.name = params.pop('name', 'window')
