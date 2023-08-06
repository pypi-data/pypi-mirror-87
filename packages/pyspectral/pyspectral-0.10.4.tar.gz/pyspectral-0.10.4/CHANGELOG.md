## Version <v0.10.4> (2020/12/07)


### Pull Requests Merged

#### Features added

* [PR 125](https://github.com/pytroll/pyspectral/pull/125) - Add GitHub ci support

In this release 1 pull request was closed.


## Version <v0.10.3> (2020/12/04)

### Issues Closed

* [Issue 89](https://github.com/pytroll/pyspectral/issues/89) - GK2A AMI RSR wavelengths are reversed

In this release 1 issue was closed.

## Version <v0.10.2> (2020/11/20)

### Issues Closed

* [Issue 122](https://github.com/pytroll/pyspectral/issues/122) - Pyspectral incompatible with h5py=3.1.0 ([PR 123](https://github.com/pytroll/pyspectral/pull/123) by [@pnuu](https://github.com/pnuu))

In this release 1 issue was closed.

### Pull Requests Merged

#### Bugs fixed

* [PR 124](https://github.com/pytroll/pyspectral/pull/124) - Refactor the rsr-reader and add more test coverage ([122](https://github.com/pytroll/pyspectral/issues/122))
* [PR 123](https://github.com/pytroll/pyspectral/pull/123) - Add a utility function to decode HDF5 strings ([122](https://github.com/pytroll/pyspectral/issues/122))
* [PR 120](https://github.com/pytroll/pyspectral/pull/120) - Fix scale of AGRI response values
* [PR 118](https://github.com/pytroll/pyspectral/pull/118) - Update documentation with new satellites / sensors and correct typos

#### Features added

* [PR 124](https://github.com/pytroll/pyspectral/pull/124) - Refactor the rsr-reader and add more test coverage ([122](https://github.com/pytroll/pyspectral/issues/122))
* [PR 123](https://github.com/pytroll/pyspectral/pull/123) - Add a utility function to decode HDF5 strings ([122](https://github.com/pytroll/pyspectral/issues/122))
* [PR 121](https://github.com/pytroll/pyspectral/pull/121) - Fix codefactor issues and appveyor testing
* [PR 119](https://github.com/pytroll/pyspectral/pull/119) - Add wavelength rangefinder

#### Documentation changes

* [PR 118](https://github.com/pytroll/pyspectral/pull/118) - Update documentation with new satellites / sensors and correct typos

In this release 9 pull requests were closed.


## Version <v0.10.1> (2020/10/06)

### Issues Closed

* [Issue 112](https://github.com/pytroll/pyspectral/issues/112) - Do not cut NIR reflectance with a single threshold ([PR 113](https://github.com/pytroll/pyspectral/pull/113))
* [Issue 111](https://github.com/pytroll/pyspectral/issues/111) - Error in equation in documentation ([PR 117](https://github.com/pytroll/pyspectral/pull/117))

In this release 2 issues were closed.

### Pull Requests Merged

#### Bugs fixed

* [PR 117](https://github.com/pytroll/pyspectral/pull/117) - Fix documentation error in SI unit conversion ([111](https://github.com/pytroll/pyspectral/issues/111))

#### Features added

* [PR 116](https://github.com/pytroll/pyspectral/pull/116) - Skip python2 support
* [PR 113](https://github.com/pytroll/pyspectral/pull/113) - Separate masking and Sun zenith angle correction ([112](https://github.com/pytroll/pyspectral/issues/112))
* [PR 110](https://github.com/pytroll/pyspectral/pull/110) - Add bandname mapping for slstr

#### Documentation changes

* [PR 117](https://github.com/pytroll/pyspectral/pull/117) - Fix documentation error in SI unit conversion ([111](https://github.com/pytroll/pyspectral/issues/111))

In this release 5 pull requests were closed.



## Version v0.10.0 (2020/06/24)

### Issues Closed

* [Issue 96](https://github.com/pytroll/pyspectral/issues/96) - Spectral response function for SLSTR on Sentinel 3B ([PR 104](https://github.com/pytroll/pyspectral/pull/104))

In this release 1 issue was closed.

### Pull Requests Merged

#### Bugs fixed

* [PR 105](https://github.com/pytroll/pyspectral/pull/105) - Use original channel data on the night side for NIR emissive

#### Features added

* [PR 109](https://github.com/pytroll/pyspectral/pull/109) - add more realistic METimage RSRs
* [PR 108](https://github.com/pytroll/pyspectral/pull/108) - Add option to specify sun-zenith angle threshold applied
* [PR 107](https://github.com/pytroll/pyspectral/pull/107) - Add support for FCI
* [PR 105](https://github.com/pytroll/pyspectral/pull/105) - Use original channel data on the night side for NIR emissive
* [PR 104](https://github.com/pytroll/pyspectral/pull/104) - Updated Zenodo link for addition of SLSTR on Sentinel 3B ([96](https://github.com/pytroll/pyspectral/issues/96))

In this release 5 pull requests were closed.



## Version v0.9.5 (2020/02/04)

### Issues Closed

* [Issue 101](https://github.com/pytroll/pyspectral/issues/101) - Getting the near infrared reflectance of a viirs scene crashes. ([PR 102](https://github.com/pytroll/pyspectral/pull/102))

In this release 1 issue was closed.

### Pull Requests Merged

#### Bugs fixed

* [PR 103](https://github.com/pytroll/pyspectral/pull/103) - Fix '-' (minus) sign in math string
* [PR 102](https://github.com/pytroll/pyspectral/pull/102) - Fix round returning a float ([101](https://github.com/pytroll/pyspectral/issues/101), [101](https://github.com/pytroll/pyspectral/issues/101))

#### Documentation changes

* [PR 103](https://github.com/pytroll/pyspectral/pull/103) - Fix '-' (minus) sign in math string
* [PR 100](https://github.com/pytroll/pyspectral/pull/100) - Updated the documentation of inverse Planck function for broad channels

In this release 4 pull requests were closed.


## Version v0.9.4 (2019/12/30)


### Pull Requests Merged

#### Bugs fixed

* [PR 99](https://github.com/pytroll/pyspectral/pull/99) - Fix Read The Doc pages - does not build at the moment

#### Features added

* [PR 97](https://github.com/pytroll/pyspectral/pull/97) - Fix NIR computations to be more lenient towards dask arrays

#### Documentation changes

* [PR 99](https://github.com/pytroll/pyspectral/pull/99) - Fix Read The Doc pages - does not build at the moment

In this release 3 pull requests were closed.


## Version v0.9.3 (2019/12/06)

### Issues Closed

* [Issue 92](https://github.com/pytroll/pyspectral/issues/92) - Fails to pull from Github because of a git-lfs quota limit ([PR 93](https://github.com/pytroll/pyspectral/pull/93))
* [Issue 90](https://github.com/pytroll/pyspectral/issues/90) - CREFL rayleigh Goes-16 ABI L1B 

In this release 2 issues were closed.

### Pull Requests Merged

#### Bugs fixed

* [PR 95](https://github.com/pytroll/pyspectral/pull/95) - Adapt for later versions of TQDM
* [PR 93](https://github.com/pytroll/pyspectral/pull/93) - Abandon gitlfs ([92](https://github.com/pytroll/pyspectral/issues/92))
* [PR 87](https://github.com/pytroll/pyspectral/pull/87) - Fix doc strings (flake8 complaints).

#### Features added

* [PR 95](https://github.com/pytroll/pyspectral/pull/95) - Adapt for later versions of TQDM
* [PR 88](https://github.com/pytroll/pyspectral/pull/88) - Feature pytest
* [PR 87](https://github.com/pytroll/pyspectral/pull/87) - Fix doc strings (flake8 complaints).
* [PR 86](https://github.com/pytroll/pyspectral/pull/86) - Switch from versioneer

#### Documentation changes

* [PR 94](https://github.com/pytroll/pyspectral/pull/94) - Add the atm correction paper reference
* [PR 87](https://github.com/pytroll/pyspectral/pull/87) - Fix doc strings (flake8 complaints).

In this release 9 pull requests were closed.


## Version v0.9.2 (2019/10/03)

### Pull Requests Merged

#### Bugs fixed

* [PR 85](https://github.com/pytroll/pyspectral/pull/85) - Fix doc tests for r37 derivations
* [PR 84](https://github.com/pytroll/pyspectral/pull/84) - Add AMI channel aliases from Satpy

In this release 2 pull requests were closed.


## Version <RELEASE_VERSION> (2019/09/30)

### Issues Closed

### Pull Requests Merged

#### Features added

* [PR 83](https://github.com/pytroll/pyspectral/pull/83) - Fix for appveyor, using Daves custom branch&fork of ci-helpers
* [PR 82](https://github.com/pytroll/pyspectral/pull/82) - Add support for AMI on GEO-KOMPSAT-2A

In this release 2 pull requests were closed.


## Version <RELEASE_VERSION> (2019/08/30)

### Issues Closed

* [Issue 73](https://github.com/pytroll/pyspectral/issues/73) - Fix blackbody code to work with dask arrays ([PR 74](https://github.com/pytroll/pyspectral/pull/74))

In this release 1 issue was closed.

### Pull Requests Merged

#### Bugs fixed

* [PR 80](https://github.com/pytroll/pyspectral/pull/80) - Fix doc tests for python 2&3
* [PR 79](https://github.com/pytroll/pyspectral/pull/79) - Fix rsr zenodo version
* [PR 74](https://github.com/pytroll/pyspectral/pull/74) - Fix dask compatibility in blackbody functions ([73](https://github.com/pytroll/pyspectral/issues/73))

#### Features added

* [PR 78](https://github.com/pytroll/pyspectral/pull/78) - Add FY-3B VIRR and FY-3C VIRR RSRs
* [PR 77](https://github.com/pytroll/pyspectral/pull/77) - Add FY-4A AGRI support

In this release 5 pull requests were closed.


## Version <RELEASE_VERSION> (2019/06/07)

### Issues Closed

* [Issue 75](https://github.com/pytroll/pyspectral/issues/75) - 'download_luts' and 'download_rsr' functions always download files ([PR 76](https://github.com/pytroll/pyspectral/pull/76))

In this release 1 issue was closed.

### Pull Requests Merged

#### Features added

* [PR 76](https://github.com/pytroll/pyspectral/pull/76) - Feature download LUT files only if outdated ([75](https://github.com/pytroll/pyspectral/issues/75))

In this release 1 pull request was closed.

## Version <RELEASE_VERSION> (2019/04/29)

### Issues Closed

* [Issue 70](https://github.com/pytroll/pyspectral/issues/70) - Update yaml usage to work with pyyaml 5.1+ ([PR 71](https://github.com/pytroll/pyspectral/pull/71))
* [Issue 66](https://github.com/pytroll/pyspectral/issues/66) - Throws a warning about non-existing directory - storing/reading cached radiance-tb look-up-tables ([PR 67](https://github.com/pytroll/pyspectral/pull/67))
* [Issue 61](https://github.com/pytroll/pyspectral/issues/61) - can this program be used for user-defined sensor or rsr？ ([PR 62](https://github.com/pytroll/pyspectral/pull/62))
* [Issue 58](https://github.com/pytroll/pyspectral/issues/58) - Use dask instead of numpy masked arrays ([PR 59](https://github.com/pytroll/pyspectral/pull/59))

In this release 4 issues were closed.

### Pull Requests Merged

#### Features added

* [PR 71](https://github.com/pytroll/pyspectral/pull/71) - Fix yaml 5.1+ support with unsafe loading ([70](https://github.com/pytroll/pyspectral/issues/70), [70](https://github.com/pytroll/pyspectral/issues/70))
* [PR 69](https://github.com/pytroll/pyspectral/pull/69) - Feature rayleigh catch exception
* [PR 68](https://github.com/pytroll/pyspectral/pull/68) - Feaure metimage multiple detectors
* [PR 65](https://github.com/pytroll/pyspectral/pull/65) - Feature add metimage


In this release 4 pull requests were closed.


## Version <RELEASE_VERSION> (2019/04/09)

### Issues Closed

* [Issue 66](https://github.com/pytroll/pyspectral/issues/66) - Throws a warning about non-existing directory - storing/reading cached radiance-tb look-up-tables ([PR 67](https://github.com/pytroll/pyspectral/pull/67))
* [Issue 61](https://github.com/pytroll/pyspectral/issues/61) - can this program be used for user-defined sensor or rsr？ ([PR 62](https://github.com/pytroll/pyspectral/pull/62))
* [Issue 58](https://github.com/pytroll/pyspectral/issues/58) - Use dask instead of numpy masked arrays ([PR 59](https://github.com/pytroll/pyspectral/pull/59))

In this release 3 issues were closed.

### Pull Requests Merged

#### Bugs fixed

* [PR 67](https://github.com/pytroll/pyspectral/pull/67) - Bugfix tb2rad lut caching ([66](https://github.com/pytroll/pyspectral/issues/66))
* [PR 64](https://github.com/pytroll/pyspectral/pull/64) - Fix interp function in rayleigh correction to be serializable


#### Features added

* [PR 59](https://github.com/pytroll/pyspectral/pull/59) - Daskify NIR reflectance calculations ([58](https://github.com/pytroll/pyspectral/issues/58))

In this release 2 pull requests were closed.


## Version <RELEASE_VERSION> (2018/12/04)

### Issues Closed

* [Issue 38](https://github.com/pytroll/pyspectral/issues/38) - Download RSR data in vain

In this release 1 issue was closed.

### Pull Requests Merged

#### Features added

* [PR 60](https://github.com/pytroll/pyspectral/pull/60) - Fix readthedocs

In this release 1 pull request was closed.


## Version <RELEASE_VERSION> (2018/11/30)

### Issues Closed

* [Issue 50](https://github.com/pytroll/pyspectral/issues/50) - Re-download of RSR files ([PR 56](https://github.com/pytroll/pyspectral/pull/56))

In this release 1 issue was closed.

### Pull Requests Merged

#### Bugs fixed

* [PR 53](https://github.com/pytroll/pyspectral/pull/53) - Fix masking of calculated NIR reflectances

#### Features added

* [PR 57](https://github.com/pytroll/pyspectral/pull/57) - Script cleanup and document
* [PR 56](https://github.com/pytroll/pyspectral/pull/56) - Rsr download fix ([50](https://github.com/pytroll/pyspectral/issues/50))

In this release 3 pull requests were closed.


## Version <RELEASE_VERSION> (2018/11/30)

### Issues Closed

* [Issue 50](https://github.com/pytroll/pyspectral/issues/50) - Re-download of RSR files ([PR 56](https://github.com/pytroll/pyspectral/pull/56))

In this release 1 issue was closed.

### Pull Requests Merged

#### Bugs fixed

* [PR 53](https://github.com/pytroll/pyspectral/pull/53) - Fix masking of calculated NIR reflectances

#### Features added

* [PR 57](https://github.com/pytroll/pyspectral/pull/57) - Script cleanup and document
* [PR 56](https://github.com/pytroll/pyspectral/pull/56) - Rsr download fix ([50](https://github.com/pytroll/pyspectral/issues/50))

In this release 3 pull requests were closed.
