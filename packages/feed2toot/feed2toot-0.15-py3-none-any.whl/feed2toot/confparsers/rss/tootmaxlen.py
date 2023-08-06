# -*- coding: utf-8 -*-
# Copyright © 2015-2020 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/

# Get value of the toot/tweet option of rss section
'''Get value of the toot/tweet option of the rss section'''

# standard library imports
import sys
import logging

def parsetootmaxlen(config):
    '''Parse configuration value of the toot_max_len option of the rss section'''
    section = 'rss'
    tootmaxlen = 500
    if config.has_section(section):
        ############################
        # toot_max_len parameter
        ############################
        confoption = 'toot_max_len'
        if config.has_option(section, confoption):
            try:
                tootmaxlen = int(config.get(section, confoption))
            except ValueError as err:
                sys.exit('Error in configuration with the {confoption} parameter in [{section}]: {err}'.format(confoption=confoption, section=section, err=err))
    return tootmaxlen
