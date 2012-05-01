PYTHON= /usr/include/python2.7

BOOST_INC= /Users/zouf/pool/include
BOOST_LIB= /Users/zouf/pool/lib

OBJ= fastnmf

ALL= fastnmf.so

all: $(ALL)

fastnmf.so: fastnmf.o
	g++ -shared -dynamic  \
	fastnmf.o -L$(BOOST_LIB) -lboost_python \
	-L/usr/lib/python2.7/config -lpython2.7 \
	-o fastnmf.so


fastnmf.o: fastnmf.cpp
	g++ -I$(PYTHON) -I$(BOOST_INC) -c -fPIC fastnmf.cpp -o fastnmf.o
