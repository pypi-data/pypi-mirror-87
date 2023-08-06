{INSERTION-SOURCE:../embermaker/defaults/paramdefs.md}

This page documents parameters which may be used in input files. 
The starting point to learn about the input format for the 'Ember Factory' is the [Tutorial](tutorial).
This page provides more detailed information, including a comprehensive list of available parameters.

# Spreadsheets in an Ember Factory input file

The Excel workbooks may include up to 3 spreadsheets, of which only the first is mandatory:

- the 'data' spreadsheet contains metadata and embers data, describing the transitions. The first spreadsheet
is always used for data input, and may have any name. The format of this sheet can be "Basic" or "Fullflex" 
(see tutorial).
- the "Graph parameters" sheet is recognised by its name. It is optional and provides as many (and as little) 
parameters as desired, among those defined below. Those parameters are mostly related
to how the embers needs to be drawn - layout, ordering, additional information on the axis...
- the "Color definitions" sheet is recognised by its name. It is also optional, and describes sets of colours to
be used in ember gradients (see example in [Tutorial / Colour Palettes](tutorial#Colour)). 
For the "Fullflex" format, it also defines the risk index values for which colors are defined.

# Parameters in the 'data' spreadsheet

The parameters which can be provided in the 'data' spreadsheet are 

- metadata about the content of the file
- general information about how to plot the data in the embers, such as the name of the 'hazard' variable
  (e.g. 'mean surface temperature change') and the range of the 'hazard' (vertical) axis.
  By contrast to the parameters in the other sheets, those are simple parameters almost always made of a single value,
  and they must be 'data related' (layout-related parameters can only be in the Graph parameters sheet).

{INSERT:table1}

# Graph parameters sheet 

The "Graph parameters" sheet is an optional spreadsheet (its name cannot be changed).

In this sheet, parameters are made of a name (key) in column A, and one or more columns providing information. 
Lines which start with an empty first column are *comments*. 

In the Excel spreadsheets, a parameter has one of the two following structures:

||||||
|---|---|---|---|---|
|name | main value | optional unit of length for the layout ('cm' or 'mm')| | |
|name | main value | additional data 1 | additional data 2 | ...|

However, to facilitate the reading of the table of parameters provided below, the additional data is presented
here between square brackets rather than in separate columns, i.e. main value [add data 1, add data 2... ].

The specialized parameters are explained below, and a summary table is provided at the bottom of this page.

## Selecting and sorting embers

The purpose of these specific parameters is to generate different diagrams without changing the 'data' sheet.
Instead of manually moving data or deleting lines from the data sheet, you may list the ember names.
The easiest case is to sort embers by name without changing their groups. It is done like this:

||||||
|---|---|---|---|---|
|sort_2nd_by| Name | `name of ember wanted at 1st place` | `name of ember wanted at 2nd place` | ...|

The name of the parameter, 'sort_2nd_by', may look odd. The reason for that is that embers are first arranged
in groups (generating a panel of several embers with a common title and axis), then by name. 
*For most cases, you just need to know that 'sort_2nd_by' is the right parameter and that it needs to be followed by
"Name" (it means that embers within a group are sorted by name)*.
If an ember which is in the data does not have its name in the list in column C, D, E... then it will be omitted.
If there is nothing in column B, i.e. "Name" is deleted, no sorting will occur: it is a way to come back to the
order in your data without deleting the optional sorting list.

The other paramter, 'sort_first_by', is meant to control the ordering of groups. 
This handles more complex cases where the role of ember group names and embers names can be swapped. 
An example is provide in the workbook from Zommers et al.
2020, where the data is provided for RFC1 in all reports, then RFC2 etc. The sorting parameters make it possible
to re-arrange all embers by report: all RFCs in TAR, all RFCs in Smith et al. 2009, etc.
For more information, please e-mail philippe.marbaix@uclouvain.be.

## Positioning elements in the layout

The following diagram explains how ember figures are designed, using various parameters 
for setting the width and length of its components or the distance between these. As shown in the example files,
those parameters generally have a unit (such as 'cm'), to be provided in column C.

![Schematic illustration of graphic parameters](../static/ef-gp-definitions.png "Positional graphic parameters")

## Legend (colour bar) <a name="legpos"></a> 

This parameter controls how the whole "colour legend block" is positioned around the embers.

| Parameter            | Default  | Description                                             |
|----------------------|----------|---------------------------------------------------------|
|leg_pos               |under     | There are 5 permitted values for `leg_pos`: *under*, *right*, *in-grid-horizontal*, *in-grid-vertical*, and *none* (which results in the absence of legend); *in-grid-*... is specific to more complex figures in which there are at least two lines of "ember" groups, which form a "grid".|

## Grid lines and related hazard-level indications <a name="gridlines"></a> 

The parameters starting with `haz_grid_lines` control de axis tick marks and related horizontal grid lines.
`haz_grid_lines` controls the approximate number of main lines, which is software-adjusted. Other parameters
enable additional grid lines at user selected levels and even shaded areas, as illustrated 
in [SROCC example](examples/SROCC_SPM3.xlsx).

## Indicating confidence levels and highlighting transitions

The parameter `show_confidence` indicates whether confidence levels regarding the transitions must be drawn, and
where (as usual, on the right of the ember, or on the top of the embers). The symbols can be selected. For more
information, see "Confidence levels" in the table below.  

## Highlighting changes from one ember to the next trough lines

`show_changes` connects the given risk levels from each ember by a line (within a group of embers); 
to use, type 'True' in the first columns. The levels that needs to be connected are then provided in the 
next columns (see details in the table below).

{INSERT:table2}

