Fronius Smartmeter Emulator (HACS Integration)

Dies ist das Basis-Repository für die Home Assistant Integration, um ein Fronius Smartmeter zu emulieren.

## Struktur

```
custom_components/fronius_smartmeter_emulator/
│
├── __init__.py
├── const.py
├── manifest.json
├── sensor.py
└── ... (optional weitere Plattformen)
```

## Installation

- Kopiere den Ordner `custom_components/fronius_smartmeter_emulator` in dein `custom_components` Verzeichnis.
- Kompatibel mit HACS, nach Einbindung als Custom Repository.

## Entwicklung

- Erweitere die Integration z.B. um weitere Sensoren oder Services.
- Dokumentiere alle Funktionen in [`manifest.json`](custom_components/fronius_smartmeter_emulator/manifest.json) und hier im Readme.

## Links

- [Home Assistant Developer Docs](https://developers.home-assistant.io/docs/)
- [HACS](https://hacs.xyz/)
