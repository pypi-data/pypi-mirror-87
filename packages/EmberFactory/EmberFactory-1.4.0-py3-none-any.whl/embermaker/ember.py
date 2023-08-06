# -*- coding: utf-8 -*-
""" 
The ember module contains the basis elements to build IPCC-style 'burning ember diagrams'
Copyright (C) 2020  philippe.marbaix@uclouvain.be
"""

import numpy as np
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors as col
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from embermaker import helpers as hlp
from embermaker.helpers import norm, isempty

sortlist = []  # Default sortlist is empty
sortrlev = -1E6  # Default sortrlev means undefined
sorthazl = -1E6  # Default sorthazl means undefined


def skeygroup(be):
    """
    Used for sorting embers by group. If sortlist is defined, tries to use the order defined in this list.

    :param be: an ember object
    :return: sort key
    """
    global sortlist
    if sortlist:
        try:
            pos = sortlist.index(be.group.lower())
        except ValueError:
            pos = -1
    else:  # sortlist is not defined: will sort by alphabetic order
        pos = be.group
    # hlp.addlogmes("Sort key for group:" + str(be.group.lower()) + "->" + str(pos))
    return pos


def skeyname(be):
    """
    Used for sorting embers by name. If sortlist is defined, tries to use the order defined in this list.

    :param be: an ember object
    :return: sort key
    """
    global sortlist
    if sortlist:
        try:
            pos = sortlist.index(be.name.lower())
        except ValueError:
            pos = -1
    else:  # sortlist is not defined: will sort by alphabetic order
        pos = be.name
    # hlp.addlogmes("Sort key for name:" + str(be.name.lower()) + "->" + str(pos))
    return pos


def skeyrisk(be):
    """
    :param be: an ember object
    :return: sort key
    """
    global sortrlev, sorthazl
    try:
        if sortrlev > -1E3:
            if be.risk[-1] > sortrlev:
                pos = np.interp(sortrlev, be.risk, be.hazl)
            else:
                # Todo: think twice, improve; idea is to keep a minimal sorting when the sort criteria cannot work...
                pos = 5.0 + np.interp(sortrlev / 2.0, be.risk, be.hazl)
        elif sorthazl > -1E3:
            if be.hazl[-1] > sorthazl:
                pos = np.interp(sorthazl, be.hazl, be.risk)
            else:
                pos = be.risk[-1]
        else:
            raise Exception("Skeyrisk cannot generate a sort key because no sort level was provided.")
    except ValueError:
        pos = 999
    if be.getmeta("inclusion_level") == 0:  # Ignore embers with Inclusion Level = 0; could be improved in the future.
        pos = -1  # ignore ember
    return pos


def selecsort(lbes, fkey, reverse=False):
    """
    Sorts embers in lbes but ignores those absent from sortlist (=> fkey(be) = -1 above)
    (no ready-made option to do that?).

    :param lbes: a list of BEs
    :param fkey: the sort-key function
    :param reverse: reverses sorting order
    :return: sorted and filtered list of BEs
    """
    global sortlist, sortrlev
    # Filtering
    if sortlist is not None or sortrlev is not None or sorthazl is not None:
        # Filtering occurs only if a sort criteria is defined (no sorting => no filtering)
        lbes = [be for be in lbes if fkey(be) != -1]
    # Sorting
    lbes.sort(key=fkey, reverse=reverse)
    return lbes


def cbyinterp(rlev, csys, cdefs):
    """
    Provides a color by interpolating between the defined color levels associated to risk levels.

    :param rlev: the risk level for which a color is requested
    :param csys: the name of the color system (currently CMYK or RGB)
    :param cdefs: the definition of the colors associated to risk levels, such that
         - cdefs[0] : a risk level index (1D numpy array of risk indexes)
         - cdefs[1:]: the color densities for each value of the risk index :
                    (1D numpy array of color densities for each risk index)
    :return: the color associated to the risk level
    """
    cvals = [np.interp(rlev, cdefs[0], cdefs[1 + i]) for i in range(len(csys))]
    if csys == 'CMYK':
        c, m, y, k = cvals
        thecol = col.CMYKColor(c, m, y, k)
    elif csys == 'RGB':
        r, g, b = cvals
        thecol = col.Color(r, g, b, alpha=1.0)
    else:
        raise Exception("Undefined color system")
    return thecol


class Ember(object):
    """ An ember is one set of data in a "burning embers" diagram.
        It contains hazard levels and associated risk levels, as well as the 'draw' method to plot itself.
    """

    def __init__(self):
        """
        Initializes an ember, by creating standard attributes
        """
        self.name = ""
        self.group = ""
        self.risk = []  # Risk levels (array-like : list or numpy array)
        self.hazl = []  # Hazard levels (array-like : list or numpy array)
        self.conf = []  # Confidence levels
        self.hazvalid = None  # Maximum hazard for which this ember is assumed valid (= risk was assessed)
        self.hazn = None  # Standard name of the hazard variable
        self.meta = {}  # Dictionnary of ember-related metadata
        self._inited = True

    def draw(self, egr, xpos):
        """
        Draws an ember. Applies parameters from egr.
        In particular, if egr.circular is True, will draw the ember as a piece of pie rather than a vertical line
        (circular embers may not be 'supported' in the future, they are experimental)

        :param egr: an ember graph (including the canvas to draw to and methods that deal with the entire graph)
        :param xpos: the x coordinates that define the ember's drawing area [x0, width]
        """
        c = egr.c
        plotlevels = []
        colorlevels = []

        xmin, xmax = xpos
        yamin = egr.get_y0()
        yamax = egr.get_y1()
        # Canvas range occupied by the gradients:
        ygmin = min(egr.haztocan(np.min(self.hazl)), yamin)
        ygmax = max(egr.haztocan(np.max(self.hazl)), yamax)
        # Canvas range for the "valid" area (intesection of the valid range and axis):
        yvmin = max(egr.get_y0(), egr.haztocan(self.hazvalid[0]))
        yvmax = min(egr.get_y1(), egr.haztocan(self.hazvalid[1]))

        # To ensure full consistency, all hazard values are converted to canvas coordinates, and divided
        # by the range of each gradient in these coordinates (ygmax - ygmin) when plotting a gradient.

        # Generate the lists of colour change positions (plotlevels) and coulours (colorlevels):
        for ihaz in range(len(self.risk)):
            # Fractional position within a gradient of each colour change
            plotlevels.append((egr.haztocan(self.hazl[ihaz]) - ygmin) / (ygmax - ygmin))
            # Associated colour
            color = cbyinterp(self.risk[ihaz], egr.csys, egr.cdefs)
            colorlevels.append(color)
        # Copy the start and end colors at both ends of the plot range
        # (= extend the last colour beyond the last transition):
        plotlevels.append(1.0)
        colorlevels.append(colorlevels[-1])
        plotlevels.insert(0, 0)
        colorlevels.insert(0, colorlevels[0])  # top (copy the last available colour to the 'top' level)

        hlp.addlogmes("Hazard range of the gradient: {:7.2f}-{:7.2f} ".format(egr.cantohaz(ygmin), egr.cantohaz(ygmax)))
        hlp.addlogmes(plotlevels)
        hlp.addlogmes(colorlevels)

        self.drawlinear(egr, xmin, xmax, yamin, yamax, ygmin, ygmax, yvmin, yvmax, plotlevels, colorlevels)

        # Add the name of the BE
        # - - - - - - - - - - -
        thestyle = egr.style
        thestyle.alignment = TA_CENTER
        thestyle.fontSize = egr.gp['fnt_size']
        thestyle.leading = thestyle.fontSize * 1.1
        par = Paragraph(self.name, thestyle)
        # This calculates the height needed to render the paragraph, it is the only way to get it
        # vertically aligned to "top" (= right under the graphic)
        w, h = par.wrap(egr.gp['be_x'] + egr.gp['be_int_x'], egr.gp['be_bot_y'])
        xp = xmin - egr.gp['be_int_x'] / 2
        yp = yamin - h
        par.drawOn(c, xp, yp)

        # Note:
        # Annotating embers could possibly be useful to add information, but it produced PDF erros, hence disabled:
        # (it is an undocumented feature in ReportLab, labelled experimental although appears to be in since years)
        # c.textAnnotation(emb.desc, Rect=[xp, yp, xp+2*cm, yp+2*cm],relative=True)

        return xmin + egr.gp['be_x'] / 2

    @staticmethod
    def drawlinear(egr, xmin, xmax, yamin, yamax, ygmin, ygmax, yvmin, yvmax, plotlevels, colorlevels):
        """
        This method handles the drawing of a colour gradient in a box, to fulfill the common needs of
        drawing embers and drawing the legend.
        The arguments are explained in self.draw.
        """
        c = egr.c
        # Set the properties of the box around the ember:
        linewidth = 0.3 * mm
        c.setLineWidth(linewidth)
        c.setStrokeColor(egr.colors['black'])
        c.setFillColor(egr.colors['vlgrey'])

        # Useful intermediary variable(s):
        xsiz = xmax - xmin

        # Draw the background grey area in case of 'missing data'
        c.rect(xmin, yamin, xsiz, yamax - yamin, stroke=0, fill=1)

        # Store the drawing context to come back to it after plotting the gradients
        c.saveState()

        # Restrict the viewable area to the frame enclosing the BE
        # (colour gradients do not have x limits, hence the need to limit their visible part):
        p = c.beginPath()
        p.rect(xmin, yvmin, xsiz, yvmax - yvmin)
        c.clipPath(p, stroke=0)

        # Draw the color gradients
        if yamax - yamin > xmax - xmin:  # vertical (the criteria is based on the axis, regardless of the data)
            c.linearGradient(xmin, ygmin, xmin, ygmax, colorlevels, plotlevels, extend=False)
        else:  # horizontal, for legend only (would not work for regular embers, as these are more complex)
            c.linearGradient(xmin, ygmin, xmax, ygmin, colorlevels, plotlevels, extend=False)

        # Revert back to the normal viewable area
        c.restoreState()

        # Draw the surounding box
        c.rect(xmin, yamin, xsiz, yamax - yamin, stroke=1, fill=0)

    def _drawcircular(self, egr, by, sy, ty, ygmax, iemb, colorlevels, plotlevels):
        """
        Experimental function to draw circular 'pie' embers.
        A preliminary version worked in 10/2020, but development is halted by lack of interest in the result
        (the structure and variables of the self.draw was improved since then, so changes are needed here)
        """
        c = egr.c

        u = 15 * cm  # Temporary static position for circular embers. Todo: rework if circular embers are used.
        extang = 360 / float(egr.glen)
        startang = iemb * extang
        p = c.beginPath()
        p.moveTo(u, by)
        p.arcTo(u - sy, by - sy, u + sy, by + sy, startAng=startang, extent=extang)
        p.lineTo(u, by)
        c.drawPath(p, stroke=1, fill=1)
        # Prepare a new path here because the gradient may end (at ty) below the top value on the axis (sy)
        p = c.beginPath()
        p.moveTo(u, by)
        p.arcTo(u - ty, by - ty, u + ty, by + ty, startAng=startang, extent=extang)
        p.lineTo(u, by)

        c.saveState()
        c.clipPath(p, stroke=0)

        # Plot the BE gradients
        # An extension of the standard radialGradient was written for the case were an ember would not start
        # at the center of its cycle; as necessity is unclear, the code is not provide for now to avoid needing
        # investigations about licence etc. The code can be obtained from the author on request. The call is:
        # c.extRadialGradient(u, by, ygmin, ygmax, colorlevels, plotlevels)
        c.radialGradient(u, by, ygmax, colorlevels, plotlevels)

        # Revert back to the normal viewable area
        c.restoreState()

        # Add the name of the BE
        # - - - - - - - - - - -
        thestyle = egr.style
        thestyle.alignment = TA_CENTER
        thestyle.fontSize = egr.gp['fnt_size']
        thestyle.leading = thestyle.fontSize * 1.1
        par = Paragraph(self.name, thestyle)
        # This calculate the height needed to render the paragraph, it is the only way to get it
        # vertically aligned to "top" (= right under the graphic)
        w, h = par.wrap(egr.gp['be_x'] + egr.gp['be_int_x'], egr.gp['be_bot_y'])
        # Circular embers; first caclulate the angle and radius to position the name:
        lang = (startang + extang / 2.0) / 180.0 * np.pi
        lmov = w * 0.8
        lrad = lmov + sy
        xp = u + lrad * np.cos(lang) - lmov * 0.7
        yp = by + lrad * np.sin(lang) - lmov * 0.5
        par.drawOn(c, xp, yp)

        return None

    def getmeta(self, name):
        """
        Returns ember-related metadata (these defer from file-related metadata).

        :param name: the name of the parameter to be returned.
        :return: the requested metadata, or None if the metadata is not defined.
        """
        try:
            return self.meta[name]
        except KeyError:
            return None


class EmberGraph(object):
    """
    EmberGraphs stores the general information on a graphic containing embers,
    and provides methods for drawing such graphs (except for the embers themselves, which are dealt with
    in the Ember class)
    We have included the creation of the drawing canvas here because we want to perfom some intialisation
    before the main program can access the canvas; before that, it could draw RGB color on an otherwise CMYK figure,
    now the main drawing parameters are set here to prevent that.
    Note: it might be that defining this as a class is useless (in Python) - it might be in the module.
    """

    def __init__(self, outfile, cpal, gp, circular=False):
        """
        :param outfile: the intended outfile path
        :param cpal: a dict defining a color palette
        :param gp: a dict of graphic parameters
        :param circular: draws a 'circular' version of the embers; the distance to the center represents 'hazard',
                         and the coulour gradients remain identical to what they are in the 'straight ember' version;
                         this differs from a polar diagram, in which distance to the center may represent risk.
                         Circular diagrams are at alpha dev. stage for the moment.
        """
        self._protected = ()  # Will include the names of protected parameters once set (see pincoord)
        self._y0 = 0.0
        self._y1 = 0.0
        self._y = 0.0
        self._hz0 = 0.0
        self._hz1 = 0.0
        self._hz = 0.0

        self.csys = cpal['csys']
        self.cdefs = cpal['cdefs']
        self.cnames = cpal['cnames']
        self.gp = gp
        self.circular = circular
        self.glen = 10  # Default number of embers in the current group; needed for circular diagrams.

        # Define the drawing canvas
        self.c = Canvas(outfile, enforceColorSpace=self.csys)  # drawing canevas
        # Define colors for texts and lines according to the color system;
        # a PDF may contain several color systems at the same time, hence this seems to provide consistency.
        if self.csys == "CMYK":
            self.colors = {
                'black': col.CMYKColor(0, 0, 0, 1),  # Standard black, for texts and lines
                'blue': col.CMYKColor(1, 0.4, 0, 0),
                'red': col.CMYKColor(0, 0.88, 0.85, 0),
                'green': col.CMYKColor(0.95, 0.0, 0.95, 0),
                'grey': col.CMYKColor(0, 0, 0, 0.4),
                'lgrey': col.CMYKColor(0, 0, 0, 0.2),
                'vlgrey': col.CMYKColor(0, 0, 0, 0.1),  # Very light grey
                'tgrey': col.CMYKColor(0, 0, 0, 1, alpha=0.5),  # Transparent grey
                'tdarkgrey': col.CMYKColor(0, 0, 0, 1, alpha=0.7),  # Transparent dark grey
                'white': col.CMYKColor(0, 0, 0, 0)
            }
        else:
            self.colors = {
                'black': col.Color(0, 0, 0),
                'blue': col.Color(0, 0, 0.9),
                'red': col.Color(0.9, 0, 0),
                'green': col.Color(0, 0.9, 0),
                'grey': col.Color(0.6, 0.6, 0.6),
                'lgrey': col.Color(0.8, 0.8, 0.8),
                'vlgrey': col.Color(0.9, 0.9, 0.9),  # Very light grey
                'tgrey': col.Color(0, 0, 0, alpha=0.5),
                'tdarkgrey': col.Color(0, 0, 0, alpha=0.7),  # Transparent dark grey
                'white': col.Color(1, 1, 1)
            }

        self.c.setStrokeColor(self.colors['black'])
        self.c.setFillColor(self.colors['black'])

        # text paragraphs styles
        stylesheet = getSampleStyleSheet()
        self.style = stylesheet['BodyText']
        self.style.fontName = gp['fnt_name']
        self.style.fontSize = gp['fnt_size']
        self.style.alignment = TA_CENTER
        self.style.leading = 10
        self.c.setFont(gp['fnt_name'], gp['fnt_size'])
        self.font = (self.style.fontName, self.style.fontSize)

    def isdefined(self, gpname):
        if gpname not in self.gp:
            return False
        else:
            return not isempty(self.gp[gpname])

    def pincoord(self, be_y0, be_y):
        """
        Establishes the correspondance between hazard values and 'physical' coordinates on the canvas.
        To avoid potential inconsistencies, the coordinates should be changed only with this function, so that
        every use mapping from hazard to canvas is done in the same way.
        Note: be_y0, be_y0+be_y define the drawing area on the canvas and correspond to haz_axis_bottom, haz_axis_top;
        (however it is permitted to enter data outside the haz_ range, they will remain invisible but may have
        a visible impact trough interpolation from a visible data point)

        :param be_y0: bottom of the drawing area on the canvas
        :param be_y: height of the drawing area on the canvas
        """
        # All of the following are 'protected' variables: they should not be changed from outside the EmberGraph class.
        # PyCharm (at least) provides a warning against this because it would like to have it in __init__;
        # Such a change would not be possible without a broader refactoring and does not appear needed.
        self._protected = ()
        self._y0 = be_y0
        self._y1 = be_y0 + be_y
        self._y = be_y
        self._hz0 = self.gp['haz_axis_bottom']
        self._hz1 = self.gp['haz_axis_top']
        self._hz = self._hz1 - self._hz0
        self._protected = ('_y0', '_y1', '_y', '_hz0', '_hz1', '_hz')

    # Need to allow reading y0 and y without it being regarded as a violation of its "protected" status (_y)
    def get_y0(self):
        return self._y0

    def get_y1(self):
        return self._y1

    def get_y(self):
        return self._y

    def __setattr__(self, key, value):
        """
        Enforces protection of a tuple of protected variables when changing attributes

        :param key: the name of the attribute to be changed
        :param value: the value of the attribute to be change
        """
        if hasattr(self, '_protected') and key in self._protected:
            raise Exception("Attempt at changing a protected variable (set by pincoord): " + str(key))
        object.__setattr__(self, key, value)

    def haztocan(self, hazvalue):
        """
        Calculates the position in canvas coordinate for a given hazard value.

        :param hazvalue: a value on the y-axis (hazard axis, e.g. temperature)
        :return: the result of the scaling to the y canevas coordinates
        """
        hz0 = self._hz0
        hz = self._hz
        y = self._y
        y0 = self._y0
        return y0 + y * (hazvalue - hz0) / hz

    def cantohaz(self, canvalue):
        """
        Inverse of haztocan. Provides the hazard value of a given y position on the canvas.

        :param canvalue: a 'physical' position on the y-axis, in canvas coordinates
        :return: the hazard value
        """
        hz0 = self._hz0
        hz = self._hz
        y = self._y
        y0 = self._y0
        return ((canvalue - y0) * hz / y) + hz0

    def vaxis(self, xbas, nbe, showname=True):
        """
        Plots the 'hazard' axis graduation values and grid lines

        :param xbas: the x coordinate at the left of the ember group (start position and width on the canvas)
        :param nbe: the number of burning ember columns to be included, to calculate the length of grid lines
        :param showname: whether the name of the axis should be drawn.
        :return: the x coordinate at the left of the grid lines, as a starting point to draw the embers
        """

        # Total width of the grid lines:
        sx = self.gp['scale_x'] + nbe * (self.gp['be_x'] + self.gp['be_int_x'])

        # Set drawing properties
        self.c.setStrokeColor(self.colors['grey'])
        self.c.setFillColor(self.colors['black'])

        # Draw the name of the axis
        xnam = self.gp['haz_name_x']
        if showname:
            self.c.saveState()
            self.c.rotate(90)
            # Warning: the 'reference frame' is rotated -> coordinates work differently
            hlp.drawstring(self.c, self._y0 + self._y / 2.0, -xnam * 0.6, self.gp['haz_name'],
                           font=(self.gp['fnt_name'], self.gp['fnt_size']), align='center')
            self.c.restoreState()
            xbas += xnam

        # Get nice looking levels for the horizontal lines
        glines, labfmt = hlp.nicelevels(self._hz0, self._hz1,
                                        nalevels=self.gp['haz_grid_lines'], enclose=False)

        # Prepare unit for axis labels: if it is in the axis name, do not include it in the labels:
        axisunit = (" " + self.gp['haz_unit']) if self.gp['haz_unit'] not in self.gp['haz_name'] else ""

        # Self defined grid lines (from nicelevels above):
        lbx = xbas + self.gp['scale_x']
        sbx = xbas + 0.94 * self.gp['scale_x']
        for haz in glines:
            if not self.circular:
                yp = self.haztocan(haz)
                self.c.line(lbx, yp, xbas + sx, yp)
                gllabel = labfmt.format(haz) + axisunit
                hlp.drawstring(self.c, sbx, yp - self.gp['fnt_size'] * 0.3, gllabel, align='right', font=self.font)
            else:
                # Experimental circular - Todo: rework
                u = 15 * cm
                self.c.circle(u, self.get_y0(), self.haztocan(haz), stroke=1, fill=0)

        # Add any user-defined specific grid lines (done separately due to a different formatting method)
        if self.gp.lst('haz_grid_lines'):
            glcolors = norm(self.gp.lst('haz_grid_lines_colors'))
            gllabels = self.gp.lst('haz_grid_lines_labels')
            gllaboffs = self.gp.lst('haz_grid_lines_labels_off')
            glends = self.gp.lst('haz_grid_lines_ends')  # Used to get a colored area, eg. 'recent temp'
            self.c.setLineWidth(0.5 * mm)
            for ic, haz in enumerate(self.gp.lst('haz_grid_lines')):
                glcolor = self.colors[glcolors[ic]] if hlp.hasindex(glcolors,ic) else self.colors['grey']
                try:
                    yp = self.haztocan(float(haz))
                except ValueError:
                    hlp.addlogwarn("Could not process data for a custom haz_grid_line")
                    continue
                if hlp.hasindex(glends,ic):
                    # Colored area (between the standard grid-line and grid-line-ends
                    sy = self.haztocan(glends[ic]) - self.haztocan(haz)
                    self.c.setFillColor(glcolor)
                    self.c.rect(lbx, yp, xbas + sx - lbx, sy, stroke=0, fill=1)
                    self.c.setFillColor(self.colors['black'])
                else:
                    # Grid-lines
                    sy = 0.0
                    self.c.setStrokeColor(glcolor)
                    self.c.line(lbx, yp, xbas + sx, yp)
                # Prepare for drawing label (for colored areas, the text is centered by using sy/2)
                gllabel =  gllabels[ic] if hlp.hasindex(gllabels, ic) else (str(haz) + axisunit)
                sby = yp + sy / 2.0
                # Handle custom label offsetting (see doc about haz_grid_lines_labels_off)
                if hlp.hasindex(gllaboffs,ic):
                    oby = sby
                    # Move the label
                    sby += gllaboffs[ic] * self.gp['fnt_size']
                    # Draw a small connecting line
                    xp = sbx + self.gp['fnt_size'] * 0.1
                    obx = xp + self.gp['be_int_x'] / 4.0 + self.gp['fnt_size'] * 0.2
                    yp = sby + self.gp['fnt_size'] * 0.15
                    self.c.setLineWidth(0.3 * mm)
                    self.c.setStrokeColor(self.colors['black'])
                    self.c.line(xp, yp, obx, oby)
                # Add label
                sby = sby - self.gp['fnt_size'] * 0.3
                hlp.drawstring(self.c, sbx, sby, gllabel, align='right', font=self.font)
        return lbx

    def drawlegend(self, emberbox, isinside):
        """
        Draws a legend (colour bar)

        :param emberbox: a box representing the ember diagram area to which the legend needs to be attached OR
                         in which the legend needs to be drawn
        :param isinside: True if the legend needs to be inside emberbox,
                         False if it needs to be attached outside emberbox
                         (needed because isinside is decided together with emberbox, it is not an input parameter)
        :return: additional horizontal space that is needed because it is occupied by the legend.
        """
        c = self.c
        gp = self.gp
        if norm(gp['leg_pos']) in ['under', 'in-grid-horizontal']:
            ishoriz = True
        else:
            ishoriz = False
            if norm(gp['leg_pos']) not in ['right', 'in-grid-vertical']:
                hlp.addlogwarn("Parameter leg_pos has an unknown value: " + str(gp['leg_pos']))

        # pseudo-ember used as legend:
        rlevels = self.cdefs[0]
        # include each level twice to have color transition + uniform area:
        plotlevels = np.arange(len(rlevels) * 2, dtype=float)
        plotlevels = plotlevels / plotlevels[-1]  # normalize
        colorlevels = np.repeat(rlevels, 2)
        colorlevels = [cbyinterp(clev, self.csys, self.cdefs) for clev in colorlevels]

        # Intermediate variables for the position of the legend

        # Size of the legend area
        # Here x and y are in 'legend coordinates', ie x is along the main axis of the legend (vertical OR horizontal)
        ltot_y_h = gp['leg_bot_y'] + gp['leg_y'] + gp['leg_top_y']
        # For vertical embers, the width depends on the (drawn) length of the risk level names:
        l_cnames = max((c.stringWidth(name, gp['fnt_name'], gp['fnt_size']) for name in self.cnames))
        ltot_y_v = gp['leg_y'] + gp['leg_bot_y'] + max(l_cnames, gp['leg_top_y'])
        ltot_y = ltot_y_h if ishoriz else ltot_y_v
        ltot_x = gp['leg_x']
        # Allow the text to extend up to 10% beyond the ember on each side
        # (better could be done if needed, this is a rough trick to have a slightly better design):
        ltot_xtext = ltot_x * 0.2

        # Extension of the canvas space when the legend is outside the current graphic area (=> addright):
        if ishoriz:  # in-grid-horizontal: needs to increase the size of emberbox if too small !
            addright = max(0.0, ltot_x + ltot_xtext - emberbox[2])  # by how much is the legend wider than emberbox ?
            emberbox[2] += addright
        elif not isinside:  # legend on the right : entirely in additional space, but outside emberbox.
            addright = ltot_y
        else:
            addright = 0.0  # in-grid-vertical

        #  Center of emberbox
        boxmid = ((emberbox[0] + emberbox[2] / 2.0), (emberbox[1] + emberbox[3] / 2.0))
        #  Center of the legend area
        lmid_x = boxmid[0] if (ishoriz or isinside) else (emberbox[0] + emberbox[2] + ltot_y / 2.0)
        lmid_y = boxmid[1] if (isinside or not ishoriz) else (emberbox[1] - ltot_y / 2.0)

        #  Position of the legend's burning ember (basis for the entire legend):
        #  Here xpos, ypos are in canvas coordinates.
        if ishoriz:
            xmin = lmid_x - ltot_x / 2.0
            xmax = lmid_x + ltot_x / 2.0
            ymin = lmid_y - ltot_y / 2.0 + gp['leg_bot_y']
            ymax = ymin + gp['leg_y']
        else:  # vertical legend
            xmin = lmid_x - ltot_y / 2.0  # the ember is on the left of the legend
            xmax = xmin + gp['leg_y']
            ymin = lmid_y - ltot_x / 2.0
            ymax = lmid_y + ltot_x / 2.0

        # Draw the 'ember' (for a legend, all y ranges are identical : axis, ember, and valid range):
        Ember.drawlinear(self, xmin, xmax, ymin, ymax, ymin, ymax, ymin, ymax, plotlevels, colorlevels)

        # Draw the text of the legend and connect text to colors with lines
        # -----------------------------------------------------------------
        # Prepare for drawing lines
        c.setStrokeColor(self.colors['black'])
        c.setFillColor(self.colors['black'])
        c.setLineWidth(0.5 * mm)
        c.setFontSize(40.0 / len(rlevels))
        # Position of the lines (link between ember and risk level) relative to the 'ember'(halfway in the solid colors)
        xlines = (plotlevels[1::2] + plotlevels[:-1:2]) / 2.0 * self.gp['leg_x']
        # Prepare for drawing the title of the legend as a paragraph
        st = self.style
        st.fontSize = gp['fnt_size']
        st.textColor = self.colors['black']
        # Draw the lines, name of risk levels, and title of paragraph
        if ishoriz:
            for i, xline in enumerate(xlines):
                c.line(xmin + xline, ymin - gp['leg_bot_y'] * 0.4, xmin + xline, (ymin + ymax) / 2.0)
                c.drawCentredString(xmin + xline, ymin - gp['leg_bot_y'] * 0.8, self.cnames[i])
            if gp['leg_title']:
                st.alignment = TA_CENTER
                par = Paragraph(gp['leg_title'], st)
                par.wrap(ltot_x + ltot_xtext, 10 * cm)  # The max height doesn't matter
                par.drawOn(c, xmin - ltot_xtext / 2.0, ymax + gp['leg_top_y'] * 0.3)
        else:  # Vertical ember
            for i, xline in enumerate(xlines):
                c.line((xmin + xmax) / 2.0, ymin + xline, xmax + gp['leg_bot_y'] * 0.5, ymin + xline)
                c.drawString(xmax + gp['leg_bot_y'] * 0.6, ymin + xline - 1 * mm, self.cnames[i])
            if gp['leg_title']:
                st.alignment = TA_LEFT
                par = Paragraph(gp['leg_title'], st)
                par.wrap(ltot_y, 10 * cm)  # The max height doesn't matter
                par.drawOn(c, xmin, ymax + gp['leg_x'] * 0.05)

        # Return the horizontal length added to the the draw area in the canvas.
        return addright


def getcpal(wbcol, prefcsys='', cpalname=''):
    """
    Reads the color palette. The palette is be defined by:
     - its color system (RGB, CMYK...): csys
     - names of risk levels associated to colors : cnames (see excel sheet)
     - a risk level index: cdefs[0] (1D numpy array of risk indexes)
     - the color densities for each color corresponding to a risk index :
         cdefs[i] (1D numpy array of color densities for each risk index, given i=#color within the color system)
     :param wbcol: an Excel workbook from openpyxl
     :param prefcsys: a colour system choice from the user, among (RGB, CMYK, standard);
                    'standard' means that the user makes no choice, so it will use cpalname if set,
                    then 'ACTIVE-P' if set, and if is also unavailable, revert to an internal default (RGB-SRCCL-C7).
                    ACTIVE-P is a legacy parameter which may be provided in the 'colour' spreadsheet (read here).
     :param cpalname: the name of the desired palette, used only if the color sheet does not set 'ACTIVE-P'
     :return: csys, cnames, cdefs
     """
    read = False
    cnames, ctmp = [], []
    csys = ''  # csys will be the colour system, read from file
    cref = 1.0  # Reference (max) value of the color range (optional parameter)
    sht = wbcol["Color definitions"]
    # Default palette (if no palette defined in the color sheet or provided as cpalname
    if prefcsys == 'RGB':  # if prefcsys is set to RGB or CMYK, it gets the priority over any parameter
        cpalname = 'RGB-SRCCL-C7'
    elif prefcsys == 'CMYK':
        cpalname = 'CMYK-IPCC'
    elif cpalname == '':
        # if prefcsys did not specify a colour system and cpalname is not set,
        # then we set a default here and will overwrite it below if 'ACTIVE-P' is found
        cpalname = 'RGB-SRCCL-C7'

    for row in sht.rows:
        key = hlp.stripped(row[0].value)
        name = hlp.stripped(row[1].value)
        inda = [acell.value for acell in row[2:]]  # input data
        if key == 'ACTIVE-P' and prefcsys == 'standard':
            cpalname = name  # ACTIVE-P is a legacy parameter
        elif key == 'PALETTE' and cpalname == name:
            hlp.addlogmes('Will use color palette: ' + cpalname)
            read = True
        elif key == '' or key is None:
            read = False
        elif key == 'HEADERS' and read:
            if inda[1:4] == ['Red', 'Green', 'Blue']:
                csys = 'RGB'
            elif inda[1:5] == ['Cyan', 'Magenta', 'Yellow', 'Black']:
                csys = 'CMYK'
            else:
                raise Exception("Unknown color system (see colors in sheet 'Color definitions').")
        elif key == 'DATA' and read:
            cnames.append(name)
            ctmp.append(inda[:1 + len(csys)])
        elif key == 'REFERENCE' and read:
            # The "reference" is an arbitrary number that is the maximum of colour values, typically 1, 100, or 255.
            # (default value is 1, see above)
            try:
                cref = float(inda[0])
            except ValueError:
                return [None, hlp.addlogfail(
                    "REFERENCE value for the colors is wrong or misplaced (must be 3rd col in 'Color definitions').")]
    cdiv = [1.0] + ([cref] * (len(ctmp[0]) - 1))  # We need to divide each line by the ref, but not element 0
    cdefs = (np.array(ctmp) / cdiv).transpose()  # color definitions array
    del ctmp
    hlp.addlogmes("Palette risk levels and colors: " + str(cdefs))

    return {'name': cpalname, 'csys': csys, 'cnames': cnames, 'cdefs': cdefs}
