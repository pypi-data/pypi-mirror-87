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

# Get values of the no_tags_in_toot option of the hashtaglist section
'''Get values of the no_tags_in_toot option of the hashtaglist section'''

def parsenotagsintoot(config):
    '''Parse configuration values and get values of the the no_tags_in_toot option of the hashtaglist section'''
    section = 'hashtaglist'
    option = 'no_tags_in_toot'
    notagsintoot = False
    if config.has_option(section, option):
        notagsintoot = config.getboolean(section, option)
    return notagsintoot
