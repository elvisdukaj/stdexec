cmake_minimum_required(VERSION 3.25.0)

if(POLICY CMP0135)
  # make the timestamps of ExternalProject_ADD match the download time
  # https://cmake.org/cmake/help/latest/policy/CMP0135.html
  cmake_policy(SET CMP0135 NEW)
  set(CMAKE_POLICY_DEFAULT_CMP0135 NEW)
endif()

if(POLICY CMP0141)
  # Enables the use of the MSVC_DEBUG_INFORMATION_FORMAT target property
  # https://cmake.org/cmake/help/latest/policy/CMP0141.html
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_POLICY_DEFAULT_CMP0141 NEW)
endif()

##############################################################################
# - Project definition -------------------------------------------------------

# Define the project and set the version and languages
if(NOT EXISTS ${CMAKE_BINARY_DIR}/execution.bs)
  file(DOWNLOAD "https://raw.githubusercontent.com/cplusplus/sender-receiver/main/execution.bs"
      ${CMAKE_BINARY_DIR}/execution.bs)
endif()
file(STRINGS "${CMAKE_BINARY_DIR}/execution.bs" STD_EXECUTION_BS_REVISION_LINE REGEX "Revision: [0-9]+")
string(REGEX REPLACE "Revision: ([0-9]+)" "\\1" STD_EXECUTION_BS_REVISION ${STD_EXECUTION_BS_REVISION_LINE})

# nvc++ isn't supported by (s)ccache yet, so unset these before the `project()`
# call so CMake's CXX compiler detection doesn't throw attempting to use it

project(STDEXEC VERSION "0.${STD_EXECUTION_BS_REVISION}.0" LANGUAGES CXX)

# Print CMake configuration
message(STATUS "System           : ${CMAKE_SYSTEM}")
message(STATUS "System name      : ${CMAKE_SYSTEM_NAME}")
message(STATUS "System ver       : ${CMAKE_SYSTEM_VERSION}")
message(STATUS)

# Set the version and current build date
set(STDEXEC_VERSION "${PROJECT_VERSION}")
set(STDEXEC_VERSION_MAJOR "${PROJECT_VERSION_MAJOR}")
string(TIMESTAMP STDEXEC_BUILD_DATE "%Y-%m-%d")
string(TIMESTAMP STDEXEC_BUILD_YEAR "%Y")

message(STATUS "Library ver      : ${STDEXEC_VERSION}")
message(STATUS "Build date       : ${STDEXEC_BUILD_DATE}")
message(STATUS "Build year       : ${STDEXEC_BUILD_YEAR}")
message(STATUS)

# Integrate with LLVM/clang tooling
include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/clangd_compile_info.cmake)

##############################################################################
# - Dependencies -------------------------------------------------------------

# Ensure that we link with the threading library
find_package(Threads REQUIRED)

##############################################################################
# - Main library targets -----------------------------------------------------

# Define the main library
add_library(stdexec)

# Set library version
set_target_properties(stdexec PROPERTIES
                      VERSION "${STDEXEC_VERSION}"
                      SOVERSION "${STDEXEC_VERSION_MAJOR}")
target_sources(stdexec 
  PRIVATE 
      src/system_context/system_context.cpp

  PUBLIC FILE_SET HEADERS
  BASE_DIRS include
  FILES
      include/stdexec/__detail/__as_awaitable.hpp
      include/stdexec/__detail/__awaitable.hpp
      include/stdexec/__detail/__basic_sender.hpp
      include/stdexec/__detail/__bulk.hpp
      include/stdexec/__detail/__completion_signatures.hpp
      include/stdexec/__detail/__concepts.hpp
      include/stdexec/__detail/__config.hpp
      include/stdexec/__detail/__connect_awaitable.hpp
      include/stdexec/__detail/__continues_on.hpp
      include/stdexec/__detail/__cpo.hpp
      include/stdexec/__detail/__debug.hpp
      include/stdexec/__detail/__diagnostics.hpp
      include/stdexec/__detail/__domain.hpp
      include/stdexec/__detail/__ensure_started.hpp
      include/stdexec/__detail/__env.hpp
      include/stdexec/__detail/__execute.hpp
      include/stdexec/__detail/__execution_fwd.hpp
      include/stdexec/__detail/__force_include.hpp
      include/stdexec/__detail/__inline_scheduler.hpp
      include/stdexec/__detail/__into_variant.hpp
      include/stdexec/__detail/__intrusive_mpsc_queue.hpp
      include/stdexec/__detail/__intrusive_ptr.hpp
      include/stdexec/__detail/__intrusive_queue.hpp
      include/stdexec/__detail/__intrusive_slist.hpp
      include/stdexec/__detail/__just.hpp
      include/stdexec/__detail/__let.hpp
      include/stdexec/__detail/__manual_lifetime.hpp
      include/stdexec/__detail/__meta.hpp
      include/stdexec/__detail/__on.hpp
      include/stdexec/__detail/__operation_states.hpp
      include/stdexec/__detail/__optional.hpp
      include/stdexec/__detail/__ranges.hpp
      include/stdexec/__detail/__read_env.hpp
      include/stdexec/__detail/__receiver_adaptor.hpp
      include/stdexec/__detail/__receiver_ref.hpp
      include/stdexec/__detail/__receivers.hpp
      include/stdexec/__detail/__run_loop.hpp
      include/stdexec/__detail/__schedule_from.hpp
      include/stdexec/__detail/__schedulers.hpp
      include/stdexec/__detail/__scope.hpp
      include/stdexec/__detail/__sender_adaptor_closure.hpp
      include/stdexec/__detail/__sender_introspection.hpp
      include/stdexec/__detail/__senders_core.hpp
      include/stdexec/__detail/__senders.hpp
      include/stdexec/__detail/__shared.hpp
      include/stdexec/__detail/__spin_loop_pause.hpp
      include/stdexec/__detail/__split.hpp
      include/stdexec/__detail/__start_detached.hpp
      include/stdexec/__detail/__starts_on.hpp
      include/stdexec/__detail/__stop_token.hpp
      include/stdexec/__detail/__stopped_as_error.hpp
      include/stdexec/__detail/__stopped_as_optional.hpp
      include/stdexec/__detail/__submit.hpp
      include/stdexec/__detail/__sync_wait.hpp
      include/stdexec/__detail/__tag_invoke.hpp
      include/stdexec/__detail/__then.hpp
      include/stdexec/__detail/__transfer_just.hpp
      include/stdexec/__detail/__transform_completion_signatures.hpp
      include/stdexec/__detail/__transform_sender.hpp
      include/stdexec/__detail/__tuple.hpp
      include/stdexec/__detail/__type_traits.hpp
      include/stdexec/__detail/__upon_error.hpp
      include/stdexec/__detail/__upon_stopped.hpp
      include/stdexec/__detail/__utility.hpp
      include/stdexec/__detail/__variant.hpp
      include/stdexec/__detail/__when_all.hpp
      include/stdexec/__detail/__with_awaitable_senders.hpp
      include/stdexec/__detail/__write_env.hpp
      
      include/stdexec/concepts.hpp
      include/stdexec/coroutine.hpp
      include/stdexec/execution.hpp
      include/stdexec/functional.hpp
      include/stdexec/stop_token.hpp

      include/exec/any_sender_of.hpp
      include/exec/async_scope.hpp
      include/exec/at_coroutine_exit.hpp
      include/exec/create.hpp
      include/exec/env.hpp
      include/exec/finally.hpp
      include/exec/inline_scheduler.hpp
      include/exec/into_tuple.hpp
      include/exec/just_from.hpp
      include/exec/libdispatch_queue.hpp
      include/exec/materialize.hpp
      include/exec/on_coro_disposition.hpp
      include/exec/on.hpp
      include/exec/repeat_effect_until.hpp
      include/exec/repeat_n.hpp
      include/exec/reschedule.hpp
      include/exec/scope.hpp
      include/exec/sequence_senders.hpp
      include/exec/sequence.hpp
      include/exec/single_thread_context.hpp
      include/exec/start_now.hpp
      include/exec/static_thread_pool.hpp
      include/exec/system_context.hpp
      include/exec/task.hpp
      include/exec/timed_scheduler.hpp
      include/exec/timed_thread_scheduler.hpp
      include/exec/trampoline_scheduler.hpp
      include/exec/variant_sender.hpp
      include/exec/when_any.hpp

      include/exec/__detail/__atomic_intrusive_queue.hpp
      include/exec/__detail/__atomic_ref.hpp
      include/exec/__detail/__basic_sequence.hpp
      include/exec/__detail/__bit_cast.hpp
      include/exec/__detail/__bwos_lifo_queue.hpp
      include/exec/__detail/__numa.hpp
      include/exec/__detail/__system_context_default_impl_entry.hpp
      include/exec/__detail/__system_context_default_impl.hpp
      include/exec/__detail/__system_context_replaceability_api.hpp
      include/exec/__detail/__xorshift.hpp
      include/exec/__detail/intrusive_heap.hpp

      include/exec/linux include/exec/linux/__detail
      include/exec/linux/__detail/memory_mapped_region.hpp
      include/exec/linux/__detail/safe_file_descriptor.hpp
      include/exec/linux/io_uring_context.hpp
      include/exec/linux/memory_mapped_region.hpp
      include/exec/linux/safe_file_descriptor.hpp

      include/exec/sequence/any_sequence_of.hpp
      include/exec/sequence/empty_sequence.hpp
      include/exec/sequence/ignore_all_values.hpp
      include/exec/sequence/iterate.hpp
      include/exec/sequence/transform_each.hpp
)

# Declare the public include directories
target_link_libraries(stdexec PUBLIC Threads::Threads)

# Enable coroutines for GCC
target_compile_options(stdexec PUBLIC
                       $<$<COMPILE_LANG_AND_ID:CXX,GNU>:-fcoroutines -fconcepts-diagnostics-depth=10>
                       $<$<COMPILE_LANG_AND_ID:CXX,MSVC>:/Zc:__cplusplus /Zc:preprocessor>
    )

##############################################################################
# Install targets ------------------------------------------------------------
include(GNUInstallDirs)
install(
  TARGETS stdexec 
  FILE_SET HEADERS
)