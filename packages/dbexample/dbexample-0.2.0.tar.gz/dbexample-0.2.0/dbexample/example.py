# Create an object named `catalog_instance` which is referenced in the
# setup.py, and will be discovered by databroker. How the instance is
# created, and what type of catalog it is, is completely up to the
# implementation. This is just one possible example.
import intake
from pkg_resources import resource_filename

# the directory with the msgpack files
data_dir = resource_filename("dbexample", "data")

# Look up a driver class by its name in the registry.
catalog_class = intake.registry['bluesky-msgpack-catalog']

catalog_instance = catalog_class(
    paths=r"{}/*.msgpack".format(data_dir)
)
