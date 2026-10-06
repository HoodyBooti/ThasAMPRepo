#!/usr/bin/env python3
"""Generator für das AMP-Template "Garry's Mod – TTT".
Erzeugt: gmodttt.kvp, gmodtttconfig.json, gmodtttmetaconfig.json
Neue Waffen: einfach in WEAPONS / FLOOR_WEAPONS eintragen und das Skript neu ausführen."""
import json, os
OUT = os.environ.get("OUT", ".")

CB = {"False": "0", "True": "1"}
settings, srvcfg, wepmap = [], {}, {}

def add(cat, name, field, desc, itype, default, cvar=None, cmd=None, **kw):
    s = {"DisplayName": name, "Description": desc, "Keywords": field, "FieldName": field,
         "InputType": itype, "Category": cat, "DefaultValue": str(default),
         "IncludeInCommandLine": cmd is not None, "Hidden": False}
    if cmd is not None:
        s["ParamFieldName"] = cmd
        s["SkipIfEmpty"] = kw.pop("skip_empty", True)
    else:
        s["ParamFieldName"] = field
    if itype == "checkbox": s["EnumValues"] = CB
    s.update(kw)
    settings.append(s)
    if cvar: srvcfg[field] = cvar

# ---------- Server ----------
C = "Server"
add(C, "Servername", "hostname", "Name im Serverbrowser (hostname).", "text", "My TTT Server", cvar="hostname")
add(C, "Startmap", "map", "Map beim Start (z.B. ttt_67thway_v14).", "text", "ttt_67thway_v14")
add(C, "Server-Passwort", "sv_password", "Leer = öffentlich.", "password", "", cvar="sv_password")
add(C, "Region", "sv_region", "Region im Serverbrowser.", "enum", "3", cvar="sv_region",
    EnumValues={"255": "Weltweit", "0": "US-Ost", "1": "US-West", "2": "Südamerika", "3": "Europa",
                "4": "Asien", "5": "Australien", "6": "Naher Osten", "7": "Afrika"})
add(C, "LAN-Modus", "sv_lan", "Nur LAN, nicht im Internet sichtbar.", "checkbox", "0", cvar="sv_lan")
add(C, "Tickrate", "tickrate", "Nur beim Start wirksam. 66 ist Standard.", "number", 66, cmd="-tickrate", minValue="16", maxValue="128")
add(C, "GSLT (Game Server Login Token)", "sv_setsteamaccount", "Optional, https://steamcommunity.com/dev/managegameservers", "text", "", cmd="+sv_setsteamaccount")
add(C, "Client-Lua erlauben", "sv_allowcslua", "sv_allowcslua – für TTT normalerweise AUS.", "checkbox", "0", cvar="sv_allowcslua")
add(C, "Voice aktiv", "sv_voiceenable", "sv_voiceenable", "checkbox", "1", cvar="sv_voiceenable")
add(C, "FastDL URL", "sv_downloadurl", "sv_downloadurl", "text", "", cvar="sv_downloadurl")
add(C, "Loading-Screen URL", "sv_loadingurl", "sv_loadingurl", "text", "", cvar="sv_loadingurl")
add("Workshop", "Workshop-Collection ID", "workshop_collection", "host_workshop_collection – Collection mit Maps/Waffen.", "text", "", cmd="+host_workshop_collection")
add("Workshop", "Steam Web API Key", "authkey", "-authkey, nötig für Workshop-Collections.", "password", "", cmd="-authkey")

# ---------- TTT-Konvars ----------
def ttt(cat, rows):
    for cvar, name, default, kind, *rest in rows:
        desc = (rest[0] if rest else name) + f"  [{cvar}]"
        if kind == "bool":
            add(cat, name, cvar, desc, "checkbox", default, cvar=cvar)
        elif kind == "int":
            add(cat, name, cvar, desc, "number", default, cvar=cvar, minValue="0", maxValue="100000")
        else:  # float -> text
            add(cat, name, cvar, desc, "text", default, cvar=cvar)

ttt("TTT - Runden", [
 ("ttt_round_limit", "Max. Runden pro Map", 6, "int"),
 ("ttt_time_limit_minutes", "Max. Zeit pro Map (Min.)", 75, "int"),
 ("ttt_roundtime_minutes", "Rundenzeit (Min.)", 10, "int"),
 ("ttt_preptime_seconds", "Vorbereitungszeit (Sek.)", 30, "int"),
 ("ttt_firstpreptime", "Erste Vorbereitung (Sek.)", 60, "int"),
 ("ttt_posttime_seconds", "Nachrundenzeit (Sek.)", 30, "int"),
 ("ttt_haste", "Haste-Modus", 1, "bool", "Jeder Tod verlängert die Runde."),
 ("ttt_haste_starting_minutes", "Haste: Startzeit (Min.)", 5, "int"),
 ("ttt_haste_minutes_per_death", "Haste: Min. pro Tod", 0.5, "float"),
 ("ttt_minimum_players", "Mindestspieler", 2, "int"),
 ("ttt_always_use_mapcycle", "Immer Mapcycle", 0, "bool"),
 ("ttt_postround_dm", "Deathmatch nach der Runde", 0, "bool"),
 ("ttt_no_nade_throw_during_prep", "Keine Granaten in der Vorbereitung", 0, "bool"),
 ("ttt_idle_limit", "Idle-Limit (Sek.)", 180, "int", "Danach Spectator/Kick."),
])
ttt("TTT - Rollen und Credits", [
 ("ttt_traitor_pct", "Traitor-Anteil (0-1)", 0.25, "float"),
 ("ttt_traitor_max", "Max. Traitor", 32, "int"),
 ("ttt_detective_pct", "Detective-Anteil (0-1)", 0.13, "float"),
 ("ttt_detective_max", "Max. Detectives", 32, "int"),
 ("ttt_detective_min_players", "Min. Spieler für Detectives", 8, "int"),
 ("ttt_detective_karma_min", "Min. Karma für Detective", 600, "int"),
 ("ttt_credits_starting", "Traitor Start-Credits", 2, "int"),
 ("ttt_credits_award_pct", "Credit-Bonus ab Anteil toter Innocents", 0.35, "float"),
 ("ttt_credits_award_size", "Credit-Bonus Größe", 1, "int"),
 ("ttt_credits_award_repeat", "Credit-Bonus wiederholen", 1, "bool"),
 ("ttt_credits_detectivekill", "Credits für Detective-Kill", 1, "int"),
 ("ttt_det_credits_starting", "Detective Start-Credits", 1, "int"),
 ("ttt_det_credits_traitorkill", "Detective-Credits pro Traitor-Kill", 0, "int"),
 ("ttt_det_credits_traitordead", "Detective-Credits bei Traitor-Tod", 1, "int"),
])
ttt("TTT - Karma", [
 ("ttt_karma", "Karma-System", 1, "bool"),
 ("ttt_karma_strict", "Striktes Karma", 1, "bool"),
 ("ttt_karma_starting", "Start-Karma", 1000, "int"),
 ("ttt_karma_max", "Max. Karma", 1000, "int"),
 ("ttt_karma_ratio", "Schaden-Ratio", 0.001, "float"),
 ("ttt_karma_kill_penalty", "Kill-Strafe", 15, "int"),
 ("ttt_karma_round_increment", "Karma pro Runde", 5, "int"),
 ("ttt_karma_clean_bonus", "Clean-Round-Bonus", 30, "int"),
 ("ttt_karma_traitorkill_bonus", "Bonus Traitor-Kill", 40, "int"),
 ("ttt_karma_traitordmg_ratio", "Traitor-Schaden-Ratio", 0.0003, "float"),
 ("ttt_karma_clean_half", "Clean-Bonus Halbierung", 0.25, "float"),
 ("ttt_karma_low_autokick", "Auto-Kick bei niedrigem Karma", 1, "bool"),
 ("ttt_karma_low_amount", "Karma-Grenze für Kick/Ban", 450, "int"),
 ("ttt_karma_low_ban", "Statt Kick bannen", 1, "bool"),
 ("ttt_karma_low_ban_minutes", "Bandauer (Min.)", 60, "int"),
 ("ttt_karma_persist", "Karma speichern", 0, "bool"),
])
ttt("TTT - Sonstiges", [
 ("ttt_voice_drain", "Voice-Drain", 0, "bool"),
 ("ttt_voice_drain_normal", "Voice-Drain normal", 0.2, "float"),
 ("ttt_voice_drain_admin", "Voice-Drain Admin", 0.05, "float"),
 ("ttt_voice_drain_recharge", "Voice-Recharge", 0.05, "float"),
 ("ttt_locational_voice", "Positionsabhängige Voice", 0, "bool"),
 ("ttt_namechange_kick", "Kick bei Namenswechsel", 1, "bool"),
 ("ttt_namechange_bantime", "Ban bei Namenswechsel (Min.)", 10, "int"),
 ("ttt_dyingshot", "Dying Shot", 0, "bool"),
 ("ttt_killer_dna_range", "DNA-Reichweite", 550, "int"),
 ("ttt_killer_dna_basetime", "DNA-Haltbarkeit (Sek.)", 100, "int"),
 ("ttt_weapon_carrying_range", "Tragereichweite", 50, "int"),
 ("ttt_teleport_telefrags", "Telefrags", 0, "bool"),
 ("ttt_ragdoll_pinning", "Ragdoll-Pinning", 1, "bool"),
 ("ttt_ragdoll_pinning_innocents", "Ragdoll-Pinning Innocents", 0, "bool"),
 ("ttt_use_weapon_spawn_scripts", "Weapon-Spawn-Skripte nutzen", 1, "bool"),
 ("ttt_detective_hats", "Detective-Hüte", 1, "bool"),
 ("ttt_enforce_playermodel", "Playermodel erzwingen", 1, "bool"),
 ("ttt_bots_are_spectators", "Bots als Spectator", 0, "bool"),
])

# ---------- Waffen-GUI ----------
SHOP = {"default": "Standard (unverändert)", "none": "Nicht im Shop",
        "traitor": "Nur Traitor", "detective": "Nur Detective", "both": "Traitor + Detective"}
FLOOR = {"default": "Standard (unverändert)", "on": "Spawnt auf der Map", "off": "Spawnt NICHT"}

WEAPONS = [  # (Klasse, Anzeigename)
 ("weapon_ttt_c4", "C4"), ("weapon_ttt_flaregun", "Flare Gun"), ("weapon_ttt_knife", "Messer"),
 ("weapon_ttt_phammer", "Poltergeist"), ("weapon_ttt_push", "Newton Launcher"),
 ("weapon_ttt_radio", "Radio"), ("weapon_ttt_sipistol", "Schalldämpfer-Pistole"),
 ("weapon_ttt_teleport", "Teleporter"), ("weapon_ttt_decoy", "Decoy"),
 ("weapon_ttt_health_station", "Heilstation"), ("weapon_ttt_binoculars", "Fernglas"),
 ("weapon_ttt_defuser", "Defuser"), ("weapon_ttt_cse", "Visualizer"),
 ("weapon_ttt_stungun", "UMP Prototype"), ("weapon_ttt_wtester", "DNA-Scanner"),
 ("weapon_ttt_confgrenade", "Discombobulator"), ("weapon_ttt_smokegrenade", "Rauchgranate"),
 ("weapon_zm_molotov", "Brandgranate"),
 ("weapon_ttt_m16", "M16"), ("weapon_zm_mac10", "MAC10"), ("weapon_zm_rifle", "Scout-Gewehr"),
 ("weapon_zm_shotgun", "Shotgun"), ("weapon_zm_sledge", "H.U.G.E.-249"),
 ("weapon_zm_revolver", "Deagle"), ("weapon_zm_pistol", "Five-seveN"), ("weapon_ttt_glock", "Glock"),
]
FLOOR_WEAPONS = {"weapon_ttt_m16", "weapon_zm_mac10", "weapon_zm_rifle", "weapon_zm_shotgun",
                 "weapon_zm_sledge", "weapon_zm_revolver", "weapon_zm_pistol", "weapon_ttt_glock",
                 "weapon_ttt_confgrenade", "weapon_ttt_smokegrenade", "weapon_zm_molotov"}
ITEMS = [("item_armor", "Körperpanzer"), ("item_radar", "Radar"), ("item_disguiser", "Disguiser")]

for cls, nm in WEAPONS:
    f = "shop_" + cls
    add("TTT - Waffen Shop", nm, f, f"Wer kann „{nm}“ im Shop kaufen? [{cls}]", "enum", "default", EnumValues=SHOP)
    wepmap[f] = "shop." + cls
for cls, nm in ITEMS:
    f = "shop_" + cls
    add("TTT - Waffen Shop", "Item: " + nm, f, f"Wer kann „{nm}“ kaufen? [{cls}]", "enum", "default", EnumValues=SHOP)
    wepmap[f] = "shop." + cls
for cls, nm in WEAPONS:
    if cls in FLOOR_WEAPONS:
        f = "floor_" + cls
        add("TTT - Waffen Boden-Spawn", nm, f, f"Zufälliger Boden-Spawn für „{nm}“. [{cls}]", "enum", "default", EnumValues=FLOOR)
        wepmap[f] = "floor." + cls
add("TTT - Waffen Custom", "Workshop-Waffen im Shop", "custom_shop",
    "Klasse:Modus, kommagetrennt. Modus = none|traitor|detective|both. Z.B. weapon_ttt_foo:traitor,weapon_ttt_bar:both",
    "text", "")
add("TTT - Waffen Custom", "Workshop-Waffen am Boden", "custom_floor",
    "Klasse:Modus, kommagetrennt. Modus = on|off. Z.B. weapon_ttt_foo:on", "text", "")
wepmap["custom_shop"] = "custom.shop"; wepmap["custom_floor"] = "custom.floor"

# ---------- Dateien schreiben ----------
meta = [
 {"ConfigFile": "4020/garrysmod/cfg/server.cfg", "ConfigType": "kvp", "ConfigFormat": "{0} \"{1}\"",
  "Subsections": [{"Heading": "$root", "SettingMappings": srvcfg}]},
 {"ConfigFile": "4020/garrysmod/data/amp_ttt_weapons.txt", "ConfigType": "kvp", "ConfigFormat": "{0}={1}",
  "Subsections": [{"Heading": "$root", "SettingMappings": wepmap}]},
]
json.dump(settings, open(f"{OUT}/gmodtttconfig.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
json.dump(meta, open(f"{OUT}/gmodtttmetaconfig.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

updates = [{"UpdateStageName": "SteamCMD Download (GMod)", "UpdateSourcePlatform": "All",
            "UpdateSource": "SteamCMD", "UpdateSourceData": "4020"}]
kvp = f"""Meta.DisplayName=Garry's Mod – TTT
Meta.Description=Garry's Mod Dedicated Server mit TTT-Einstellungen und Waffen-/Shop-GUI
Meta.OS=Windows, Linux
Meta.Arch=x86_64
Meta.Author=Community
Meta.URL=https://gmod.facepunch.com/
Meta.DisplayImageSource=steam:4020
Meta.EndpointURIFormat=steam://connect/{{0}}
Meta.ConfigManifest=gmodtttconfig.json
Meta.MetaConfigManifest=gmodtttmetaconfig.json
Meta.ConfigRoot=gmodttt.kvp
Meta.MinAMPVersion=2.4.0.8

App.DisplayName=Garry's Mod – TTT
App.RootDir=./gmodttt/
App.WorkingDir=4020
App.ExecutableWin=4020/srcds.exe
App.ExecutableLinux=4020/srcds_linux
App.CommandLineParameterFormat={{0}} "{{1}}"
App.CommandLineArgs=-game garrysmod -console -usercon -ip {{{{$ApplicationIPBinding}}}} -port {{{{$ApplicationPort1}}}} +maxplayers {{{{$MaxUsers}}}} +gamemode terrortown +map {{{{map}}}} +rcon_password "{{{{$RemoteAdminPassword}}}}" {{{{$FormattedArgs}}}}
App.EnvironmentVariables={{"LD_LIBRARY_PATH": ".:./bin:./garrysmod/bin:%LD_LIBRARY_PATH%", "SteamAppId": "4020"}}
App.AppSettings={{"map": "ttt_67thway_v14"}}
App.ApplicationPort1=27015
App.RemoteAdminPort=27015
App.UseRandomAdminPassword=True
App.MaxUsers=24
App.AdminMethod=SourceRCON
App.HasWriteableConsole=True
App.HasReadableConsole=True
App.ExitMethod=String
App.ExitString=quit
App.SteamUpdateAnonymousLogin=True
App.UpdateSources={json.dumps(updates)}

Console.AppReadyRegex=^(VAC secure mode is activated\\.|Connection to Steam servers successful\\.|Assigned anonymous gameserver Steam ID.*)$
Console.UserJoinRegex=^Client "(?<username>.+?)" spawned in server <(?<userid>STEAM_[0-9:_A-Z]+)>.*$
Console.UserLeaveRegex=^Dropped (?<username>.+?) from server \\(.*\\)$
"""
open(f"{OUT}/gmodttt.kvp", "w", encoding="utf-8").write(kvp)
print(len(settings), "Einstellungen")
