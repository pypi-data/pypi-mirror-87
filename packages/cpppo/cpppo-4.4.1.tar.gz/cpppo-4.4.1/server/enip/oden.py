
# 
# Cpppo -- Communication Protocol Python Parser and Originator
# 
# Copyright (c) 2016, Hard Consulting Corporation.
# 
# Cpppo is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.  See the LICENSE file at the top of the source tree.
# 
# Cpppo is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# 

from __future__ import absolute_import, print_function, division
try:
    from future_builtins import zip, map # Use Python 3 "lazy" zip, map
except ImportError:
    pass

__author__                      = "Perry Kundert"
__email__                       = "perry@hardconsulting.com"
__copyright__                   = "Copyright (c) 2019 Hard Consulting Corporation"
__license__                     = "Dual License: GPLv3 (or later) and Commercial (see LICENSE)"

__all__				= ['oden']

from cpppo.server.enip.get_attribute import proxy

# Example of some Oden structs

class oden( proxy ):
    """Specific parameters and their addresses, for some known Oden structs in Rockwell CPUs."""
    PARAMETERS			= dict( proxy.PARAMETERS,
        line_tracability	= proxy.parameter(
            # The target Tag's symbolic address             
            'Line_Tracability',
            # The encoding of each record            
            [
                'DINT', # DINT       Station_Number
                'DINT', # COUNTER ?  Cycle_Counter
                'DINT', # DINT       Part_Type
                'REAL', # REAL       Cycle_Time
                'BOOL', # BOOL       Station_Blocked
                'BOOL', # BOOL       Station_Starved
                'BOOL', # BOOL       Operator_Needs_Assistance
                'BOOL', # BOOL       Operator_Needs_Parts
	    ],
            # A description of the structure encoding
            'Line Tracability Structure' ),
    )

def main():
    with oden( 'localhost' ) as o:
        for i,r in enumerate(o.read(o.parameter_substitution('Line_Tracability'))):
            print("%3d: %r" % ( i, r ))
