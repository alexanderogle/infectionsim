cc_library(
    name = "data_structs",
    srcs = [
            "simulation/person.cpp",
            "simulation/population.cpp",
            "simulation/network.cpp",
            ],
    hdrs = [
            "simulation/person.h",
            "simulation/population.h",
            "simulation/network.h",
        ],
)

cc_binary(
    name = "run_simulation",
    srcs = ["simulation/run_simulation.cpp"],
    deps = [":data_structs"]
)