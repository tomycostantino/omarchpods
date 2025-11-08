// Omarchpods: https://github.com/tomycostantino/omarchpods
// Tomas Costantino 2025

#include "AapEarDetectionCapability.h"

namespace MagicPodsCore
{
    nlohmann::json AapEarDetectionCapability::CreateJsonBody()
    {
        auto bodyJson = nlohmann::json::object();
        bodyJson["selected"] = true; // Always true for ear detection
        return bodyJson;
    }

    void AapEarDetectionCapability::OnReceivedData(const std::vector<unsigned char> &data)
    {
        watcher.ProcessResponse(data);
    }

    AapEarDetectionCapability::AapEarDetectionCapability(AapDevice& device) : AapCapability("earDetection", true, device)
    {
        watcherEventId = watcher.GetEvent().Subscribe([this](size_t id, AapEarDetectionState state){
            Logger::Info("Ear detection state: %s", AapEarDetectionStateToString(state).c_str());
            _onChanged.FireEvent(*this);
        });
    }

    AapEarDetectionCapability::~AapEarDetectionCapability()
    {
        watcher.GetEvent().Unsubscribe(watcherEventId);
    }
}
