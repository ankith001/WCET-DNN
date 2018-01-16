#include <iostream>
#include <opencv2/imgproc/imgproc.hpp>
#include <boost/python.hpp>
#include <time.h>
#include "conversion.h"

namespace py = boost::python;

static double gettime()
{
    struct timeval t;
    gettimeofday(&t,NULL);
    return t.tv_sec+t.tv_usec*1e-6;
}

PyObject*
resize_img(PyObject *ndarr_img)
{
    NDArrayConverter cvt;
    cv::Mat mat_img;
    mat_img = cvt.toMat(ndarr_img);
    cv::Mat mat_resz_img;
    double start, end;
    float new_width = 227;
    float new_height = 227;
    int l_x, l_y;
    float height = mat_img.size().height;
    float width = mat_img.size().width;
    float x_ratio = new_width/width;
    float y_ratio = new_height/height;
    start = gettime();
    for (int i = 0 ; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            cv::Vec3b color = mat_img.at<cv::Vec3b>(cv::Point(i,j));
            l_x =  (i* x_ratio);
            l_y =  (j * y_ratio);
            mat_resz_img.at<cv::Vec3b>(cv::Point(l_x,l_y)) = color;
        }
    }

    end = gettime();

	std::cout<<"Time taken to resize "<<(end-start)<<std::endl;

    PyObject* ndarr_resz_img = cvt.toNDArray(mat_resz_img);

    return ndarr_resz_img;
}

static void init()
{
    Py_Initialize();
    import_array();
}

BOOST_PYTHON_MODULE(resizing)
{
    init();
    py::def("resize_img", resize_img);
}
