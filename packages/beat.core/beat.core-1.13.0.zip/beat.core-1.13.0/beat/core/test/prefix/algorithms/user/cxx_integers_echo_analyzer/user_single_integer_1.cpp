// NOTE: This file was automatically generated from the dataformat declaration file
// 'user/single_integer/1.json'

#include "user_single_integer_1.h"
#include <beat.backend.cxx/dataformatfactory.h>

using namespace beat::backend::cxx;

dataformats::user::single_integer_1::single_integer_1()
{
}

//---------------------------------------------------------

size_t dataformats::user::single_integer_1::fixed_size()
{
    return sizeof(int32_t);
}

//---------------------------------------------------------

size_t dataformats::user::single_integer_1::size() const
{
    return dataformats::user::single_integer_1::fixed_size();
}

//---------------------------------------------------------

void dataformats::user::single_integer_1::pack(uint8_t** buffer) const
{
    beat::backend::cxx::pack(value, buffer);
}

//---------------------------------------------------------

void dataformats::user::single_integer_1::unpack(uint8_t** buffer)
{
    value = beat::backend::cxx::unpack_scalar<int32_t>(buffer);
}

//---------------------------------------------------------

Data* dataformats::user::single_integer_1::create()
{
    return new user::single_integer_1();
}

//---------------------------------------------------------

const char *dataformats::user::single_integer_1::getNameStatic()
{
    return "user/single_integer/1";
}

//---------------------------------------------------------

std::string dataformats::user::single_integer_1::toJson() const
{
return "{"
"\"field\":\"int32_t\""
"}";
}
