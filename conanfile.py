from conans import ConanFile, CMake, tools


class LibuvcConan(ConanFile):
    name = "libuvc"
    version = "0.0.10"
    license = "https://raw.githubusercontent.com/pupil-labs/libuvc/master/LICENSE.txt"
    author = "KudzuRunner"
    url = "https://github.com/kudzurunner/conan-libuvc"
    description = "A cross-platform library for USB video devices"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    exports = (
        "patches/*.patch")
    git_hash = "b394ccc"
    suffix = ""

    def requirements(self):
        self.requires.add('libusb/1.0.23@bincrafters/stable')
        if self.settings.os == "Windows":
            self.requires.add('pthreads4w/2.9.1@bincrafters/stable')

    def configure(self):
        self.options["libusb"].shared = self.options.shared
        if self.settings.os == "Windows":
            self.options["pthreads4w"].shared = self.options.shared

    def source(self):
        git = tools.Git(folder=self.name)
        git.clone("https://github.com/pupil-labs/libuvc.git", branch="master")
        git.checkout(self.git_hash)

        tools.patch(base_path=self.name, patch_file="patches/fixed_paths.patch", strip=1)
        tools.patch(base_path=self.name, patch_file="patches/fixed_include.patch", strip=1)

        self.suffix = ("_d" if self.settings.build_type == "Debug" else "")
        tools.replace_in_file("{}/CMakeLists.txt".format(self.name), "project(libuvc)",
                              '''project(libuvc)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(NOT CMAKE_DEBUG_POSTFIX)
  set(CMAKE_DEBUG_POSTFIX %s)
endif()''' % self.suffix)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_BUILD_TYPE"] = self.settings.build_type
        cmake.definitions["CMAKE_BUILD_TARGET"] = "Shared" if self.options.shared else "Static"
        cmake.configure(source_folder=self.name)
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.name)
        self.copy("*.h", dst="include", src="include")
        self.copy("libuvc.h", dst="include/libuvc", src=self.name+"/include/libuvc")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["uvc" + self.suffix]
