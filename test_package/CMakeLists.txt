cmake_minimum_required(VERSION 3.17)
project(PackageTest)
enable_testing()

find_package(stdexec REQUIRED)

add_executable(test_stdexec test.cpp)
target_link_libraries(test_stdexec stdexec::stdexec)
add_test(test_stdexec test_stdexec)
