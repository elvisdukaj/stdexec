from conan import ConanFile
from conan.tools.build.cppstd import check_min_cppstd
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import copy
from conan.tools.scm import Git

class StdexecPackage(ConanFile):
  name = "stdexec"
  description = "std::execution"
  version = "0.11.0"
  author = "Michał Dominiak, Lewis Baker, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach"
  topics = ("WG21", "concurrency")
  homepage = "https://github.com/NVIDIA/stdexec"
  url = "https://github.com/NVIDIA/stdexec"
  license = "Apache 2.0"

  settings = "os", "arch", "compiler", "build_type"
  exports_sources = (
    "include/*",
    "src/*",
    "CMakeLists.txt"
  )
  generators = "CMakeToolchain", "CMakeDeps"

  def validate(self):
    check_min_cppstd(self, "20")

  def set_version(self):
    if not self.version:
      git = Git(self, self.recipe_folder)
      self.version = git.get_commit()

  def layout(self):
    cmake_layout(self)

  def build(self):
    cmake = CMake(self)
    cmake.configure()
    cmake.build()

  def package(self):
    cmake = CMake(self)
    cmake.install()

  def package_info(self):
    self.cpp_info.set_property("cmake_file_name", "stdexec")
    self.cpp_info.set_property("cmake_target_name", "stdexec::stdexec")

    self.cpp_info.libs = ["stdexec"]
    if self.settings.compiler == "msvc":
      self.cpp_info.cxxflags = ["/Zc:__cplusplus", "/Zc:preprocessor"]
    else:
      self.cpp_info.cxxflags = ["-fcoroutines", "-fconcepts-diagnostics-depth=10"]


