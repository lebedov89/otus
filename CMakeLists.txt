cmake_minimum_required(VERSION 3.10)

if(DEFINED ENV{GITHUB_RUN_NUMBER})
  set(PATCH_NUM $ENV{GITHUB_RUN_NUMBER})
else()
  set(PATCH_NUM 0)
endif()

project(hello LANGUAGES CXX
    VERSION 0.0.${PATCH_NUM}
)

set(CMAKE_CXX_STANDARD 17)

set(FLAGS_COMMON
        "-pedantic"
        "-Wall"
        "-Wcast-align"
        "-Wcast-qual"
        "-Wconversion"
        "-Wextra"
        "-Wshadow"
        "-Wold-style-cast"
        "-Woverloaded-virtual"
        "-fno-exceptions"
        "-fno-rtti"
)

string(REPLACE ";" " " FLAGS_COMMON "${FLAGS_COMMON}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${FLAGS_CPU} ${FLAGS_COMMON}")

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose build type: Debug Release." FORCE)
endif()

include(${PROJECT_SOURCE_DIR}/cmake/conan.cmake)

conan_cmake_run(
  CONANFILE conanfile.py
  BASIC_SETUP
  CMAKE_TARGETS # individual targets to link to
  BUILD
    missing 
)
configure_file(version.h.in version.h)

option(BUILD_TESTS "Build unittests" OFF)

add_subdirectory(src)

target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_BINARY_DIR})

if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

install(TARGETS sayhello RUNTIME DESTINATION bin)

set(CPACK_GENERATOR DEB)
set(CPACK_PACKAGE_VERSION_MAJOR "${PROJECT_VERSION_MAJOR}")
set(CPACK_PACKAGE_VERSION_MINOR "${PROJECT_VERSION_MINOR}")
set(CPACK_PACKAGE_VERSION_PATCH "${PROJECT_VERSION_PATCH}")

set(CPACK_PACKAGE_CONTACT example@example.com)

include(CPack)
