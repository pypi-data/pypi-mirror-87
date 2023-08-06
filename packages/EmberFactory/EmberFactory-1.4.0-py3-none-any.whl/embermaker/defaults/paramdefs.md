<!--- 
This file provides  default values AND documentation of the parameters to the Ember Factory
Any line containing
- #, ##...
- the HTML tags <section>, <h3>, or <h4>
is only used for the documentation (thus parameter defaults or descriptions cannot contain any of these).
A parameter surrounded with <del>...</del> means that it is deprecated; no default will be read.
All parameters are made of a single value + an optional list part (called 'additional data'). 
Parameter values are strings by default; 
For other types, it must be indicated in the description: (number) means float, (length) means a lenght on the PDF page
-->

<section id="table1"> 

## Parameters allowed in the 'data' sheet
  
| Parameter              | Default value | Description                     |
|------------------------|---------------|---------------------------------|
|<h3> General metadata </h3>                                               ||
|project_name            | -             | A project name which could be used to identify these embers within a larger ensemble|
|project_source          | -             | Where the data is from, e.g. IPCC supplementary material X.SM.Y|
|project_revision_date   | -             | When the last important edit was done |
|project_version         | -             | An optional version              |
|project_data_verified   | -             | Whether you regard the data as fully verified; this may be important to track work on the file. You may use column C to provide detailed information on what is verified (or not). |
|<h3> 'Hazard' (vertical) scale</h3>                                        |||
|haz_name                | Global mean temperature change     | Name of the hazard variable, used as axis name |
|haz_name_std            | -             | Experimental. A standard name for the variable defining hazard levels. The purpose is to allow for conversion of hazard data from different embers to a common unit/variable. Currently used are GMST and GM-SST - names are not fully settled. If you wish to use, please contact us. |
|haz_unit                | °C            | Hazard axis unit, such as °C, °C/yr or ocean pH. Note: the unit will not be included in the labels if is included in haz_name, to avoid duplication|
|haz_axis_bottom         | 0             | The bottom of the hazard axis (number) |
|haz_axis_top            | 5             | The top of the hazard axis (number) |
|<del>haz_bottom_value</del>|            | Deprecated. Automatically converted to haz_axis_bottom (and haz_valid_bottom)|
|<del>haz_top_value</del>   |            | Deprecated. Automatically converted to haz_axis_top (and haz_valid_top) |
|<h4> haz_valid_* </h4>                  || The two parameters below define the 'valid' range of hazard values, i.e. range over which risks were assessed. These parameters are not actual *file* metadata: they are attributed to each ember provided in rows under the haz_range indication. A similar process was used in Zommers et al. 2020 to show the 'valid ranges' associated to several reports. As those parameters are new in the basic format, if you use them it would be good to inform us. |
|haz_valid_bottom        | -             | The bottom of the range of valid hazard values (number)|
|haz_valid_top           | -             | The top of the range of valid hazard values (number)|
|<h4> haz_map_* </h4>                    || Used to 'map' the hazard coordinate from the ember data to another coordinate, such as SST to GMST. In the future, this might potentially be replaced with 'unit conversion rules' based on `haz_name_std`. A warning is issued and included as information in the resulting PDF to limit the potential for confusion (number) |
|haz_map_factor          | -             | Multiplies all hazard values from embers data by the provided value (number) |
|haz_map_shift           | -             | Shifts all hazard values by the provided value (number) |
|<h3> Miscellanea </h3>                  |||
|software_version_min    | 1.2.0         | The minimum version of the software which is needed to use all information from this file. We hope to keep compatibility of existing files with future software, but a newer file may include information which old software does not use; it is especially the case when a new version is available for testing: if an older software is used, it may at least ignore some of the information in the new file. Used to produce a warning. |
</section> 

<section id="table2">

## List of graph parameters
 
| Parameter              | Default value | Description                     |
|------------------------|---------------|---------------------------------|
|<h3> Hazard-scale related grid-lines (horizontal lines) </h3>             |||
|haz_grid_lines          | 6 []          | The main value is an approximate indication of the desired axis tick-marks / grid lines, which will be rounded to a graph-adapted value by the software. The additional data provides a way to add custom grid-lines, such as for 1.5°C or the temperature at the start of a given time period (number) |
|haz_grid_lines_ends     | - []          | (main value: not used) The additional data provides a way to define shaded areas instead of grid lines, such as to illustrate temperatures during a certain time period ('recent', etc.). The previous parameter and this one jointly provide a way to define this range : haz_grid_lines provides the lower limit, haz_grid_lines_ends provides the upper limit; the second must be in the cell just below the first (number) |
|haz_grid_lines_labels   | - []          | (main value: not used) A label (name) for the custom grid-lines or shaded areas provided by the above parameters. The label must be indicated in a cell under the one providing the hazard level (i.e. in the same column as haz_grid_lines) (number) |
|haz_grid_lines_labels_off| - []         | (main value: not used) An offset for the position of the label on the axis, expressed as fraction of the height of fonts (e.g. to lower the label by its own size, type -1.0). Used to manually ajust labels so that they do not overlap. (number)|
|haz_grid_lines_colors   | - []          | (main value: not used) A color for the grid-lines or shaded areas provided above  |
|<h3> Colour palette selection </h3>
|be_palette              |               | The name of the desired colour palette. Available palettes include: RGB-SRCCL-C7, CMYK-SRCCL, CMYK-SR15, BW (black and white), RGB-TAR+VH (as in Zommers 2015). Palettes can also be entirely customized through an additional spreadsheet.|
|<h3> Legend (colour bar) </h3> |||
|leg_title               | Level of additional impact/risk due to climate change | The title to be written on top of the legend |
|leg_pos                 | Under         | Defines the position of the legend. Allowed values are *under*, *right*, *in-grid-horizontal*, *in-grid-vertical* (more details are provided above) ||
|<h3> Special parameters </h3>           |||
|show_changes            | False [1.5]   | When set to 'True', results in a dashed line connecting one ember to the next at a certain risk level. In the basic format, risk levels are defined as follows: undetectable=0, moderate=1, high=2, very high=3 (thus a value of 1.5 would connect the midpoints between moderate and high risk)   |
|sort_first_by           | - []          | Requests a sorting of embers which will produce new 'groups of embers'. Rarely used, but an example is [RFCs-data-2020_01_26-Z2020_rev1_byPubli.xlsx](examples/RFCs-data-2020_01_26-Z2020_rev1_byPubli.xlsx)  |
|sort_2nd_by             | - []          | Requests a sorting of embers which within groups. Commonly used with the main value set to "Name", then listing embers names in the desired order. This also selects embers: embers which are not included in this list will be ignored in the graphic.||
|max_gr_line             | 3             | The maximum number of ember groups on a "line of embers" in the graphic. After that number of groups, the next line starts (number)|
|<h3> Confidence levels </h3>     |||
|show_confidence         | True          | "True" or "Right" provide the traditional IPCC confidence marks. "On top" will draw confidence mark on top of the ember colours. Also provides the vertical lines used in recent IPCC reports to highlight the ranges of risk (colour) transitions. If False or empty, confidence levels are not shown.|
|conf_levels_file        | -   [Low;Medium;High;Very high] | The confidence level names used in defining your embers. |
|conf_levels_graph       | 1.9 [•;••;•••;••••]             | The size of the confidence level marks (number) and the symbols for the confidence levels, corresponding to the names in the previous line. For text labels, use e.g. 1.0 [L, M, H, VH] |
|conf_fnt_name           | Helvetica                       | Name of the font used for the confidence level marks |
|<h3> Fonts </h3>                        |
|fnt_size                | 10            | The main font size, used e.g. for the ember names (number) |
|fnt_name                | Helvetica     | The main font name; *font names are currently limited to standard PDF fonts* |
|gr_fnt_size             | 12            | The font size used for the ember goup names, which is indicated on top of the embers (number) |
|<h3> Layout positions </h3>          |||   
|<h4> Embers - y axis (vertical) </h4>          |||
|be_top_y                | 1.8 cm        | Description: see above diagram (length)	     |
|be_y                    | 8.4 cm        | (length)
|be_bot_y                | 1.6 cm        | (length)
|<h4> Embers - x axis (horizontal) </h4>          |||
|be_int_x	             | 1.3 cm        | (length)
|be_x	                 | 1.0 cm        | (length)
|gr_int_x                | 1 cm          | (length)
|scale_x                 | 1 cm          | (length)
|haz_name_x              | 1 cm          | (length)
|<h4> Legend </h4>     |||
|leg_top_y               | 1 cm          | (length)
|leg_y	                 | 1 cm          | (length)
|leg_bot_y	             | 0.9 cm        | (length)
|leg_x	 	             | 7 cm          | (length)
</section>
