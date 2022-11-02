# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
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
