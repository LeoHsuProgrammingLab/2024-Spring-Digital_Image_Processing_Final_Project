CXX := g++
CXXFLAGS := -std=c++11 -O3 -Wall $(shell pkg-config --cflags opencv4)
LDLIBS := $(shell pkg-config --libs opencv4)

SRC := pyramid.cpp affine.cpp siftdesc.cpp helpers.cpp hesaff.cpp
OBJ := $(SRC:.cpp=.o)
DEP := $(OBJ:.o=.d)
EXE := hesaff

all: $(EXE)
	@rm -f $(OBJ) $(DEP)

$(EXE): $(OBJ)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDLIBS)
	@echo "Build complete."

-include $(DEP)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -MMD -MP -c $< -o $@

clean:
	rm -f $(OBJ) $(EXE) $(DEP)

.PHONY: all clean