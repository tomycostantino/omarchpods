// Omarchpods: https://github.com/tomycostantino/omarchpods
// Tomas Costantino 2025

#include "AapEarDetectionCapability.h"

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
        StopPlayback();
        std::this_thread::sleep_for(std::chrono::milliseconds(250));
        SwitchToNonBluetoothSink();
    }

    void AapEarDetectionCapability::HandleEarInserted()
    {
        SwitchToDeviceSink();
        StartPlayback();
    }

    void AapEarDetectionCapability::SwitchToDeviceSink()
    {
        std::string btAddr = device.GetBluezOutputAddress();
        SwitchToBluetoothSink(btAddr);
    }
}
