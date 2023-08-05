# Makefile for Rapid Binary Star Evolution program

# you will need to set the BINARY_C variable to point
# to the root binary_c directory
ifeq ($(BINARY_C),)
  $(error BINARY_C is not set)
endif

# TODO: Create the directories if they dont exist.


# Name of program
PROGRAM 			:= binary_c_python_api

# Some directories
SRC_DIR 			:= src
INC_DIR 			:= include
OBJ_DIR 			:= obj
TARGET_LIB_DIR 		:= lib

# some commands
CC      			:= gcc
LD      			:= gcc
MAKE    			:= /usr/bin/make
MKDIR_P 			:= mkdir -p
PWD 				:= pwd

# Libraries
LIBS 				:= -lbinary_c $(shell $(BINARY_C)/binary_c-config --libs)

# Source files and cflags
C_SRC 				:= $(SRC_DIR)/binary_c_python_api.c
CFLAGS 				:= -fPIC $(shell $(BINARY_C)/binary_c-config --flags | sed s/-fvisibility=hidden// )

# Incdirs
INCDIRS 			:= -I$(BINARY_C)/src/ -I$(BINARY_C)/src/API -I$(INC_DIR)/

# Object files and flags
OBJECTS 			:= $(C_SRC:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)
OBJ_FLAGS 			:= -c

# Shared lib files and flags
SO_NAME 			:= $(TARGET_LIB_DIR)/libbinary_c_python_api.so
SO_FLAGS 			:= -shared
SO_NAME_EXTRA 		:= binarycpython/libbinary_c_python_api.so

all: create_directories create_objects create_library

debug: create_directories create_objects_debug create_library_debug

create_directories:
	${MKDIR_P} ${TARGET_LIB_DIR}
	${MKDIR_P} ${OBJ_DIR}

create_objects:
	$(CC) -DBINARY_C=$(BINARY_C) $(CFLAGS) $(INCDIRS) $(C_SRC) -o $(OBJECTS) $(OBJ_FLAGS) $(LIBS) 

create_objects_debug: 
	$(CC) -DBINARY_C=$(BINARY_C) -DBINARY_C_PYTHON_DEBUG $(CFLAGS) $(INCDIRS) $(C_SRC) -o $(OBJECTS) $(OBJ_FLAGS) $(LIBS) 

create_library:
	@echo $(PWD)
	$(CC) -DBINARY_C=$(BINARY_C) $(SO_FLAGS) -o $(SO_NAME) $(OBJECTS)
	$(CC) -DBINARY_C=$(BINARY_C) $(SO_FLAGS) -o $(SO_NAME_EXTRA) $(OBJECTS)

create_library_debug:
	$(CC) -DBINARY_C=$(BINARY_C) -DBINARY_C_PYTHON_DEBUG $(SO_FLAGS) -o $(SO_NAME) $(OBJECTS)

echo_vars:	
	@echo OBJECTS: $(OBJECTS)
	@echo LIBS: $(LIBS)
	@echo C_SRC: $(C_SRC)
	@echo CFLAGS: $(CFLAGS)
	@echo INCDIRS: $(INCDIRS)
	@echo SO_NAME: $(SO_NAME)

clean:
	$(RM) $(OBJ_DIR)/*.o $(TARGET_LIB_DIR)/*.so
	$(RM) *.o
	$(RM) *.so
	$(RM) -r build/
