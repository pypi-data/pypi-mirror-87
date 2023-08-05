// NOTE: This file implements the algorithm declared in the file
// 'user/cxx_integers_echo/1.json'

#include "algorithm.h"
#include "beat.backend.cxx/input.h"
#include "beat.backend.cxx/inputlist.h"
#include "beat.backend.cxx/outputlist.h"
#include "user_single_integer_1.h"
#include <iostream>

using namespace beat::backend::cxx;


Algorithm::Algorithm()
{
}

//---------------------------------------------------------

Algorithm::~Algorithm()
{
}

//---------------------------------------------------------

bool Algorithm::setup(const json& parameters)
{
    return true;
}

//---------------------------------------------------------

bool Algorithm::process(const InputList& inputs, const OutputList& outputs)
{
    auto data = inputs["in_data"]->data<dataformats::user::single_integer_1>();

    outputs["out_data"]->write(data);

    return true;
}

//---------------------------------------------------------

IAlgorithm* create_algorithm()
{
    return new Algorithm();
}
