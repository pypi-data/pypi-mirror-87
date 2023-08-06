# MprisFakePlayer

Most of modern bluetooth headphones has internal volume control that works over AVRCP interface.
AVRCP interface requires an active [MPRIS](https://specifications.freedesktop.org/mpris-spec/latest/) player to activate volume control but not all desktop media players implements MPRIS.

This app runs fake mpris player with `Playing` status. It helps to activate `avrcp` volume controls on headphones like `Powerbeats Pro` when using non-mpris media player.

## Installation

### aur: `mpris-fakeplayer`

### pip:

```
$ pip install mpris-fakeplayer
$ sudo -E mpris-fakeplayer --install-service
```

### systems requirements:

* active [mpris-proxy](https://wiki.archlinux.org/index.php/Bluetooth_headset#Media_controls) service

## Usage

```
$ systemctl --user start mpris-fakeplayer.service
$ systemctl --user enable mpris-fakeplayer.service
```
