# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

- Nothing yet!

## [1.0.0] - 2021-06-28

### Added

- Added signup email validator
- Added update file feature with bootstrap modal view to myfiles page
- Added check and revoke access shared with user feature to myfile page
(on click shared button)
- Added multi-delete file feature with checkbox and bootstrap modal view
to myfiles page
- Added modified datetime to detail view
- Added success, error, warning, info messages for some actions (delete,
share, revoke, login, signup, upload file, update file, multi-delete)
- Added user name to navbar
- Added bootstrap modal upload view to myfiles page
- Added bootstrap modal detail view to sharedfiles page and admin page
- Added expandAll and closeAll feature for look shared user to myfiles
and admin page
- Added file name to delete confirm modal
- Added help text for password to Sign Up page
- Added hamburger menu to navbar
- Added check shared with user feature to adminpage (on click shared
button)

### Changed

- Changed detail view to bootstrap modal view on myfiles page
- Changed background white to dynamic color
- Changed file title to uploader name on detail veiw
- Showing file type ext on detail view
- Detail view changed to modal view on myfiles page
- Datetime on adminpage, myfiles and sharedfiles humanized
- On Login and Sign Up page changed simple layout to floating layout
- Navbar color changed to dark
- File table changed totally on admin view
- Removed file size from table

### Fixed

- Fixed share dropdown onclick inside close
- Fixed share dropdown onclick email no checking
- Fixed detail view showing delete confirm message
- Fixed detail view description alert head
- Fixed share button position
- Fixed admin page not giving non-staff user 403 message


[Unreleased]: https://github.com/nickjj/flask-static-digest/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/nickjj/flask-static-digest/releases/tag/v1.0.0
