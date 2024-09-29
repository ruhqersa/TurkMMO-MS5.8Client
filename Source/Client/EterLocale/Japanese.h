#pragma once

BOOL ShiftJIS_IsLeadByte( const char chByte );
BOOL ShiftJIS_IsTrailByte( const char chByte );
int ShiftJIS_StringCompareCI( LPCSTR szStringLeft, LPCSTR szStringRight, size_t sizeLength );
//martysama0134's ec11de26810c4b4081710343a364aa44
