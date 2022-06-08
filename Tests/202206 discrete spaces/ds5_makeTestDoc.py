# make a test designspace format 5 with 1 continuous and 2 discrete axes.

# axis width is a normal interpolation with a change in width
# axis DSC1 is a discrete axis showing 1, 2, 3 items in the glyph
# axis DSC2 is a discrete axis showing a solid or outlined shape

from fontTools.designspaceLib import DesignSpaceDocument, SourceDescriptor, InstanceDescriptor, AxisDescriptor, RuleDescriptor, processRules, DiscreteAxisDescriptor

import os
import fontTools
print(fontTools.version)

doc = DesignSpaceDocument()

#https://fonttools.readthedocs.io/en/latest/designspaceLib/python.html#axisdescriptor
a1 = AxisDescriptor()
a1.minimum = 400
a1.maximum = 1000
a1.default = 400
a1.name = "width"
a1.tag = "wdth"
a1.axisOrdering = 1
doc.addAxis(a1)

a2 = DiscreteAxisDescriptor()
a2.values = [1, 2, 3]
a2.default = 1
a2.name = "countedItems"
a2.tag = "DSC1"
a2.axisOrdering = 2
doc.addAxis(a2)

a3 = DiscreteAxisDescriptor()
a3.values = [0, 1]
a3.default = 0
a3.name = "outlined"
a3.tag = "DSC2"
a3.axisOrdering = 3
doc.addAxis(a3)


# add sources
for c in [a1.minimum, a1.maximum]:
	for d1 in a2.values:
		for d2 in a3.values:

			s1 = SourceDescriptor()
			s1.path = os.path.join("masters", f"geometryMaster_c_{c}_d1_{d1}_d2_{d2}.ufo")
			print(s1.path, os.path.exists(s1.path))
			s1.name = f"geometryMaster{c} {d1} {d2}"
			s1.location = dict(width=c, countedItems=d1, outlined=d2)
			s1.familyName = "MasterFamilyName"
			td1 = ["One", "Two", "Three"][(d1-1)]
			if c == 400:
				tc = "Narrow"
			elif c == 1000:
				tc = "Wide"
			if d2 == 0:
				td2 = "solid"
			else:
				td2 = "open"
			s1.styleName = f"{td1}{tc}{td2}"
			doc.addSource(s1)

def ip(a,b,f):
	return a + f*(b-a)

# add instances
steps = 4
for s in range(steps+1):
	factor = s / steps
	c = int(ip(a1.minimum, a1.maximum, factor))
	for d1 in a2.values:
		for d2 in a3.values:

			s1 = InstanceDescriptor()
			s1.path = os.path.join("instances", f"geometryInstance_c_{c}_d1_{d1}_d2_{d2}.ufo")
			print(s1.path, os.path.exists(s1.path))
			s1.location = dict(width=c, countedItems=d1, outlined=d2)
			s1.familyName = "InstanceFamilyName"
			td1 = ["One", "Two", "Three"][(d1-1)]
			if c == 400:
				tc = "Narrow"
			elif c == 1000:
				tc = "Wide"
			if d2 == 0:
				td2 = "Solid"
			else:
				td2 = "Open"
			s1.name = f"geometryInstance {td1} {tc} {td2}"
			s1.styleName = f"{td1}{tc}{td2}"
			doc.addInstance(s1)


path = "test.ds5.designspace"
doc.write(path)


for a in doc.axes:
	if hasattr(a, "values"):
		print(a.name, "d", a.values)
	else:
		print(a.name, "r", a.minimum, a.maximum)
	
for s in doc.sources:
	print(s.location)
