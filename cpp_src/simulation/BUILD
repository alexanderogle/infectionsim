cc_library(
    name = "data_structs",
    srcs = [
            "person.cpp",
            "population.cpp",
            "network.cpp",
            ],
    hdrs = [
            "person.h",
            "population.h",
            "network.h",
        ],
)

cc_binary(
    name = "run_simulation",
    srcs = ["run_simulation.cpp"],
    deps = [":data_structs"]
)