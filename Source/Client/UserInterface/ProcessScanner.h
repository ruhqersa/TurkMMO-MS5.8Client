#pragma once

typedef std::pair<DWORD, std::string> CRCPair;

void ProcessScanner_Destroy();
bool ProcessScanner_Create();
void ProcessScanner_ReleaseQuitEvent();

bool ProcessScanner_PopProcessQueue(std::vector<CRCPair>* pkVct_crcPair);
//martysama0134's ec11de26810c4b4081710343a364aa44
