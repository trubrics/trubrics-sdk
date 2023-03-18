# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.1] - 2023-03-18

### Added
- Custom type for streamlit FeedbackCollector
- Unit tests for streamlit FeedbackCollector
- Example code snippets for Demo app

## [1.3.0] - 2023-03-17

### Added
- A brand new, shiny FeedbackCollector for streamlit 🎉. Highlights:
  - A new demo app on Titanic, with options for auth directly in the CLI
  - New FeedbackCollector object that stores metadata of your models and dataset versions
  - New auth component for Trubrics platform
  - New st_feedback() component with multiple types available
  - Updated docs

### Fixed
- Flex dependencies versions
- Moved Streamlit, Gradio and Dash to extra_dependencies
- Moved feedback integrations to an integrations/ dir

## [1.2.9] - 2023-03-03

### Fixed

- Display up to 50 projects from Trubrics in `trubrics init`
- Add @lru_cache to get Idtoken upon each write
- Hide locals in typer print (for sensitive password on error)

## [1.2.8] - 2023-02-27

### Changed

- Refactored TrubricRun to include methods to generate a Trubric
- Update CLI docs and gifs

## [1.2.7] - 2023-02-26

### Fixed

- Added .json to python package

## [1.2.6] - 2023-02-24

### Changed

- Refactored CLI with rich prints
- Moved trubric_run_context path argument to `trubrics run` from `trubrics init`

## [1.2.5] - 2023-02-20

### Changed

- Change collaborators in feedback from email to display name
- Add archived projects filter in trubrics init

## [1.2.4] - 2023-02-20

### Added

- Python \_\_version\_\_ number in cli and \_\_init\_\_.py
- Add save_ui param to trubrics example-app in CLI

## [1.2.3] - 2023-02-16

### Fixed

- Added project_id to `trubrics init`

## [1.2.0] - 2023-02-15

### Changed

- `trubrics init` refactoring with authentication with Trubrics
- `trubrics run` refactoring to store validations to firestore (Trubrics DB)
- `Feedback` and `Trubric` have adapted data model
- Cleaned notebooks examples/ folder
- Updated docs and README with Trubrics platform references

### Added

- FeedbackCollector now has authentication for Trubrics users
- `Feedback` and `Trubric` have `save_ui()` methods for new DB

### Fixed

- Bumped streamlit version

## [1.1.1] - 2022-11-14

### Changed

- Allow for list types to be saved in result dict validation output
- Restricted extra_fields of `Trubric` pydantic model
- Changed `trubric_name` field to `name` in `Trubric` pydantic model

## [1.1.0] - 2022-11-02

### Added

- Getting started video to readme
- Features field for DataContext
- Integration with Gradio for collecting feedback
- Integration with Dash for collecting feedback

### Changed

- Adopted a functional approach to FeedbackCollector
- Separated feedback collector to collect and experiment functions
- Updated feedback collector readme and docs

## [1.0.2] - 2022-10-14

### Fixed

- Fixed github action to display changelog to release tag

## [1.0.1] - 2022-10-13

### Fixed

- Fixed save feedback log
- FeedbackCollector has simplified feedback form

## [1.0.0] - 2022-10-06

### Added

- New CHANGELOG.md
- New CONTRIBUTING.md

### Removed

- Getting started video from README and docs. Soon to be replaced with updated video

## [0.2.3] - 2022-10-03

### Added

- New metrics, cli & data_context docs

### Changed

- Restructure readme with examples that run
- Restructure docs to follow readme key features
- Complete unit tests for ModelValidator
- Separate out "contexts" from context.py into their respective folders

### Fixed

- PyPI packaged example data is now readable
