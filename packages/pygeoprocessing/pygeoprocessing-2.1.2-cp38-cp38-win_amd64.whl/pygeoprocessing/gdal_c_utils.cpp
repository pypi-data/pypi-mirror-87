#include "gdal_c_utils.h"

namespace gdal_utils {
    // Default constructor
    GdalRaster::GdalRaster (char *pszFilename) {
        GDALAllRegister();
        this->poDataset = (GDALDataset *) GDALOpen( pszFilename, GA_ReadOnly );
    }

    // Destructor
    GdalRaster::~GdalRaster () {
        GDALClose(this->poDataset);
    }
}
