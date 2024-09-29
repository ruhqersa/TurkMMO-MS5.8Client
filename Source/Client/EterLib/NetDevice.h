#pragma once

class CNetworkDevice
{
	public:
		CNetworkDevice();
		virtual ~CNetworkDevice();

		void Destroy();
		bool Create();

	protected:
		void Initialize();

	protected:
		bool m_isWSA;
};
//martysama0134's ec11de26810c4b4081710343a364aa44
