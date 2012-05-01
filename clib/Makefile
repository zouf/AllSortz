PYTHON= /usr/include/python2.7

BOOST_INC= /Users/zouf/pool/include
BOOST_LIB= /Users/zouf/pool/lib

OBJ= hello

ALL= hello.so

all: $(ALL)

hello.so: hello.o
	g++ -shared -dynamic  \
	hello.o -L$(BOOST_LIB) -lboost_python \
	-L/usr/lib/python2.7/config -lpython2.7 \
	-o hello.so


hello.o: hello.cpp
	g++ -I$(PYTHON) -I$(BOOST_INC) -c -fPIC hello.cpp -o hello.o
