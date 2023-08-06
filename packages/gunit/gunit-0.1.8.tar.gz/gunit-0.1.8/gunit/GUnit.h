#pragma once
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

typedef void (*gunit_function_t)();

/**
 * All asserts will call this function. GDB will catch any call to this function
 * and logs it
 */
__attribute__((optimize(0)))
inline static bool gunit_hook(uintmax_t expected, uintmax_t result, uintmax_t line_number, const char *file, bool no) {
  return (expected == result) ^ no;
}

/**
 * Function for asserting arrays and objects
 */
__attribute__((optimize(0)))
inline static bool gunit_array(void *expected, void *result, uintmax_t size, uintmax_t line_number, const char *file, bool no) {
  uint8_t *ex = (uint8_t *) expected;
  uint8_t *re = (uint8_t *) result;

  // Check if equal
  for (uint32_t i = 0; i < size; ++i) {
    if (ex[i] != re[i])
      return gunit_hook(ex[i], re[i], line_number, file, no);
  }

  // If no differences were found
  return gunit_hook((uintmax_t) expected, (uintmax_t) result, line_number, file, !no);
}

/**
 * This has to be called at the end of a test suite
 */
__attribute__((optimize(0)))
inline static void gunit_end() {
  return;
}

/**
 * Execute a test suite
 */
__attribute__((optimize(0)))
inline static void gunit_suite(gunit_function_t before, gunit_function_t after, gunit_function_t *tests, uintmax_t nr_of_tests) {
  for (uintmax_t i = 0; i < nr_of_tests; ++i) {
    if (before)
      (*before)();

    (*tests[i])();

    if (after)
      (*after)();
  }
}

/**
 * Execute given tests with before and after functions
 */
#define GEXECUTE(before, after, ...)  {gunit_suite(before, after, (gunit_function_t[]){__VA_ARGS__}, \
    sizeof((gunit_function_t[]){__VA_ARGS__}) / sizeof(gunit_function_t));}

/**
 * Exevute tests without before or after
 */
#define GSIMPLE_EXECUTE(...) GEXECUTE(NULL, NULL, __VA_ARGS__)

/**
 * Signal the end of all the tests
 */
#define GEND() {gunit_end();}

/**
 * Assert if given values are equel.
 */
#define GASSERT(expected, result)  {if (!gunit_hook((uintmax_t) expected, (uintmax_t) result, __LINE__, __FILE__, false)) return;}

/**
 * Assert if given values are not equal.
 */
#define GNOT_ASSERT(not_expected, result) {if (!gunit_hook((uintmax_t) not_expected, (uintmax_t) result, __LINE__, __FILE__, true)) return;}

/**
 * Assert if given arrays contain same elements
 */
#define GARRAY_ASSERT(expected, result, nr_of_elements) {for (int __gi = 0; __gi < nr_of_elements; ++__gi) {if (!gunit_array((void *) expected, (void *) result, nr_of_elements * sizeof(typeof(expected[0])), __LINE__, __FILE__, false)) return;}}

/**
 * Assert if given arrays don't have same elements
 */
#define GARRAY_NOT_ASSERT(not_expected, result, nr_of_elements) {for (int __gi = 0; __gi < nr_of_elements; ++__gi) {if (!gunit_array((void *) not_expected, (void *) result, nr_of_elements * sizeof(typeof(not_expected[0])), __LINE__, __FILE__, true)) return;}}

/**
 * Assert if given structs contain same values
 */
#define GSTRUCT_ASSERT(expected, result) {if (!gunit_array((void *) &expected, (void *) &result, sizeof(typeof(expected)), __LINE__, __FILE__, false)) return;}

/**
 * Assert if given structs don't contain same values
 */
#define GSTRUCT_NOT_ASSERT(not_expected, result) {if (!gunit_array((void *) &not_expected, (void *) &result, sizeof(typeof(not_expected)), __LINE__, __FILE__, true)) return;}
