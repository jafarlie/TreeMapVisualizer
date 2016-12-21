"""Assignment 2: Modelling Population Data

=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a new class, PopulationTree, which is used to model
population data drawn from the World Bank API.
Even though this data has a fixed hierarchichal structure (only three levels:
world, region, and country), because we are able to model it using an
AbstractTree subclass, we can then run it through our treemap visualisation
tool to get a nice interactive graphical representation of this data.

NOTE: You'll need an Internet connection to access the World Bank API
to get started working on this assignment.

Recommended steps:
1. Read through all docstrings in this files once. There's a lot to take in,
   so don't feel like you need to understand it all the first time.
   It may be helpful to draw a small diagram of how all the helper functions
   fit together - we've provided most of the structure for you already.
2. Complete the helpers _get_population_data and _get_region_data.
   Both of these can be completed without recursion or any use of trees
   at all: they are simply exercises in taking some complex JSON data,
   and extracting the necessary information from them.
3. Review the PopulationTree constructor docstring. Note that when the first
   parameter is set to False, this behaves exactly the same as the
   AbstractTree constructor.
4. Complete _load_data. Use the PopulationTree constructor, but you should
   only need to pass in False for the first argument (this allows you to
   create the region and country nodes directly, without trying to access
   the World Bank API again).
"""
import json
import urllib.request as request

from tree_data import AbstractTree


# Constants for the World Bank API urls.
WORLD_BANK_BASE = 'http://api.worldbank.org/countries'
WORLD_BANK_POPULATIONS = (
    WORLD_BANK_BASE +
    '/all/indicators/SP.POP.TOTL?format=json&date=2014:2014&per_page=270'
)
WORLD_BANK_REGIONS = (
    WORLD_BANK_BASE + '?format=json&date=2014:2014&per_page=310'
)


class PopulationTree(AbstractTree):
    """A tree representation of country population data.

    This tree always has three levels:
      - The root represents the entire world.
      - Each node in the second level is a region (defined by the World Bank).
      - Each node in the third level is a country.

    The data_size attribute corresponds to the 2014 population of the country,
    as reported by the World Bank.

    See https://datahelpdesk.worldbank.org/ for details about this API.
    """
    def __init__(self, world, root=None, subtrees=None, data_size=0):
        """Initialize a new PopulationTree.

        If <world> is True, then this tree is the root of the population tree,
        and it should load data from the World Bank API.
        In this case, none of the other parameters are used.

        If <world> is False, pass the other arguments directly to the superclass
        constructor. Do NOT load new data from the World Bank API.

        @type self: PopulationTree
        @type world: bool
        @type root: object
        @type subtrees: list[PopulationTree] | None
        @type data_size: int
        """
        if world:
            region_trees = _load_data()
            AbstractTree.__init__(self, 'World', region_trees)
        else:
            if subtrees is None:
                subtrees = []
            AbstractTree.__init__(self, root, subtrees, data_size)

    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.
        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.
        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.
        @type self: PopulationTree
        @rtype: str
        """
        return "-->"

    def get_path(self, separator, node):
        """Returns path from root to the node
        @type self: PopulationTree
        @type separator: str
        @type node: PopulationTree
        @rtype: str
        """
        result_str = ""
        curr = node
        while curr.get_parent() is not None:
            result_str = separator + str(curr.get_root) + result_str
            curr = curr.get_parent()
        result_str = str(curr.get_root) + result_str
        return result_str


def _load_data():
    """Create a list of trees corresponding to different world regions.

    Each tree consists of a root node -- the region -- attached to one or
    more leaves -- the countries in that region.

    @rtype: list[PopulationTree]
    """
    lst = []
    lst2 = []
    # Get data from World Bank API.
    country_populations = _get_population_data()
    regions = _get_region_data()
    for i in regions.keys():   # i --> REGION
        for h in regions[i]:  # h --> COUNTRY
            if h in country_populations.keys():
                lst.append(PopulationTree(False, h, None, country_populations[h]))

        lst2.append(PopulationTree(False, i, lst))
        lst = []
    return lst2


def _get_population_data():
    """Return country population data from the World Bank.

    The return value is a dictionary, where the keys are country names,
    and the values are the corresponding populations of those countries.

    Ignore all countries that do not have any population data,
    or population data that cannot be read as an int.

    @rtype: dict[str, int]
    """
    # The first element returned is ignored because it's just metadata.
    # The second element's first 47 elements are ignored because they aren't
    # countries.
    _, population_data = _get_json_data(WORLD_BANK_POPULATIONS)
    population_data = population_data[47:]
    countries = {}
    for i in range(len(population_data)):
        if population_data[i]['country']['value']:
            if population_data[i]['value']:
                if int(population_data[i]['value']):
                    countries[population_data[i]['country']['value']] = int(population_data[i]['value'])
    return countries


def _get_region_data():
    """Return country region data from the World Bank.

    The return value is a dictionary, where the keys are region names,
    and the values a list of country names contained in that region.

    Ignore all regions that do not contain any countries.

    @rtype: dict[str, list[str]]
    """
    # We ignore the first component of the returned JSON, which is metadata.
    _, country_data = _get_json_data(WORLD_BANK_REGIONS)
    # The following line is a good place to put a breakpoint to help inspect
    # the contents of country_data.
    regions = {}
    for i in country_data:
        if "region" in i.keys():
            if "value" in i["region"].keys():
                if i["region"]["value"] != "Aggregates":
                    if "name" in i.keys():
                        if i["name"] != "":
                            if not i["region"]["value"] in regions.keys():
                                regions[i["region"]["value"]] = [i["name"]]
                            else:
                                regions[i["region"]["value"]].append(i["name"])
    return regions


def _get_json_data(url):
    """Return a dictionary representing the JSON response from the given url.

    You should not modify this function.

    @type url: str
    @rtype: Dict
    """
    response = request.urlopen(url)
    return json.loads(response.read().decode())


if __name__ == '__main__':
    import python_ta
    # Remember to change this to check_all when cleaning up your code.
    python_ta.check_all(config='pylintrc.txt')
