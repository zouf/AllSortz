#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nightout.settings")
    from validation.views import val_nmf
    pargs = []
    

    lower_bd = int(sys.argv[1])
    upper_bd = int(sys.argv[2])
    steps = int(sys.argv[3])
    print("Running Code with K-values " + str(lower_bd) + " to " + str(upper_bd) + " step = " + str(steps))
    val_nmf(range(lower_bd, upper_bd, 2),steps)
