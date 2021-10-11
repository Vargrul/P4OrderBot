## [0.1b3] - NotReleased
- Changed from PICKL to PostgreSQL for proper database handling.
- TODO!: Still need some of the functions from the order controller to the database_ctrl/ctrl.py

## [0.1b2] - 2021-03-08
### Added
- !fill command now gives and error is the order would be over filled
- !fill command can now be used without amount and filled whatever is needed. An error for the entire input will be produced if one or more input item is not needed.
- !fill command now works without an ID if there is only one(1) order currently available.

### Changed
- Commands are now case insensitive.
- PI shorthand are now case insensitive
- the !list command will now display a better message if there are no orders.
- The alias for !fill identifier is now case insensitive.
- An error in P4 shorthand will now return the error part to the author.
- The commands are now in categories in the !help command.
- Internally refactored a lot of bot code. (crosses fingers for no new bugs...)
- !fill command now gives an improved response message.

### Fixed
- Fixed an typo in the shorthand error message.

## [0.1b1] - 2021-02-26
### Added
- Initial Release for the versioned OrderBot.
- Version numbering to the module.
- !version command was added to get the current version and changelog of the bot within discord.