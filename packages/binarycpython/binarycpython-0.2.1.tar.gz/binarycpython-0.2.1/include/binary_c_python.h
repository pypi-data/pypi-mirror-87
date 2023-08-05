#pragma once
#ifndef BINARY_C_PYTHON_H
#define BINARY_C_PYTHON_H

/*
 * Include binary_C's API
 */
#include "binary_c.h"
//#include "binary_c_API.h"
//#include "binary_c_API_prototypes.h"

/* Binary_c's python API prototypes */
int run_system(char * argstring,
               long int custom_logging_func_memaddr,
               long int store_memaddr,
               long int persistent_data_memaddr,
               int write_logfile,
               int population,
               char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes);

/* =================================================================== */
/* Functions to call other API functionality like help and arglines    */
/* =================================================================== */

int return_arglines(char ** const outstring,
                char ** const errorstring,
                size_t * const nbytes);

int return_help_info(char * argstring,
                char ** const outstring,
                char ** const errorstring,
                size_t * const nbytes);

int return_help_all_info(char ** const outstring,
                char ** const errorstring,
                size_t * const nbytes);

int return_version_info(char ** const outstring,
                char ** const errorstring,
                size_t * const nbytes);

/* =================================================================== */
/* Functions to call other functionality                               */
/* =================================================================== */

long int return_store_memaddr(char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes);

long int return_persistent_data_memaddr(char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes);

int free_persistent_data_memaddr_and_return_json_output(long int persistent_data_memaddr,
               char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes);

int free_store_memaddr(long int store_memaddr,
               char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes);


/* C macros */
#define BINARY_C_APITEST_VERSION 0.1
#define APIprint(...) APIprintf(__VA_ARGS__);
#define NO_OUTPUT

#ifdef BINARY_C_PYTHON_DEBUG
  #define debug_printf(fmt, ...)  printf(fmt, ##__VA_ARGS__);
#else
  #define debug_printf(fmt, ...)    /* Do nothing */
#endif

#endif // BINARY_C_C_PYTHON_H
