# Changelog

All notable changes to ergodspy will be documented in this file.

## [0.1.1] - 2025-01-27

### Added
- New semicolon syntax for combining type and description: `"field: type; description"`
  - Example: `"confidence: float; Confidence score from 0-1"`
  - Cleaner than quoted descriptions: `"confidence: float 'Confidence score'"`
- Both syntaxes are supported for backward compatibility

### Fixed
- Maintained support for quoted description syntax alongside new semicolon syntax

## [0.1.0] - 2025-01-27

### Added
- Initial release
- `make_sig()` function for creating DSPy signatures with minimal syntax
- Support for multiple field formats:
  - Simple names: `"field"`
  - With types: `"field: type"`
  - With descriptions: `"field: 'description'"`
  - Tuple formats: `("field", type)`, `("field", "description")`, `("field", type, "description")`
- Progressive complexity - start simple, add details as needed
- Full DSPy compatibility