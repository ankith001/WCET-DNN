//#include <opencv2/highgui/highgui.hpp>
//#include <iostream>
//#include <opencv2/imgproc/imgproc.hpp>
//#include <time.h>
//#include <sys/time.h>
#define BOOST_PYTHON_MAX_ARITY 16
#include <boost/python.hpp>
#include <typeinfo>

//#include "conversion.h"
//#include "resizing.h"

/*double gettime()
{
    struct timeval t;
    gettimeofday(&t,NULL);
    return t.tv_sec+t.tv_usec*1e-6;
}
PyObject* resize_time (std::string path) {
    using namespace std; 
    using namespace cv;
    int new_width = 227;
    int new_height = 227;
    double resizing_time;
    vector <String> filenames;
    int l_x, l_y;
    NDArrayConverter cvt;
    cv::glob(path,filenames);
    PyObject* ndarray;
    for (size_t k=0; k<filenames.size(); k++)
    {
        cv::Mat image = imread(filenames[k], CV_LOAD_IMAGE_COLOR);
        cv::Mat blank_image(new_width, new_height, CV_8UC3);
        float height = image.size().height;
        float width = image.size().width;
        float x_ratio = new_width/width;
        float y_ratio = new_height/height;
	double start = gettime(); 
	for (int i = 0 ; i < width; i++)
	{
	    for (int j = 0; j < height; j++) 
	    {
		Vec3b color = image.at<Vec3b>(Point(i,j));
		l_x =  (i* x_ratio);
		l_y =  (j * y_ratio);
		blank_image.at<Vec3b>(Point(l_x,l_y)) = color;
	    }
	}
	std::cout<<"a is of type: "<<typeid(blank_image).name()<<std::endl;
        double end = gettime();
	resizing_time = end-start;
	std::cout<<"Time taken: "<<resizing_time<<std::endl;
	ndarray = cvt.toNDArray(blank_image);
    }
   return ndarray;
}*/

void resize_time(){return;}

BOOST_PYTHON_MODULE(resizing)
{
    //Py_Initialize();
    //import_array();
    namespace py=boost::python;
    py::def("resize_time", resize_time);
}
