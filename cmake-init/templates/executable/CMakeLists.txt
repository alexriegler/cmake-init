cmake_minimum_required(VERSION 3.26)

include(cmake/prelude.cmake)

project(
    {= name =}
    VERSION {= version =}
    DESCRIPTION "{= description =}"
    HOMEPAGE_URL "{= homepage =}"
    LANGUAGES CXX
)

include(cmake/project-is-top-level.cmake)
include(cmake/variables.cmake)

# ---- Common compiler options

add_library({= name =}_compiler_flags INTERFACE)

set(gcc_like_cxx "$<COMPILE_LANG_AND_ID:CXX,ARMClang,AppleClang,Clang,GNU,LCC>")
set(msvc_cxx "$<COMPILE_LANG_AND_ID:CXX,MSVC>")
target_compile_options({= name =}_compiler_flags INTERFACE
    "$<${gcc_like_cxx}:$<BUILD_INTERFACE:-Wall;-Wextra;-Wpedantic;-Wconversion;-Wsign-conversion;-Wcast-qual;-Wformat=2;-Wundef;-Werror=float-equal;-Wshadow;-Wcast-align;-Wunused;-Wnull-dereference;-Wdouble-promotion;-Wimplicit-fallthrough;-Wextra-semi;-Woverloaded-virtual;-Wnon-virtual-dtor;-Wold-style-cast>>"
    "$<${msvc_cxx}:$<BUILD_INTERFACE:-utf-8;-w14165;-w44242;-w44254;-w44263;-w34265;-w34287;-w44296;-w44365;-w44388;-w44464;-w14545;-w14546;-w14547;-w14549;-w14555;-w34619;-w34640;-w24826;-w14905;-w14906;-w14928;-w45038;-W4;-permissive-;-volatile:iso;-Zc:preprocessor;-Zc:__cplusplus;-Zc:externConstexpr;-Zc:throwingNew;-EHsc>>"
)

# ---- Declare library ----

add_library(
    {= name =}_lib OBJECT
    source/lib.ixx
)

target_compile_features({= name =}_lib PUBLIC cxx_std_{= std =}){% if pm %}

find_package(fmt REQUIRED)
target_link_libraries({= name =}_lib PRIVATE fmt::fmt){% end %}

target_link_libraries({= name =}_lib PUBLIC {= name =}_compiler_flags)

if (MSVC)
  # HACK: This is a workaround to get STL modules working with MSVC.
  #       See this post for more info:
  #       https://gitlab.kitware.com/cmake/cmake/-/issues/24922
  set_target_properties(
    {= name =}_lib PROPERTIES
    VS_GLOBAL_BuildStdModules "true"
  )
  set_target_properties(
    {= name =}_lib PROPERTIES
    VS_USER_PROPS "${CMAKE_SOURCE_DIR}/experimental/buildstlmodules.props"
  )

  # Variables for correcting module .obj filename (removing .ixx)
  set({= name =}_lib_obj_path "$<TARGET_OBJECTS:{= name =}_lib>")
  set({= name =}_lib_obj_parent_path "$<PATH:GET_PARENT_PATH,${{= name =}_lib_obj_path}>")
  set({= name =}_lib_obj_file_stem "$<PATH:GET_STEM,${{= name =}_lib_obj_path}>")
  set({= name =}_lib_obj_file_ext "$<PATH:GET_EXTENSION,${{= name =}_lib_obj_path}>")

  set({= name =}_lib_obj_wrong_path "${{= name =}_lib_obj_parent_path}/${{= name =}_lib_obj_file_stem}.ixx${{= name =}_lib_obj_file_ext}")
  set({= name =}_lib_obj_correct_path "${{= name =}_lib_obj_parent_path}/${{= name =}_lib_obj_file_stem}${{= name =}_lib_obj_file_ext}")
endif()

# ---- Declare executable ----

add_executable({= name =}_exe source/main.cpp)
add_executable({= name =}::exe ALIAS {= name =}_exe)

set_property(TARGET {= name =}_exe PROPERTY OUTPUT_NAME {= name =})

target_compile_features({= name =}_exe PRIVATE cxx_std_{= std =})

target_link_libraries({= name =}_exe PRIVATE {= name =}_lib)

if (MSVC)
  # HACK: This is a workaround to get STL modules working with MSVC.
  #       See this post for more info:
  #       https://gitlab.kitware.com/cmake/cmake/-/issues/24922
  set_target_properties(
    {= name =}_exe PROPERTIES
    VS_GLOBAL_BuildStdModules "true"
  )
  set_target_properties(
    {= name =}_exe PROPERTIES
    VS_USER_PROPS "${CMAKE_SOURCE_DIR}/experimental/buildstlmodules.props"
  )

  # HACK: This is a workaround for the .obj filenames produced by modules with MSVC.
  #       See this issue for more info:
  #       https://gitlab.kitware.com/cmake/cmake/-/issues/25732
  # Correct library module .obj filenames (remove .ixx)
  # (Must be done here since object libraries can't have PRE_BUILD commands)
  find_package(Python)

  add_custom_command(
      TARGET {= name =}_exe
      PRE_BUILD
      COMMAND ${Python_EXECUTABLE} "${CMAKE_SOURCE_DIR}/experimental/obj_fixer.py"
              ${PROJECT_BINARY_DIR}
              {= name =}_lib
              $<CONFIG>
      COMMENT "Running python script..."
  )
endif()

# ---- Install rules ----

if(NOT CMAKE_SKIP_INSTALL_RULES)
  include(cmake/install-rules.cmake)
endif()

# ---- Developer mode ----

if(NOT {= name =}_DEVELOPER_MODE)
  return()
elseif(NOT PROJECT_IS_TOP_LEVEL)
  message(
      AUTHOR_WARNING
      "Developer mode is intended for developers of {= name =}"
  )
endif()

include(cmake/dev-mode.cmake)
