from conan import ConanFile
from conan.tools.cmake import cmake_layout

class HelloConan(ConanFile):
    name = "hello"
    version = "0.1"
    license = "None"
    author = "Lebedov Test(from Pavel Filonov filonovpv@gmail.com)"
    url = "https://github.com/lebedov89/otus"
    description = "C++ pets"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "CMakeToolchain", "CMakeDeps"

    exports_sources = "src/*", "CMakeLists.txt", "version.h.in", "cmake/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def requirements(self):
        self.requires("gtest/1.14.0")

    def layout(self):
        cmake_layout(self)

    # def generate(self):
    #     tc = CMakeToolchain(self)
    #     tc.generate()

    def package(self):
        self.copy("*.h", dst="include", src="src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]
        if self.settings.compiler in ["gcc", "clang", "apple-clang"]:
            self.cpp_info.cxxflags = ["-std=c++17"]
