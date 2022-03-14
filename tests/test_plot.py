import pytest

from plot_tool import main

all_regions = ["pymedeas_w", "pymedeas_eu", "pymedeas_cat"]


@pytest.mark.skip(reason="not implemented")
@pytest.mark.parametrize("region", all_regions, ids=all_regions)
def test_open_plot_tool(default_config):
    """Run of the 3 models in cascade"""
    main(default_config)
