local msg = require("mp.msg")
local utils = require("mp.utils")

-- Pakai user-agent biar url bisa di play
mp.set_property("user-agent","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36")

mp.add_hook("on_load", 10, function()
    local url = mp.get_property("stream-open-filename")
    
    if url and string.match(url, "animeinweb%.com/anime/") then
        msg.info("Loading animeinweb playlist...")
        
        -- Ambil format dari ytdl-format kalo ada
        local user_format = mp.get_property("ytdl-format") or ""
        
        -- Build args
        local args = {
            "yt-dlp",
            "--get-url",
            "--yes-playlist",
            "--flat-playlist",
        }
        
        -- Tambah format filter kalo user kasih
        if user_format ~= "" then
            table.insert(args, "--format")
            table.insert(args, user_format)
        end
        
        table.insert(args, url)
        
        local result = utils.subprocess({args = args})
        
        if result.status == 0 then
            local count = 0
            local first = true
            
            for episode_url in result.stdout:gmatch("[^\r\n]+") do
                episode_url = episode_url:gsub("%s+$", "")
                if episode_url ~= "" then
                    if first then
                        mp.commandv("loadfile", episode_url, "replace")
                        first = false
                    else
                        mp.commandv("loadfile", episode_url, "append-play")
                    end
                    count = count + 1
                end
            end
            
            if count > 0 then
                msg.info("Loaded " .. count .. " episodes")
            end
        end
        
        return true
    end
end)