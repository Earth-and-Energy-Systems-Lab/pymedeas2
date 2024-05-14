import pytest

import pandas as pd

import tools.data_manager as dm


@pytest.mark.parametrize(
    "aggregation,region",
    [("14sectors_cat", "pymedeas_w")]
)
def test_data_container(proj_folder, doc):
    """Test the data container"""
    data_container = dm.DataContainer()
    data_container.add(
        dm.DataFile(
            proj_folder.joinpath(
                "tests/data/results_BAU_1995_2050_0.03125.csv")))

    variables = data_container.variable_list
    assert len(variables) > 1000
    assert len(data_container) == 1

    data_container.add(
        dm.DataFile(
            proj_folder.joinpath(
                "tests/data/unknown.csv")))

    assert variables == data_container.variable_list
    assert len(data_container) == 2

    data_container.add(
        dm.DataVensim(
            proj_folder.joinpath(
                "tests/data/vensim.tab"), doc))

    assert set(variables).issubset(data_container.variable_list)
    assert len(data_container) == 3

    data_container.set_var("gdp")
    assert not data_container.dimensions
    values = data_container.get_values()
    assert isinstance(values, dict)

    assert isinstance(values["BAU"], pd.Series)
    assert isinstance(values["Unknown"], pd.Series)
    assert isinstance(values["Vensim output"], pd.Series)

    data_container.set_var("gfcf_not_covered")
    assert data_container.dimensions

    data_container.clear()
    assert len(data_container) == 0


@pytest.mark.parametrize(
    "filename,scenario",
    [
        (  # BAU_full
            ("tests/data/results_BAU_1995_2050_0.03125.csv", "BAU")
        ),
        (  # Unknown
            ("tests/data/unknown.csv", "Unknown")
        )
    ],
    ids=["BAU_full", "Unknown"]
)
class TestDataFile:
    """test for data coming from model outputs"""

    @pytest.fixture()
    def data_file(self, proj_folder, filename):
        """return data file object"""
        return dm.DataFile(proj_folder.joinpath(filename))

    def test_metadata(self, proj_folder, filename, data_file, scenario):
        """test the main attributes"""
        assert data_file.filename == proj_folder.joinpath(filename)
        assert data_file.scenario == scenario

    def test_colnames(self, data_file, scenario):
        """test that colnames are correct"""
        assert hasattr(data_file, "variable_list")
        assert len(data_file.variable_list) > 1000
        assert len([var for var in data_file.variable_list if "[" in var]) == 0

    def test_set_get_var(self, data_file, scenario):
        """test that setting a var works"""
        assert "gdp" not in data_file.cached_values
        assert data_file.current_var is None

        data_file.set_var("gdp")
        assert isinstance(
            data_file.get_values(),
            pd.Series)

        assert "gdp" in data_file.cached_values
        assert data_file.current_var == "gdp"

        data_file.set_var("gfcf_not_covered")
        assert isinstance(
            data_file.get_values(("Construction",)),
            pd.Series)

        assert "gfcf_not_covered" in data_file.cached_values
        assert data_file.current_var == "gfcf_not_covered"

        data_file.set_var("share_tech_change_fuel")
        assert isinstance(
            data_file.get_values(("Construction", "electricity", "heat")),
            pd.Series)

        assert data_file.get_values(("Construction", "god", "heat")) is None

        assert "share_tech_change_fuel" in data_file.cached_values
        assert data_file.current_var == "share_tech_change_fuel"

        data_file.set_var("this var does not exist")
        assert data_file.get_values() is None

        assert "this var does not exist" in data_file.cached_values
        assert data_file.current_var == "this var does not exist"


@pytest.mark.parametrize(
    "filename",
    [
        (  # Vensim
            "tests/data/vensim.tab"
        )
    ],
    ids=["Vensim"]
)
@pytest.mark.parametrize(
    "aggregation,region",
    [("14sectors_cat", "pymedeas_w")]
)
class TestDataVensim:
    """test for data coming from Vensim outputs"""

    @pytest.fixture()
    def data_file(self, proj_folder, filename, doc):
        """return data file object"""
        return dm.DataVensim(proj_folder.joinpath(filename), doc)

    def test_metadata(self, proj_folder, filename, data_file):
        """test the main attributes"""
        assert data_file.filename == proj_folder.joinpath(filename)
        assert data_file.scenario == "Vensim output"

    def test_colnames(self, data_file):
        """test that colnames are correct"""
        assert hasattr(data_file, "variable_list")
        assert len(data_file.variable_list) > 1000
        assert len([var for var in data_file.variable_list if "[" in var]) == 0

    def test_set_get_var(self, data_file):
        """test that setting a var works"""
        assert "gdp" not in data_file.cached_values
        assert data_file.current_var is None

        data_file.set_var("gdp")
        assert isinstance(
            data_file.get_values(),
            pd.Series)

        assert "gdp" in data_file.cached_values
        assert data_file.current_var == "gdp"

        data_file.set_var("gfcf_not_covered")
        assert isinstance(
            data_file.get_values(("Construction",)),
            pd.Series)

        assert "gfcf_not_covered" in data_file.cached_values
        assert data_file.current_var == "gfcf_not_covered"

        data_file.set_var("share_tech_change_fuel")
        assert isinstance(
            data_file.get_values(("Construction", "electricity", "heat")),
            pd.Series)

        assert data_file.get_values(("Construction", "god", "heat")) is None

        assert "share_tech_change_fuel" in data_file.cached_values
        assert data_file.current_var == "share_tech_change_fuel"

        data_file.set_var("this var does not exist")
        assert data_file.get_values() is None

        assert "this var does not exist" in data_file.cached_values
        assert data_file.current_var == "this var does not exist"
