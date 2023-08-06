from io import StringIO
import turpy

# arbitrary string to be used as content for yaml
yaml_string = "test:\n  ok\nstatus:\n  True"

# Using the StringIO method to set as file object
file = StringIO(yaml_string)

def test_io_load_yaml(file):
    my_dict = load_yaml(filepath=file)
    assert my_dict is not None
    assert isinstance(my_dict, dict)


