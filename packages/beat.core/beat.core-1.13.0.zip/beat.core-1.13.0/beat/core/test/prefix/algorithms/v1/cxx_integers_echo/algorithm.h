// NOTE: This file implements the algorithm declared in the file
// 'user/cxx_integers_echo/1.json'

#ifndef _BEAT_GENERATED_ALGORITHM_H_
#define _BEAT_GENERATED_ALGORITHM_H_

#include <beat.backend.cxx/algorithm.h>


class Algorithm: public beat::backend::cxx::IAlgorithm
{
public:
    Algorithm();
    virtual ~Algorithm();

    virtual bool setup(const json& parameters);

    virtual bool process(const beat::backend::cxx::InputList& inputs,
                         const beat::backend::cxx::OutputList& outputs);
};


extern "C" {
    beat::backend::cxx::IAlgorithm* create_algorithm();
}

#endif
