cmake_minimum_required(VERSION 2.8)

project(jheaps)

list(INSERT CMAKE_MODULE_PATH 0 "${CMAKE_CURRENT_SOURCE_DIR}/etc/cmake")

find_package(Java 11)
find_package(JNI)
find_program(NativeImage native-image REQUIRED)
find_package(Maven REQUIRED)

message(STATUS "native-image found at ${NativeImage}")

include(GNUInstallDirs)

SET(JHEAPS_LIBRARY "${CMAKE_SHARED_LIBRARY_PREFIX}jheaps_capi${CMAKE_SHARED_LIBRARY_SUFFIX}")

add_custom_command(
    OUTPUT ${CMAKE_BINARY_DIR}/target/jheaps-capi-0.1.jar
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_SOURCE_DIR}/jheaps-capi/pom.xml ${CMAKE_BINARY_DIR}/
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_SOURCE_DIR}/jheaps-capi/src ${CMAKE_BINARY_DIR}/src
    COMMAND mvn -B -f ${CMAKE_BINARY_DIR} package
    COMMENT "Building jar file with C native scopes"
)

add_custom_target(
    build-jar 
    DEPENDS ${CMAKE_BINARY_DIR}/target/jheaps-capi-0.1.jar
)

add_custom_command(
    OUTPUT ${JHEAPS_LIBRARY} jheaps_capi.h jheaps_capi_dynamic.h graal_isolate.h graal_isolate_dynamic.h
    COMMAND native-image -cp ${CMAKE_BINARY_DIR}/target/jheaps-capi-0.1.jar --no-fallback --initialize-at-build-time --no-server --shared
    COMMAND ${CMAKE_COMMAND} -E rename ${CMAKE_BINARY_DIR}/jheaps_capi${CMAKE_SHARED_LIBRARY_SUFFIX} ${CMAKE_BINARY_DIR}/${JHEAPS_LIBRARY}
    DEPENDS build-jar
    COMMENT "Producing shared library from jar file"
)

if(APPLE)
  add_custom_command(
    OUTPUT ${JHEAPS_LIBRARY} APPEND
    COMMAND install_name_tool -id "@rpath/${JHEAPS_LIBRARY}" ${CMAKE_BINARY_DIR}/${JHEAPS_LIBRARY}
  )
endif(APPLE)

add_custom_target(
    build-jheaps-sharedlib
    DEPENDS ${JHEAPS_LIBRARY}
)

set_property(SOURCE ${CMAKE_BINARY_DIR}/jheaps-capi/jheaps_capi.h PROPERTY GENERATED 1)
set_property(SOURCE ${CMAKE_BINARY_DIR}/jheaps-capi/jheaps_capi_dynamic.h PROPERTY GENERATED 1)
set_property(SOURCE ${CMAKE_BINARY_DIR}/jheaps-capi/graal_isolate.h PROPERTY GENERATED 1)
set_property(SOURCE ${CMAKE_BINARY_DIR}/jheaps-capi/graal_isolate_dynamic.h PROPERTY GENERATED 1)
set_property(SOURCE ${CMAKE_BINARY_DIR}/jheaps-capi/${JHEAPS_LIBRARY} PROPERTY GENERATED 1)

add_library(jheaps_capi SHARED IMPORTED)
set_property(TARGET jheaps_capi PROPERTY IMPORTED_LOCATION ${CMAKE_BINARY_DIR}/${JHEAPS_LIBRARY})
IF(WIN32)
    set_property(TARGET jheaps_capi PROPERTY IMPORTED_IMPLIB ${CMAKE_BINARY_DIR}/jheaps_capi.lib)
ENDIF(WIN32)

add_dependencies(jheaps_capi build-jheaps-sharedlib)

install(
    FILES
    ${CMAKE_BINARY_DIR}/jheaps_capi.h 
    ${CMAKE_BINARY_DIR}/jheaps_capi_dynamic.h
    ${CMAKE_BINARY_DIR}/graal_isolate.h
    ${CMAKE_BINARY_DIR}/graal_isolate_dynamic.h
    ${CMAKE_SOURCE_DIR}/jheaps-capi/src/main/native/jheaps_capi_types.h
    DESTINATION 
    ${CMAKE_INSTALL_INCLUDEDIR}/jheaps_capi
)

install(
    FILES
    ${CMAKE_BINARY_DIR}/${JHEAPS_LIBRARY}
    DESTINATION        
    ${CMAKE_INSTALL_LIBDIR}
)

enable_testing()
include(CTest)

set(
    TEST_SOURCES 
    "test_double_pairing.c"
    "test_long_pairing.c"
)
foreach(testsourcefile ${TEST_SOURCES})
    string(REPLACE ".c" "" testname ${testsourcefile})
    add_executable(${testname} test/${testsourcefile})
    target_include_directories(${testname} PUBLIC ${CMAKE_BINARY_DIR} ${CMAKE_SOURCE_DIR}/jheaps-capi/src/main/native)
    target_link_libraries(${testname} jheaps_capi)
    if(UNIX)
      target_link_libraries(${testname} m)
    endif(UNIX)
    add_test(NAME ${testname} COMMAND ${testname})
endforeach(testsourcefile ${TEST_SOURCES})

