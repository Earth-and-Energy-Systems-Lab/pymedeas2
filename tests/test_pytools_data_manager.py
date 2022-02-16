import pytest

import pandas as pd

import pytools.data_manager as dm


@pytest.mark.parametrize(
    "filename",
    [
        (  # BAU_full
            "tests/data/results_BAU_1995_2050_0.03125.csv"
        )
    ],
    ids=["BAU_full"]
)
class TestDataFile:
    """test for data coming from model outputs"""

    @pytest.fixture()
    def data_file(self, proj_folder, filename):
        """return data file object"""
        return dm.DataFile(proj_folder.joinpath(filename))

    def test_metadata(self, proj_folder, filename, data_file):
        """test the main attributes"""
        assert data_file.filename == proj_folder.joinpath(filename)
        assert data_file.scenario == "BAU"

    def test_colnames(self, data_file):
        """test that colnames are correct"""
        assert hasattr(data_file, "variable_list")
        assert len(data_file.variable_list) > 1000
        assert len([var for var in data_file.variable_list if "[" in var]) == 0

    def test_set_var(self, data_file):
        """test that setting a var works perfect"""
        assert "gdp" not in data_file.cached_values
        assert data_file.current_var is None

        data_file.set_var("gdp")
        data_file.get_values()

        assert "gdp" in data_file.cached_values
        assert data_file.current_var == "gdp"

        data_file.set_var("gfcf_not_covered")
        data_file.get_values(("Construction",))

        assert "gfcf_not_covered" in data_file.cached_values
        assert data_file.current_var == "gfcf_not_covered"

        data_file.set_var("share_tech_change_fuel")
        data_file.get_values(("Construction", "electricity", "heat"))

        assert "share_tech_change_fuel" in data_file.cached_values
        assert data_file.current_var == "share_tech_change_fuel"


@pytest.mark.parametrize(
    "filename,transpose",
    [
        (  # BAU_full
            ("tests/data/results_BAU_1995_2050_0.03125.csv", True)
        )
    ],
    ids=["BAU_full"]
)
class TestDataLoaded:
    """test for data coming from model outputs"""

    @pytest.fixture()
    def data_file(self, proj_folder, filename, transpose):
        """return data file object"""
        if transpose:
            return dm.DataLoaded(
                "My scen",
                pd.read_csv(proj_folder.joinpath(filename), index_col=0).T)
        else:
            return dm.DataLoaded(
                "My scen",
                pd.read_csv(proj_folder.joinpath(filename),
                index_col=0))

    def test_metadata(self, data_file):
        """test the main attributes"""
        assert data_file.scenario == "My scen"

    def test_colnames(self, data_file):
        """test that colnames are correct"""
        assert hasattr(data_file, "variable_list")
        assert len(data_file.variable_list) > 1000
        assert len([var for var in data_file.variable_list if "[" in var]) == 0

    def test_set_var(self, data_file):
        """test that setting a var works perfect"""
        assert "gdp" not in data_file.cached_values
        assert data_file.current_var is None

        data_file.set_var("gdp")
        data_file.get_values()

        assert "gdp" in data_file.cached_values
        assert data_file.current_var == "gdp"

        data_file.set_var("gfcf_not_covered")
        data_file.get_values(("Construction",))

        assert "gfcf_not_covered" in data_file.cached_values
        assert data_file.current_var == "gfcf_not_covered"

        data_file.set_var("share_tech_change_fuel")
        data_file.get_values(("Construction", "electricity", "heat"))

        assert "share_tech_change_fuel" in data_file.cached_values
        assert data_file.current_var == "share_tech_change_fuel"
