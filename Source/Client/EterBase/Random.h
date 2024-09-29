#ifndef __INC_ETERBASE_RANDOM_H__
#define __INC_ETERBASE_RANDOM_H__

extern void				srandom(unsigned long seed);
extern unsigned long	random();
extern float			frandom(float flLow, float flHigh);
extern long				random_range(long from, long to);

#endif
//martysama0134's ec11de26810c4b4081710343a364aa44
