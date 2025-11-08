// Omarchpods: https://github.com/tomycostantino/omarchpods
// Tomas Costantino 2025

#include "AapEarDetectionCapability.h"
#include <cstdlib>
#include <sstream>

namespace MagicPodsCore
{
    nlohmann::json AapEarDetectionCapability::CreateJsonBody()
    {
        auto bodyJson = nlohmann::json::object();
        bodyJson["status"] = AapEarDetectionStateToString(currentState);
        return bodyJson;
    }

    void AapEarDetectionCapability::OnReceivedData(const std::vector<unsigned char> &data)
    {
        watcher.ProcessResponse(data);
    }

    AapEarDetectionCapability::AapEarDetectionCapability(AapDevice& device) : AapCapability("earDetection", true, device)
    {
        isAvailable = true;  // Ear detection is always available
        watcherEventId = watcher.GetEvent().Subscribe([this](size_t id, AapEarDetectionState state) {
            Logger::Info("Ear detection state: %s", AapEarDetectionStateToString(state).c_str());
            currentState = state;

            if (state == AapEarDetectionState::OutOfEar) {
                HandleEarRemoved();
            } else if (state == AapEarDetectionState::InEar) {
                HandleEarInserted();
            }

            _onChanged.FireEvent(*this);
        });
    }

    AapEarDetectionCapability::~AapEarDetectionCapability()
    {
        watcher.GetEvent().Unsubscribe(watcherEventId);
    }

    void AapEarDetectionCapability::HandleEarRemoved()
    {
        PausePlayback();
        std::this_thread::sleep_for(std::chrono::milliseconds(250));
        SwitchToDefaultSink();
    }

    void AapEarDetectionCapability::HandleEarInserted()
    {
        SwitchToBluetoothSink();
        ResumePlayback();
    }

    void AapEarDetectionCapability::PausePlayback()
    {
        ExecuteCommand("playerctl pause");
    }

    void AapEarDetectionCapability::ResumePlayback()
    {
        ExecuteCommand("playerctl play");
    }

    void AapEarDetectionCapability::SwitchToDefaultSink()
    {
        ExecuteCommand("pactl set-default-sink alsa_output.pci-0000_c1_00.6.HiFi__Speaker__sink");
    }

    void AapEarDetectionCapability::SwitchToBluetoothSink()
    {
        std::string btAddress = device.GetBluezOutputAddress();
        std::string command = "pactl set-default-sink bluez_output." + btAddress + ".1";
        ExecuteCommand(command);
    }
}
