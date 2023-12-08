#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>

int main()
{
    cv::VideoCapture cap(0);

    if (!cap.isOpened())
    {
        std::cerr << "Error: Couldn't open the camera." << std::endl;
        return -1;
    }

    cv::Mat img;
    cv::CascadeClassifier facedetect;
    facedetect.load("haarcascade_frontalface_default.xml");

    while (cap.read(img))
    {
        std::vector<cv::Rect> faces;
        facedetect.detectMultiScale(img, faces, 1.3, 5);

        for (size_t i = 0; i < faces.size(); i++)
        {
            cv::rectangle(img, faces[i].tl(), faces[i].br(), cv::Scalar(50, 50, 50), 3);
            std::cout << faces.size() << std::endl;
            //cv::putText(img, std::to_string(faces.size()), cv::Point(10,40), cv::FONT_HERSHEY_DUPLEX, 1, cv::Scalar(255,255,255), 1);
        }

        cv::imshow("title", img);

        if (cv::waitKey(1) == 27) 
            break;
    }

    cap.release();
    cv::destroyAllWindows();

    return 0;
}
