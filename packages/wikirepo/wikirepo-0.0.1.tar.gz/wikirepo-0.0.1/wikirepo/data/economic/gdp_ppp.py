# =============================================================================
# Functions querying 'P4010' (GDP PPP) information
#
# Contents
# --------
#   0. No Class
#       query_gdp_ppp
# =============================================================================

from wikirepo.data import data_utils

pid = 'P4010'
sub_pid = None
col_name = 'gdp_ppp'
col_prefix = None
ignore_char = ''
span = False

def query_gdp_ppp(dir_name=None,
                  ents_dict=None,
                  depth=0,
                  locations=None, 
                  time_lvl=None, 
                  timespan=None):
    """
    Queries the GDP PPP for given location(s) over the given time_lvl and timespan
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