// MagicPodsCore: https://github.com/steam3d/MagicPodsCore
// Copyright: 2020-2025 Aleksandr Maslov <https://magicpods.app> & Andrei Litvintsev <a.a.litvintsev@gmail.com>
// License: GPL-3.0

#include "Capability.h"
#include "Logger.h"

namespace MagicPodsCore
{
    nlohmann::json Capability::CreateJsonBody()
    {
        return nlohmann::json::object();
    }

    void Capability::Reset()
    {
        isAvailable = false;
        Logger::Debug("Capability: %s was reset", name.c_str());
    }

    nlohmann::json Capability::GetAsJson()
    {
        if (!isAvailable)
            return {};

        auto bodyJson = CreateJsonBody();
        bodyJson["readonly"] = isReadOnly;

        return nlohmann::json{{name, bodyJson}};
    }
    void Capability::SetFromJson(const nlohmann::json &json)
    {
    }

    void Capability::ExecuteCommand(const std::string& command)
    {
        std::string fullCommand = command + " 2>/dev/null || true";
        system(fullCommand.c_str());
    }

    std::string Capability::ExecuteCommandWithOutput(const std::string& command)
    {
        FILE* pipe = popen((command + " 2>/dev/null").c_str(), "r");
        if (!pipe) return "";

        char buffer[256];
        std::string result;
        if (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
            result = buffer;
            result.erase(result.find_last_not_of("\n\r") + 1);
        }
        pclose(pipe);
        return result;
    }

    std::string Capability::GetPlayerStatus()
    {
      return ExecuteCommandWithOutput("playerctl status");
    }

    void Capability::StopPlayback()
    {
        if (GetPlayerStatus() != "Playing") return;
        ExecuteCommand(OSD_COMMAND + " --playerctl pause");
    }

    void Capability::StartPlayback()
    {
        if (GetPlayerStatus() == "Playing") return;
        ExecuteCommand(OSD_COMMAND + " --playerctl play");
    }

    void Capability::SwitchToNonBluetoothSink()
    {
        std::string nonBluetoothSink = ExecuteCommandWithOutput("pactl list short sinks | grep -v \"bluez\" | grep \"alsa_output\" | head -1 | awk '{print $2}'");

        if (nonBluetoothSink.empty()) {
            return;
        }

        std::string command = "pactl set-default-sink " + nonBluetoothSink;
        ExecuteCommand(command);
    }

    void Capability::SwitchToBluetoothSink(std::string btAddr)
    {
      std::string command = "pactl set-default-sink bluez_output." + btAddr + ".1";
      ExecuteCommand(command);
    }
}
