from defcon.objects.base import BaseDictObject
from defcon.objects.color import Color
from defcon.tools.identifiers import makeRandomIdentifier


class Guideline(BaseDictObject):

    """
    This object represents a guideline.

    **This object posts the following notifications:**

    ===========================
    Name
    ===========================
    Guideline.Changed
    Guideline.XChanged
    Guideline.YChanged
    Guideline.AngleChanged
    Guideline.NameChanged
    Guideline.IdentifierChanged
    ===========================

    During initialization a guideline dictionary, following the format defined
    in the UFO spec, can be passed. If so, the new object will be populated
    with the data from the dictionary.
    """

    changeNotificationName = "Guideline.Changed"
    representationFactories = {}

    def __init__(self, guidelineDict=None):
        super(Guideline, self).__init__()
        self._dirty = False
        if guidelineDict is not None:
            self.x = guidelineDict.get("x")
            self.y = guidelineDict.get("y")
            self.angle = guidelineDict.get("angle")
            self.name = guidelineDict.get("name")
            self.color = guidelineDict.get("color")
            self.identifier = guidelineDict.get("identifier")

    # ----------
    # Properties
    # ----------

    # parents

    def _get_font(self):
        glyph = self.glyph
        if glyph is not None:
            return glyph.font
        info = self.info
        if info is not None:
            return info.font
        return None

    font = property(_get_font, doc="The :class:`Font` that this object belongs to.")

    def _get_info(self):
        from defcon.objects.info import Info
        parent = self.getParent()
        if not isinstance(parent, Info):
            return None
        return parent

    info = property(_get_info, doc="The :class:`Info` that this object belongs to (if it is a font info guideline).")

    def _get_layerSet(self):
        glyph = self.glyph
        if glyph is None:
            return None
        return glyph.layerSet

    layerSet = property(_get_layerSet, doc="The :class:`LayerSet` that this object belongs to (if it isn't a font a guideline).")

    def _get_layer(self):
        glyph = self.glyph
        if glyph is None:
            return None
        return glyph.layer

    layer = property(_get_layer, doc="The :class:`Layer` that this object belongs to (if it isn't a font a guideline).")

    def _get_glyph(self):
        from defcon.objects.glyph import Glyph
        parent = self.getParent()
        if not isinstance(parent, Glyph):
            return None
        return parent

    glyph = property(_get_glyph, doc="The :class:`Glyph` that this object belongs to (if it isn't a font a guideline).")

    def _get_x(self):
        return self.get("x")

    def _set_x(self, value):
        old = self.get("x")
        if value == old:
            return
        self["x"] = value
        self.postNotification("Guideline.XChanged", data=dict(oldValue=old, newValue=value))

    x = property(_get_x, _set_x, doc="The x coordinate. Setting this will post *Guideline.XChanged* and *Guideline.Changed* notifications.")

    def _get_y(self):
        return self.get("y")

    def _set_y(self, value):
        old = self.get("y")
        if value == old:
            return
        self["y"] = value
        self.postNotification("Guideline.YChanged", data=dict(oldValue=old, newValue=value))

    y = property(_get_y, _set_y, doc="The y coordinate. Setting this will post *Guideline.YChanged* and *Guideline.Changed* notifications.")

    def _get_angle(self):
        return self.get("angle")

    def _set_angle(self, value):
        old = self.get("angle")
        if value == old:
            return
        self["angle"] = value
        self.postNotification("Guideline.AngleChanged", data=dict(oldValue=old, newValue=value))

    angle = property(_get_angle, _set_angle, doc="The angle. Setting this will post *Guideline.AngleChanged* and *Guideline.Changed* notifications.")

    def _get_name(self):
        return self.get("name")

    def _set_name(self, value):
        old = self.get("name")
        if value == old:
            return
        self["name"] = value
        self.postNotification("Guideline.NameChanged", data=dict(oldValue=old, newValue=value))

    name = property(_get_name, _set_name, doc="The name. Setting this will post *Guideline.NameChanged* and *Guideline.Changed* notifications.")

    def _get_color(self):
        return self.get("color")

    def _set_color(self, color):
        if color is None:
            newColor = None
        else:
            newColor = Color(color)
        oldColor = self.get("color")
        if newColor == oldColor:
            return
        self["color"] = newColor
        self.postNotification("Guideline.ColorChanged", data=dict(oldValue=oldColor, newValue=newColor))

    color = property(_get_color, _set_color, doc="The guideline's :class:`Color` object. When setting, the value can be a UFO color string, a sequence of (r, g, b, a) or a :class:`Color` object. Setting this posts *Guideline.ColorChanged* and *Guideline.Changed* notifications.")

    # -------
    # Methods
    # -------

    def _get_identifiers(self):
        identifiers = None
        parent = self.glyph
        if parent is None:
            parent = self.info
        if parent is not None:
            identifiers = parent.identifiers
        if identifiers is None:
            identifiers = set()
        return identifiers

    identifiers = property(_get_identifiers, doc="Set of identifiers for the object that this guideline belongs to. This is primarily for internal use.")

    def _get_identifier(self):
        return self.get("identifier")

    def _set_identifier(self, value):
        oldIdentifier = self.identifier
        if value == oldIdentifier:
            return
        # don't allow a duplicate
        identifiers = self.identifiers
        assert value not in identifiers
        # free the old identifier
        if oldIdentifier in identifiers:
            identifiers.remove(oldIdentifier)
        # store
        self["identifier"] = value
        if value is not None:
            identifiers.add(value)
        # post notifications
        self.postNotification("Guideline.IdentifierChanged", data=dict(oldValue=oldIdentifier, newValue=value))

    identifier = property(_get_identifier, _set_identifier, doc="The identifier. Setting this will post *Guideline.IdentifierChanged* and *Guideline.Changed* notifications.")

    def generateIdentifier(self):
        """
        Create a new, unique identifier for and assign it to the guideline.
        This will post *Guideline.IdentifierChanged* and *Guideline.Changed* notifications.
        """
        identifier = makeRandomIdentifier(existing=self.identifiers)
        self.identifier = identifier


def _test():
    """
    >>> g = Guideline()
    >>> g.dirty
    False

    >>> g = Guideline()
    >>> g.x = 100
    >>> g.x
    100
    >>> g.dirty
    True
    >>> g.x = None
    >>> g.x
    >>> g.dirty
    True

    >>> g = Guideline()
    >>> g.y = 100
    >>> g.y
    100
    >>> g.dirty
    True
    >>> g.y = None
    >>> g.y
    >>> g.dirty
    True

    >>> g = Guideline()
    >>> g.angle = 100
    >>> g.angle
    100
    >>> g.dirty
    True
    >>> g.angle = None
    >>> g.angle
    >>> g.dirty
    True

    >>> g = Guideline()
    >>> g.name = "foo"
    >>> g.name
    'foo'
    >>> g.dirty
    True
    >>> g.name = None
    >>> g.name
    >>> g.dirty
    True

    >>> g = Guideline()
    >>> g.color = "1,1,1,1"
    >>> g.color
    '1,1,1,1'
    >>> g.dirty
    True

    >>> g = Guideline()
    >>> g.identifier
    >>> g.generateIdentifier()
    >>> g.identifier is None
    False

    >>> g = Guideline(dict(x=1, y=2, angle=3, name="4", identifier="5", color="1,1,1,1"))
    >>> g.x, g.y, g.angle, g.name, g.identifier, g.color
    (1, 2, 3, '4', '5', '1,1,1,1')
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod()
