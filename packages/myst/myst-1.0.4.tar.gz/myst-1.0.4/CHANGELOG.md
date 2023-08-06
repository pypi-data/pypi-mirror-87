# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.4](https://pypi.org/project/myst/1.0.4/) - 2020-12-01

### Added

- Switched to using soft dependency matching in `requirements.txt` to play nicely with `pip` version 20.3's (see
  [`pip` changelog](https://pip.pypa.io/en/stable/news/) for details) new strict dependency resolution.

## [1.0.3](https://pypi.org/project/myst/1.0.3/) - 2020-08-27

### Added

- Improved authentication logic that only refreshes Google OAuth credentials when they expire, which reduces
  authentication rate limiting.

## [1.0.2](https://pypi.org/project/myst/1.0.2/) - 2020-03-30

### Added

- Improved retry logic that retries native Python errors, including network-related errors like `ConnectionError`.

### Changed

- Upgraded `google-auth` dependency to version 1.11.0.

## [1.0.1](https://pypi.org/project/myst/1.0.1/) - 2020-01-06

### Added

- Basic retry logic.
- Support for passing the `service_account_key_file_path` to `myst.authenticate` without having to also specify the `use_service_account` flag.

### Changed

- Renamed `TimeSeries.fetch_data` to `TimeSeries.fetch_data_series`.

## [1.0.0](https://pypi.org/project/myst/1.0.0/) - 2020-01-06 [YANKED]

### Added

- Basic retry logic.
- Support for passing the `service_account_key_file_path` to `myst.authenticate` without having to also specify the `use_service_account` flag.

## [0.1.1](https://pypi.org/project/myst/0.1.1/) - 2019-09-17

### Added

- First official `myst` release
- Support for authenticating using a Google User Account
- Support for authenticating with a Myst AI Service Account
- Support for listing, getting, and fetching data for `TimeSeries`
- Support for caching and clearing credentials locally

## [0.0.1](https://pypi.org/project/myst/0.0.1/) - 2019-05-01

### Added

- Initial empty `myst` release
