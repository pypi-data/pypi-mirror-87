// NOTE: This file was automatically generated from the dataformat declaration file
// 'user/single_integer/1.json'

#ifndef _BEAT_GENERATED_user_single_integer_1_H_
#define _BEAT_GENERATED_user_single_integer_1_H_

#include <beat.backend.cxx/data.h>

namespace user {

class single_integer_1: public beat::backend::cxx::Data
{
public:
    single_integer_1();

    virtual size_t size() const;
    virtual void pack(uint8_t** buffer) const;
    virtual void unpack(uint8_t** buffer);

    static Data* create();

public:
    int32_t value;
};

}

#endif
