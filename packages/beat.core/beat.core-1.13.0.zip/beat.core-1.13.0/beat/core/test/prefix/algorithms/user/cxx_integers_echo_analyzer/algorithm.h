// NOTE: This file implements the algorithm declared in the file
// 'user/cxx_integers_echo/1.json'

#ifndef _BEAT_GENERATED_ALGORITHM_H_
#define _BEAT_GENERATED_ALGORITHM_H_

#include <beat.backend.cxx/algorithm.h>


class Algorithm: public beat::backend::cxx::IAlgorithmSequential
{
public:
    Algorithm();
    virtual ~Algorithm();

    bool setup(const json& parameters) override;

    bool prepare(const beat::backend::cxx::DataLoaderList& data_load_list) override;
	bool process(const beat::backend::cxx::InputList& inputs,
                 const beat::backend::cxx::DataLoaderList& data_load_list,
                 const beat::backend::cxx::OutputList& outputs) override;

};


extern "C" {
    beat::backend::cxx::IAlgorithm* create_algorithm();
}

#endif
