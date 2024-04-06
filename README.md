# sacd-extract GUI

### Yet another sacd_extract GUI

While I am aware of the existence of at least two such tools for running [sacd-extract](https://github.com/setmind/sacd-ripper) (pre-fork [here](https://github.com/sacd-ripper/sacd-ripper)), namely [SACDExtractGUI](https://github.com/setmind/SACDExtractGUI) and [SACD Extract GUI](https://archive.org/details/sacd-extract-gui-winforms-dotnet) (and probably some other I did not stumble upon yet), well here is another, written in Python using PySide6.

#### Installation

Steps assume that `python` (>= 3.8) and `pip` are already installed.

Install dependencies (see sections below)

Then, run:

    $ pip install sacd-extract-gui

Install directly from ``github``:

    $ pip install git+https://github.com/amstelchen/sacd-extract-gui#egg=sacd-extract-gui

When completed, run it with:

    $ sacd-extract-gui

#### Dependencies

None, except [sacd-extract](https://github.com/setmind/sacd-ripper).

**sacd-extract-gui** is tested to work on the following distributions:

- Debian 11.3 or newer 
- Ubuntu, Kubuntu, Xubuntu, Pop!_OS 20.04 or newer
- Linux Mint 21 or newer
- LMDE 6 or newer
- MX Linux 23 or newer
- Arch Linux (or any Arch based distribution like Manjaro, ArcoLinux, Garuda Linux, ...)
- Void Linux 
- Artix Linux
- openSUSE Tumbleweed
- Zorin OS 16.3 or newer
- EndeavourOS
- elementary OS
- Fedora 37 Workstation or newer 
- Slackware 64 14.2 and 15.0
- Gentoo Linux, MocaccinoOS

#### Reporting bugs

If you encounter any bugs or incompatibilities, __please report them [here](https://github.com/amstelchen/sacd-extract-gui/issues/new)__.

#### Enabling logging/debugging

```
$ sacd_extract_gui DEBUG
DEBUG:2024-04-06 19:25:50,121:__main__.py:283:UI initialized.
Yet another sacd_extract GUI 0.1.0
Copyright (C) 2024, by Michael John
```

#### Licences

*sacd_extract_gui* is licensed under the [GPLv2](LICENSE) license.
