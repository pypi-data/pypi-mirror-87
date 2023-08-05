// NOTE: This file was automatically generated from the dataformat declaration file
// 'user/single_integer/1.json'

#ifndef _BEAT_GENERATED_user_single_integer_1_H_
#define _BEAT_GENERATED_user_single_integer_1_H_

#include <beat.backend.cxx/data.h>

namespace dataformats {
namespace user {

class single_integer_1: public beat::backend::cxx::DataImpl<single_integer_1>
{
public:
    single_integer_1();

	static size_t fixed_size();

    size_t size() const override;
    void pack(uint8_t** buffer) const override;
    void unpack(uint8_t** buffer) override;

    static Data* create();
    static const char *getNameStatic();

    std::string toJson() const override;

public:
    int32_t value;
};

} // user
} // dataformats

#endif
