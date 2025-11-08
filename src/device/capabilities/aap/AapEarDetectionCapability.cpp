// Omarchpods: https://github.com/tomycostantino/omarchpods
// Tomas Costantino 2025

#include "AapEarDetectionCapability.h"
#include <cstdlib>

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
        watcherEventId = watcher.GetEvent().Subscribe([this](size_t id, AapEarDetectionState state){
            Logger::Info("Ear detection state: %s", AapEarDetectionStateToString(state).c_str());
            currentState = state;

            if (state == AapEarDetectionState::OutOfEar) {
                system("playerctl pause 2>/dev/null || true");
                std::this_thread::sleep_for(std::chrono::milliseconds(250));
                system("pactl set-default-sink alsa_output.pci-0000_c1_00.6.HiFi__Speaker__sink 2>/dev/null || true");
            } else if (state == AapEarDetectionState::InEar) {
                system("pactl set-default-sink bluez_output.F8_73_DF_23_CA_E9.1 2>/dev/null || true");
                system("playerctl play 2>/dev/null || true");
            }

            _onChanged.FireEvent(*this);
        });
    }

    AapEarDetectionCapability::~AapEarDetectionCapability()
    {
        watcher.GetEvent().Unsubscribe(watcherEventId);
    }
}
