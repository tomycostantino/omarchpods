// Omarchpods: https://github.com/tomycostantino/omarchpods
// Tomas Costantino 2025

#pragma once
#include "AapCapability.h"
#include "sdk/aap/watchers/AapEarDetectionWatcher.h"

namespace MagicPodsCore
{
    class AapEarDetectionCapability : public AapCapability
    {
    private:
        AapEarDetectionWatcher watcher{};
        size_t watcherEventId;
        AapEarDetectionState currentState = AapEarDetectionState::OutOfEar;

    protected:
        nlohmann::json CreateJsonBody() override;
        void OnReceivedData(const std::vector<unsigned char> &data) override;

    public:
        explicit AapEarDetectionCapability(AapDevice& device);
        ~AapEarDetectionCapability() override;
        void SetFromJson(const nlohmann::json &json) override {};
    };
}
