from __future__ import division

import io
import unittest

from svgelements import *


class TestParser(unittest.TestCase):

    def test_svg_examples(self):
        """Examples from the SVG spec"""
        path1 = Path('M 100 100 L 300 100 L 200 300 z')
        self.assertEqual(path1, Path(Move(100 + 100j),
                                     Line(100 + 100j, 300 + 100j),
                                     Line(300 + 100j, 200 + 300j),
                                     Close(200 + 300j, 100 + 100j)))  # CHANGED. Closed object
        self.assertTrue(path1.closed)

        # for Z command behavior when there is multiple subpaths
        path1 = Path('M 0 0 L 50 20 M 100 100 L 300 100 L 200 300 z')
        self.assertEqual(path1, Path(
            Move(0j),
            Line(0 + 0j, 50 + 20j),
            Move(50 + 20j, 100+100j),  # CHANGED. Move knows start position.
            Line(100 + 100j, 300 + 100j),
            Line(300 + 100j, 200 + 300j),
            Close(200 + 300j, 100 + 100j)))  # CHANGED. Closed object

        path1 = Path('M 100 100 L 200 200')
        path2 = Path('M100 100L200 200')
        self.assertEqual(path1, path2)

        path1 = Path('M 100 200 L 200 100 L -100 -200')
        path2 = Path('M 100 200 L 200 100 -100 -200')
        self.assertEqual(path1, path2)

        path1 = Path("""M100,200 C100,100 250,100 250,200
                              S400,300 400,200""")
        self.assertEqual(path1,
                         Path(Move(100 + 200j),
                              CubicBezier(100 + 200j, 100 + 100j, 250 + 100j, 250 + 200j),
                              CubicBezier(250 + 200j, 250 + 300j, 400 + 300j, 400 + 200j)))

        path1 = Path('M100,200 C100,100 400,100 400,200')
        self.assertEqual(path1,
                         Path(Move(100 + 200j),
                              CubicBezier(100 + 200j, 100 + 100j, 400 + 100j, 400 + 200j)))

        path1 = Path('M100,500 C25,400 475,400 400,500')
        self.assertEqual(path1,
                         Path(Move(100 + 500j),
                              CubicBezier(100 + 500j, 25 + 400j, 475 + 400j, 400 + 500j)))

        path1 = Path('M100,800 C175,700 325,700 400,800')
        self.assertEqual(path1,
                         Path(Move(100+800j),
                              CubicBezier(100 + 800j, 175 + 700j, 325 + 700j, 400 + 800j)))

        path1 = Path('M600,200 C675,100 975,100 900,200')
        self.assertEqual(path1,
                         Path(Move(600 + 200j),
                              CubicBezier(600 + 200j, 675 + 100j, 975 + 100j, 900 + 200j)))

        path1 = Path('M600,500 C600,350 900,650 900,500')
        self.assertEqual(path1,
                         Path(Move(600 + 500j),
                              CubicBezier(600 + 500j, 600 + 350j, 900 + 650j, 900 + 500j)))

        path1 = Path("""M600,800 C625,700 725,700 750,800
                              S875,900 900,800""")
        self.assertEqual(path1,
                         Path(Move(600 + 800j),
                              CubicBezier(600 + 800j, 625 + 700j, 725 + 700j, 750 + 800j),
                              CubicBezier(750 + 800j, 775 + 900j, 875 + 900j, 900 + 800j)))

        path1 = Path('M200,300 Q400,50 600,300 T1000,300')
        self.assertEqual(path1,
                         Path(Move(200 + 300j),
                              QuadraticBezier(200 + 300j, 400 + 50j, 600 + 300j),
                              QuadraticBezier(600 + 300j, 800 + 550j, 1000 + 300j)))

        path1 = Path('M300,200 h-150 a150,150 0 1,0 150,-150 z')
        self.assertEqual(path1,
                         Path(Move(300 + 200j),
                              Line(300 + 200j, 150 + 200j),
                              Arc(150 + 200j, 150 + 150j, 0, 1, 0, 300 + 50j),
                              Close(300 + 50j, 300 + 200j)))   # CHANGED. Closed object

        path1 = Path('M275,175 v-150 a150,150 0 0,0 -150,150 z')
        self.assertEqual(path1,
                         Path(Move(275 + 175j),
                              Line(275 + 175j, 275 + 25j),
                              Arc(275 + 25j, 150 + 150j, 0, 0, 0, 125 + 175j),
                              Close(125 + 175j, 275 + 175j)))   # CHANGED. Closed object

        path1 = Path('M275,175 v-150 a150,150 0 0,0 -150,150 L 275,175 z')
        self.assertEqual(path1,
                         Path(Move(275 + 175j),
                              Line(275 + 175j, 275 + 25j),
                              Arc(275 + 25j, 150 + 150j, 0, 0, 0, 125 + 175j),
                              Line(125 + 175j, 275 + 175j),
                              Close(275 + 175j, 275 + 175j)))   # CHANGED. Closed object

        path1 = Path("""M600,350 l 50,-25
                              a25,25 -30 0,1 50,-25 l 50,-25
                              a25,50 -30 0,1 50,-25 l 50,-25
                              a25,75 -30 0,1 50,-25 l 50,-25
                              a25,100 -30 0,1 50,-25 l 50,-25""")
        self.assertEqual(path1,
                         Path(Move(600 + 350j),
                              Line(600 + 350j, 650 + 325j),
                              Arc(650 + 325j, 25 + 25j, -30, 0, 1, 700 + 300j),
                              Line(700 + 300j, 750 + 275j),
                              Arc(750 + 275j, 25 + 50j, -30, 0, 1, 800 + 250j),
                              Line(800 + 250j, 850 + 225j),
                              Arc(850 + 225j, 25 + 75j, -30, 0, 1, 900 + 200j),
                              Line(900 + 200j, 950 + 175j),
                              Arc(950 + 175j, 25 + 100j, -30, 0, 1, 1000 + 150j),
                              Line(1000 + 150j, 1050 + 125j)))

    def test_others(self):
        # Other paths that need testing:

        # Relative moveto:
        path1 = Path('M 0 0 L 50 20 m 50 80 L 300 100 L 200 300 z')
        self.assertEqual(path1, Path(
            Move(0j),
            Line(0 + 0j, 50 + 20j),
            Move(50 + 20j, 100 + 100j),  # CHANGED. Path saves the start point if it knows it.
            Line(100 + 100j, 300 + 100j),
            Line(300 + 100j, 200 + 300j),
            Close(200 + 300j, 100 + 100j)))  # CHANGED. This is a Close object now.

        # Initial smooth and relative CubicBezier
        path1 = Path("""M100,200 s 150,-100 150,0""")
        self.assertEqual(path1,
                         Path(Move(100 + 200j),
                              CubicBezier(100 + 200j, 100 + 200j, 250 + 100j, 250 + 200j)))

        # Initial smooth and relative QuadraticBezier
        path1 = Path("""M100,200 t 150,0""")
        self.assertEqual(path1,
                         Path(Move(100 + 200j),
                              QuadraticBezier(100 + 200j, 100 + 200j, 250 + 200j)))

        # Relative QuadraticBezier
        path1 = Path("""M100,200 q 0,0 150,0""")
        self.assertEqual(path1,
                         Path(Move(100 + 200j),
                              QuadraticBezier(100 + 200j, 100 + 200j, 250 + 200j)))

    def test_negative(self):
        """You don't need spaces before a minus-sign"""
        path1 = Path('M100,200c10-5,20-10,30-20')
        path2 = Path('M 100 200 c 10 -5 20 -10 30 -20')
        self.assertEqual(path1, path2)

    def test_numbers(self):
        """Exponents and other number format cases"""
        # It can be e or E, the plus is optional, and a minimum of +/-3.4e38 must be supported.
        path1 = Path('M-3.4e38 3.4E+38L-3.4E-38,3.4e-38')
        path2 = Path(Move(-3.4e+38 +  3.4e+38j), Line(-3.4e+38 + 3.4e+38j, -3.4e-38 + 3.4e-38j))
        self.assertEqual(path1, path2)

    def test_errors(self):
        self.assertRaises(ValueError, Path, 'M 100 100 L 200 200 Z 100 200')

    def test_non_path(self):
        # It's possible in SVG to create paths that has zero length,
        # we need to handle that.

        path = Path("M10.236,100.184")
        self.assertEqual(path.d(), 'M 10.236,100.184')

    def test_issue_47(self):
        arc_path_declared = Path(Move(0 + 25j), Arc(0 + 25j, 25 + 25j, 0.0, 0, 0, 0 - 25j))
        arc_path_parsed = Path('M 0 25 A25,25 0.0 0 0 0,-25')
        arc_path_parsed_scaled = Path('M 0 25 A1,1 0.0 0 0 0,-25')
        self.assertEqual(arc_path_declared, arc_path_parsed)
        self.assertEqual(arc_path_parsed_scaled, arc_path_declared)

    def test_svg_parse(self):
        s = io.StringIO('<svg><path d="M0,0 L1,0 z"/></svg>')
        svg = SVG.parse(s)
        for e in svg.elements():
            if isinstance(e, Path):
                self.assertEqual(e, "M0,0 L1,0 z")

    def test_svg_parse_group(self):
        s = io.StringIO('<svg><g transform="scale(10,10)"><path d="M0,0 L1,0 z"/></g></svg>')
        svg = SVG.parse(s)
        for e in svg.elements():
            if isinstance(e, Path):
                self.assertEqual(e, "M0,0 L10,0 z")

    def test_svg_parse_group_2(self):
        s = io.StringIO('<svg><g><path d="M0,0 L1,0 z"/><path d="M0,0 L1,0 z"/></g></svg>')
        svg = SVG.parse(s)
        for e in svg.elements():
            if isinstance(e, Path):
                self.assertEqual(e, "M0,0 L1,0 z")

    def test_solo_move(self):
        move_only = Path("M0,0")
        self.assertEqual(move_only.point(0), 0 + 0j)
        self.assertEqual(move_only.point(0.5), 0 + 0j)
        self.assertEqual(move_only.point(1), 0 + 0j)
        self.assertEqual(move_only.length(), 0)

        move_onlyz = Path("M0,0Z")
        self.assertEqual(move_onlyz.point(0), 0 + 0j)
        self.assertEqual(move_onlyz.point(0.5), 0 + 0j)
        self.assertEqual(move_onlyz.point(1), 0 + 0j)
        self.assertEqual(move_onlyz.length(), 0)

        move_2_places = Path("M0,0M1,1")
        self.assertEqual(move_2_places.point(0), 0 + 0j)
        self.assertEqual(move_2_places.point(0.49), 0 + 0j)
        self.assertEqual(move_2_places.point(0.51), 1 + 1j)
        self.assertEqual(move_2_places.point(1), 1 + 1j)
        self.assertEqual(move_2_places.length(), 0)


class TestParseDisplay(unittest.TestCase):
    """
    Tests for the parsing of displayed objects within an svg for conforming to the spec. Anything with a viewbox that
    has a zero width or zero height is not rendered. Any svg with a zero height or zero width is not rendered. Anything
    with a display="none" is not rendered whether this property comes from class, style, or direct attribute. Items with
    visibility="hidden" are rendered and returned but should be hidden by the end user.
    """

    def test_svgfile(self):
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" '
                        'xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
                        '<g style="display:inline">\n'
                        '<line x1="0.0" x2="0.0" y1="0.0" y2="100"/>\n'
                        '</g>\n'
                        '</svg>')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertTrue(isinstance(q[-1], SimpleLine))

    def test_svgfile_0_width(self):
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg width="0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" '
                        'xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
                        '<g style="display:inline">\n'
                        '<line x1="0.0" x2="0.0" y1="0.0" y2="100"/>\n'
                        '</g>\n'
                        '</svg>')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertFalse(isinstance(q[-1], SimpleLine))

    def test_svgfile_0_height(self):
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg width="3.0cm" height="0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" '
                        'xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
                        '<g style="display:inline">\n'
                        '<line x1="0.0" x2="0.0" y1="0.0" y2="100"/>\n'
                        '</g>\n'
                        '</svg>')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertFalse(isinstance(q[-1], SimpleLine))

    def test_svgfile_viewbox_0_height(self):
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg width="3.0cm" height="3.0cm" viewBox="0 0 100 0" xmlns="http://www.w3.org/2000/svg" '
                        'xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
                        '<g style="display:inline">\n'
                        '<line x1="0.0" x2="0.0" y1="0.0" y2="100"/>\n'
                        '</g>\n'
                        '</svg>')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertFalse(isinstance(q[-1], SimpleLine))

    def test_svgfile_viewbox_0_width(self):
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg width="3.0cm" height="3.0cm" viewBox="0 0 0 100" xmlns="http://www.w3.org/2000/svg" '
                        'xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
                        '<g style="display:inline">\n'
                        '<line x1="0.0" x2="0.0" y1="0.0" y2="100"/>\n'
                        '</g>\n'
                        '</svg>')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertFalse(isinstance(q[-1], SimpleLine))

    def test_svgfile_display_none_inline(self):
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" '
                        'xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
                        '<g style="display:none">\n'
                        '<line x1="0.0" x2="0.0" y1="0.0" y2="100"/>\n'
                        '</g>\n'
                        '</svg>')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertFalse(isinstance(q[-1], SimpleLine))

    def test_svgfile_display_none_attribute(self):
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" '
                        'xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
                        '<g display="none">\n'
                        '<line x1="0.0" x2="0.0" y1="0.0" y2="100"/>\n'
                        '</g>\n'
                        '</svg>')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertFalse(isinstance(q[-1], SimpleLine))

    def test_svgfile_display_mixed(self):
        """
        All children of a display="none" are excluded, even if they override that display.
        """
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" '
                        'xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
                        '<g display="none">\n'
                        '<line display="show" x1="0.0" x2="0.0" y1="0.0" y2="100"/>\n'
                        '</g>\n'
                        '</svg>')
        m = SVG.parse(q)
        q = list(m.elements())
        print(q)
        self.assertFalse(isinstance(q[-1], SimpleLine))


    def test_svgfile_display_none_class(self):
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
                        '<style type="text/css">\n'
                        '.hide { \n'
                        '     display:none;\n'
                        '}\n'
                        '</style>\n'
                        '<g class="hide">\n'
                        '<line x1="0.0" x2="0.0" y1="0.0" y2="100"/>\n'
                        '</g>\n'
                        '</svg>\n')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertFalse(isinstance(q[-1], SimpleLine))

    def test_svgfile_visibility_hidden(self):
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" '
                        'xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
                        '<g style="visibility:hidden">\n'
                        '<line x1="0.0" x2="0.0" y1="0.0" y2="100"/>\n'
                        '</g>\n'
                        '</svg>')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertTrue(isinstance(q[-1], SimpleLine))  # Hidden elements still exist.