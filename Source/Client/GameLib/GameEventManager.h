#pragma once

#include "ActorInstance.h"

///////////////////////////////////////////////////////////////////////////////////////////////////
//
//	CGameEventManager
//
//
//

class CGameEventManager : public CSingleton<CGameEventManager>, public CScreen
{
	public:
		CGameEventManager();
		virtual ~CGameEventManager();

		void SetCenterPosition(float fx, float fy, float fz);
		void Update();

		void ProcessEventScreenWaving(CActorInstance * pActorInstance, const CRaceMotionData::TScreenWavingEventData * c_pData);

	protected:
		TPixelPosition m_CenterPosition;
};
//martysama0134's ec11de26810c4b4081710343a364aa44
