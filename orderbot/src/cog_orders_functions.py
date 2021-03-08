from orderbot.src.global_data import FILL_INPUT_TYPE
import orderbot.src.validators as validators
import orderbot.src.regexes as regexes
import orderbot.src.webOrderParser as webOrderParser

def input_parser_fill(arg_str: str):
    input_type = None
    if validators.valid_id_and_link(arg_str):
        input_type = FILL_INPUT_TYPE.ID_AND_LINK
        output_data = regexes.regex_id_and_link().match(arg_str).groups()
        output_data = (output_data[0].replace('\"', ''), output_data[1])
    elif validators.valid_link(arg_str):
        input_type = FILL_INPUT_TYPE.ONLY_LINK
        output_data = arg_str
    elif validators.valid_id_and_shorthand(arg_str):
        input_type = FILL_INPUT_TYPE.ID_AND_SHORTHAND
        output_data = regexes.regex_id_and_shorthand().match(arg_str).groups()
        output_data = (output_data[0].replace('\"', ''), output_data[1])
    elif validators.valid_shorthand(arg_str):
        input_type = FILL_INPUT_TYPE.ONLY_SHORTHAND
        output_data = arg_str
    elif validators.valid_id_and_p4type(arg_str):
        input_type = FILL_INPUT_TYPE.ID_AND_P4TYPE
        output_data = regexes.regex_id_and_p4type().match(arg_str).groups()
        output_data = (output_data[0].replace('\"', ''), output_data[1])
    elif validators.valid_p4type(arg_str):
        input_type = FILL_INPUT_TYPE.ONLY_P4TYPE
        output_data = arg_str
    
    return input_type, output_data

def input_extractor_fill(input_type: FILL_INPUT_TYPE, data: str):
    if input_type == FILL_INPUT_TYPE.ID_AND_SHORTHAND or input_type == FILL_INPUT_TYPE.ONLY_SHORTHAND:
        if data[0].isdigit():
            regex = regexes.regex_extract_shorthand()
        else:
            regex = regexes.regex_extract_shorthand_reverse()
        res = regex.findall(data.upper())

        if res[0][0].isdigit():
            count = [int(c[0]) for c in res[:]]
            shorthand = [c[1] for c in res[:]]
        else:
            shorthand = [c[0] for c in res[:]]
            count = [int(c[1]) for c in res[:]]

        remainder = regex.sub('', data).strip()
    elif input_type == FILL_INPUT_TYPE.ID_AND_P4TYPE or input_type == FILL_INPUT_TYPE.ONLY_P4TYPE:
        regex = regexes.regex_extract_p4types()

        shorthand = regex.findall(data.upper())
        count = [None] * len(shorthand)
        remainder = regex.sub('', data).strip()
    elif input_type == FILL_INPUT_TYPE.ID_AND_LINK or input_type == FILL_INPUT_TYPE.ONLY_LINK:
        shorthand, count = webOrderParser.get_lsts_from_web_order(data)
        remainder = ''

    return shorthand, count, remainder
