// Omarchpods: https://github.com/tomycostantino/omarchpods
// Tomas Costantino 2025

#pragma once

#include "Event.h"
#include "AapWatcher.h"

namespace MagicPodsCore
{
    enum class AapEarDetectionState : unsigned char
    {
        InEar = 0x00,
        OutOfEar = 0x01,
        InCase = 0x02
    };

    static std::string AapEarDetectionStateToString(AapEarDetectionState value)
    {
        switch (value)
        {
        case AapEarDetectionState::InEar:
            return "InEar";
        case AapEarDetectionState::OutOfEar:
            return "OutOfEar";
        case MagicPodsCore::AapEarDetectionState::InCase:
            return "InCase";
        default:
            return "Unknown";
        }
    }

    class AapEarDetectionWatcher : public AapWatcher
    {
    private:
        Event<AapEarDetectionState> _event{};

    public:
        AapEarDetectionWatcher();
        void ProcessResponse(const std::vector<unsigned char> &data) override;

        Event<AapEarDetectionState> &GetEvent()
        {
            return _event;
        }
    };

}
