# MprisFakePlayer

Most of modern bluetooth headphones has internal volume control that works over AVRCP interface.
AVRCP interface requires an active [MPRIS](https://specifications.freedesktop.org/mpris-spec/latest/) player to activate volume control but not all desktop media players implements MPRIS.

This app runs fake mpris player with `Playing` status. It helps to activate `avrcp` volume controls on headphones like `Powerbeats Pro` when using non-mpris media player.
