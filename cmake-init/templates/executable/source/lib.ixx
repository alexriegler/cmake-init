{% if pm %}module;

#include <fmt/core.h>

{% end %}export module library;

import std;

export {
/**
 * @brief The core implementation of the executable
 *
 * This class makes up the library part of the executable, which means that the
 * main logic is implemented here. This kind of separation makes it easy to
 * test the implementation for the executable, because the logic is nicely
 * separated from the command-line logic implemented in the main function.
 */
struct library
{
    /**
     * @brief Simply initializes the name member to the name of the project
     */
    library()
        : name {{% if pm %}fmt::format("{}", "{= name =}"){% else %}"{= name =}"{% end %}}
    {
    }

    std::string name;
};
}
