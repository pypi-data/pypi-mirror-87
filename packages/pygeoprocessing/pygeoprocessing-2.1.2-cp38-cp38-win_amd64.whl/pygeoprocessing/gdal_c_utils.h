#ifndef GDAL_C_UTILS
#define GDAL_C_UTILS

#include "gdal_priv.h"
#include "cpl_conv.h" // for CPLMalloc()

namespace gdal_utils {
    class GdalRaster {
        public:
            GDALDataset  *poDataset;
            GdalRaster(char *pszFilename);
            ~GdalRaster();
    };
}

#endif