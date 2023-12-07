//Read the README first 
#include <opencv2/opencv.hpp>
#include <iostream>
#include <ctime>
#include <string>

int main()
{	
	cv::VideoCapture vid_cap(0);
  
	while (true)
	{
		cv::Mat img;

		vid_cap.read(img);
		std::time_t t = std::time(0);

		cv::imshow("window", img);

		int key = cv::waitKey(1);  

		if (key == 'q' || key == 27)  
		{
			break;
		}
		
		else if (key == 32)
		{
			std::string fileName = std::to_string(t);
			fileName.append(".jpeg");
			cv::imwrite(fileName, img);
		}
	}

	return 0;
}
