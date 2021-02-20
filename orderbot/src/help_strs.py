username_str = '\"<user name>\"'
alias_str = '\"<alias>\"'
discription_str = '\"<discription>\"'
identify_str = '<"user name" | "alias" | user id>'


BUY_BRIEF_STR = f"Add buy order"
BUY_USAGE_STR = f"<(link|amount shorthand)>"
BUY_HELP_STR = f"""Add a buy order.

    {'<(link|amount shorthand)>':20} - The argument for the command can be an appraisal link form either janice.e-351.com/ or http://evepraisal.com/, alternatively a text string of amount follow by shorthand.

    Examples:
    \t!buy https://janice.e-351.com/a/CaukRs
    \t!buy http://evepraisal.com/a/ykpgr
    \t!buy 234 SC 184 NF 100 IRD 184 OMA 53 BN 53 SHPC 53 RCM 40 WM"""

FILL_BRIEF_STR = f"Fill a buy order"
FILL_USAGE_STR = f'{identify_str} <(link|amount shorthand)>'
FILL_HELP_STR = f"""Fill a buy order.

    {identify_str:20} - Either name, alias or ID or buyer.
    {'<(link|amount shorthand)>':20} - The argument for the command can be an appraisal link form either janice.e-351.com/ or http://evepraisal.com/, alternatively a text string of amount follow by shorthand.

    Examples:
    \t!buy Neorim" https://janice.e-351.com/a/CaukRs
    \t!buy Neo http://evepraisal.com/a/ykpgr
    \t!buy 14 234 SC 184 NF 100 IRD 184 OMA 53 BN 53 SHPC 53 RCM 40 WM"""

CANCELFILL_BRIEF_STR = f"NOT YET IMPLEMENTED"
CANCELFILL_USAGE_STR = f"NOT YET IMPLEMENTED"
CANCELFILL_HELP_STR = f"NOT YET IMPLEMENTED"

LIST_BRIEF_STR = f"List all buy orders"
LIST_USAGE_STR = f""
LIST_HELP_STR = f"""List all the current ourstanding buy orders.

    Examples:
    \t!list
    """

CANCELBUY_BRIEF_STR = f"Cancel an buy order"
CANCELBUY_USAGE_STR = f"<order id>"
CANCELBUY_HELP_STR = f"""Cancel an outstanding buy order.
    !! This command is limited to registered users !!

    {'<order id>':20} - The id of the target order.

    Example:
    \t!cancelbuy 58
    """

ADDUSER_BRIEF_STR = f"Add a user"
# user_name: str, alias: str, priority: int, disc: str)
ADDUSER_USAGE_STR = f"\"<user name>\" \"<alias>\" <priority> \"<discription>\""
ADDUSER_HELP_STR = f"""Add a user as a buyer
    !! This command is limited to registered users !!

    {username_str:20} - The user name, as displayed on Discord.
    {alias_str:20} - The wanted alias, used for identifying buyer in fill orders. Should be short.
    {'<priority>':20} - The priority of the buyer. (Future feature - filling orders buy priority).
    {discription_str:20} - Add a descripion of the user dor identification.

    Example:
    \t!adduser Neorim Neo 5 "The creater of the bot"
    """

REMOVEUSER_BRIEF_STR = f"Remove a user"
REMOVEUSER_USAGE_STR = f"\"<user name>\""
REMOVEUSER_HELP_STR = f"""Removes a user as a buyer
    !! This command is limited to registered users !!

    {username_str:20} - The user name, as displayed on Discord.

    Example:
    \t!removeuser Neorim
    """

LISTUSERS_BRIEF_STR = f"List the buy order users"
LISTUSERS_USAGE_STR = f""
LISTUSERS_HELP_STR = f"""List all user capable of creating buy orders

    Example:
    \t!listusers
    """
