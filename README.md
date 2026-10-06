# Garry's Mod – TTT (AMP-Template)

## Wichtig vorab
Das GUI des fest eingebauten GMod-Moduls lässt sich nicht per Addon erweitern.
Dieses Paket ist deshalb ein eigenes **Generic-Module-Template** ("Garry's Mod – TTT"),
das Standard-Einstellungen **und** TTT-/Waffen-Einstellungen im AMP-GUI anbietet.

## Dateien
| Datei | Zweck |
|---|---|
| `gmodttt.kvp` | Start, Update (SteamCMD 4020), Konsole |
| `gmodtttconfig.json` | Alle GUI-Einstellungen (117) |
| `gmodtttmetaconfig.json` | Schreibt `server.cfg` und `data/amp_ttt_weapons.txt` |
| `amp_ttt_weapons.lua` | Setzt Shop-/Spawn-Einstellungen im Spiel um |
| `generate.py` | Generator – hier neue Waffen/Cvars ergänzen |

## Installation
1. Die drei Template-Dateien in einen lokalen Template-Ordner legen:
   `<AMP-Datastore>/instances/ADS01/Plugins/ADSModule/DeploymentTemplates/LOCAL-main/`
   (Ordnername: Prefix `LOCAL`, Suffix `-main`; ggf. weitere Dateien aus dem Wiki-Abschnitt
   "Adding custom templates to AMP" beachten, z.B. eine `manifest.json`), dann AMP neu laden.
   Alternativ in einem eigenen GitHub-Repo veröffentlichen und unter
   *Configuration → Instance Deployment* als Configuration Repository hinzufügen.
2. Neue Instanz "Garry's Mod – TTT" anlegen, Update ausführen (lädt GMod per SteamCMD).
3. `amp_ttt_weapons.lua` hochladen nach
   `4020/garrysmod/addons/amp_ttt_weapons/lua/autorun/amp_ttt_weapons.lua`
4. Einstellungen im GUI setzen, Server starten.

Bestehenden Server übernehmen: `garrysmod/`-Ordner (addons, data, maps) in die neue Instanz
unter `4020/garrysmod/` kopieren.

## Waffen-GUI
* **TTT – Waffen: Shop**: pro Waffe/Item Standard / Nicht im Shop / Traitor / Detective / beide.
* **TTT – Waffen: Boden-Spawn**: pro Waffe Standard / spawnt / spawnt nicht.
  (Komplett deaktiviert = Shop „Nicht im Shop“ + Boden „spawnt nicht“.)
* **Custom**: Workshop-Waffen ohne Generator-Lauf, z.B. `weapon_ttt_foo:traitor,weapon_ttt_bar:both`.
* Weitere Waffen dauerhaft als GUI-Eintrag: in `generate.py` bei `WEAPONS` ergänzen und
  `OUT=. python3 generate.py` ausführen.
* Kategorie-Namen werden auch als UI-Selektoren verwendet; deshalb enthalten sie kein `&` oder `:`.
* Änderungen greifen nach Server-Neustart.

## Bekannte Einschränkungen / bitte testen
* `server.cfg` wird von AMP verwaltet, manuelle Änderungen können überschrieben werden.
* Cvar-Namen/Defaults stammen aus dem Vanilla-TTT; prüfen mit `find ttt_` in der Server-Konsole.
* Der Shop-Cache-Reset auf dem Client (`Equipment = nil`) und das Hinzufügen von Waffen ohne
  `EquipMenuData` sind der heikelste Teil; bitte im Spiel prüfen.
* Dateipfade in der Metaconfig sind relativ zum Instanz-Root angenommen (`4020/garrysmod/...`).
* Floats (z.B. Traitor-Anteil) sind Textfelder, da AMP-Zahlenfelder nur ganze Zahlen kennen.
* Console-Regexe (Ready/Join/Leave) ggf. an deine Konsolenausgabe anpassen.
