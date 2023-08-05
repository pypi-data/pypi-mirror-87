// NOTE: This file was automatically generated from the algorithm declaration file
// 'user/cxx_integers_echo/1.json'

#include <beat.backend.cxx/dataformatfactory.h>
#include "beat_setup.h"
#include "user_single_integer_1.h"

using namespace beat::backend::cxx;


void setup_beat_cxx_module()
{
    DataFormatFactory* factory = DataFormatFactory::getInstance();

    factory->registerDataFormat("user/single_integer/1", &user::single_integer_1::create);
}
