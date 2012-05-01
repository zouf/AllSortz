#include <boost/python.hpp>
#include <iostream>
#include <string>

using namespace boost::python;

list test_extract(list& ls)
{
	list newList;
	for(int i = 0; i < len(ls); ++i)
  {
    std::cout << boost::python::extract<int>(ls[i]) << std::endl;
    newList.append(i);
  }
	return newList;
}


char const* greet(unsigned x)
{
   static char const* const msgs[] = { "hello", "Boost.Python", "world!" };

   if (x > 2)
       throw std::range_error("greet: index out of range");

   return msgs[x];
}

using namespace boost::python;

BOOST_PYTHON_MODULE(hello)
{
    def("test_extract", test_extract, "return list");
}
