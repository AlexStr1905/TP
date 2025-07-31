cmake_minimum_required(VERSION 3.11) #Минимальная версия CMake

# Компиляторы из окружения
set(ENV{CC} gcc)
set(ENV{CXX} g++)

project(train_your_dragon LANGUAGES C CXX) # Название проетка

# Стандарты языков
set(CMAKE_C_STANDARD 17)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Флаги для покрытия
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -O0 -fprofile-arcs -ftest-coverage -pthread")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -g -O0 -fprofile-arcs -ftest-coverage")

# Вывод стандартов языков, по условию
message(STATUS "C standard ${CMAKE_C_STANDARD}")
message(STATUS "C++ standard ${CMAKE_CXX_STANDARD}")

# Линтер
add_custom_target(lint ALL
  COMMAND python3 ${CMAKE_SOURCE_DIR}/utils/includeLint.py -d ${CMAKE_SOURCE_DIR}
  COMMENT "Executing linter"
)

# Этап 1. Создание target train
add_executable(train train/train.cpp train/trench.cpp)
set_target_properties(train PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/results")

# Этап 2. Тесты + покрытие

# Библиотеки драконов
add_library(fiery STATIC
  ${CMAKE_SOURCE_DIR}/drachenland/fiery/orange_dragon.cpp
  ${CMAKE_SOURCE_DIR}/drachenland/fiery/red_dragon.cpp
)

add_library(fury STATIC
  ${CMAKE_SOURCE_DIR}/drachenland/fury/toothless.c
)

add_library(icy STATIC
  ${CMAKE_SOURCE_DIR}/drachenland/icy/blue_dragon.cpp
)

target_include_directories(fiery PUBLIC
  ${CMAKE_SOURCE_DIR}/utils
  ${CMAKE_SOURCE_DIR}/drachenland/fiery
)

target_include_directories(fury PUBLIC
  ${CMAKE_SOURCE_DIR}/drachenland/fury
)

target_include_directories(icy PUBLIC
  ${CMAKE_SOURCE_DIR}/utils
  ${CMAKE_SOURCE_DIR}/drachenland/icy
)

# Тесты с автоматической загрузкой GTest
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/heads/main.zip
)
FetchContent_MakeAvailable(googletest)

add_executable(tests
  ${CMAKE_SOURCE_DIR}/arena/battle.cpp
)

target_link_libraries(
  tests
  fiery
  icy
  fury
  GTest::gtest_main
  pthread
)

target_include_directories(tests PRIVATE
  ${CMAKE_SOURCE_DIR}/utils
)

include(GoogleTest)
enable_testing()
gtest_discover_tests(tests)

# Покрытие кода

set(COVERAGE_MODULE_URL "https://gitlab.com/atpd/progtech/cmake/-/raw/main/CodeCoverage.cmake?ref_type=heads")
set(COVERAGE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake/CodeCoverage.cmake")

file(DOWNLOAD ${COVERAGE_MODULE_URL} ${COVERAGE_MODULE_PATH})

include("${COVERAGE_MODULE_PATH}")

setup_target_for_coverage(
  coverage
  tests
  coverage_tmp
)

add_custom_command(TARGET coverage POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy_directory
          "${CMAKE_BINARY_DIR}/coverage_tmp"
          "${CMAKE_SOURCE_DIR}/coverage"
)
# Профили сборки

option(DAY "DAY" OFF)
option(NIGHT "NIGHT" OFF)

if(DAY)
    add_compile_definitions(day)
endif()
if(NIGHT)
    add_compile_definitions(night)
endif()

# Удаление директорий и файлов сборки

add_custom_target(
    clear
    COMMAND ${CMAKE_COMMAND} -E remove_directory "${CMAKE_SOURCE_DIR}/${BUILD_SOURCE_DIR}"
    COMMAND ${CMAKE_COMMAND} -E remove "${CMAKE_SOURCE_DIR}/cmake/CodeCoverage.cmake"
    COMMAND ${CMAKE_COMMAND} -E remove_directory "${CMAKE_SOURCE_DIR}/coverage"
    COMMAND ${CMAKE_COMMAND} -E remove_directory "${CMAKE_BINARY_DIR}/coverage_temp"
    COMMAND ${CMAKE_COMMAND} -E remove_directory "${CMAKE_SOURCE_DIR}/results"
)
