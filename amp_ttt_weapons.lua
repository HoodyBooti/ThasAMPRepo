-- AMP TTT Weapon Config
-- Ablage: garrysmod/addons/amp_ttt_weapons/lua/autorun/amp_ttt_weapons.lua
-- Liest garrysmod/data/amp_ttt_weapons.txt (wird von AMP geschrieben) und passt
-- Shop-Rechte (CanBuy) und Boden-Spawns (AutoSpawnable) an. Läuft auf Server UND Client,
-- weil der Shop-Dialog die Waffentabellen clientseitig auswertet.

if engine.ActiveGamemode() ~= "terrortown" then return end

local DATA_FILE = "amp_ttt_weapons.txt"
local NET_NAME  = "AMP_TTT_WeaponCfg"

local function ParseFile(txt)
    local cfg = { shop = {}, floor = {}, custom_shop = {}, custom_floor = {} }
    for line in string.gmatch(txt or "", "[^\r\n]+") do
        local key, val = string.match(line, "^%s*([^=]+)=(.*)$")
        if key then
            key, val = string.Trim(key), string.Trim(val)
            local group, name = string.match(key, "^(%a+)%.(.+)$")
            if group == "shop" or group == "floor" then
                if val ~= "" and val ~= "default" then cfg[group][name] = val end
            elseif group == "custom" and val ~= "" then
                local target = (name == "shop") and cfg.custom_shop or cfg.custom_floor
                for entry in string.gmatch(val, "[^,]+") do
                    local cls, mode = string.match(entry, "^%s*([%w_]+)%s*:%s*(%a+)%s*$")
                    if cls then target[cls] = mode end
                end
            end
        end
    end
    -- Custom-Einträge überschreiben/ergänzen die GUI-Einträge
    for cls, mode in pairs(cfg.custom_shop)  do cfg.shop[cls]  = mode end
    for cls, mode in pairs(cfg.custom_floor) do cfg.floor[cls] = mode end
    cfg.custom_shop, cfg.custom_floor = nil, nil
    return cfg
end

local function RolesFor(mode)
    if mode == "traitor"   then return { ROLE_TRAITOR } end
    if mode == "detective" then return { ROLE_DETECTIVE } end
    if mode == "both"      then return { ROLE_TRAITOR, ROLE_DETECTIVE } end
    return nil -- "none"
end

local ITEM_IDS = function()
    return { item_armor = EQUIP_ARMOR, item_radar = EQUIP_RADAR, item_disguiser = EQUIP_DISGUISE }
end

local function ApplyItems(shop)
    if not EquipmentItems or not ROLE_TRAITOR then return end
    local ids, pool = ITEM_IDS(), {}
    for _, role in ipairs({ ROLE_TRAITOR, ROLE_DETECTIVE }) do
        for _, it in ipairs(EquipmentItems[role] or {}) do pool[it.id] = pool[it.id] or it end
    end
    for name, mode in pairs(shop) do
        local id = ids[name]
        if id and pool[id] then
            for _, role in ipairs({ ROLE_TRAITOR, ROLE_DETECTIVE }) do
                EquipmentItems[role] = EquipmentItems[role] or {}
                for i = #EquipmentItems[role], 1, -1 do
                    if EquipmentItems[role][i].id == id then table.remove(EquipmentItems[role], i) end
                end
            end
            for _, role in ipairs(RolesFor(mode) or {}) do
                table.insert(EquipmentItems[role], pool[id])
            end
        end
    end
end

local function Apply(cfg)
    if not cfg or not ROLE_TRAITOR then return end

    for class, mode in pairs(cfg.shop) do
        local w = weapons.GetStored(class)
        if w then
            local roles = RolesFor(mode)
            w.CanBuy = roles
            if roles and not w.EquipMenuData then
                w.EquipMenuData = { type = "Weapon", desc = w.PrintName or class }
            end
        end
    end

    for class, mode in pairs(cfg.floor) do
        local w = weapons.GetStored(class)
        if w then w.AutoSpawnable = (mode == "on") end
    end

    ApplyItems(cfg.shop)

    -- TTT cached die Shop-Liste beim ersten Öffnen; Cache verwerfen
    if CLIENT then Equipment = nil end
    print("[AMP-TTT] Waffenkonfiguration angewendet.")
end

if SERVER then
    util.AddNetworkString(NET_NAME)
    AddCSLuaFile()

    local cfg

    hook.Add("InitPostEntity", "AMP_TTT_Apply", function()
        cfg = ParseFile(file.Read(DATA_FILE, "DATA"))
        Apply(cfg)
    end)

    hook.Add("PlayerInitialSpawn", "AMP_TTT_Sync", function(ply)
        if not cfg then return end
        net.Start(NET_NAME)
        net.WriteString(util.TableToJSON(cfg))
        net.Send(ply)
    end)
else
    net.Receive(NET_NAME, function()
        Apply(util.JSONToTable(net.ReadString()))
    end)
end
