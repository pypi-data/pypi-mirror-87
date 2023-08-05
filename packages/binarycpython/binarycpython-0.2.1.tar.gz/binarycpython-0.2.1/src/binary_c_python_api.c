#include "binary_c_python.h"
#include <time.h>
#include <sys/timeb.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>

/* Binary_c python API 
 * Set of c-functions that interface with the binary_c api.
 * These functions are called by python, first through binary_c_python.c, 
 * and there further instructions are given on how to interface
 * 
 * Contains several functions:
 * // evolution
 * run_system

 * // utility
 * return_arglines
 * return_help_info
 * return_help_all_info
 * return_version_info

 * // other
 * create_store
 *
 */

// #define _CAPTURE
#ifdef _CAPTURE
static void show_stdout(void);
static void capture_stdout(void);
#endif

/* global variables */
int out_pipe[2];
int stdoutwas;

/* =================================================================== */
/* Functions to evolve systems                                         */
/* =================================================================== */

/* 
Function that runs a system. Has multiple input parameters:
Big function. Takes several arguments. See binary_c_python.c docstring.
TODO: Describe each input
*/
int run_system(char * argstring,
               long int custom_logging_func_memaddr,
               long int store_memaddr,
               long int persistent_data_memaddr,
               int write_logfile,
               int population,
               char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    /* memory for system */
    struct libbinary_c_stardata_t *stardata = NULL;

    // Store:
    /* Check the value of the store_memaddr */
    struct libbinary_c_store_t *store;
    if(store_memaddr != -1)
    {
        // load the store from the integer that has been passed
        store = (void*)store_memaddr;
    }
    else
    {
        // struct libbinary_c_store_t * store = NULL;
        store = NULL;
    }

    // persistent_data:
    struct libbinary_c_persistent_data_t *persistent_data;
    if(persistent_data_memaddr != -1)
    {
        // load the persistent data from the long int that has been passed
        persistent_data = (void*)persistent_data_memaddr;
        debug_printf("Took long int memaddr %ld and loaded it to %p\n", persistent_data_memaddr, (void*)&persistent_data);
    }
    else
    {
        persistent_data = NULL;
        debug_printf("persistent_data memory adress was -1, now setting it to NULL\n");
    }

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        &persistent_data,   // persistent_data
                        &argstring,         // argv
                        -1                  // argc
    );

    // Add flag to enable
    /* disable logging */
    if(write_logfile != 1)
    {
        snprintf(stardata->preferences->log_filename,
                 STRING_LENGTH-1,
                 "%s",
                 "/dev/null");
        snprintf(stardata->preferences->api_log_filename_prefix,
                 STRING_LENGTH-1,
                 "%s",
                 "/dev/null");
    }

    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* Check the value of the custom_logging_memaddr */
    if(custom_logging_func_memaddr != -1)
    {
        stardata->preferences->custom_output_function = (void*)(struct stardata_t *)custom_logging_func_memaddr;
    }

    debug_printf("ensemble_defer: %d\n", stardata->preferences->ensemble_defer);

    /* do binary evolution */
    binary_c_evolve_for_dt(stardata,
                           stardata->model.max_evolution_time);
        
    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);

    /* Determine whether to free the store memory adress*/
    Boolean free_store = FALSE;
    if (store_memaddr == -1)
    {
        Boolean free_store = TRUE;
    }

    /* Determine whether to free the persistent data memory adress*/
    Boolean free_persistent_data = FALSE;
    if (persistent_data_memaddr == -1)
    {
        debug_printf("Decided to free the persistent_data memaddr\n");
        Boolean free_persistent_data = TRUE;
    }

    /* free stardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        free_store,                 // free_store
        FALSE,                      // free_raw_buffer
        free_persistent_data        // free_persistent
    );

    return 0;
}

/* =================================================================== */
/* Functions to call other API functionality like help and arglines    */
/* =================================================================== */

int return_arglines(char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    /* memory for N binary systems */
    struct libbinary_c_stardata_t *stardata = NULL;
    struct libbinary_c_store_t *store = NULL;
    char *empty_str = "";

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        NULL,               // persistent_data
                        &empty_str,         // argv
                        -1                  // argc
    );

    /* disable logging */
    snprintf(stardata->preferences->log_filename,
             STRING_LENGTH-1,
             "%s",
             "/dev/null");
    snprintf(stardata->preferences->api_log_filename_prefix,
             STRING_LENGTH-1,
             "%s",
             "/dev/null");

    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* List available arguments */
    binary_c_list_args(stardata);

    /* get buffer pointer */
    binary_c_buffer_info(stardata,buffer,nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata,error_buffer);
    
    /* free stardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        TRUE,                       // free_store
        FALSE,                      // free_raw_buffer
        TRUE                        // free_persistent
    );
    
    return 0;
}


int return_help_info(char * argstring,
               char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    struct libbinary_c_stardata_t *stardata = NULL;
    struct libbinary_c_store_t *store = NULL;

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        NULL,               // persistent_data
                        &argstring,         // argv
                        -1                  // argc
    );

    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* Ask the help api */
    binary_c_help(stardata, argstring);
        
    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);
        
    /* free stardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        TRUE,                       // free_store
        FALSE,                      // free_raw_buffer
        TRUE                        // free_persistent
    );

    return 0;
}


int return_help_all_info(char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    struct libbinary_c_stardata_t *stardata = NULL;
    struct libbinary_c_store_t *store = NULL;
    char * empty_str = "";

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        NULL,               // persistent_data
                        &empty_str,         // argv
                        -1                  // argc
    );

    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* Ask the help api */
    binary_c_help_all(stardata);
        
    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);
        
    /* free stardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        TRUE,                       // free_store
        FALSE,                      // free_raw_buffer
        TRUE                        // free_persistent
    );

    return 0;
}


int return_version_info(char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    struct libbinary_c_stardata_t *stardata = NULL;
    struct libbinary_c_store_t * store = NULL;
    char * empty_str = "";

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        NULL,               // persistent_data
                        &empty_str,         // argv
                        -1                  // argc
    );

    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* Ask the help api */
    binary_c_version(stardata);
        
    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);
    
    /* free stardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        TRUE,                       // free_store
        FALSE,                      // free_raw_buffer
        TRUE                        // free_persistent
    );

    return 0;
}

/* =================================================================== */
/* Functions set up memoery adresses                                   */
/* =================================================================== */

long int return_store_memaddr(char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    struct libbinary_c_stardata_t * stardata = NULL;
    struct libbinary_c_store_t * store = NULL;
    char * empty_str = "";

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        NULL,               // persistent_data
                        &empty_str,         // argv
                        -1                  // argc
    );

    /* output to strings */
    // stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    // stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);
        
    /* free stardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        FALSE,                      // free_store
        FALSE,                      // free_raw_buffer
        TRUE                        // free_persistent
    );

    /* convert the pointer */ 
    uintptr_t store_memaddr_int = (uintptr_t)store; // C Version converting ptr to int
    debug_printf("store is at address: %p store_memaddr_int: %ld\n", (void*)&store, store_memaddr_int);

    /* Return the memaddr as an int */
    return store_memaddr_int;
}


long int return_persistent_data_memaddr(char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    /* Function to allocate the persistent_data_memaddr */
    struct libbinary_c_stardata_t *stardata = NULL;
    struct libbinary_c_store_t * store = NULL;
    struct libbinary_c_persistent_data_t * persistent_data = NULL; 
    char * empty_str = "";

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        &persistent_data,   // persistent_data
                        &empty_str,         // argv
                        -1                  // argc
    );

    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);
        
    /* convert the pointer */
    uintptr_t persistent_data_memaddr_int = (uintptr_t)stardata->persistent_data; // C Version converting ptr to int
    debug_printf("persistent_data is at address: %p persistent_data_memaddr_int: %ld\n", (void*)&stardata->persistent_data, persistent_data_memaddr_int);
    
    /* free stardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        TRUE,                       // free_store
        FALSE,                      // free_raw_buffer
        FALSE                       // free_persistent
    );

    /* Return the memaddr as an int */
    return persistent_data_memaddr_int;
}

/* =================================================================== */
/* Functions free memory                                               */
/* =================================================================== */

int free_persistent_data_memaddr_and_return_json_output(long int persistent_data_memaddr,
               char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    struct libbinary_c_store_t *store = NULL;
    struct libbinary_c_stardata_t *stardata = NULL;
    char * empty_str = "";

    // persistent_data:
    struct libbinary_c_persistent_data_t *persistent_data;
    if(persistent_data_memaddr != -1)
    {
        // load the persistent data from the long int that has been passed
        persistent_data = (void*)persistent_data_memaddr;
        debug_printf("Took long int memaddr %ld and loaded it to %p\n", persistent_data_memaddr, (void*)&persistent_data);
    }
    else
    {
        printf("ERROR: this function needs a valid persistent_data_memaddr value. not -1\n");
        // persistent_data = NULL;
        // TODO: put break in the function here. 
    }

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        &persistent_data,   // persistent_data
                        &empty_str,         // argv
                        -1                  // argc
    );

    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* get output and free memory */
    binary_c_output_to_json(stardata);

    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);

    /* free the reststardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        TRUE,                       // free_store
        FALSE,                      // free_raw_buffer
        FALSE                       // free_persistent
    );

    return 0;
}

int free_store_memaddr(long int store_memaddr,
               char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes)
{
    struct libbinary_c_stardata_t *stardata = NULL;
    struct libbinary_c_persistent_data_t *persistent_data = NULL;
    char * empty_str = "";

    // Store:
    /* Check the value of the store_memaddr */
    struct libbinary_c_store_t *store;
    if(store_memaddr != -1)
    {
        // load the store from the integer that has been passed
        store = (void*)store_memaddr;
        debug_printf("Took long int store_memaddr %ld and loaded it to %p\n", store_memaddr, (void*)&store);
    }
    else
    {
        store = NULL;
    }

    /* Set up new system */
    binary_c_new_system(&stardata,          // stardata
                        NULL,               // previous_stardatas
                        NULL,               // preferences
                        &store,             // store
                        &persistent_data,   // persistent_data
                        &empty_str,         // argv
                        -1                  // argc
    );

    printf("freed store memaddr\n");
    /* output to strings */
    stardata->preferences->internal_buffering = INTERNAL_BUFFERING_STORE;
    stardata->preferences->batchmode = BATCHMODE_LIBRARY;

    /* get buffer pointer */
    binary_c_buffer_info(stardata, buffer, nbytes);
    
    /* get error buffer pointer */
    binary_c_error_buffer(stardata, error_buffer);

    /* free the reststardata (except the buffer) */
    binary_c_free_memory(&stardata, // Stardata
        TRUE,                       // free_preferences
        TRUE,                       // free_stardata
        TRUE,                       // free_store
        FALSE,                      // free_raw_buffer
        TRUE                        // free_persistent
    );

    return 0;
}
