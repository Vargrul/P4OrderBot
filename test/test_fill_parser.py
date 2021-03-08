import unittest

import  orderbot.src.cog_orders_functions as cog_orders_functions
from orderbot.src.global_data import FILL_INPUT_TYPE

class TestFillParserLink(unittest.TestCase):
    # Link tests
    def test_full_name_and_link(self):
        test_in = '"Neorim Onix" https://janice.e-351.com/a/CaukRs'
        test_out = (FILL_INPUT_TYPE.ID_AND_LINK ,('Neorim Onix', 'https://janice.e-351.com/a/CaukRs'))
        test_ret = cog_orders_functions.input_parser_fill(test_in)
        self.assertEqual(test_ret, test_out)
    
    def test_alias_and_link(self):
        test_in = 'Neo https://janice.e-351.com/a/CaukRs'
        test_out = (FILL_INPUT_TYPE.ID_AND_LINK ,('Neo', 'https://janice.e-351.com/a/CaukRs'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_at_name_and_link(self):
        test_in = '@Neorim https://janice.e-351.com/a/CaukRs'
        test_out = (FILL_INPUT_TYPE.ID_AND_LINK ,('@Neorim', 'https://janice.e-351.com/a/CaukRs'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_disc_name_id_and_link(self):
        test_in = 'Neorim#0099 https://janice.e-351.com/a/CaukRs'
        test_out = (FILL_INPUT_TYPE.ID_AND_LINK ,('Neorim#0099', 'https://janice.e-351.com/a/CaukRs'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_id_and_link(self):
        test_in = '3 https://janice.e-351.com/a/CaukRs'
        test_out = (FILL_INPUT_TYPE.ID_AND_LINK ,('3', 'https://janice.e-351.com/a/CaukRs'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_only_link(self):
        test_in = 'https://janice.e-351.com/a/CaukRs'
        test_out = (FILL_INPUT_TYPE.ONLY_LINK ,'https://janice.e-351.com/a/CaukRs')
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)

class TestFillParserShorthand(unittest.TestCase):
    # Shorthand Tests
    def test_full_name_and_shorthand(self):
        test_in = '"Neorim Onix" 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'
        test_out = (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('Neorim Onix','234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_alias_and_shorthand(self):
        test_in = 'Neo 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'
        test_out = (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('Neo','234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_at_name_and_shorthand(self):
        test_in = '@Neorim 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'
        test_out = (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('@Neorim','234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_disc_name_id_and_shorthand(self):
        test_in = 'Neorim#0099 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'
        test_out = (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('Neorim#0099','234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_id_and_shorthand(self):
        test_in = '3 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'
        test_out = (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('3','234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_only_shorthand(self):
        test_in = '234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM'
        test_out = (FILL_INPUT_TYPE.ONLY_SHORTHAND, '234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM')
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
class TestFillParserShorthandOpposite(unittest.TestCase):
    # Shorthand Tests
    def test_full_name_and_shorthand(self):
        test_in = '"Neorim Onix" SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'
        test_out = (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('Neorim Onix','SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_alias_and_shorthand(self):
        test_in = 'Neo SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'
        test_out = (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('Neo','SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_at_name_and_shorthand(self):
        test_in = '@Neorim SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'
        test_out = (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('@Neorim','SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_disc_name_id_and_shorthand(self):
        test_in = 'Neorim#0099 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'
        test_out = (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('Neorim#0099','SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_id_and_shorthand(self):
        test_in = '3 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'
        test_out = (FILL_INPUT_TYPE.ID_AND_SHORTHAND, ('3','SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_only_shorthand(self):
        test_in = 'SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234'
        test_out = (FILL_INPUT_TYPE.ONLY_SHORTHAND, 'SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234')
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)

class TestFillParserP4Type(unittest.TestCase):
    # P4Types Tests
    def test_full_name_and_p4types(self):
        test_in = '"Neorim Onix" SC NF IRD OMA BCN SHPC RCM WM'
        test_out = (FILL_INPUT_TYPE.ID_AND_P4TYPE, ('Neorim Onix','SC NF IRD OMA BCN SHPC RCM WM'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_alias_and_p4types(self):
        test_in = 'Neo SC NF IRD OMA BCN SHPC RCM WM'
        test_out = (FILL_INPUT_TYPE.ID_AND_P4TYPE, ('Neo','SC NF IRD OMA BCN SHPC RCM WM'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_at_name_and_p4types(self):
        test_in = '@Neorim SC NF IRD OMA BCN SHPC RCM WM'
        test_out = (FILL_INPUT_TYPE.ID_AND_P4TYPE, ('@Neorim','SC NF IRD OMA BCN SHPC RCM WM'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_disc_name_id_and_p4types(self):
        test_in = 'Neorim#0099 SC NF IRD OMA BCN SHPC RCM WM'
        test_out = (FILL_INPUT_TYPE.ID_AND_P4TYPE, ('Neorim#0099','SC NF IRD OMA BCN SHPC RCM WM'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_id_and_p4types(self):
        test_in = '3 SC NF IRD OMA BCN SHPC RCM WM'
        test_out = (FILL_INPUT_TYPE.ID_AND_P4TYPE, ('3','SC NF IRD OMA BCN SHPC RCM WM'))
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)
    
    def test_only_p4types(self):
        test_in = 'SC NF IRD OMA BCN SHPC RCM WM'
        test_out = (FILL_INPUT_TYPE.ONLY_P4TYPE, 'SC NF IRD OMA BCN SHPC RCM WM')
        self.assertEqual(cog_orders_functions.input_parser_fill(test_in), test_out)

class TestFillExtractorShorthand(unittest.TestCase):
    def test_normal_order(self):
        test_in = (FILL_INPUT_TYPE.ID_AND_SHORTHAND, '234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM')
        test_out = (['SC', 'NF', 'IRD', 'OMA', 'BCN', 'SHPC', 'RCM', 'WM'], [234, 184, 100, 184, 53, 53, 53, 40], '')
        test_ret = cog_orders_functions.input_extractor_fill(*test_in)
        self.assertEqual(test_ret, test_out)

    def test_normal_order_typo(self):
        test_in = (FILL_INPUT_TYPE.ID_AND_SHORTHAND, '234 SeC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM')
        test_out = (['NF', 'IRD', 'OMA', 'BCN', 'SHPC', 'RCM', 'WM'], [184, 100, 184, 53, 53, 53, 40], '234 SeC')
        test_ret = cog_orders_functions.input_extractor_fill(*test_in)
        self.assertEqual(test_ret, test_out)


    def test_reverse_order(self):
        test_in = (FILL_INPUT_TYPE.ONLY_SHORTHAND, 'SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234')
        test_out = (['SC', 'NF', 'IRD', 'OMA', 'BCN', 'SHPC', 'RCM', 'WM'], [184, 100, 184, 53, 53, 53, 40, 234], '')
        test_ret = cog_orders_functions.input_extractor_fill(*test_in)
        self.assertEqual(test_ret, test_out)

    def test_reverse_order_typo(self):
        test_in = (FILL_INPUT_TYPE.ONLY_SHORTHAND, 'SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCEM 40 WM 234')
        test_out = (['SC', 'NF', 'IRD', 'OMA', 'BCN', 'SHPC', 'WM'], [184, 100, 184, 53, 53, 53, 234], 'RCEM 40')
        test_ret = cog_orders_functions.input_extractor_fill(*test_in)
        self.assertEqual(test_ret, test_out)

class TestFillExtractorP4Only(unittest.TestCase):
    def test_normal_order(self):
        test_in = (FILL_INPUT_TYPE.ID_AND_P4TYPE, 'SC NF IRD OMA BCN SHPC RCM WM')
        test_out = (['SC', 'NF', 'IRD', 'OMA', 'BCN', 'SHPC', 'RCM', 'WM'], [None, None, None, None, None, None, None, None], '')
        test_ret = cog_orders_functions.input_extractor_fill(*test_in)
        self.assertEqual(test_ret, test_out)

    def test_normal_order_typo(self):
        test_in = (FILL_INPUT_TYPE.ONLY_P4TYPE, 'SC NF IRD OMA BCN SeHPC RCM WM')
        test_out = (['SC', 'NF', 'IRD', 'OMA', 'BCN', 'RCM', 'WM'], [None, None, None, None, None, None, None], 'SeHPC')
        test_ret = cog_orders_functions.input_extractor_fill(*test_in)
        self.assertEqual(test_ret, test_out)

class TestFillExtractorLink(unittest.TestCase):
    def test_normal_order(self):
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
        self.assertEqual(test_ret, test_out)

# #  ID and Link
# !fill "Neorim Onix" https://janice.e-351.com/a/CaukRs
# !fill Neo https://janice.e-351.com/a/CaukRs
# !fill @Neorim https://janice.e-351.com/a/CaukRs
# !fill Neorim#0099 https://janice.e-351.com/a/CaukRs
# !fill 3 https://janice.e-351.com/a/CaukRs
# # Link Only
# !fill https://janice.e-351.com/a/CaukRs

# # ID and Shorthand
# !fill "Neorim Onix" 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM
# !fill Neo 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM
# !fill @Neorim 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM
# !fill Neorim#0099 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM
# !fill 3 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM
# # Shorthand Only
# !fill 234 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM

# # ID and Shorthand Opposite Order
# "Neorim Onix" SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234
# Neo SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234
# @Neorim SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234
# Neorim#0099 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234
# 3 SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234
# # Shorthand Only Opposite Order
# SC 184 NF 100 IRD 184 OMA 53 BCN 53 SHPC 53 RCM 40 WM 234

# # ID and P4TYPE
# !fill "Neorim Onix" SC NF IRD OMA BCN SHPC RCM WM
# !fill Neo SC NF IRD OMA BCN SHPC RCM WM
# !fill @Neorim SC NF IRD OMA BCN SHPC RCM WM
# !fill Neorim#0099 SC NF IRD OMA BCN SHPC RCM WM
# !fill 3 SC NF IRD OMA BCN SHPC RCM WM
# # P4TYPE only
# !fill SC NF IRD OMA BCN SHPC RCM WM

if __name__ == '__main__':
    unittest.main()