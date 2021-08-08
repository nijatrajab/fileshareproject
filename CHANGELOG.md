# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

_No unreleased changes_


## [1.2.0] - 2021-08-08

### Added
- Added `timestamp` for file sharing with your friend
- Added `files list` to account page
- Added `shared date` to my files page
- Added the ability to see the file your friend shared with you

### Changed
- The `friendly system` has been activated for `file uploads`
- When you cancel a friendship, file sharing between both users will be deleted
- Theme of modals changed to dark


## [1.1.2] - 2021-07-27

### Added
- Added `profile picture` to share and revoke sharing
- Added `thumbnail profile picture` to friends list, friend requests and user search result page
- Added birth-date validation
- Added real time email validation to edit profile page
- Added `regular expression` for email domain name validation

### Changed
- Changed checkbox style on my files page
- Changed Password change form style

### Fixed
- User cannot see red border on the edge of the not-friend user box on friend list page
- DoesNotExist error if user has no friend on user search page
- User email not set to lowercase during registration and updating profile
- User email validation error message does not disappear when checking valid email during registration

### Security
- Fixed security vulnerability in `validation email` when updating user profile


## [1.1.1] - 2021-07-22

### Added
- Added Friend System (not active in file sharing)
- Added `friends list` and `friend requests` to user profile page
- Added `friend request` to user basic detail view in friend requests page
- Added `user search` feature
- Added revoke sharing feature for multiple users
- Added `user basic detail view` to user search result page
- Added `go to profile` button to user basic detail view in user search result page
- Added `Friend list` and `Friend requests` to django advanced admin view

### Changed
- The user will be able to determine whether the searched users are friends based on the red(_not-friend_) and green(_friend_) colors
- Both `Profile Info` and `Edit Profile` Info cards color changed to dark

### Fixed
- The user cannot change the profile picture correctly
- Fixed a bug that prevented the selection of the correct data in the `user basic detail view`
- Fixed the problem of the user seeing himself in the `user search result`


## [1.1.0] - 2021-07-08

### Added

- Added account view feature
- Added account edit feature
- Added not required `date birth`, `about me`, and `profile picture` (less than 10mb)
- Added crop feature for uploaded profile picture
- Added account dropdown menu to navbar
- Added password change feature
- Added password reset feature (development stage)
- Added `advanced admin view` button for custom django admin page to admin page
- Added search bar to `user` and `user file` list display on custom django admin view
- Added custom `503 Service Unavailable` page

### Changed

- Location of `My files` and `Shared with me` features in the navbar changed to the `account dropdown menu`
- Changed user files directory path
- Changed list display for `user` and `user file` on custom django admin view
- Changed fieldsets for `user` and `user file` on custom django admin view

### Fixed

- Fixed "case-sensitive" issue on `login`
- Fixed authenticated user can see `login` and `signup page`
- Fixed some redirecting issues


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


[Unreleased]: https://github.com/nijatrajab/fileshareproject/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/nijatrajab/fileshareproject/compare/v1.1.2...v1.2.0
[1.1.2]: https://github.com/nijatrajab/fileshareproject/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/nijatrajab/fileshareproject/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/nijatrajab/fileshareproject/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/nijatrajab/fileshareproject/releases/tag/v1.0.0
