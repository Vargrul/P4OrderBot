import pytest

import orderbot.src.cog_orders_functions as cog_orders_functions
from orderbot.src.global_data import FILL_INPUT_TYPE


# Parameters
test_data = [
    ('"Neorim Onix" https://janice.e-351.com/a/CaukRs', (FILL_INPUT_TYPE.ID_AND_LINK ,('Neorim Onix', 'https://janice.e-351.com/a/CaukRs'))),
    ('Neo https://janice.e-351.com/a/CaukRs', (FILL_INPUT_TYPE.ID_AND_LINK ,('Neo', 'https://janice.e-351.com/a/CaukRs'))),
    ('@Neorim https://janice.e-351.com/a/CaukRs', (FILL_INPUT_TYPE.ID_AND_LINK ,('@Neorim', 'https://janice.e-351.com/a/CaukRs'))),
    ('Neorim#0099 https://janice.e-351.com/a/CaukRs', (FILL_INPUT_TYPE.ID_AND_LINK ,('Neorim#0099', 'https://janice.e-351.com/a/CaukRs'))),
    ('3 https://janice.e-351.com/a/CaukRs', (FILL_INPUT_TYPE.ID_AND_LINK ,('3', 'https://janice.e-351.com/a/CaukRs'))),
    ('https://janice.e-351.com/a/CaukRs', (FILL_INPUT_TYPE.ONLY_LINK ,'https://janice.e-351.com/a/CaukRs'))
]
# Link tests
@pytest.mark.parametrize("input, expected", test_data)
def test_full_name_and_link(input, expected):
    assert cog_orders_functions.input_parser_fill(input) == expected


# Parameters
test_data = [
    ('"Neorim Onix" 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM', (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('Neorim Onix','234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'))),
    ('Neo 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM', (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('Neo','234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'))),
    ('@Neorim 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM', (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('@Neorim','234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'))),
    ('Neorim#0099 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM', (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('Neorim#0099','234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'))),
    ('3 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM', (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('3','234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'))),
    ('234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM', (FILL_INPUT_TYPE.ONLY_SHORTHAND, '234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'))
]
# Shorthand Tests
@pytest.mark.parametrize("input, expected", test_data)
def test_full_name_and_shorthand(input, expected):
    assert cog_orders_functions.input_parser_fill(input) == expected
    
# Parameters
test_data = [
    ('"Neorim Onix" SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234', (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('Neorim Onix','SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'))),
    ('Neo SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234', (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('Neo','SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'))),
    ('@Neorim SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234', (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('@Neorim','SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'))),
    ('Neorim#0099 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234', (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('Neorim#0099','SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'))),
    ('3 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234', (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('3','SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'))),
    ('SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234', (FILL_INPUT_TYPE.ONLY_SHORTHAND, 'SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'))
]

@pytest.mark.parametrize("input, expected", test_data)
def test_full_name_and_shorthand_reverse(input, expected):
    assert cog_orders_functions.input_parser_fill(input) == expected

test_data = [
    ('"Neorim Onix" SC NF IRD OMA BCN SHPC RCM WM', (FILL_INPUT_TYPE.ID_AND_P4TYPE, ('Neorim Onix','SC NF IRD OMA BCN SHPC RCM WM'))),
    ('Neo SC NF IRD OMA BCN SHPC RCM WM', (FILL_INPUT_TYPE.ID_AND_P4TYPE, ('Neo','SC NF IRD OMA BCN SHPC RCM WM'))),
    ('@Neorim SC NF IRD OMA BCN SHPC RCM WM', (FILL_INPUT_TYPE.ID_AND_P4TYPE, ('@Neorim','SC NF IRD OMA BCN SHPC RCM WM'))),
    ('Neorim#0099 SC NF IRD OMA BCN SHPC RCM WM', (FILL_INPUT_TYPE.ID_AND_P4TYPE, ('Neorim#0099','SC NF IRD OMA BCN SHPC RCM WM'))),
    ('3 SC NF IRD OMA BCN SHPC RCM WM', (FILL_INPUT_TYPE.ID_AND_P4TYPE, ('3','SC NF IRD OMA BCN SHPC RCM WM'))),
    ('SC NF IRD OMA BCN SHPC RCM WM', (FILL_INPUT_TYPE.ONLY_P4TYPE, 'SC NF IRD OMA BCN SHPC RCM WM'))
]

@pytest.mark.parametrize("input, expected", test_data)
def test_full_name_and_p4types(input, expected):
    assert cog_orders_functions.input_parser_fill(input) == expected
    
test_data = [
    ((FILL_INPUT_TYPE.ID_AND_SHORTHAND, '234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'), (['SC', 'NF', 'IRD', 'OMA', 'BCN', 'SHPC', 'RCM', 'WM'], [234, 184, 100, 184, 53, 53, 53, 40], '')),
    ((FILL_INPUT_TYPE.ID_AND_SHORTHAND, '234 SeC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'), (['NF', 'IRD', 'OMA', 'BCN', 'SHPC', 'RCM', 'WM'], [184, 100, 184, 53, 53, 53, 40], '234 SeC')),
    ((FILL_INPUT_TYPE.ONLY_SHORTHAND, 'SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'), (['SC', 'NF', 'IRD', 'OMA', 'BCN', 'SHPC', 'RCM', 'WM'], [184, 100, 184, 53, 53, 53, 40, 234], '')),
    ((FILL_INPUT_TYPE.ONLY_SHORTHAND, 'SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCEM 40 WM 234'), (['SC', 'NF', 'IRD', 'OMA', 'BCN', 'SHPC', 'WM'], [184, 100, 184, 53, 53, 53, 234], 'RCEM 40'))
]

@pytest.mark.parametrize("input, expected", test_data)
def test_extractor_normal(input, expected):
    assert cog_orders_functions.input_extractor_fill(*input) == expected

test_data = [
    ((FILL_INPUT_TYPE.ID_AND_P4TYPE, 'SC NF IRD OMA BCN SHPC RCM WM'), (['SC', 'NF', 'IRD', 'OMA', 'BCN', 'SHPC', 'RCM', 'WM'], [None, None, None, None, None, None, None, None], '')),
    ((FILL_INPUT_TYPE.ONLY_P4TYPE, 'SC NF IRD OMA BCN SeHPC RCM WM'), (['SC', 'NF', 'IRD', 'OMA', 'BCN', 'RCM', 'WM'], [None, None, None, None, None, None, None], 'SeHPC'))
]

@pytest.mark.parametrize("input, expected", test_data)
def test_extractor_shorthand(input, expected):
    assert cog_orders_functions.input_extractor_fill(*input) == expected

def test_normal_order():
    test_in = (FILL_INPUT_TYPE.ID_AND_LINK, 'https://janice.e-351.com/a/CaukRs')
    test_out = (['Sterile Conduits', 
        'Nano-Factory', 
        'Integrity Response Drones', 
        'Organic Mortar Applicators', 
        'Broadcast Node', 
        'Self-Harmonizing Power Core', 
        'Recursive Computing Module', 
        'Wetware Mainframe'], [234, 184, 100, 184, 53, 53, 53, 40], '')
    test_ret = cog_orders_functions.input_extractor_fill(*test_in)
    assert test_ret == test_out