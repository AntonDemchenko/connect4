cmake_minimum_required(VERSION 3.9)
project(connect4)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -W -Wall -O3")

add_executable(c4solver main.cpp solver.cpp)