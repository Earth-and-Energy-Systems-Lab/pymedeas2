"""
Module aggregated_indicators_i
Translated using PySD version 2.2.0
"""


def annual_tfes_intensity_change_rate():
    """
    Real Name: Annual TFES intensity change rate
    Original Eqn: -1+ZIDZ( TFES intensity EJ T$, TFES intensity EJ T$ delayed 1yr )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Annual TFES intensity change rate.
    """
    return -1 + zidz(tfes_intensity_ej_t(), tfes_intensity_ej_t_delayed_1yr())


def annual_tfes_intensity_change_rate_without_eroi():
    """
    Real Name: Annual TFES intensity change rate without EROI
    Original Eqn: -1+ZIDZ( TFES intensity EJ T$ without EROI, TFES intensity without EROI delayed 1yr )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Annual TFES intensity change rate without EROI.
    """
    return -1 + zidz(
        tfes_intensity_ej_t_without_eroi(), tfes_intensity_without_eroi_delayed_1yr()
    )


def annual_tpes_intensity_change_rate():
    """
    Real Name: Annual TPES intensity change rate
    Original Eqn: -1+ZIDZ( TPES intensity EJ T$, TPES intensity EJ T$ delayed 1yr )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Annual TPES intensity change rate.
    """
    return -1 + zidz(tpes_intensity_ej_t(), tpes_intensity_ej_t_delayed_1yr())


def cumulative_tfec_intensity_change_from_2009():
    """
    Real Name: Cumulative TFEC intensity change from 2009
    Original Eqn: IF THEN ELSE(Time<2009, 0, -1+(TFES intensity EJ T$/TFEC intensity until 2009))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        time() < 2009,
        lambda: 0,
        lambda: -1 + (tfes_intensity_ej_t() / tfec_intensity_until_2009()),
    )


def cumulative_tfec_intensity_change_from_2009_without_eroi():
    """
    Real Name: Cumulative TFEC intensity change from 2009 without EROI
    Original Eqn: IF THEN ELSE(Time<2009, 0, -1+(TFES intensity EJ T$ without EROI/TFEC intensity until 2009 without EROI))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        time() < 2009,
        lambda: 0,
        lambda: -1
        + (
            tfes_intensity_ej_t_without_eroi()
            / tfec_intensity_until_2009_without_eroi()
        ),
    )


def cumulative_tpes_intensity_change_from_2009():
    """
    Real Name: Cumulative TPES intensity change from 2009
    Original Eqn: IF THEN ELSE(Time<2009, 0, -1+(TPES intensity EJ T$/TPES intensity until 2009 ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Cumulative TPES intensity change from 2009.
    """
    return if_then_else(
        time() < 2009,
        lambda: 0,
        lambda: -1 + (tpes_intensity_ej_t() / tpes_intensity_until_2009()),
    )


def tfec_intensity_until_2009():
    """
    Real Name: TFEC intensity until 2009
    Original Eqn: SAMPLE IF TRUE(Time<2009, TFES intensity EJ T$, TFES intensity EJ T$)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    TFEC intensity until the year 2009.
    """
    return _sample_if_true_tfec_intensity_until_2009()


def tfec_intensity_until_2009_without_eroi():
    """
    Real Name: TFEC intensity until 2009 without EROI
    Original Eqn: SAMPLE IF TRUE(Time<2009, TFES intensity EJ T$ without EROI, TFES intensity EJ T$ without EROI)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    TFEC intensity without EROI until the year 2009.
    """
    return _sample_if_true_tfec_intensity_until_2009_without_eroi()


def tfes_intensity_ej_t():
    """
    Real Name: TFES intensity EJ T$
    Original Eqn: ZIDZ( Real TFEC, GDP EU )
    Units: EJ/T$
    Limits: (None, None)
    Type: component
    Subs: None

    Total final energy intensity.
    """
    return zidz(real_tfec(), gdp_eu())


def tfes_intensity_ej_t_delayed_1yr():
    """
    Real Name: TFES intensity EJ T$ delayed 1yr
    Original Eqn: DELAY FIXED ( TFES intensity EJ T$, 1, 8.827)
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    TFES intensity delayed 1 year.
    """
    return _delayfixed_tfes_intensity_ej_t_delayed_1yr()


def tfes_intensity_ej_t_without_eroi():
    """
    Real Name: TFES intensity EJ T$ without EROI
    Original Eqn: ZIDZ(Real TFEC, GDP EU)
    Units: EJ/T$
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(real_tfec(), gdp_eu())


def tfes_intensity_without_eroi_delayed_1yr():
    """
    Real Name: TFES intensity without EROI delayed 1yr
    Original Eqn: DELAY FIXED ( TFES intensity EJ T$ without EROI, 1, 8.827)
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    TFES intensity delayed 1 year.
    """
    return _delayfixed_tfes_intensity_without_eroi_delayed_1yr()


def tpes_intensity_ej_t():
    """
    Real Name: TPES intensity EJ T$
    Original Eqn: ZIDZ( TPES EJ, GDP EU )
    Units: EJ/Tdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary energy intensity.
    """
    return zidz(tpes_ej(), gdp_eu())


def tpes_intensity_ej_t_delayed_1yr():
    """
    Real Name: TPES intensity EJ T$ delayed 1yr
    Original Eqn: DELAY FIXED ( TPES intensity EJ T$, 1, 13.14)
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None

    TPES intensity delayed 1 year.
    """
    return _delayfixed_tpes_intensity_ej_t_delayed_1yr()


def tpes_intensity_until_2009():
    """
    Real Name: TPES intensity until 2009
    Original Eqn: SAMPLE IF TRUE(Time<2009, TPES intensity EJ T$, TPES intensity EJ T$)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    TPES intensity until the year 2009.
    """
    return _sample_if_true_tpes_intensity_until_2009()


_sample_if_true_tfec_intensity_until_2009 = SampleIfTrue(
    lambda: time() < 2009,
    lambda: tfes_intensity_ej_t(),
    lambda: tfes_intensity_ej_t(),
    "_sample_if_true_tfec_intensity_until_2009",
)


_sample_if_true_tfec_intensity_until_2009_without_eroi = SampleIfTrue(
    lambda: time() < 2009,
    lambda: tfes_intensity_ej_t_without_eroi(),
    lambda: tfes_intensity_ej_t_without_eroi(),
    "_sample_if_true_tfec_intensity_until_2009_without_eroi",
)


_delayfixed_tfes_intensity_ej_t_delayed_1yr = DelayFixed(
    lambda: tfes_intensity_ej_t(),
    lambda: 1,
    lambda: 8.827,
    time_step,
    "_delayfixed_tfes_intensity_ej_t_delayed_1yr",
)


_delayfixed_tfes_intensity_without_eroi_delayed_1yr = DelayFixed(
    lambda: tfes_intensity_ej_t_without_eroi(),
    lambda: 1,
    lambda: 8.827,
    time_step,
    "_delayfixed_tfes_intensity_without_eroi_delayed_1yr",
)


_delayfixed_tpes_intensity_ej_t_delayed_1yr = DelayFixed(
    lambda: tpes_intensity_ej_t(),
    lambda: 1,
    lambda: 13.14,
    time_step,
    "_delayfixed_tpes_intensity_ej_t_delayed_1yr",
)


_sample_if_true_tpes_intensity_until_2009 = SampleIfTrue(
    lambda: time() < 2009,
    lambda: tpes_intensity_ej_t(),
    lambda: tpes_intensity_ej_t(),
    "_sample_if_true_tpes_intensity_until_2009",
)
