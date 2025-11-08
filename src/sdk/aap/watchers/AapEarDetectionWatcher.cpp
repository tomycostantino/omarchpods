// Omarchpods: https://github.com/tomycostantino/omarchpods
// Tomas Costantino 2025

#include "AapEarDetectionWatcher.h"

namespace MagicPodsCore
{
    AapEarDetectionWatcher::AapEarDetectionWatcher() : AapWatcher{"AapEarDetectionWatcher"}
    {
    }

    void AapEarDetectionWatcher::ProcessResponse(const std::vector<unsigned char> &data)
    {
        if (data.size() < 8)
            return;

        if (data[4] != 0x06)
            return;

        AapEarDetectionState state = static_cast<AapEarDetectionState>(data[7]);

        Logger::Info("%s: %s", _tag.c_str(), AapEarDetectionStateToString(state).c_str());
        _event.FireEvent(state);
    }

}
