#ifndef __INC_ETERLIB_MUTEX_H__
#define __INC_ETERLIB_MUTEX_H__

class Mutex
{
	public:
		Mutex();
		~Mutex();

		void Lock();
		void Unlock();
		bool Trylock();

	private:
		CRITICAL_SECTION lock;
};

#endif
//martysama0134's ec11de26810c4b4081710343a364aa44
