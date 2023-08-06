# =============================================================================
# Functions querying 'PXYZ' (freedom house category) information
#
# This is done via 'P1552' (has quality) applied to regions
# Idealy a property would be created for this that would allow it to be traced over time
#
# Contents
# --------
#   0. No Class
#       query_fh_category
# =============================================================================

from wikirepo.data import data_utils

pid = 'P1552'
sub_pid = None
col_name = 'fh_category'
col_prefix = None
ignore_char = ' country'
span = False

def query_fh_category(dir_name=None,
                      ents_dict=None,
                      depth=0,
                      locations=None, 
                      time_lvl=None, 
                      timespan=None):
    """
    Queries the freedom house catefory for given location(s) over the given time_lvl and timespan
    """
    df, ents_dict = data_utils.query_wd_prop(dir_name=dir_name,
                                             ents_dict=ents_dict,
                                             depth=depth,
                                             locations=locations, 
                                             time_lvl=time_lvl, 
                                             timespan=timespan,
                                             pid=pid,
                                             sub_pid=sub_pid,
                                             col_name=col_name,
                                             col_prefix=col_prefix,
                                             ignore_char=ignore_char,
                                             span=span)

    return df, ents_dict