#!/usr/bin/env python

"""
konvert.py
This script was created in order to backport KDE4/Konsole colorscheme based files into KDE3/Konsole schema files.
It uses a template.schema file. As it parses the colorscheme file, it puts the color field into a dictionary and
replaces the colors in the template.schema file.
This is a fairly basic hacky script, and is susceptible to breakage if the colorscheme file does not meet the format
that I anticipated while writing this. I have tried it on a couple of files and it seemed to work great.
It also does not support transparency/bold fields yet.

This script requires Python 2.7.
"""

import sys, re

# Read colorscheme file

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "This script converts a colorscheme file (used by KDE4 based Konsole) into a schema file (used by KDE3 based Konsole)"
        print "Essentially this backports a colorscheme to be able to use them on older versions of Konsole"
        print "Usage:"
        print "  konvert.py [input colorscheme file] [output schema name]"
        print "This generates a schema called = [output schema name] in a file called [output schema name].schema"
        sys.exit(0)

    in_file = sys.argv[1]
    out_file = sys.argv[2]

    with open(in_file, 'r') as f:
        in_list = f.read().split('\n')

    color_list = {}

    for line1,line2  in zip(in_list, in_list[1:]):
        # Check if the current line is the name of a color, and then put it in a key variable
        if re.match("\[.*\]",line1):
            key = line1
        # Check if the current line describes the color, and then use the previously assigned key variable
        elif re.match("Color=.*", line1):
            color_list[key] = line1

    print color_list

    template_file = "template.schema"

    with open(template_file, 'r') as f_template:
        with open(out_file + ".schema", 'w') as f_out:
            for in_line in f_template:
                if re.match("title \[.*\].*", in_line):
                    # Replace the title line with the parameter passed to the script
                    f_out.write("title " + out_file + "\n")
                elif re.match("color.*\[.*\]", in_line):
                    # w_m here finds the name of the color
                    w_m = re.match("color.*\[(.*)\]", in_line)
                    colortype = w_m.group(1)
                    # Get the colors line from the dictionary so we can substitute it in
                    colors = color_list["[" + colortype + "]"]
                    c_m = re.match("Color=([0-9]+),([0-9]+),([0-9]+)", colors)
                    r = c_m.group(1)
                    g = c_m.group(2)
                    b = c_m.group(3)
                    # Get the front portion of the original color line again (this describes the KDE3-base colors)
                    w_m = re.match("(color\s*[0-9]+).*", in_line)
                    color_label = w_m.group(1)
                    out_line = [color_label,
                                str(r),
                                str(g),
                                str(b),
                                '0',
                                '0',
                                '[' + colortype + ']',
                                '\n']
                    f_out.write(' '.join(out_line))
                else:
                    f_out.write(in_line)
    
