// NOTE: This file implements the algorithm declared in the file
// 'user/cxx_integers_echo/1.json'

#include "algorithm.h"
#include "beat.backend.cxx/outputlist.h"
#include "beat.backend.cxx/dataloader.h"
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

bool Algorithm::prepare(const DataLoaderList& data_load_list)
{
    return true;
}

//---------------------------------------------------------

bool Algorithm::process(const DataLoaderList& data_load_list, const OutputList& outputs)
{

    auto data_loader = data_load_list.loader_of("in_data");

    std::map<std::string, beat::backend::cxx::Data *> data;
    int64_t start = -1;
    int64_t end = -1;

    for (int i = 0 ; i < data_loader->count() ; ++i) {
        std::tie(data, start, end) = (*data_loader)[i];
        auto value = static_cast<dataformats::user::single_integer_1*>(data["in_data"]);
        outputs["out_data"]->write(value);
    }

    return true;
}

//---------------------------------------------------------

IAlgorithm* create_algorithm()
{
    return new Algorithm();
}
