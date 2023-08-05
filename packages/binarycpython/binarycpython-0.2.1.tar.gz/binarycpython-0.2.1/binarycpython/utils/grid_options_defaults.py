"""
Module that contains the default options for the population gric code.
"""

import os

from binarycpython.utils.custom_logging_functions import temp_dir

grid_options_defaults_dict = {
    ##########################
    # general (or unordered..)
    ##########################
    "amt_cores": 1,  # total amount of cores used to evolve the population
    "binary": 0,  # FLag on whether the systems are binary systems or single systems.
    "parse_function": None,  # FUnction to parse the output with.
    "tmp_dir": temp_dir(),  # Setting the temp dir of the program
    "main_pid": -1,  # Placeholder for the main process id of the run.
    # "output_dir":
    "commandline_input": "",
    ##########################
    # Execution log:
    ##########################
    "verbosity": 0,  # Level of verbosity of the simulation. 0=INFO,
    "log_file": os.path.join(
        temp_dir(), "binary_c_python.log"
    ),  # Set to None to not log to file. The directory will be created
    ##########################
    # binary_c files
    ##########################
    "binary_c_executable": os.path.join(
        os.environ["BINARY_C"], "binary_c"
    ),  # TODO: make this more robust
    "binary_c_shared_library": os.path.join(
        os.environ["BINARY_C"], "src", "libbinary_c.so"
    ),  # TODO: make this more robust
    "binary_c_config_executable": os.path.join(
        os.environ["BINARY_C"], "binary_c-config"
    ),  # TODO: make this more robust
    "binary_c_dir": os.environ["BINARYC_DIR"],
    ##########################
    # Custom logging
    ##########################
    "C_auto_logging": None,  # Should contain a dictionary where the kes are they headers
    # and the values are lists of parameters that should be logged.
    # This will get parsed by autogen_C_logging_code in custom_loggion_functions.py
    "C_logging_code": None,  # Should contain a string which holds the logging code.
    "custom_logging_func_memaddr": -1,  # Contains the custom_logging functions memory address
    "custom_logging_shared_library_file": None,
    ##########################
    # Store pre-loading:
    ##########################
    "store_memaddr": -1,  # Contains the store object memory adress, useful for preloading.
    # defaults to -1 and isnt used if thats the default then.
    ##########################
    # Log args: logging of arguments
    ##########################
    "log_args": 0,  #
    "log_args_dir": "/tmp/",
    ##########################
    # Population evolution
    ##########################
    ## General
    "evolution_type": "mp",  # Flag for type of population evolution
    "evolution_type_options": [
        "mp",
        "linear",
    ],  # available choices for type of population evolution
    "system_generator": None,  # value that holds the function that generates the system
    # (result of building the grid script)
    "population_type": "grid",  #
    "population_type_options": [
        "grid",
        "source_file",
    ],  # Available choices for type of population generation # TODO: fill later with monte carlo etc
    "source_file_filename": None,  # filename for the source
    "count": 0,  # total count of systems
    "probtot": 0,  # total probability
    "weight": 1.0,  # weighting for the probability
    "repeat": 1.0,  # number of times to repeat each system (probability is adjusted to be 1/repeat)
    "results_per_worker": {},  # dict which can store info per worker. meh. doesnt work properly
    "start_time_evolution": 0,  # Start time of the grid
    "end_time_evolution": 0,  # end time of the grid
    "error": 0,  # error?
    "failed_count": 0,  # amt of failed systems
    "failed_prob": 0,  # Summed probability of failed systems
    "id": 0,  # Random id of this grid/population run,
    "modulo": 1,  # run modulo n of the grid.
    ## Grid type evolution
    "grid_variables": {},  # grid variables
    "grid_code": None,  # literal grid code: contains the whole script that'll be written to a file
    "gridcode_filename": None,  # filename of gridcode
    ## Monte carlo type evolution
    # TODO: make MC options
    ## Evolution from source file
    # TODO: make run from sourcefile options.
    ## Other no yet implemented parts for the population evolution part
    #     # start at this model number: handy during debugging
    #     # to skip large parts of the grid
    #     start_at => 0
    #     global_error_string => undef,
    #     monitor_files => [],
    #     nextlogtime   => 0,
    #     nthreads      => 1, # number of threads
    #     # start at model offset (0-based, so first model is zero)
    #     offset        => 0,
    #     resolution=>{
    #         shift   =>0,
    #         previous=>0,
    #         n       =>{} # per-variable resolution
    #     },
    #     thread_q      => undef,
    #     threads       => undef, # array of threads objects
    #     tstart        => [gettimeofday], # flexigrid start time
    #     __nvar        => 0, # number of grid variables
    #     _varstub      => undef,
    #     _lock         => undef,
    #     _evcode_pids  => [],
    # };
    ########################################
    # Slurm stuff
    ########################################
    "slurm": 0,  # dont use the slurm by default. 1 = use slurm
    "slurm_ntasks": 1,  # CPUs required per array job: usually only need this
    "slurm_command": "",  # Command that slurm runs (e.g. evolve or join_datafiles)
    "slurm_dir": "",  # working directory containing scripts output logs etc.
    "slurm_njobs": 0,  # number of scripts; set to 0 as default
    "slurm_jobid": "",  # slurm job id (%A)
    "slurm_memory": 512,  # in MB, the memory use of the job
    "slurm_warn_max_memory": 1024,  # in MB : warn if mem req. > this
    "slurm_use_all_node_CPUs": 0,  # 1 = use all of a node's CPUs. 0 = use a given amount of CPUs
    "slurm_postpone_join": 0,  # if 1 do not join on slurm, join elsewhere. want to do it off the slurm grid (e.g. with more RAM)
    "slurm_jobarrayindex": "",  # slurm job array index (%a)
    "slurm_jobname": "binary_grid",  # default
    "slurm_partition": None,
    "slurm_time": 0,  # total time. 0 = infinite time
    "slurm_postpone_sbatch": 0,  # if 1: don't submit, just make the script
    "slurm_array": None,  # override for --array, useful for rerunning jobs
    "slurm_use_all_node_CPUs": 0,  # if given nodes, set to 1
    # if given CPUs, set to 0
    # you will want to use this if your Slurm SelectType is e.g. linear
    # which means it allocates all the CPUs in a node to the job
    "slurm_control_CPUs": 0,  # if so, leave this many for Pythons control (0)
    "slurm_array": None,  # override for --array, useful for rerunning jobs
    "slurm_partition": None,  # MUST be defined
    "slurm_extra_settings": {},  # Place to put extra configuration for the SLURM batch file. The key and value of the dict will become the key and value of the line in te slurm batch file. Will be put in after all the other settings (and before the command). Take care not to overwrite something without really meaning to do so.
    ########################################
    # Condor stuff
    ########################################
    "condor": 0,  # 1 to use condor, 0 otherwise
    "condor_command": "",  # condor command e.g. "evolve", "join"
    "condor_dir": "",  # working directory containing e.g. scripts, output, logs (e.g. should be NFS available to all)
    "condor_njobs": "",  # number of scripts/jobs that CONDOR will run in total
    "condor_jobid": "",  # condor job id
    "condor_postpone_join": 0,  # if 1, data is not joined, e.g. if you want to do it off the condor grid (e.g. with more RAM)
    # "condor_join_machine": None, # if defined then this is the machine on which the join command should be launched (must be sshable and not postponed)
    "condor_join_pwd": "",  # directory the join should be in (defaults to $ENV{PWD} if undef)
    "condor_memory": 1024,  # in MB, the memory use (ImageSize) of the job
    "condor_universe": "vanilla",  # usually vanilla universe
    "condor_extra_settings": {},  # Place to put extra configuration for the CONDOR submit file. The key and value of the dict will become the key and value of the line in te slurm batch file. Will be put in after all the other settings (and before the command). Take care not to overwrite something without really meaning to do so.
    # snapshots and checkpoints
    # condor_snapshot_on_kill=>0, # if 1 snapshot on SIGKILL before exit
    # condor_load_from_snapshot=>0, # if 1 check for snapshot .sv file and load it if found
    # condor_checkpoint_interval=>0, # checkpoint interval (seconds)
    # condor_checkpoint_stamp_times=>0, # if 1 then files are given timestamped names
    # (warning: lots of files!), otherwise just store the lates
    # condor_streams=>0, # stream stderr/stdout by default (warning: might cause heavy network load)
    # condor_save_joined_file=>0, # if 1 then results/joined contains the results
    # (useful for debugging, otherwise a lot of work)
    # condor_requirements=>'', # used?
    #     # resubmit options : if the status of a condor script is
    #     # either 'finished','submitted','running' or 'crashed',
    #     # decide whether to resubmit it.
    #     # NB Normally the status is empty, e.g. on the first run.
    #     # These are for restarting runs.
    #     condor_resubmit_finished=>0,
    # condor_resubmit_submitted=>0,
    # condor_resubmit_running=>0,
    # condor_resubmit_crashed=>0,
    ##########################
    # Unordered. Need to go through this. Copied from the perl implementation.
    ##########################
    ##
    # return_array_refs=>1, # quicker data parsing mode
    # sort_args=>1,
    # save_args=>1,
    # nice=>'nice -n +20',  # nice command e.g. 'nice -n +10' or ''
    # timeout=>15, # seconds until timeout
    # log_filename=>"/scratch/davidh/results_simulations/tmp/log.txt",
    # # current_log_filename=>"/scratch/davidh/results_simulations/tmp/grid_errors.log",
    ############################################################
    # Set default grid properties (in %self->{_grid_options}}
    # and %{$self->{_bse_options}})
    # This is the first thing that should be called by the user!
    ############################################################
    # # set signal handlers for timeout
    # $self->set_class_signal_handlers();
    # # set operating system
    # my $os = rob_misc::operating_system();
    # %{$self->{_grid_options}}=(
    #     # save operating system
    # operating_system=>$os,
    #     # process name
    #     process_name => 'binary_grid'.$VERSION,
    # grid_defaults_set=>1, # so we know the grid_defaults function has been called
    # # grid suspend files: assume binary_c by default
    # suspend_files=>[$tmp.'/force_binary_c_suspend',
    #         './force_binary_c_suspend'],
    # snapshot_file=>$tmp.'/binary_c-snapshot',
    # ########################################
    # # infomration about the running grid script
    # ########################################
    # working_directory=>cwd(), # the starting directory
    # perlscript=>$0, # the name of the perlscript
    # perlscript_arguments=>join(' ',@ARGV), # arguments as a string
    # perl_executable=>$^X, # the perl executable
    # command_line=>join(' ',$0,@ARGV), # full command line
    # process_ID=>$$, # process ID of the main perl script
    # ########################################
    # # GRID
    # ########################################
    #     # if undef, generate gridcode, otherwise load the gridcode
    #     # from this file. useful for debugging
    #     gridcode_from_file => undef,
    #     # assume binary_grid perl backend by default
    #     backend =>
    #     $self->{_grid_options}->{backend} //
    #     $binary_grid2::backend //
    #     'binary_grid::Perl',
    #     # custom C function for output : this automatically
    #     # binds if a function is available.
    #     C_logging_code => undef,
    #     C_auto_logging => undef,
    #     custom_output_C_function_pointer => binary_c_function_bind(),
    # # control flow
    # rungrid=>1, # usually run the grid, but can be 0
    # # to skip it (e.g. for condor/slurm runs)
    # merge_datafiles=>'',
    # merge_datafiles_filelist=>'',
    # # parameter space options
    # binary=>0, # set to 0 for single stars, 1 for binaries
    #     # if use_full_resolution is 1, then run a dummy grid to
    #     # calculate the resolution. this could be slow...
    #     use_full_resolution => 1,
    # # the probability in any distribution must be within
    # # this tolerance of 1.0, ignored if undef (if you want
    # # to run *part* of the parameter space then this *must* be undef)
    # probability_tolerance=>undef,
    # # how to deal with a failure of the probability tolerance:
    # # 0 = nothing
    # # 1 = warning
    # # 2 = stop
    # probability_tolerance_failmode=>1,
    # # add up and log system error count and probability
    # add_up_system_errors=>1,
    # log_system_errors=>1,
    # # codes, paths, executables etc.
    # # assume binary_c by default, and set its defaults
    # code=>'binary_c',
    # arg_prefix=>'--',
    # prog=>'binary_c', # executable
    # nice=>'nice -n +0', # nice command
    # ionice=>'',
    # # compress output?
    # binary_c_compression=>0,
    #     # get output as array of pre-split array refs
    #     return_array_refs=>1,
    # # environment
    # shell_environment=>undef,
    # libpath=>undef, # for backwards compatibility
    # # where is binary_c? need this to get the values of some counters
    # rootpath=>$self->okdir($ENV{BINARY_C_ROOTPATH}) //
    # $self->okdir($ENV{HOME}.'/progs/stars/binary_c') //
    # '.' , # last option is a fallback ... will fail if it doesn't exist
    # srcpath=>$self->okdir($ENV{BINARY_C_SRCPATH}) //
    # $self->okdir($ENV{BINARY_C_ROOTPATH}.'/src') //
    # $self->okdir($ENV{HOME}.'/progs/stars/binary_c/src') //
    # './src' , # last option is fallback... will fail if it doesn't exist
    # # stack size per thread in megabytes
    # threads_stack_size=>50,
    # # thread sleep time between starting the evolution code and starting
    # # the grid
    # thread_presleep=>0,
    # # threads
    # # Max time a thread can sit looping (with calls to tbse_line)
    # # before a warning is issued : NB this does not catch real freezes,
    # # just infinite loops (which still output)
    # thread_max_freeze_time_before_warning=>10,
    # # run all models by default: modulo=1, offset=0
    # modulo=>1,
    # offset=>0,
    #     # max number of stars on the queue
    #     maxq_per_thread => 100,
    # # data dump file : undef by default (do nothing)
    # results_hash_dumpfile => '',
    # # compress files with bzip2 by default
    # compress_results_hash => 1,
    # ########################################
    # # CPU
    # ########################################
    # cpu_cap=>0, # if 1, limits to one CPU
    # cpu_affinity => 0, # do not bind to a CPU by default
    # ########################################
    # # Code, Timeouts, Signals
    # ########################################
    # binary_grid_code_filtering=>1, #  you want this, it's (MUCH!) faster
    # pre_filter_file=>undef, # dump pre filtered code to this file
    # post_filter_file=>undef,  # dump post filtered code to this file
    # timeout=>30, # timeout in seconds
    # timeout_vb=>0, # no timeout logging
    # tvb=>0, # no thread logging
    # nfs_sleep=>1, # time to wait for NFS to catch up with file accesses
    # # flexigrid checks the timeouts every
    # # flexigrid_timeout_check_interval seconds
    # flexigrid_timeout_check_interval=>0.01,
    # # this is set to 1 when the grid is finished
    # flexigrid_finished=>0,
    # # allow signals by default
    # 'no signals'=>0,
    # # but perhaps disable specific signals?
    # 'disable signal'=>{INT=>0,ALRM=>0,CONT=>0,USR1=>0,STOP=>0},
    # # dummy variables
    # single_star_period=>1e50,  # orbital period of a single star
    # #### timers : set timers to 0 (or empty list) to ignore,
    # #### NB these must be given context (e.g. main::xyz)
    # #### for functions not in binary_grid
    # timers=>0,
    # timer_subroutines=>[
    #     # this is a suggested default list
    #     'flexigrid',
    #         'set_next_alarm',
    #     'vbout',
    #         'vbout_fast',
    #     'run_flexigrid_thread',
    #         'thread_vb'
    # ],
    # ########################################
    # # INPUT/OUTPUT
    # ########################################
    # blocking=>undef, # not yet set
    # # prepend command with stdbuf to stop buffering (if available)
    # stdbuf_command=>`stdbuf --version`=~/stdbuf \(GNU/ ? ' stdbuf -i0 -o0 -e0 ' : undef,
    # vb=>("@ARGV"=~/\Wvb=(\d+)\W/)[0] // 0, # set to 1 (or more) for verbose output to the screen
    # log_dt_secs=>1, # log output to stdout~every log_dt_secs seconds
    # nmod=>10, # every nmod models there is output to the screen,
    # # if log_dt_secs has been exceeded also (ignored if 0)
    # colour=>1, # set to 1 to use the ANSIColor module for colour output
    # log_args=>0, # do not log args in files
    # log_fins=>0, # log end of runs too
    #     sort_args=>0, # do not sort args
    # save_args=>0, # do not save args in a string
    # log_args_dir=>$tmp, # where to output the args files
    # always_reopen_arg_files=>0, # if 1 then arg files are always closed and reopened
    #   (may cause a lot of disk I/O)
    # lazy_arg_sending=>1, # if 1, the previous args are remembered and
    # # only args that changed are sent (except M1, M2 etc. which always
    # # need sending)
    # # force output files to open on a local disk (not an NFS partion)
    # # not sure how to do this on another OS
    # force_local_hdd_use=>($os eq 'unix'),
    # # for verbose output, define the newline
    # # For terminals use "\x0d", for files use "\n", in the
    # # case of multiple threads this will be set to \n
    # newline=> "\x0d",
    #     # use reset_stars_defaults
    #     reset_stars_defaults=>1,
    # # set signal captures: argument determines behaviour when the code locks up
    # # 0: exit
    # # 1: reset and try the next star (does this work?!)
    # alarm_procedure=>1,
    # # exit on eval failure?
    # exit_on_eval_failure=>1,
    # ## functions: these should be set by perl lexical name
    # ## (they are automatically converted to function pointers
    # ## at runtime)
    # # function to be called just before a thread is created
    # thread_precreate_function=>undef,
    #     thread_precreate_function_pointer=>undef,
    # # function to be called just after a thread is created
    # # (from inside the thread just before *grid () call)
    # threads_entry_function=>undef,
    #     threads_entry_function_pointer=>undef,
    # # function to be called just after a thread is finished
    # # (from inside the thread just after *grid () call)
    # threads_flush_function=>undef,
    # threads_flush_function_pointer=>undef,
    # # function to be called just after a thread is created
    # # (but external to the thread)
    # thread_postrun_function=>undef,
    # thread_postrun_function_pointer=>undef,
    # # function to be called just before a thread join
    # # (external to the thread)
    # thread_prejoin_function=>undef,
    # thread_prejoin_function_pointer=>undef,
    # # default to using the internal join_flexigrid_thread function
    # threads_join_function=>'binary_grid2::join_flexigrid_thread',
    # threads_join_function_pointer=>sub{return $self->join_flexigrid_thread(@_)},
    # # function to be called just after a thread join
    # # (external to the thread)
    # thread_postjoin_function=>undef,
    # thread_postjoin_function_pointer=>undef,
    # # usually, parse_bse in the main script is called
    # parse_bse_function=>'main::parse_bse',
    #     parse_bse_function_pointer=>undef,
    # # if starting_snapshot_file is defined, load initial
    # # values for the grid from the snapshot file rather
    # # than a normal initiation: this enables you to
    # # stop and start a grid
    # starting_snapshot_file=>undef,
}
